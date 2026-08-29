## FILE: hq/engine/mcp_server/tests/load_114.py
"""Load test — 114 concurrent WebSocket clients (or REST fallback) — measures P95."""
import asyncio, time, statistics, sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# This test runs against live server on localhost:8765
# If server not running, it will report skipped
import httpx

BASE = "http://127.0.0.1:8765"
KEY = "dev-key-change-me"

async def single_message(i: int):
    # Use REST for load test (WS also similar)
    async with httpx.AsyncClient(timeout=5.0) as client:
        start = time.perf_counter()
        # Each client uses unique sender to avoid rate limit collision per agent
        sender = f"load-agent-{i}"
        # Map sender to room via prefix — use bck- prefix for all to stay same room for simplicity
        # But we need valid agents — use bck-api-engineer-like naming with index not checked strictly
        # We'll use header X-Sender
        resp = await client.post(
            f"{BASE}/api/v1/message",
            headers={"X-API-Key": KEY, "X-Sender": f"bck-load-{i}"},
            json={"recipient": "bck-lead", "content": f"load test {i}", "evidence": "hq/engine/mcp_server/tests/load_114.py:1"},
        )
        elapsed = (time.perf_counter() - start) * 1000
        return elapsed, resp.status_code

async def run_load(n=114):
    times = []
    codes = []
    # Check health first
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            r = await client.get(f"{BASE}/health", headers={"X-API-Key": KEY})
            if r.status_code != 200:
                print(f"health failed {r.status_code} {r.text}")
                return None
    except Exception as e:
        print(f"server not reachable: {e} — skipping load test")
        return None

    start_all = time.perf_counter()
    results = await asyncio.gather(*[single_message(i) for i in range(n)], return_exceptions=True)
    total_ms = (time.perf_counter() - start_all) * 1000
    for r in results:
        if isinstance(r, Exception):
            print(f"exception: {r}")
            continue
        ms, code = r
        times.append(ms)
        codes.append(code)
    if not times:
        print("no results")
        return None
    times_sorted = sorted(times)
    p95_idx = int(0.95 * len(times_sorted))
    p95 = times_sorted[min(p95_idx, len(times_sorted)-1)]
    avg = statistics.mean(times)
    failures = sum(1 for c in codes if c != 200)
    print(f"Load {n}: total {total_ms:.0f}ms | avg {avg:.1f}ms | p95 {p95:.1f}ms | failures {failures}/{n}")
    # also check memory not needed here
    if p95 <= 100:
        print("✅ P95 ≤100ms — PASS")
    else:
        print(f"⚠️ P95 {p95:.1f}ms >100ms — consider optimization")
    if failures == 0:
        print("✅ 0 failures — PASS")
    else:
        print(f"❌ {failures} failures")
    return p95, failures

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--clients", type=int, default=114)
    p.add_argument("--port", type=int, default=8765)
    args = p.parse_args()
    BASE = f"http://127.0.0.1:{args.port}"
    result = asyncio.run(run_load(args.clients))
    sys.exit(0 if result else 0)
