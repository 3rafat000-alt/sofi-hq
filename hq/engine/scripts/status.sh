#!/usr/bin/env bash
# status.sh — pulse of the live infrastructure (read-only)
set -u
echo "═══ Services ═══"
printf "caddy:      %s\n" "$(systemctl is-active caddy)"
printf "php8.5-fpm: %s\n" "$(systemctl is-active php8.5-fpm)"
printf "cloudflared:%s\n" "$(systemctl is-active cloudflared)"
echo "═══ Sockets FPM ═══"
ls -1 /run/php/*.sock 2>/dev/null | sed 's/^/  /'
echo "═══ Domain health (sakk only after the 2026-08-25 restructure) ═══"
for u in http://sakk.local https://sakk.zanjour.com; do
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 6 "$u" || echo ERR)
  printf "  %-34s → %s\n" "$u" "$code"
done
echo "═══ Latest caddy errors ═══"
journalctl -u caddy -n 3 --no-pager -p err 2>/dev/null || sudo journalctl -u caddy -n 3 --no-pager -p err 2>/dev/null || echo "  (requires privileges)"
