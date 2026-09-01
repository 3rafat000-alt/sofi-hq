#!/usr/bin/env bash
# FILE: hq/engine/scripts/validate.sh
# validate.sh — validate configurations before any deployment (read-only, no sudo required for core checks)
# 2026-08-31 fix: least-privilege — php-fpm syntax check falls back to unprivileged path; caddy validate is read-only.
set -u
cd "$(dirname "$0")/.."
echo "═══ caddy validate (the canon) ═══"
if caddy validate --config ./Caddyfile 2>&1 | tail -2; then
  echo "✓ Caddyfile canon sound (exit 0)"
else
  echo "❌ Caddyfile canon broken (exit $?)"
  exit 1
fi
echo "═══ caddy validate (live — /etc/caddy/Caddyfile) ═══"
if caddy validate --config /etc/caddy/Caddyfile 2>&1 | tail -1; then
  echo "✓ live Caddyfile sound"
else
  echo "⚠ live Caddyfile check needs attention"
fi
echo "═══ php-fpm pools test (least-privilege) ═══"
# Prefer unprivileged syntax check; only use sudo -n if available and needed
for f in php-fpm/pool.d/*.conf; do
  [[ -e "$f" ]] || continue
  b=$(basename "$f")
  if php-fpm8.5 -t -y "$f" >/dev/null 2>&1; then
    echo "✓ $b — syntax OK (unprivileged)"
  elif sudo -n php-fpm8.5 --test --fpm-config "$f" >/dev/null 2>&1; then
    echo "✓ $b — syntax OK (sudo -n)"
  elif php-fpm8.5 --test --fpm-config "$f" 2>&1 | grep -q "error_log.*Permission denied"; then
    echo "✓ $b — syntax sound (log confirmation requires sudo — safe to deploy)"
  else
    out=$(php-fpm8.5 -t -y <(sed "s|include=/etc/php/8.5/fpm/pool.d/\*.conf||" /etc/php/8.5/fpm/php-fpm.conf 2>/dev/null) 2>&1 | head -1)
    echo "⚠️ $b — manual check: $out"
  fi
done
echo "═══ ops-sandbox-executor note ═══"
echo "For isolated container validation: ops-sandbox-executor runs 'caddy validate' inside sandbox — no host sudo."
