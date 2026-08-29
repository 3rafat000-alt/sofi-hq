## FILE: hq/core/templates/mcp-agent-annex.md
# Annex — MCP Communication Protocol for Agents & Leads (append-only after last line of every agent file)
> **Authority:** hq/core/standards/mcp-communication-standard.md v1.2 — 2026-08-29 — يكمّل القوانين 2/3/4/6/7 — لا يلغيها

```
## ⬛ MCP Communication Protocol — احترافي مرن (لا عمل أعمى)

1. قناتك الوحيدة: `mcp.local:8765` (أو `sofi.local`/`hq.local` أو `127.0.0.1:8765`) — كلها لنفس الحافلة — لا تستخدم Task اليدوي — SDK في `hq/engine/mcp_server/client/mcp_client.py` (Python) و `client/mcp_client.js` (JS) — يختار WS→REST تلقائياً — **داخل opencode استخدم أدوات MCP الجاهزة `sofi_*`** (`mcp__sofi__sofi_send` / `sofi_who_is` / `sofi_clarify` / `sofi_escalate` — يراها أي وكيل على أنه `SOFI` server)

2. قبل أي إرسال: جهّز `task_id` + `context` (سطر في openapi.yaml/CONTEXT.md) + `evidence: file:line` — `send_guarded` يرفض بدونها — هذا يمنع العمل الأعمى

3. أنت وكيل → ترسل لقائد غرفتك فقط — أنت قائد → تستشير قائداً آخر عبر `POST /api/v1/tickets` (Ticket Bus) — أي `agent→agent` بين غرف مختلفة = 403 + violation مسجل — `hq/engine/mcp_server/ticket_bus.py:validate_cross_room`

3b. **الحوكمة (Law 6 + اجتماع الغرف):** قائد/brd-ceo يستشير عضو المجلس أو قائداً آخر عبر `sofi_consult` (المجلس: brd-cpo/brd-cto/brd-cqo/brd-cso/brd-arbiter/brd-chief-of-staff — قائد المجلس brd-ceo) — اجتماعات الغرف عبر `sofi_meeting_new`/`sofi_meetings`/`sofi_meeting_minutes` (القرارات → CORTEX) — الدليل: `hq/core/standards/room-meetings-standard.md`

4. أنواع التذاكر 5: `task_assignment` / `consultation_request` / `escalation` / `gate_check` / `clarification_request` — حالة التذكرة `open→in_progress→resolved→closed` فقط — أي قفزة = 400

5. المرونة: WS مقطوع → 3 محاولات 1ث → REST تلقائياً — Rate 100/دقيقة → انتظر `Retry-After:60` — Header `X-API-Key` من `.env` — غيابه → 401

6. كل خطوة في `audit_logs` غير قابل للتعديل (trigger يمنع UPDATE/DELETE) — ابحث `GET /api/v1/audit?agent=...` وصدّر `GET /api/v1/audit/export?format=csv` — إن لم تُسجل، لم تحدث

7. الذاكرة: قرار → `POST /api/v1/memory/decision` → `hq/brain/cortex-decisions.md` بصيغة `- [YYYY-MM-DD HH:MM UTC] [room/lead] النص — evidence: file:line` — فصل صارم `hq/brain` ≠ `projects/*/brain` (Law 7)

8. **فكّر تسلسلياً قبل أي فعل (إلزامي):** فهم→سياق→فحص→خطة→تحقق — عائق في الفحص/الفهم → `sofi_clarify` (1-3 أسئلة حادة، تذكرة clarification_request) → لم يجب القائد خلال 30 دقيقة أو مشكلة حرجة → `sofi_escalate` فوراً إلى brd-ceo — **لا تخمين** (Law 16 · المعيار §15-§16)

9. الدليل العملي: `hq/engine/mcp_server/AGENT_GUIDE.md` (5 دقائق) + `hq/core/standards/mcp-communication-standard.md` (المعيار الكامل) + `hq/engine/mcp_server/mcp_bridge/server.py` (أدوات opencode) + `client/README.md` (أمثلة) — اقرأها قبل أي إرسال
```
*Append-only — لا تحذف أسطراً سابقة — Violation = L2*
