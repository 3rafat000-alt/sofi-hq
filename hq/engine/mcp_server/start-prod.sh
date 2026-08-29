## FILE: hq/engine/mcp_server/start-prod.sh
#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
export PYTHONPATH="/home/es3dlll/Desktop/SOFI:${PYTHONPATH:-}"
mkdir -p data
# Load .env if exists
if [ -f ".env" ]; then
  set -a
  source .env
  set +a
fi
HOST="${MCP_HOST:-127.0.0.1}"
PORT="${MCP_PORT:-8765}"
# Ensure data dir and init DB (via python)
python3 -c "import sys; sys.path.insert(0, '/home/es3dlll/Desktop/SOFI'); from hq.engine.mcp_server.ticket_bus import init_db; init_db(); print('DB ready')"
echo "[$(date -Is)] Starting SOFI MCP PROD on $HOST:$PORT — PID $$" | tee -a data/server.log
exec python3 -m uvicorn hq.engine.mcp_server.main:app --host "$HOST" --port "$PORT" --app-dir /home/es3dlll/Desktop/SOFI --log-level info
