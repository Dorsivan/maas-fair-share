#!/usr/bin/env python3
"""Open-loop, Poisson-arrival load generator for the maas-fairness-poc
fairness scenario (UNI-34 / C3).

Every load generator in this repo up to this point (04-loadgen.yaml,
12-loadgen-route.sh) is CLOSED-LOOP: a fixed pool of workers per tenant, each
worker blocking on one request before issuing its next. Offered load is
therefore capped by (worker count / mean latency) and self-throttles -- a
slow backend automatically slows the client down too, which can hide
queueing behaviour that a real, latency-independent arrival process would
expose. See docs/poc-results.md, "SUPERSEDED: the newcomer clamp hurt here"
and Outstanding work #10.

This script is OPEN-LOOP: for each tenant, request arrivals are scheduled by
an independent Poisson process at a fixed mean rate (--rate-*, requests per
second). The inter-arrival time is drawn fresh each time from
Exponential(rate), and each arrival is dispatched to a worker thread pool
WITHOUT waiting for the previous request (or any request) to complete. The
offered rate is therefore constant regardless of how fast -- or slowly -- the
backend answers, including while the backend is overloaded or erroring.

Usage (see 13-loadgen-poisson.sh for the wrapper that fetches keys):

    python3 13-loadgen-poisson.py \
        --gw https://maas-gateway-maas-fairness-poc.apps.ocp.paladinaura.com \
        --modelpath /maas-fairness-poc/maas-vllm-gpu \
        --duration 240 \
        --rate-app1 4 --rate-app2 4 --rate-end-users 4 \
        --key-app1 /keys/app1-production --key-app2 /keys/app2-batch \
        --key-end-alpha /keys/end-user-alpha --key-end-beta /keys/end-user-beta \
        --out /tmp/poisson-codes --seed 1

A rate of 0 (the default) disables that tenant entirely.
"""
import argparse
import itertools
import json
import random
import statistics
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, wait as futures_wait

PROMPT = "the quick brown fox " * 300


def read_key(path):
    with open(path) as f:
        return f.read().strip()


def send_request(gw, modelpath, token, group, arrival_t, results, lock, client_timeout=90):
    body = json.dumps(
        {
            "model": "llama-3-1-8b",
            "max_tokens": 64,
            "messages": [{"role": "user", "content": PROMPT}],
        }
    ).encode()
    req = urllib.request.Request(
        gw.rstrip("/") + modelpath + "/v1/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    start = time.time()
    code = 0
    completion_tokens = -1
    try:
        with urllib.request.urlopen(req, timeout=client_timeout) as resp:
            code = resp.status
            payload = json.loads(resp.read())
            completion_tokens = payload.get("usage", {}).get("completion_tokens", -1)
    except urllib.error.HTTPError as e:
        code = e.code
        try:
            e.read()
        except Exception:
            pass
    except Exception:
        code = 0
    latency = time.time() - start
    with lock:
        results.append((arrival_t, start, latency, code, completion_tokens))


def poisson_worker(rate, token_cycle, gw, modelpath, end_time, results, lock, executor, futures, futures_lock):
    """Schedules Poisson(rate) arrivals until end_time. Never blocks on a
    response: each arrival is handed to the thread pool and the loop moves
    straight on to drawing the next inter-arrival time."""
    if rate <= 0:
        return
    while True:
        interval = random.expovariate(rate)
        time.sleep(interval)
        now = time.time()
        if now >= end_time:
            return
        token = next(token_cycle)
        fut = executor.submit(send_request, gw, modelpath, token, None, now, results, lock)
        with futures_lock:
            futures.append(fut)


def summarize(group, rows):
    if not rows:
        return f"{group:12s} sent=0"
    lats = sorted(r[2] for r in rows)
    codes = {}
    tok_total = 0
    for _, _, _, code, tok in rows:
        codes[code] = codes.get(code, 0) + 1
        if tok and tok > 0:
            tok_total += tok

    def pct(p):
        idx = min(len(lats) - 1, max(0, int(len(lats) * p)))
        return lats[idx]

    code_str = " ".join(f"{c}={n}" for c, n in sorted(codes.items(), key=lambda kv: -kv[1]))
    return (
        f"{group:12s} sent={len(rows):<6d} completion_tokens={tok_total:<8d} "
        f"p50={pct(0.50):.2f}s p95={pct(0.95):.2f}s p99={pct(0.99):.2f}s "
        f"codes=[{code_str}]"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gw", required=True)
    ap.add_argument("--modelpath", default="/maas-fairness-poc/maas-vllm-gpu")
    ap.add_argument("--duration", type=float, required=True, help="arrival window, seconds")
    ap.add_argument("--rate-app1", type=float, default=0.0, help="req/s, Poisson mean")
    ap.add_argument("--rate-app2", type=float, default=0.0, help="req/s, Poisson mean")
    ap.add_argument("--rate-end-users", type=float, default=0.0, help="req/s, Poisson mean")
    ap.add_argument("--key-app1")
    ap.add_argument("--key-app2")
    ap.add_argument("--key-end-alpha")
    ap.add_argument("--key-end-beta")
    ap.add_argument("--out", required=True, help="directory for per-request logs")
    ap.add_argument("--max-workers", type=int, default=1000)
    ap.add_argument("--drain-timeout", type=float, default=100.0, help="seconds to wait for in-flight requests after the arrival window closes")
    ap.add_argument(
        "--client-timeout", type=float, default=90.0,
        help="UNI-157: urlopen timeout, seconds. Must exceed flowControl.defaultRequestTTL "
             "(300s live) for a run to exercise the EPP's own TTL eviction -- left at the "
             "90s default, the client abandons the connection first and the EPP records "
             "EvictedContextCancelled instead of EvictedTTL.",
    )
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    import os

    os.makedirs(args.out, exist_ok=True)

    executor = ThreadPoolExecutor(max_workers=args.max_workers)
    results = {"app1": [], "app2": [], "end-users": []}
    locks = {g: threading.Lock() for g in results}
    futures = []
    futures_lock = threading.Lock()

    def bound_send(gw, modelpath, token, group, arrival_t):
        send_request(gw, modelpath, token, group, arrival_t, results[group], locks[group], args.client_timeout)

    def make_worker(rate, group, token_cycle, end_time):
        def run():
            if rate <= 0:
                return
            while True:
                interval = random.expovariate(rate)
                time.sleep(interval)
                now = time.time()
                if now >= end_time:
                    return
                token = next(token_cycle)
                fut = executor.submit(bound_send, args.gw, args.modelpath, token, group, now)
                with futures_lock:
                    futures.append(fut)

        return run

    end_time = time.time() + args.duration
    threads = []
    if args.rate_app1 > 0:
        threads.append(threading.Thread(target=make_worker(args.rate_app1, "app1", itertools.cycle([read_key(args.key_app1)]), end_time)))
    if args.rate_app2 > 0:
        threads.append(threading.Thread(target=make_worker(args.rate_app2, "app2", itertools.cycle([read_key(args.key_app2)]), end_time)))
    if args.rate_end_users > 0:
        end_cycle = itertools.cycle([read_key(args.key_end_alpha), read_key(args.key_end_beta)])
        threads.append(threading.Thread(target=make_worker(args.rate_end_users, "end-users", end_cycle, end_time)))

    if not threads:
        print("no tenant has rate > 0, nothing to do", file=sys.stderr)
        sys.exit(1)

    print(
        f"load: open-loop Poisson arrivals rate app1={args.rate_app1}/s app2={args.rate_app2}/s "
        f"end-users={args.rate_end_users}/s duration={args.duration}s seed={args.seed}",
        flush=True,
    )

    start_wall = time.time()
    for t in threads:
        t.start()

    # Visible progress: poll rather than block silently for the whole window.
    while time.time() < end_time:
        time.sleep(15)
        elapsed = time.time() - start_wall
        with futures_lock:
            n_pending = sum(1 for f in futures if not f.done())
        counts = {g: len(r) for g, r in results.items()}
        print(f"[{elapsed:.0f}s/{args.duration:.0f}s] dispatched={counts} in-flight={n_pending}", flush=True)

    for t in threads:
        t.join()

    with futures_lock:
        pending = list(futures)
    n_before = len(pending)
    print(f"arrival window closed ({n_before} requests dispatched); draining in-flight for up to {args.drain_timeout:.0f}s", flush=True)
    done, not_done = futures_wait(pending, timeout=args.drain_timeout)
    if not_done:
        print(f"WARNING: {len(not_done)} requests still in flight after drain timeout; counted as incomplete", flush=True)
    executor.shutdown(wait=False, cancel_futures=True)

    print("load: done.", flush=True)
    for group, rows in results.items():
        # persist raw per-request rows for offline analysis
        with open(f"{args.out}/{group}.log", "w") as f:
            for arrival_t, start, latency, code, tok in rows:
                f.write(f"{arrival_t:.6f} {start:.6f} {latency:.4f} {code} {tok}\n")
        print(summarize(group, rows))


if __name__ == "__main__":
    main()
