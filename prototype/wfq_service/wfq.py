from __future__ import annotations

import asyncio
import logging
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

DEFAULT_REQUEST_TOKEN_ESTIMATE = 500


@dataclass
class GroupState:
    name: str
    weight: float
    virtual_time: float = 0.0
    tokens_used: list = field(default_factory=list)
    in_flight_tokens: int = 0
    in_flight_count: int = 0
    queue: deque = field(default_factory=deque)


@dataclass
class QueuedRequest:
    group_name: str
    request_id: str
    event: asyncio.Event = field(default_factory=asyncio.Event)
    admitted: bool = False
    cancelled: bool = False


class WeightedFairQueue:
    """Weighted Fair Queuing scheduler for LLM token-based rate limiting.

    Uses virtual finish time scheduling: each group's virtual_time advances
    by (tokens_used / weight). Groups with lower virtual_time are prioritized,
    ensuring proportional token allocation according to weights.

    Token usage is tracked in a sliding window using sub-buckets for smooth
    decay. In-flight requests contribute estimated tokens until the actual
    response usage is recorded.
    """

    def __init__(
        self,
        groups: dict[str, float],
        max_tokens_per_window: int = 1_000_000,
        window_seconds: float = 60.0,
        max_queue_depth: int = 100,
        max_concurrent: int = 50,
        num_sub_buckets: int = 10,
    ):
        self.max_tokens_per_window = max_tokens_per_window
        self.window_seconds = window_seconds
        self.max_queue_depth = max_queue_depth
        self.max_concurrent = max_concurrent
        self.num_sub_buckets = num_sub_buckets
        self.sub_bucket_duration = window_seconds / num_sub_buckets

        self.groups: dict[str, GroupState] = {}
        for name, weight in groups.items():
            self.groups[name] = GroupState(name=name, weight=weight)

        self.total_concurrent = 0
        self._lock = asyncio.Lock()
        self._drain_task: Optional[asyncio.Task] = None

    def start(self):
        self._drain_task = asyncio.create_task(self._drain_loop())

    async def stop(self):
        if self._drain_task:
            self._drain_task.cancel()
            try:
                await self._drain_task
            except asyncio.CancelledError:
                pass

    def _current_bucket_index(self) -> int:
        return int(time.monotonic() / self.sub_bucket_duration)

    def _tokens_in_window(self, group: GroupState) -> int:
        cutoff = self._current_bucket_index() - self.num_sub_buckets
        total = 0
        fresh = []
        for bucket_idx, tokens in group.tokens_used:
            if bucket_idx > cutoff:
                total += tokens
                fresh.append((bucket_idx, tokens))
        group.tokens_used = fresh
        return total

    def _total_tokens_in_window(self) -> int:
        return sum(
            self._tokens_in_window(g) + g.in_flight_tokens
            for g in self.groups.values()
        )

    def _rebalance_virtual_times(self):
        active = [g for g in self.groups.values() if self._tokens_in_window(g) > 0 or g.in_flight_count > 0]
        if not active:
            for g in self.groups.values():
                g.virtual_time = 0.0
            return

        min_vt = min(g.virtual_time for g in self.groups.values())
        if min_vt > 1000:
            for g in self.groups.values():
                g.virtual_time -= min_vt

    async def try_admit(self, group_name: str, request_id: str) -> tuple[bool, Optional[QueuedRequest], Optional[float]]:
        """Try to admit a request. Returns (admitted, queued_request, retry_after).

        If admitted=True, the request can proceed immediately.
        If queued_request is not None, await queued_request.event to be admitted.
        If retry_after is not None, the request should be rejected with 429.
        """
        async with self._lock:
            group = self.groups.get(group_name)
            if not group:
                return False, None, 5.0

            if self.total_concurrent < self.max_concurrent and self._can_admit_group(group):
                self._admit(group)
                return True, None, None

            if len(group.queue) >= self.max_queue_depth:
                retry_after = self._estimate_retry_after(group)
                return False, None, retry_after

            queued = QueuedRequest(group_name=group_name, request_id=request_id)
            group.queue.append(queued)
            return False, queued, None

    def _can_admit_group(self, group: GroupState) -> bool:
        total_used = self._total_tokens_in_window()
        if total_used >= self.max_tokens_per_window:
            group_used = self._tokens_in_window(group) + group.in_flight_tokens
            group_share = (group.weight / sum(g.weight for g in self.groups.values())) * self.max_tokens_per_window
            if group_used >= group_share:
                return False

        other_active = [
            g for g in self.groups.values()
            if g.name != group.name and (g.in_flight_count > 0 or g.queue)
        ]
        if other_active:
            min_other_vt = min(g.virtual_time for g in other_active)
            if group.virtual_time > min_other_vt + (DEFAULT_REQUEST_TOKEN_ESTIMATE / group.weight) * 2:
                return False

        return True

    def _admit(self, group: GroupState):
        group.in_flight_count += 1
        group.in_flight_tokens += DEFAULT_REQUEST_TOKEN_ESTIMATE
        group.virtual_time += DEFAULT_REQUEST_TOKEN_ESTIMATE / group.weight
        self.total_concurrent += 1

    def _estimate_retry_after(self, group: GroupState) -> float:
        tokens_used = self._tokens_in_window(group)
        weight_frac = group.weight / sum(g.weight for g in self.groups.values())
        group_budget = weight_frac * self.max_tokens_per_window
        if tokens_used <= group_budget:
            return 1.0
        overshoot = tokens_used - group_budget
        drain_rate = group_budget / self.window_seconds
        if drain_rate <= 0:
            return self.window_seconds
        return min(overshoot / drain_rate, self.window_seconds)

    async def record_completion(self, group_name: str, actual_tokens: int):
        async with self._lock:
            group = self.groups.get(group_name)
            if not group:
                return

            group.in_flight_count = max(0, group.in_flight_count - 1)
            group.in_flight_tokens = max(0, group.in_flight_tokens - DEFAULT_REQUEST_TOKEN_ESTIMATE)
            self.total_concurrent = max(0, self.total_concurrent - 1)

            bucket_idx = self._current_bucket_index()
            group.tokens_used.append((bucket_idx, actual_tokens))

            vt_correction = actual_tokens / group.weight - DEFAULT_REQUEST_TOKEN_ESTIMATE / group.weight
            group.virtual_time += vt_correction

            self._rebalance_virtual_times()
            await self._try_drain_queues()

    async def _try_drain_queues(self):
        while self.total_concurrent < self.max_concurrent:
            best_group = None
            best_vt = float("inf")

            for group in self.groups.values():
                while group.queue and group.queue[0].cancelled:
                    group.queue.popleft()
                if group.queue and group.virtual_time < best_vt:
                    if self._can_admit_group(group):
                        best_vt = group.virtual_time
                        best_group = group

            if not best_group:
                break

            queued = best_group.queue.popleft()
            if queued.cancelled:
                continue
            self._admit(best_group)
            queued.admitted = True
            queued.event.set()

    async def _drain_loop(self):
        while True:
            await asyncio.sleep(0.1)
            async with self._lock:
                await self._try_drain_queues()

    def get_stats(self) -> dict:
        total_weight = sum(g.weight for g in self.groups.values())
        stats = {}
        for name, group in self.groups.items():
            tokens = self._tokens_in_window(group)
            stats[name] = {
                "weight": group.weight,
                "weight_pct": round(group.weight / total_weight * 100, 1),
                "tokens_in_window": tokens,
                "in_flight_tokens": group.in_flight_tokens,
                "in_flight_count": group.in_flight_count,
                "queue_depth": len(group.queue),
                "virtual_time": round(group.virtual_time, 2),
            }
        stats["_total"] = {
            "concurrent": self.total_concurrent,
            "max_concurrent": self.max_concurrent,
            "total_tokens_in_window": self._total_tokens_in_window(),
            "max_tokens_per_window": self.max_tokens_per_window,
        }
        return stats
