## FILE: hq/engine/mcp_server/stop.sh
#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
PORT=$(grep -E "^MCP_PORT" .env 2>/dev/null | cut -d= -f2 | tr -d ' ' || echo "8765")
PORT=${PORT:-8765}

# Try PID file first
if [ -f "data/server.pid" ]; then
  PID=$(cat data/server.pid)
  if ps -p "$PID" > /dev/null 2>&1; then
    echo "🛑 Stopping PID $PID ..."
    kill "$PID" 2>/dev/null || true
    sleep 2
    if ps -p "$PID" > /dev/null 2>&1; then
      echo "⚠️ Force killing $PID"
      kill -9 "$PID" 2>/dev/null || true
    fi
    echo "✅ Server stopped (PID $PID)"
  else
    echo "ℹ️ PID $PID not running"
  fi
  rm -f data/server.pid
fi

# Also check lsof
if command -v lsof &>/dev/null && lsof -i :"$PORT" &>/dev/null; then
  echo "🛑 Port $PORT still busy — killing via lsof..."
  lsof -ti :"$PORT" | xargs -r kill 2>/dev/null || true
  sleep 1
  if lsof -ti :"$PORT" | xargs -r kill -9 2>/dev/null; then
    echo "✅ Killed via lsof"
  fi
fi

# pkill fallback
if pgrep -f "uvicorn.*$PORT" &>/dev/null; then
  echo "🛑 Killing via pgrep uvicorn..."
  pkill -f "uvicorn.*$PORT" || true
  sleep 1
fi

if command -v lsof &>/dev/null && lsof -i :"$PORT" &>/dev/null; then
  echo "❌ Port $PORT still busy after stop"
  lsof -i :"$PORT" || true
  exit 1
else
  echo "✅ Server stopped — port $PORT free"
  if [ -f "data/server.log" ]; then
    echo "📄 Last 5 log lines:"
    tail -n 5 data/server.log || true
  fi
fi
