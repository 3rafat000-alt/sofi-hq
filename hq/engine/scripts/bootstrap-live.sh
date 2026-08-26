#!/usr/bin/env bash
# bootstrap-live.sh — run once with root privileges (sudo):
# makes /etc/caddy/Caddyfile import the canon straight from the repository.
# Afterwards: any edit to projects/caddy/Caddyfile needs only deploy.sh (validate+reload).
set -e
REPO=/home/es3dlll/Desktop/SOFI/hq/engine/Caddyfile
cat > /etc/caddy/Caddyfile <<CADDYEOF
# SOFI GitOps — live source: $REPO
# Edit there, then run: projects/caddy/scripts/deploy.sh
import $REPO
CADDYEOF
caddy validate --config /etc/caddy/Caddyfile >/dev/null && echo "✓ bootstrap sound"
systemctl reload caddy && echo "✓ caddy runs from the SOFI repository"
rm -f /etc/caddy/README.md && echo "✓ /etc/caddy clean: only the slave Caddyfile"
