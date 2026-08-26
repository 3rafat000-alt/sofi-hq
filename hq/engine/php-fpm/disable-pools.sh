#!/usr/bin/env bash
# disable-pools.sh — run once with root privileges: sudo bash caddy/php-fpm/disable-pools.sh
# Disables the pools of retired projects and keeps sakk only — matching the repository structure after 2026-08-25
set -eu
cd /etc/php/8.5/fpm/pool.d
mkdir -p disabled
for p in jw owais sofi sofi-demo www; do
  [ -f "$p.conf" ] && mv "$p.conf" disabled/ && echo "✓ pool disabled: $p"
done
php-fpm8.5 --test >/dev/null 2>&1 || { echo "❌ syntax check failed — no reload"; exit 1; }
systemctl reload php8.5-fpm && echo "✓ php8.5-fpm reloaded seamlessly"
echo "── current sockets ──"; ls -1 /run/php/*.sock
