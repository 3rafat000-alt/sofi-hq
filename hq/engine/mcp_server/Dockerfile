## FILE: hq/engine/mcp-server/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p data
EXPOSE 8765
# Shim for hyphen package — same as run.sh
RUN echo 'from pathlib import Path; import sys, importlib.util, types; base=Path("/app"); pkg=types.ModuleType("hq"); pkg.__path__=[str(base.parent.parent)]; sys.modules["hq"]=pkg; pkg2=types.ModuleType("hq.engine"); pkg2.__path__=[str(base.parent)]; sys.modules["hq.engine"]=pkg2; pkg3=types.ModuleType("hq.engine.mcp_server"); pkg3.__path__=[str(base)]; sys.modules["hq.engine.mcp_server"]=pkg3' > /tmp/preload.py
CMD ["sh","-c","python _run_shim.py 2>/dev/null || python -m uvicorn _run_shim:app --host 0.0.0.0 --port 8765"]
