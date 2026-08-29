## FILE: hq/engine/mcp_server/scripts/measure_kpi.py
"""KPI measurement — 10 minutes — REST P95, WS latency, error rate."""
import asyncio, time, statistics, httpx, json, sys
from pathlib import Path

BASE = "http://127.0.0.1:8765"
KEY = "dev-key-change-me"

async def measure_rest(n=1000):
    times=[]
    async with httpx.AsyncClient(timeout=5) as client:
        for i in range(n):
            start=time.perf_counter()
            r=await client.post(f"{BASE}/api/v1/message", headers={"X-API-Key":KEY,"X-Sender":f"kpi-agent-{i%50}"}, json={"recipient":"bck-lead","content":f"kpi {i}","evidence":"scripts/measure_kpi.py:1"})
            elapsed=(time.perf_counter()-start)*1000
            times.append(elapsed)
            await asyncio.sleep(0.01)
    times_sorted=sorted(times)
    p95=times_sorted[int(0.95*len(times_sorted))]
    return {"avg":statistics.mean(times),"p95":p95,"min":min(times),"max":max(times),"count":n}

async def measure_ws(n=100):
    try:
        import websockets
    except ImportError:
        return {"error":"websockets not installed"}
    times=[]
    uri=f"ws://127.0.0.1:8765/ws/agent/bck-api-engineer?api_key={KEY}"
    for _ in range(n):
        async with websockets.connect(uri) as ws:
            start=time.perf_counter()
            await ws.send(json.dumps({"content":"ping","evidence":"measure_kpi.py:1"}))
            await asyncio.wait_for(ws.recv(), timeout=2)
            elapsed=(time.perf_counter()-start)*1000
            times.append(elapsed)
            await asyncio.sleep(0.02)
    times_sorted=sorted(times)
    p95=times_sorted[int(0.95*len(times_sorted))] if times else None
    return {"avg":statistics.mean(times) if times else None,"p95":p95,"count":n}

async def main():
    print("Measuring REST 200 sequential...")
    rest=await measure_rest(200)
    print(f"REST: {rest}")
    print("Measuring WS 50...")
    ws=await measure_ws(50)
    print(f"WS: {ws}")
    # Error rate via invalid requests
    async with httpx.AsyncClient() as client:
        ok=0; total=20
        for i in range(total):
            r=await client.get(f"{BASE}/health", headers={"X-API-Key":KEY})
            if r.status_code==200:
                ok+=1
        print(f"Health success {ok}/{total}")
    print("Done")

if __name__=="__main__":
    asyncio.run(main())
