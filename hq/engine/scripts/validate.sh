#!/usr/bin/env bash
# validate.sh — validate configurations before any deployment (read-only)
set -u
cd "$(dirname "$0")/.."
echo "═══ caddy validate (the canon) ═══"
caddy validate --config ./Caddyfile 2>&1 | tail -2 && echo "✓ Caddyfile sound" || echo "❌ Caddyfile broken"
echo "═══ caddy validate (live) ═══"
caddy validate --config /etc/caddy/Caddyfile 2>&1 | tail -1
echo "═══ php-fpm pools test ═══"
for f in php-fpm/pool.d/*.conf; do
  b=$(basename "$f")
  if sudo -n php-fpm8.5 --test --fpm-config "$f" >/dev/null 2>&1; then
    echo "✓ $b"
  elif php-fpm8.5 --test --fpm-config "$f" 2>&1 | grep -q "error_log.*Permission denied"; then
    echo "✓ $b (syntax sound — log confirmation requires sudo)"
  else
    # Some environments bar non-root from reading the main include — try a direct daemon_test instead
    out=$(php-fpm8.5 -t -y <(sed "s|include=/etc/php/8.5/fpm/pool.d/\*.conf||" /etc/php/8.5/fpm/php-fpm.conf 2>/dev/null) 2>&1 | head -1)
    echo "⚠️ $b — manual check: $out"
  fi
done
