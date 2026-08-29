## FILE: hq/engine/mcp_server/README.md
# SOFI HQ Local MCP Server — دليل التشغيل الكامل
> **Local-First — 100% Free — localhost:8765 — MIT/Apache only**
> **يحوّل القوانين 2 و3 و4 و7 إلى كود لا يمكن تجاوزه**

## لماذا يهمك؟
هذا النظام يربط 114 وكيلًا بـ15 قائدًا ويمنع أي تواصل مباشر بين الغرف — أي محاولة تُرفض وتُسجل فورًا. كل قرار ورسالة محفوظة للأبد ولا يمكن تعديلها. يعمل على جهازك بدون إنترنت.

## 1) التثبيت — خطوة بخطوة

```bash
# 1. تأكد Python 3.10+
python3 --version  # يجب >=3.10

# 2. انسخ الإعدادات
cp hq/engine/mcp_server/.env.example hq/engine/mcp_server/.env
# عدّل المفتاح:
nano hq/engine/mcp_server/.env  # ضع SOFI_MCP_API_KEY=sk-your-key

# 3. شغّل
bash hq/engine/mcp_server/run.sh
# ترى: MCP Server running on http://127.0.0.1:8765
```

## 2) التشغيل والإيقاف — والتشغيل الدائم بعد إعادة التشغيل

```bash
bash hq/engine/mcp_server/run.sh   # تشغيل مؤقت + فحص صحة (للتطوير)
bash hq/engine/mcp_server/stop.sh  # يوقف + يحرر المنفذ
cat hq/engine/mcp_server/data/server.log  # السجلات
```

### التشغيل الدائم — يعود تلقائياً بعد إعادة التشغيل (احترافي — systemd)
الخادم الآن يشتغل كخدمة نظام دائمة — حتى لو انقطعت الكهرباء أو أعدت التشغيل، يعود وحده خلال 3 ثوانٍ.

```bash
# تثبيت الخدمة الدائمة (مرة واحدة)
bash hq/engine/mcp_server/install-service.sh
# يفعل: إنشاء ~/.config/systemd/user/sofi-mcp.service + تفعيل linger + enable + start

# أو يدويًا:
systemctl --user daemon-reload
systemctl --user enable --now sofi-mcp.service
loginctl enable-linger $USER   # يضمن التشغيل بعد إعادة التشغيل حتى بدون تسجيل دخول

# إدارة الخدمة الدائمة
systemctl --user status sofi-mcp.service    # الحالة — يجب أن ترى active (running) و Memory 38M/500M
systemctl --user restart sofi-mcp.service   # إعادة تشغيل
systemctl --user stop sofi-mcp.service      # إيقاف (سيعود تلقائياً إن قتل — Restart=always)
journalctl --user -u sofi-mcp.service -f    # السجلات الحية
journalctl --user -u sofi-mcp.service --since "1 hour ago" --no-pager | tail -n 20
tail -f hq/engine/mcp_server/data/server.log  # سجل uvicorn المباشر

# التحقق أنه سيعود بعد إعادة التشغيل
systemctl --user is-enabled sofi-mcp.service  # يجب: enabled
loginctl show-user $USER -p Linger            # يجب: Linger=yes
```

**كيف يعمل؟** الخدمة تستخدم `Restart=always` و `RestartSec=3` — أي سقوط أو `kill` يعيدها خلال 3 ثوانٍ (تم اختباره: `kill PID` → عادت بـ PID جديد و health OK). محمية بـ `MemoryMax=500M` و `NoNewPrivileges` و `ProtectSystem=full` — احترافي.

## 3) أمثلة curl — كل endpoint (8 أمثلة)

```bash
KEY="dev-key-change-me"  # أو من .env
BASE="http://localhost:8765"

# Health
curl -H "X-API-Key: $KEY" $BASE/health

# 1. وكيل يرسل لقائده (AC1)
curl -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -H "X-Sender: bck-api-engineer" \
  -d '{"recipient":"bck-lead","content":"تم إنجاز API الدفع","evidence":"hq/engine/mcp_server/main.py:42"}' \
  $BASE/api/v1/message

# 2. محاولة cross-room تُرفض (AC3) — 403
curl -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -H "X-Sender: bck-api-engineer" \
  -d '{"recipient":"fnt-react-engineer","content":"محاولة ممنوعة"}' \
  $BASE/api/v1/message

# 3. قائد يستشير قائدًا (AC2)
curl -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -H "X-Sender: bck-lead" \
  -d '{"subject":"مراجعة معمارية","description":"هل نستخدم SQLite؟","priority":"high","type":"consultation_request","assignee":"arc-lead"}' \
  $BASE/api/v1/tickets

# 4. قائمة رسائل
curl -H "X-API-Key: $KEY" "$BASE/api/v1/messages?agent=bck-api-engineer&page=1&limit=20"

# 5. قائمة تذاكر
curl -H "X-API-Key: $KEY" "$BASE/api/v1/tickets?status=open&priority=high"

# 6. تحديث تذكرة open→in_progress
curl -X PATCH -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -H "X-Sender: arc-lead" \
  -d '{"status":"in_progress"}' $BASE/api/v1/tickets/1

# 7. كتابة قرار في الذاكرة (AC5)
curl -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"content":"اعتمدنا SQLite كقاعدة محلية","room":"bck-lead","evidence":"hq/engine/mcp_server/main.py:1"}' \
  $BASE/api/v1/memory/decision

# 8. البحث في التدقيق
curl -H "X-API-Key: $KEY" "$BASE/api/v1/audit?agent=bck-api-engineer&type=violation"

# 9. تصدير التدقيق JSON/CSV
curl -H "X-API-Key: $KEY" "$BASE/api/v1/audit/export?format=json" -o audit.json
curl -H "X-API-Key: $KEY" "$BASE/api/v1/audit/export?format=csv" -o audit.csv

# 10. بدون مفتاح → 401 (AC7)
curl $BASE/api/v1/message -d '{}' -H "Content-Type: application/json"

# 11. محتوى فارغ → 422
curl -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -H "X-Sender: bck-api-engineer" \
  -d '{"recipient":"bck-lead","content":""}' $BASE/api/v1/message

# 12. أولوية خاطئة → 422
curl -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"subject":"x","description":"y","priority":"urgent","type":"consultation_request","assignee":"arc-lead"}' \
  $BASE/api/v1/tickets
```

## 4) أمثلة WebSocket — wscat + Python (2 أمثلة)

```bash
# wscat (npm i -g wscat)
wscat -c "ws://localhost:8765/ws/agent/bck-api-engineer?api_key=dev-key-change-me"
# ثم أرسل:
{"content":"تم","evidence":"hq/engine/mcp_server/main.py:10"}
# تتلقى: {"success":true,"status":"delivered","id":1}

wscat -c "ws://localhost:8765/ws/lead/bck-lead?api_key=dev-key-change-me"
{"content":"رد القائد","recipient":"bck-api-engineer"}
```

```python
# Python WebSocket client
import asyncio, websockets, json
async def test():
    uri = "ws://localhost:8765/ws/agent/bck-api-engineer?api_key=dev-key-change-me"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"content":"تم إنجاز المهمة","evidence":"test.py:1"}))
        print(await ws.recv())
        # محاولة cross-room تُرفض:
        await ws.send(json.dumps({"content":"محاولة","recipient":"fnt-react-engineer"}))
        print(await ws.recv())  # {"success":false,"message":"ممنوع التواصل..."}
asyncio.run(test())
```

## 5) المعمارية — DDD 4 مجالات

```
hq/engine/mcp_server/
├── config.py      — 15 غرفة + 114 وكيل + env + helpers get_room/is_lead
├── models.py      — Pydantic Envelope + Enums + validation 1-4096
├── ticket_bus.py  — validate_cross_room() + DB + triggers + audit
├── memory.py      — كتابة فورية في hq/brain/* مع filelock
├── agents_mcp.py  — send_to_lead + persistence messages.db
├── leads_mcp.py   — Ticket CRUD + escalation every hour
└── main.py        — FastAPI + WS + RateLimit + Envelope
data/
├── messages.db    — رسائل + audit_logs (WAL)
├── tickets.db     — تذاكر + audit_logs (WAL)
└── server.log
```

**التدفق:**
```
agent --WS/REST--> main.py --validate_cross_room()--> agents_mcp.py --> messages.db + audit_logs
                                          |
                                          └─> إن violation → 403 + audit + لا حفظ

lead --REST--> main.py --> leads_mcp.py --> tickets.db + WS push → assignee + incident إن critical
                                                                  └─> escalation كل ساعة → brd-ceo إن >24h

POST /memory/decision --> memory.py --> hq/brain/cortex-decisions.md (append + lock)
```

## 6) API Reference — جدول

| Method | Path | وصف | Auth | Rate |
|---|---|---|---|---|
| GET | /health | صحة | X-API-Key | لا |
| POST | /api/v1/message | إرسال رسالة | X-API-Key | 100/دقيقة لكل sender |
| GET | /api/v1/messages | قائمة رسائل | X-API-Key | لا |
| POST | /api/v1/tickets | إنشاء تذكرة | X-API-Key | 100/دقيقة |
| GET | /api/v1/tickets | قائمة تذاكر | X-API-Key | لا |
| GET | /api/v1/tickets/{id} | تفصيل تذكرة | X-API-Key | لا |
| PATCH | /api/v1/tickets/{id} | تحديث حالة | X-API-Key | لا |
| POST | /api/v1/memory/decision | كتابة قرار | X-API-Key | لا |
| POST | /api/v1/memory/session | كتابة جلسة | X-API-Key | لا |
| POST | /api/v1/memory/incident | كتابة حادث | X-API-Key | لا |
| GET | /api/v1/audit | بحث تدقيق | X-API-Key | لا |
| GET | /api/v1/audit/export | تصدير JSON/CSV | X-API-Key | لا |
| WS | /ws/agent/{id} | WS للوكلاء | ?api_key= | 100/دقيقة |
| WS | /ws/lead/{id} | WS للقادة | ?api_key= | لا |

## 7) الأسئلة الشائعة

**س: المنفذ مشغول؟** ج: `bash hq/engine/mcp_server/stop.sh` أو `lsof -i :8765`
**س: أين المفتاح؟** ج: `hq/engine/mcp_server/.env` — `SOFI_MCP_API_KEY` — لا تضع secret في الكود
**س: كيف أختبر cross-room؟** ج: أرسل `bck-api-engineer → fnt-react-engineer` → ترى 403 ورسالة عربية
**س: أين السجلات؟** ج: `data/server.log` + `sqlite3 data/messages.db "SELECT * FROM messages;"` + `sqlite3 data/tickets.db "SELECT * FROM audit_logs;"`
**س: كيف أغير 24h في الاختبار؟** ج: في `.env` ضع `ESCALATION_HOURS=0.033` (=2 دقيقة) ثم `bash run.sh`
**س: هل يدعم العربية؟** ج: نعم UTF-8 في content + رسائل أخطاء عربية/إنجليزية
**س: Docker؟** ج: `docker build -f hq/engine/mcp_server/Dockerfile -t sofi-mcp . && docker run -p 8765:8765 --env-file hq/engine/mcp_server/.env sofi-mcp`
**س: كيف أتأكد أنه دائم؟** ج: `systemctl --user is-enabled sofi-mcp.service` → enabled و `systemctl --user status sofi-mcp.service` → active (running)

## 8) الانvelope — مثال

```json
// Success
{"success":true,"message":"Message delivered","data":{"id":42,"status":"delivered"},"error":null,"meta":{"request_id":"uuid","timestamp":"2026-08-29T00:00:00Z","envelope_version":"v1","pagination":null}}
// Error 403
{"success":false,"message":"ممنوع التواصل المباشر بين الغرف — أرسل عبر قائد غرفتك (Cross-room blocked by Law 2)","data":null,"error":{"code":"FORBIDDEN","message":"Cross-room blocked by Law 2","details":[]},"meta":{}}
```

---
*Evidence: hq/engine/mcp_server/main.py:1 — openapi.yaml:1 — schema.sql:1 — Law 4 file:line + exit code + screenshot*
*License: MIT/Apache only — checked via pip-licenses*
