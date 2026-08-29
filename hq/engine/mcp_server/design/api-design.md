## FILE: hq/engine/mcp_server/design/api-design.md
# API Design — SOFI HQ Local MCP Server
> **Frozen:** 2026-08-29 — implements openapi.yaml 1.0.0
> **DDD:** 4 domains — MCP / Ticket / Memory / Audit

## 1) Envelope — كل استجابة (api-envelope.md v1)
```json
{"success": true|false, "message": "نص بشري", "data": {}|null, "error": {"code":"UPPER_SNAKE","message":"","details":[]}|null, "meta": {"request_id":"uuid","timestamp":"ISO8601","envelope_version":"v1","pagination":{}} }
```
Codes: 200/201 success — 204 no-body — 401 UNAUTHENTICATED — 403 FORBIDDEN — 404 NOT_FOUND — 409 CONFLICT — 422 VALIDATION_ERROR — 429 RATE_LIMITED — 500 SERVER_ERROR — 503 SERVICE_UNAVAILABLE. لا stack trace في 500/503 إطلاقًا.

## 2) Endpoints — تفصيل كل واحد

### POST /api/v1/message — إرسال رسالة (F1+F3)
- **Auth:** Header `X-API-Key` — 401 إن غاب/خطأ — رسالة "مفتاح API غير صحيح"
- **Body:** `{sender?, recipient, content(1-4096), evidence?}` — sender يؤخذ من API key context إن لم يرسل
- **Logic:** `validate_cross_room(sender, recipient)` أول سطر — إن cross-room وsender هو agent → 403 + violation في audit_logs + `{"success":false,"message":"ممنوع التواصل المباشر بين الغرف — أرسل عبر قائد غرفتك"}` — لا صف في messages
- **Success:** حفظ في messages.db + سطر audit_logs `message_sent` + إن recipient متصل WS → دفع فوري ≤50ms → 200 `{success:true, data:{id, status:"delivered"}}` — إلا فـ pending
- **Errors:** 422 محتوى فارغ/طويل — 429 تجاوز 100/دقيقة — 403 عزل
- **Example curl:** `curl -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" -d '{"recipient":"bck-lead","content":"تم إنجاز API الدفع","evidence":"hq/engine/mcp_server/main.py:42"}' http://localhost:8765/api/v1/message`

### GET /api/v1/messages — قائمة رسائل
- **Query:** `agent?, room?, page=1, limit=20 (max100)`
- **Logic:** فلترة + ترتيب `timestamp DESC` + pagination — فهرسة على sender/timestamp
- **Example:** `curl -H "X-API-Key: $KEY" "http://localhost:8765/api/v1/messages?agent=bck-api-engineer&page=1&limit=20"`

### POST /api/v1/tickets — إنشاء تذكرة (F2)
- **Body:** `{subject(1-256), description(1-4096), priority(low/medium/high/critical), type(task_assignment/consultation_request/escalation/gate_check), assignee, requester?}`
- **Logic:** إنشاء status=open + `created_at/updated_at` ISO8601 + إشعار WS لـ assignee ≤50ms — إن priority=critical → كتابة فورية في amygdala عبر memory.py + سطر audit
- **Success:** 201 `{ticket_id, status:"open"}`
- **Errors:** 422 priority/type غير معروف
- **Example:** `curl -X POST -H "X-API-Key: $KEY" -d '{"subject":"مراجعة معمارية","description":"هل نستخدم SQLite؟","priority":"high","type":"consultation_request","assignee":"arc-lead"}' http://localhost:8765/api/v1/tickets`

### PATCH /api/v1/tickets/{id} — تحديث حالة
- **Allowed transitions:** `open→in_progress→resolved→closed` فقط — أي قفزة →400 `"انتقال حالة غير مسموح — المسار الصحيح: open→in_progress→resolved→closed"`
- **Body:** `{status, assignee?}`
- **Logic:** تحديث `updated_at` + audit log + إن التصعيد → تغيير assignee إلى brd-ceo (مهمة hourly)

### GET /api/v1/tickets — قائمة تذاكر + فلترة
- **Query:** `status?, priority?, room?, page, limit` — ترتيب زمني تنازلي — pagination

### GET /api/v1/tickets/{id} — تفصيل تذكرة
- 404 إن غير موجودة — 200 مع Envelope

### POST /api/v1/memory/decision — كتابة قرار (F4)
- **Body:** `{content(1-4096), room?, evidence?}`
- **Logic:** كتابة فورية في `hq/brain/cortex-decisions.md` بصيغة `- [YYYY-MM-DD HH:MM UTC] [room/lead] القرار — evidence: file:line` + lock + audit — فصل صارم hq/brain vs projects/*/brain
- **Errors:** محاولة كتابة مشروع في hq/brain →403

### POST /api/v1/memory/session + /incident
- نفس النمط — session → hippocampus — incident → amygdala — درس → LESSONS.md

### GET /api/v1/audit — بحث تدقيق (F5)
- **Query:** `agent?, type?, page, limit max100` — مصدره audit_logs append-only
- **No UPDATE/DELETE endpoint إطلاقًا**

### GET /api/v1/audit/export — تصدير
- **Query:** `format=json|csv, from?, to?, room?` — يولد ملف JSON/CSV للتنزيل

### GET /health — صحة
- **Response:** `{"status":"ok","agents_online":12,"uptime_s":123,"version":"1.0.0"}` — لا يكشف أسرار — rate-limited

### WS /ws/agent/{agent_id} + /ws/lead/{lead_id}
- **Auth:** Query `?api_key=KEY` عند handshake — إن خطأ → close 4401
- **Protocol:** JSON `{content, recipient?, evidence?}` — للـ agent recipient افتراضي هو lead غرفته — الرد `{status:"delivered",id}` خلال 50ms — إعادة اتصال 3 مرات 1ث ثم fallback REST
- **Isolation:** نفس `validate_cross_room()` — cross-room agent→agent يُغلق ويُسجل violation
- **Example wscat:** `wscat -c "ws://localhost:8765/ws/agent/bck-api-engineer?api_key=KEY"` ثم `{"content":"تم","evidence":"hq/engine/mcp_server/main.py:10"}`
- **Python WS:** `import websockets; await websockets.connect("ws://localhost:8765/ws/agent/bck-api-engineer?api_key=KEY")`

## 3) رسائل الأخطاء — ثنائية اللغة حرفية
- 401: "مفتاح API غير صحيح" + "Invalid API key"
- 403 cross-room: "ممنوع التواصل المباشر بين الغرف — أرسل عبر قائد غرفتك (Cross-room communication blocked by Law 2)"
- 422 empty: "المحتوى فارغ — أرسل نصًا بين 1 و4096 حرف"
- 422 long: "المحتوى يتجاوز الحد المسموح (4096)"
- 422 priority: "الأولوية يجب أن تكون low/medium/high/critical"
- 429: "تجاوزت الحد المسموح — حاول بعد دقيقة (Rate limit 100/min)"
- 400 transition: "انتقال حالة غير مسموح — المسار الصحيح: open→in_progress→resolved→closed"

## 4) الأمان والحماية (F6)
- API Key من `.env SOFI_MCP_API_KEY` فقط — لا secret في الكود — `.env.example` بلا قيم
- Rate 100/دقيقة لكل agent_id عبر Dict + token bucket في الذاكرة — Header `Retry-After: 60`
- Pydantic strict — content 1-4096 — UUID v4 لـ request_id في meta — كل مدخل منظف قبل حفظ SQLite (يمنع حقن)
- WAL + fsync بعد كتابة + triggers تمنع UPDATE/DELETE

## 5) الأداء
- كل endpoint async/await — فهارس sender/recipient/timestamp — لا استعلام >50ms — P95 ≤100ms

*Evidence: openapi.yaml — schema.sql — api-envelope.md:6 — registry.yaml:15 غرفة*
