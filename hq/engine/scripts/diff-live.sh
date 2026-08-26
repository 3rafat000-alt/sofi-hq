#!/usr/bin/env bash
# diff-live.sh — confirm live wiring to the repository + match FPM pools
set -u
cd "$(dirname "$0")/.."
if grep -qE "SOFI/(projects/)?caddy/Caddyfile" /etc/caddy/Caddyfile 2>/dev/null; then
  echo "✓ live imports the canon from the repository (GitOps)"
else
  echo "⚠️ live is on the old path — finish the upgrade: sudo bash caddy/scripts/bootstrap-live.sh"
  exit 1
fi
fail=0
for f in php-fpm/pool.d/*.conf; do
  b=$(basename "$f")
  if diff -q "$f" "/etc/php/8.5/fpm/pool.d/$b" >/dev/null 2>&1; then
    echo "✓ pool:$b"
  else
    echo "⚠️ pool diff:$b"; fail=1
  fi
done
exit $fail
