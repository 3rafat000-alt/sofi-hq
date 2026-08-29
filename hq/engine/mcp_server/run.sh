## FILE: hq/engine/mcp_server/run.sh
#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
# Use symlink-compat package path: hq.engine.mcp_server via PYTHONPATH=/home/es3dlll/Desktop/SOFI
export PYTHONPATH="/home/es3dlll/Desktop/SOFI:${PYTHONPATH:-}"

# Check Python
if ! command -v python3 &>/dev/null; then echo "❌ Python3 not found"; exit 1; fi
PYV=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Python $PYV detected"

# Create data dir
mkdir -p data

# Ensure .env
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then cp .env.example .env; echo "⚠️ Created .env from .env.example"; fi
fi
if [ ! -f ".env" ]; then
  echo "SOFI_MCP_API_KEY=dev-key-change-me" > .env
  echo "MCP_HOST=127.0.0.1" >> .env
  echo "MCP_PORT=8765" >> .env
fi

PORT=$(grep -E "^MCP_PORT" .env 2>/dev/null | cut -d= -f2 | tr -d ' '); PORT=${PORT:-8765}
HOST=$(grep -E "^MCP_HOST" .env 2>/dev/null | cut -d= -f2 | tr -d ' '); HOST=${HOST:-127.0.0.1}

# Free port if busy
if command -v lsof &>/dev/null && lsof -i :"$PORT" &>/dev/null; then
  echo "⚠️ Port $PORT busy — freeing via stop.sh..."
  bash "$DIR/stop.sh" || true
  sleep 1
  if lsof -i :"$PORT" &>/dev/null; then echo "❌ Port $PORT still busy"; exit 1; fi
fi

echo "🚀 Starting MCP Server on http://$HOST:$PORT ..."
echo "   Logs: $DIR/data/server.log"
# Install deps if needed using system pip with --break-system-packages or venv
if ! python3 -c "import fastapi" 2>/dev/null; then
  echo "📦 Installing requirements..."
  pip install --break-system-packages -q -r requirements.txt || pip install -q -r requirements.txt
fi

# Start uvicorn — use package import path via symlink
echo "MCP Server running on http://$HOST:$PORT" | tee -a data/server.log
nohup python3 -m uvicorn hq.engine.mcp_server.main:app --host "$HOST" --port "$PORT" --reload --app-dir /home/es3dlll/Desktop/SOFI >> data/server.log 2>&1 &
echo $! > data/server.pid
sleep 3
if ps -p $(cat data/server.pid) > /dev/null 2>&1; then
  echo "✅ MCP Server running on http://$HOST:$PORT (PID $(cat data/server.pid))"
  KEY=$(grep -E "^SOFI_MCP_API_KEY" .env | cut -d= -f2 | tr -d ' '); KEY=${KEY:-dev-key-change-me}
  if curl -sf -H "X-API-Key: $KEY" "http://$HOST:$PORT/health" > /tmp/sofi_health.json 2>/dev/null; then
    echo "✅ Health check passed:"
    cat /tmp/sofi_health.json; echo ""
  else
    echo "⚠️ Health check failed — check data/server.log"
    tail -n 30 data/server.log || true
  fi
else
  echo "❌ Failed to start — check data/server.log"
  tail -n 50 data/server.log || true
  exit 1
fi
