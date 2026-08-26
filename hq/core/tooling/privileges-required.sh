#!/usr/bin/env bash
# privileges-required.sh — everything requiring root in M10-c (single run: sudo bash tooling/privileges-required.sh)
set -u
echo "── 1) Retire the printer and OpenWA services ──"
systemctl disable --now sofi-print openwa 2>/dev/null
rm -f /etc/systemd/system/sofi-print.service /etc/systemd/system/openwa.service
systemctl daemon-reload && echo "✓ Both units removed"
echo "── 2) Docker: purge ← install ← configure ──"
bash "$(dirname "$0")/docker/reinstall.sh"
echo "── 3) Upgrade /etc/caddy to the SOFI root + clean it ──"
bash "$(dirname "$0")/../caddy/scripts/bootstrap-live.sh"
echo "═══ All done — reopen your terminal for docker group membership ══"
