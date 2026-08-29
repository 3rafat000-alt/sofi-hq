## FILE: hq/engine/mcp_server/docs/release-plan.md
# Release Plan — SOFI HQ Local MCP Server v1.0.0
> Date: 2026-08-29 — Owner: brd-ceo + ops-lead — Law 10 main tree only

## 1) ماذا ننشر؟
حافلة MCP محلية على localhost:8765 — 7 ملفات Python + 2 DB + WS+REST + Envelope v1 — تراخيص MIT/Apache/BSD فقط.

## 2) خطوات النشر — Runbook

| # | الخطوة | الأمر | التحقق |
|---|---|---|---|
| 0 | نسخ احتياطي | `cp hq/engine/mcp_server/data/*.db hq/engine/mcp_server/data/backup/$(date +%Y-%m-%d)/` | `ls backup/` |
| 1 | إيقاف قديم | `bash hq/engine/mcp_server/stop.sh` | `lsof -i :8765` فارغ |
| 2 | تحديث كود | `git pull` على الشجرة الرئيسية | `git status` clean |
| 3 | تثبيت اعتماديات | `pip install --break-system-packages -r hq/engine/mcp_server/requirements.txt` | exit 0 |
| 4 | تشغيل | `bash hq/engine/mcp_server/run.sh` | `curl -H "X-API-Key: $KEY" http://127.0.0.1:8765/health` →200 |
| 5 | فحص صحة | `sqlite3 data/messages.db "SELECT count(*) FROM messages"` | rows OK |
| 6 | اختبار دخان | 5 محاولات cross-room → كلها 403 | `pytest tests/test_ticket_bus.py -v` →7 passed |
| 7 | مراقبة | `tail -f data/server.log` + `python scripts/measure_kpi.py` | P95 <100ms |

## 3) Rollback — العودة خلال 60 ثانية
```bash
bash hq/engine/mcp_server/stop.sh
cp hq/engine/mcp_server/data/backup/2026-08-29/*.db hq/engine/mcp_server/data/
bash hq/engine/mcp_server/run.sh
# verify
curl -H "X-API-Key: $KEY" http://127.0.0.1:8765/health
```
*Evidence: كل خطوة بـ file:line و exit code — لا حذف، نسخ فقط*

## 4) المتطلبات
- Python 3.10+ (مختبر 3.14.4) — FastAPI 0.136, Pydantic 2.13, Uvicorn 0.48
- المنفذ 8765 حر — المفتاح في `.env SOFI_MCP_API_KEY`
- لا Docker مطلوب — Dockerfile اختياري: `docker build -f hq/engine/mcp_server/Dockerfile -t sofi-mcp .`

## 5) المخاطر والاحتياطات
- المنفذ مشغول → `stop.sh` يحرره
- DB locked → WAL mode + timeout 10s + retry
- ترخيص GPL → فحص `grep -r "GPL"` قبل merge — مرفوض
- سر مسرب → `grep -r "sk-"` → 0 + تدوير المفتاح

## 6) ما بعد النشر
- لوحة KPIs: `docs/kpi-dashboard.md` + `scripts/measure_kpi.py` كل 10 دقائق
- سجلات: `data/server.log` + `audit_logs` append-only
- تحديث ذاكرة: قرار النشر يُكتب في `hq/brain/cortex-decisions.md` عبر `memory.py`

## 7) إقرار
النشر المحلي تم بنجاح — المنفذ 8765 يستجيب — exit 0 — جاهز لربط OpenCode عبر WS client.

*Evidence: hq/engine/mcp_server/run.sh:1 — hq/engine/mcp_server/stop.sh:1 — data/server.log*
