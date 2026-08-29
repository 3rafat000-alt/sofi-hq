#!/usr/bin/env bash
# check-env-guard.sh — بوابة بيئة الإنتاج (RCCF-02 ضمن GATE-PZ0-2026-08-26 · غرفة DevOps)
# يفشل (exit≠0) إذا كان APP_DEBUG=true أو APP_ENV=local في backend/.env المستهدف.
# منذ GATE-INT-PURGE-2026-08-26: يفشل أيضاً إذا كانت STRIPE_SECRET/CCPAYMENT_APP_SECRET/FCM_PROJECT_ID غير فارغة
# (إبقاء البريد فقط — تجاوز موثق: ALLOW_PROVIDER_KEYS=1).
# وسيط اختياري: مسار ملف .env بديل (لمحاكاة الاختبار على نسخة مؤقتة دون لمس الحقيقي).
set -u

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
ENV_FILE="${1:-$REPO_ROOT/projects/sakk/backend/.env}"

fail() { echo "✗ ENV-GUARD FAIL: $*" >&2; exit 1; }

[ -f "$ENV_FILE" ] || fail "ملف .env غير موجود في: $ENV_FILE"

get() { sed -n "s/^$1=//p" "$ENV_FILE" | tail -n1 | tr -d '[:space:]'; }

APP_ENV_VAL="$(get APP_ENV)"
APP_DEBUG_VAL="$(get APP_DEBUG)"

# ── GATE-INT-PURGE-2026-08-26: حظر مفاتيح مزودات الدفع/الإشعارات (البريد فقط) ──
# يفشل إذا كان أي من STRIPE_SECRET أو CCPAYMENT_APP_SECRET أو FCM_PROJECT_ID غير فارغ.
# تجاوز موثق صريح: ALLOW_PROVIDER_KEYS=1 ./scripts/check-env-guard.sh
if [ "${ALLOW_PROVIDER_KEYS:-0}" = "1" ]; then
  echo "⚠ ENV-GUARD: ALLOW_PROVIDER_KEYS=1 — مفاتيح المزودات مسموحة مؤقتاً (تجاوز موثق لأمر GATE-INT-PURGE)"
else
  PROVIDER_FAIL_LIST=""
  for KEY_VAR in STRIPE_SECRET CCPAYMENT_APP_SECRET FCM_PROJECT_ID; do
    [ -n "$(get "$KEY_VAR")" ] && PROVIDER_FAIL_LIST="$PROVIDER_FAIL_LIST $KEY_VAR"
  done
  if [ -n "$PROVIDER_FAIL_LIST" ]; then
    fail "مفاتيح مزودات غير فارغة في $ENV_FILE:[$PROVIDER_FAIL_LIST] — محظورة بأمر المالك GATE-INT-PURGE-2026-08-26 (تجاوز موثق: ALLOW_PROVIDER_KEYS=1)"
  fi
fi

if [ "${ALLOW_LOCAL_ENV:-0}" = "1" ]; then
  echo "⚠ ENV-GUARD: ALLOW_LOCAL_ENV=1 — قيم التطوير المحلي مسموحة مؤقتاً (تجاوز موثق لأغراض تطويرية)"
  exit 0
fi

[ "$APP_ENV_VAL" = "production" ] || fail "APP_ENV='$APP_ENV_VAL' ليست production في $ENV_FILE"
[ "$APP_DEBUG_VAL" != "true" ] || fail "APP_DEBUG=true محظور خارج التجاوز الموثق في $ENV_FILE"

echo "✓ ENV-GUARD OK: APP_ENV=$APP_ENV_VAL APP_DEBUG=$APP_DEBUG_VAL ($ENV_FILE)"
exit 0
