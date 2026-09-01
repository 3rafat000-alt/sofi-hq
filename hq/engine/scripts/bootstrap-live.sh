#!/usr/bin/env bash
# FILE: hq/engine/scripts/bootstrap-live.sh
# bootstrap-live.sh — run ONCE with root privileges (sudo) to bind /etc/caddy/Caddyfile to the canon.
# Afterwards: any edit to hq/engine/Caddyfile needs only deploy.sh (validate+reload, no sudo for caddy reload).
# Least-privilege doctrine (Law 6 fix 2026-08-31):
#   - This is the ONLY script that requires root (writes /etc/caddy). Every other deploy path uses the
#     unauthenticated Caddy admin API (deploy.sh) and never touches /etc/caddy again.
#   - The legacy symlink `caddy → hq/engine` was removed 2026-08-31 (system-state-current.md:17 fix):
#     final removal verified `ls -l /home/es3dlll/Desktop/SOFI/caddy` = not found. No replacement symlink — the canon lives at hq/engine/Caddyfile and is imported directly by /etc/caddy/Caddyfile.
#   - For containerized builds, ops-sandbox-executor (room 11) can run bootstrap inside an isolated container instead of on the host.
set -e
REPO=/home/es3dlll/Desktop/SOFI/hq/engine/Caddyfile

if [[ $EUID -ne 0 ]]; then
  echo "✗ bootstrap-live.sh requires root: run 'sudo bash hq/engine/scripts/bootstrap-live.sh'"
  echo "  Reason: writes /etc/caddy/Caddyfile (single privileged write; all later deploys are unprivileged via Caddy admin API)."
  exit 1
fi
if [[ ! -f "$REPO" ]]; then
  echo "✗ canon not found: $REPO"
  exit 1
fi
# Least-privilege check: ensure caddy symlink legacy is gone
if [[ -L "/home/es3dlll/Desktop/SOFI/caddy" ]]; then
  echo "⚠ legacy symlink caddy → hq/engine still exists — removing (Law 13 path guard)"
  rm -f /home/es3dlll/Desktop/SOFI/caddy
  echo "✓ legacy symlink removed"
else
  echo "✓ no legacy caddy symlink (already clean)"
fi

cat > /etc/caddy/Caddyfile <<CADDYEOF
# SOFI GitOps — live source: $REPO
# Edit there, then run: bash hq/engine/scripts/deploy.sh (no sudo needed for reload)
import $REPO
CADDYEOF
echo "✓ wrote /etc/caddy/Caddyfile → import $REPO"

caddy validate --config /etc/caddy/Caddyfile >/dev/null && echo "✓ bootstrap sound — caddy validate PASS" || { echo "❌ caddy validate FAIL"; exit 1; }

# Prefer unprivileged reload via admin API; fallback to systemctl
if caddy reload --config /etc/caddy/Caddyfile >/dev/null 2>&1; then
  echo "✓ caddy reload via admin API (no sudo)"
else
  systemctl reload caddy && echo "✓ caddy reload via systemctl (privileged fallback)"
fi

rm -f /etc/caddy/README.md && echo "✓ /etc/caddy clean: only the slave Caddyfile"
echo "═══ bootstrap-live complete — future deploys: bash hq/engine/scripts/deploy.sh (unprivileged) ═══"
