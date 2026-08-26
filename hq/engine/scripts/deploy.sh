#!/usr/bin/env bash
# deploy.sh — after bootstrap: validate the canon and reload the live config (no copying — live imports directly)
set -eu
cd "$(dirname "$0")/.."
caddy validate --config ./Caddyfile >/dev/null && echo "✓ canon sound"
if caddy reload --config /etc/caddy/Caddyfile >/dev/null 2>&1; then
  echo "✓ reloaded (without sudo — via the admin API)"
else
  sudo systemctl reload caddy && echo "✓ reloaded (sudo)"
fi
./scripts/status.sh | sed -n '1,6p'
