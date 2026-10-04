import asyncio
import random
import string
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()

    prompt_tokens = 0
    for msg in body.get("messages", []):
        prompt_tokens += estimate_tokens(msg.get("content", ""))
    prompt_tokens = max(prompt_tokens, 5)

    completion_tokens = random.randint(20, 200)
    response_text = "".join(
        random.choices(string.ascii_letters + " " * 5, k=completion_tokens * 4)
    )

    delay = random.uniform(0.1, 0.5)
    await asyncio.sleep(delay)

    return JSONResponse(
        {
            "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": body.get("model", "mock-llm-v1"),
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text,
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
        }
    )


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
