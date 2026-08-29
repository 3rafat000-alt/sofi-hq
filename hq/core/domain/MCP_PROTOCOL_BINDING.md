## FILE: hq/core/domain/MCP_PROTOCOL_BINDING.md
# Binding — MCP Protocol to Rooms & Agents
> Date: 2026-08-29 — يربط المعيار بالتنفيذ — لا يلغي أي قانون

## ما تغيّر
- كل تواصل بين الغرف أصبح **حصرًا** عبر `mcp.local:8765` (Ticket Bus + Memory + Audit) — بديلاً عن Task اليدوي — احترافي مرن (WS للفورية، REST للطوارئ)
- المعيار: `hq/core/standards/mcp-communication-standard.md` — الدليل: `hq/engine/mcp_server/AGENT_GUIDE.md` — SDK: `hq/engine/mcp_server/client/mcp_client.py` + `mcp_client.js`
- الملحق الجديد `hq/core/templates/mcp-agent-annex.md` يُلحق **append-only** بنهاية كل ملف وكيل في `.opencode/agent/` بعد `Governing Doctrine` — لا حذف، لا إعادة كتابة (agent-prompt-template.md §2)

## خريطة الغرف — كيف تستخدم الحافلة

| # | الغرفة | Lead | يستخدم MCP لـ |
|---|---|---|---|
| 00 | Boardroom | brd-ceo | استقبال escalation بعد 24h + قرارات — `GET /api/v1/tickets?assignee=brd-ceo` |
| 01 | Strategy | str-lead | استشارة 02 عبر tickets — كتابة PRD قرار في cortex |
| 02 | Research | res-lead | تسليم dossier لـ 01/03 عبر message لقائده ثم ticket |
| 03 | Design | dsn-lead | استشارة 04/08 + DFR gate_check tickets لـ 09/10 |
| 04 | Architecture | arc-lead | تسليم openapi/schema لـ 05/08 عبر tickets |
| 05 | Backend | bck-lead | توزيع tasks لوكلائه + استقبال منهم عبر WS |
| 06 | Frontend | fnt-lead | انتظار Gate S4 ثم استلام design tokens عبر tickets |
| 07 | Mobile | mob-lead | نفس 06 — فريق موحد |
| 08 | Data | dat-lead | تسليم ERD لـ 04/05 |
| 09 | Security | sec-lead | DFR signature + audit search `type=violation` |
| 10 | Quality | qa-lead | Gate 5 + export audit CSV |
| 11 | DevOps | ops-lead | مراقبة server.log + restart service |
| 12 | Observability | obs-lead | كتابة incidents → amygdala |
| 13 | Knowledge | knw-lead | كتابة lessons → org_lessons |
| 14 | Gateway | gtw-dispatcher | تصنيف Gate0 + routing عبر tickets |

## كيف لا يضيع الوكيل — 3 قواعد في الكود
1. SDK `send_guarded` يرفض إن كان `task_id/context/evidence` فارغ
2. `validate_cross_room` أول سطر — يمنع القانون قبل الحفظ
3. كل إرسال يكتب في `audit_logs` + `messages.db` — قابل للبحث والتصدير

## الانتقال — لا Task بعد اليوم
- Task القديم يبقى في opencode للتوزيع الهرمي العام، لكن **التواصل بين الغرف** أصبح عبر MCP فقط — أي `agent→agent` مباشر = L3
- كل وكيل جديد يُنشأ بهذا الملحق تلقائياً — الوكلاء الحاليون يُحدَّثون append-only بالملحق

*Evidence: hq/engine/mcp_server/main.py:1 — client/mcp_client.py:1 — mcp.caddy:1 — sofi-mcp.service — AGENT_GUIDE.md*
