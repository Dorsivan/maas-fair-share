import asyncio
import json
import logging
import os
import signal
import sys
import uuid

import grpc
from grpc import aio as grpc_aio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "generated"))

from ext_proc_pb2 import (
    BodyResponse,
    CommonResponse,
    HeaderMutation,
    HeadersResponse,
    ImmediateResponse,
    ProcessingRequest,
    ProcessingResponse,
)
from ext_proc_pb2_grpc import (
    ExternalProcessorServicer,
    add_ExternalProcessorServicer_to_server,
)
from envoy.config.core.v3 import base_pb2
from envoy.type.v3 import http_status_pb2

from config import WFQConfig
from wfq import WeightedFairQueue

logger = logging.getLogger(__name__)

QUEUE_WAIT_TIMEOUT = float(os.environ.get("WFQ_QUEUE_TIMEOUT", "30"))


class ExtProcServicer(ExternalProcessorServicer):
    def __init__(self, wfq: WeightedFairQueue, config: WFQConfig):
        self.wfq = wfq
        self.config = config

    async def Process(self, request_iterator, context):
        group_name = None
        request_id = str(uuid.uuid4())[:8]

        async for req in request_iterator:
            req: ProcessingRequest
            which = req.WhichOneof("request")

            if which == "request_headers":
                group_name, response = await self._handle_request_headers(
                    req.request_headers, request_id
                )
                yield response

            elif which == "response_body":
                response = await self._handle_response_body(
                    req.response_body, group_name, request_id
                )
                yield response

            elif which == "response_headers":
                yield ProcessingResponse(
                    response_headers=HeadersResponse(
                        response=CommonResponse(
                            status=CommonResponse.CONTINUE,
                        )
                    )
                )

            elif which == "request_body":
                yield ProcessingResponse(
                    request_body=BodyResponse(
                        response=CommonResponse(
                            status=CommonResponse.CONTINUE,
                        )
                    )
                )

            else:
                logger.debug("Unhandled ext_proc phase: %s (req_id=%s)", which, request_id)
                yield ProcessingResponse(
                    response_headers=HeadersResponse(
                        response=CommonResponse(
                            status=CommonResponse.CONTINUE,
                        )
                    )
                )

    async def _handle_request_headers(self, http_headers, request_id):
        headers = {}
        if http_headers.headers:
            for hv in http_headers.headers.headers:
                headers[hv.key.lower()] = hv.raw_value.decode("utf-8", errors="replace")

        api_key = self._extract_api_key(headers)
        group_name = self.config.group_for_api_key(api_key)

        logger.info(
            "Request %s: group=%s api_key=%s...%s",
            request_id,
            group_name,
            api_key[:8] if api_key else "none",
            api_key[-4:] if api_key and len(api_key) > 8 else "",
        )

        admitted, queued, retry_after = await self.wfq.try_admit(group_name, request_id)

        if admitted:
            return group_name, self._make_continue_response(group_name, request_id)

        if queued:
            try:
                await asyncio.wait_for(queued.event.wait(), timeout=QUEUE_WAIT_TIMEOUT)
                if queued.admitted:
                    logger.info("Request %s dequeued for group %s", request_id, group_name)
                    return group_name, self._make_continue_response(group_name, request_id)
            except asyncio.TimeoutError:
                queued.cancelled = True
                logger.warning("Request %s timed out in queue for group %s", request_id, group_name)

            retry_after = retry_after or 5.0

        return group_name, self._make_reject_response(group_name, retry_after or 5.0)

    async def _handle_response_body(self, http_body, group_name, request_id):
        actual_tokens = 0
        if http_body.body:
            try:
                body = json.loads(http_body.body)
                usage = body.get("usage", {})
                actual_tokens = usage.get("total_tokens", 0)
                if not actual_tokens:
                    actual_tokens = usage.get("prompt_tokens", 0) + usage.get(
                        "completion_tokens", 0
                    )
            except (json.JSONDecodeError, AttributeError):
                logger.debug("Could not parse response body for token usage (req_id=%s)", request_id)

        if group_name:
            await self.wfq.record_completion(group_name, actual_tokens)
            logger.info(
                "Request %s completed: group=%s tokens=%d",
                request_id,
                group_name,
                actual_tokens,
            )

        return ProcessingResponse(
            response_body=BodyResponse(
                response=CommonResponse(
                    status=CommonResponse.CONTINUE,
                )
            )
        )

    def _extract_api_key(self, headers: dict) -> str:
        api_key = headers.get("x-api-key", "")
        if api_key:
            return api_key

        auth = headers.get("authorization", "")
        if auth.lower().startswith("bearer "):
            return auth[7:].strip()

        return ""

    def _make_continue_response(self, group_name: str, request_id: str):
        return ProcessingResponse(
            request_headers=HeadersResponse(
                response=CommonResponse(
                    status=CommonResponse.CONTINUE,
                    header_mutation=HeaderMutation(
                        set_headers=[
                            base_pb2.HeaderValueOption(
                                header=base_pb2.HeaderValue(
                                    key="x-wfq-group",
                                    raw_value=group_name.encode(),
                                ),
                            ),
                            base_pb2.HeaderValueOption(
                                header=base_pb2.HeaderValue(
                                    key="x-wfq-request-id",
                                    raw_value=request_id.encode(),
                                ),
                            ),
                        ]
                    ),
                )
            )
        )

    def _make_reject_response(self, group_name: str, retry_after: float):
        body = json.dumps(
            {
                "error": {
                    "message": f"Rate limited: group '{group_name}' has exceeded its token budget. Retry after {retry_after:.1f}s.",
                    "type": "rate_limit_error",
                    "code": "rate_limit_exceeded",
                    "group": group_name,
                    "retry_after": round(retry_after, 1),
                }
            }
        )

        return ProcessingResponse(
            immediate_response=ImmediateResponse(
                status=http_status_pb2.HttpStatus(
                    code=http_status_pb2.TooManyRequests,
                ),
                headers=HeaderMutation(
                    set_headers=[
                        base_pb2.HeaderValueOption(
                            header=base_pb2.HeaderValue(
                                key="content-type",
                                raw_value=b"application/json",
                            ),
                        ),
                        base_pb2.HeaderValueOption(
                            header=base_pb2.HeaderValue(
                                key="retry-after",
                                raw_value=str(int(retry_after)).encode(),
                            ),
                        ),
                        base_pb2.HeaderValueOption(
                            header=base_pb2.HeaderValue(
                                key="x-wfq-group",
                                raw_value=group_name.encode(),
                            ),
                        ),
                    ]
                ),
                body=body,
            )
        )


async def serve():
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

    config = WFQConfig()
    wfq = WeightedFairQueue(
        groups=config.group_weights(),
        max_tokens_per_window=config.settings["max_tokens_per_window"],
        window_seconds=config.settings["window_seconds"],
        max_queue_depth=config.settings["max_queue_depth"],
        max_concurrent=config.settings["max_concurrent"],
    )
    wfq.start()

    server = grpc_aio.server()
    add_ExternalProcessorServicer_to_server(ExtProcServicer(wfq, config), server)

    listen_addr = os.environ.get("WFQ_LISTEN", "[::]:50051")
    server.add_insecure_port(listen_addr)
    logger.info("WFQ ext_proc server starting on %s", listen_addr)
    logger.info("Groups: %s", {n: g["weight"] for n, g in config.groups.items()})
    logger.info("Settings: %s", config.settings)

    await server.start()

    shutdown_event = asyncio.Event()

    def _signal_handler():
        shutdown_event.set()

    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _signal_handler)

    await shutdown_event.wait()
    logger.info("Shutting down...")
    await wfq.stop()
    await server.stop(grace=5)


if __name__ == "__main__":
    asyncio.run(serve())
