#!/usr/bin/env python3
"""Integration test / demo for the WFQ proxy.

Sends concurrent requests through the Envoy proxy using different API keys
and shows how the WFQ algorithm distributes tokens across groups.

Usage:
    docker compose up -d
    python test_wfq.py
"""

import argparse
import asyncio
import json
import time
from collections import defaultdict

import aiohttp

PROXY_URL = "http://localhost:8080/v1/chat/completions"

API_KEYS = {
    "premium": ["sk-premium-key-1", "sk-premium-key-2"],
    "standard": ["sk-standard-key-1"],
    "free": ["sk-free-key-1", "sk-free-key-2"],
}

WEIGHTS = {"premium": 50, "standard": 30, "free": 20}


async def send_request(session: aiohttp.ClientSession, api_key: str, idx: int):
    payload = {
        "model": "mock-llm-v1",
        "messages": [
            {"role": "user", "content": f"Test request number {idx}. Tell me something."}
        ],
    }
    headers = {"x-api-key": api_key, "content-type": "application/json"}

    start = time.monotonic()
    try:
        async with session.post(PROXY_URL, json=payload, headers=headers) as resp:
            body = await resp.json()
            elapsed = time.monotonic() - start
            return {
                "status": resp.status,
                "tokens": body.get("usage", {}).get("total_tokens", 0),
                "elapsed": elapsed,
                "group": resp.headers.get("x-wfq-group", "unknown"),
                "error": body.get("error"),
            }
    except Exception as e:
        return {
            "status": 0,
            "tokens": 0,
            "elapsed": time.monotonic() - start,
            "group": "error",
            "error": str(e),
        }


async def run_test(
    total_requests: int = 100,
    concurrency: int = 20,
    distribution: str = "equal",
):
    """Run the integration test.

    distribution:
        "equal" - same number of requests per group
        "heavy_free" - free tier sends 3x more requests
        "burst_premium" - premium sends all at once, others trickle
    """
    tasks = []

    if distribution == "equal":
        per_group = total_requests // 3
        for group, keys in API_KEYS.items():
            for i in range(per_group):
                key = keys[i % len(keys)]
                tasks.append((key, group, i))
    elif distribution == "heavy_free":
        for i in range(total_requests // 5):
            tasks.append((API_KEYS["premium"][0], "premium", i))
            tasks.append((API_KEYS["standard"][0], "standard", i))
        for i in range(total_requests * 3 // 5):
            key = API_KEYS["free"][i % len(API_KEYS["free"])]
            tasks.append((key, "free", i))
    elif distribution == "burst_premium":
        for i in range(total_requests // 2):
            tasks.append((API_KEYS["premium"][i % 2], "premium", i))
        for i in range(total_requests // 4):
            tasks.append((API_KEYS["standard"][0], "standard", i))
        for i in range(total_requests // 4):
            key = API_KEYS["free"][i % len(API_KEYS["free"])]
            tasks.append((key, "free", i))

    results_by_group = defaultdict(list)
    semaphore = asyncio.Semaphore(concurrency)

    async def bounded_request(session, api_key, group, idx):
        async with semaphore:
            result = await send_request(session, api_key, idx)
            results_by_group[group].append(result)
            return result

    print(f"\n{'='*70}")
    print(f"WFQ Integration Test — {len(tasks)} requests, concurrency={concurrency}")
    print(f"Distribution: {distribution}")
    print(f"{'='*70}\n")

    start = time.monotonic()
    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        coros = [bounded_request(session, key, group, idx) for key, group, idx in tasks]
        await asyncio.gather(*coros)
    wall_time = time.monotonic() - start

    total_tokens_all = 0
    print(f"{'Group':<12} {'Weight':>6} {'Expected%':>9} {'Requests':>8} "
          f"{'OK':>4} {'429s':>5} {'Tokens':>8} {'Actual%':>8} {'Avg(ms)':>8}")
    print("-" * 80)

    total_weight = sum(WEIGHTS.values())
    group_tokens = {}

    for group in ["premium", "standard", "free"]:
        results = results_by_group[group]
        ok = sum(1 for r in results if r["status"] == 200)
        rejected = sum(1 for r in results if r["status"] == 429)
        errors = sum(1 for r in results if r["status"] not in (200, 429))
        tokens = sum(r["tokens"] for r in results if r["status"] == 200)
        avg_ms = (
            sum(r["elapsed"] for r in results) / len(results) * 1000 if results else 0
        )
        group_tokens[group] = tokens
        total_tokens_all += tokens

    for group in ["premium", "standard", "free"]:
        results = results_by_group[group]
        ok = sum(1 for r in results if r["status"] == 200)
        rejected = sum(1 for r in results if r["status"] == 429)
        tokens = group_tokens[group]
        avg_ms = (
            sum(r["elapsed"] for r in results) / len(results) * 1000 if results else 0
        )
        expected_pct = WEIGHTS[group] / total_weight * 100
        actual_pct = tokens / total_tokens_all * 100 if total_tokens_all else 0

        print(
            f"{group:<12} {WEIGHTS[group]:>6} {expected_pct:>8.1f}% {len(results):>8} "
            f"{ok:>4} {rejected:>5} {tokens:>8} {actual_pct:>7.1f}% {avg_ms:>7.0f}"
        )

    print("-" * 80)
    print(f"{'Total':<12} {total_weight:>6} {'100.0%':>9} {sum(len(v) for v in results_by_group.values()):>8} "
          f"     {'':>5} {total_tokens_all:>8} {'100.0%':>8} {wall_time*1000:>7.0f}")

    print(f"\nWall time: {wall_time:.2f}s")
    print(f"Total tokens consumed: {total_tokens_all:,}")

    if total_tokens_all > 0:
        print(f"\nFairness analysis:")
        for group in ["premium", "standard", "free"]:
            expected = WEIGHTS[group] / total_weight
            actual = group_tokens[group] / total_tokens_all
            deviation = abs(actual - expected) / expected * 100
            print(f"  {group}: expected {expected*100:.1f}%, got {actual*100:.1f}% "
                  f"(deviation: {deviation:.1f}%)")


def main():
    parser = argparse.ArgumentParser(description="WFQ proxy integration test")
    parser.add_argument("-n", "--requests", type=int, default=100, help="Total requests")
    parser.add_argument("-c", "--concurrency", type=int, default=20, help="Max concurrent")
    parser.add_argument(
        "-d",
        "--distribution",
        choices=["equal", "heavy_free", "burst_premium"],
        default="equal",
        help="Request distribution pattern",
    )
    parser.add_argument("--url", default=PROXY_URL, help="Proxy URL")
    args = parser.parse_args()

    global PROXY_URL
    PROXY_URL = args.url

    asyncio.run(run_test(args.requests, args.concurrency, args.distribution))


if __name__ == "__main__":
    main()
