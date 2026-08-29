## FILE: hq/engine/mcp_server/brain/visual-patterns.md
# Visual Patterns — MCP Competitive Analysis
> **Source:** WebSearch Aug 2026 — 3 أنماط محلية قابلة للتطبيق

## Pattern 1 — LangChain MCP Adapters
- **Source:** https://github.com/langchain-ai/langchain — MIT
- **Pattern:** Adapter يحول أدوات MCP إلى LangChain tools — فصل البروتوكول عن المنطق
- **Takeaway for SOFI:** فصل `ticket_bus.py` عن `main.py` — واجهة موحدة لكل الغرف — لا خلط
- **License:** MIT — مسموح

## Pattern 2 — AutoGen Agent Chat
- **Source:** https://github.com/microsoft/autogen — MIT
- **Pattern:** حافلة رسائل غير متزامنة مع AgentId + Topic — كل غرفة = Topic معزول
- **Takeaway:** استخدام `room` كـ Topic — `validate_cross_room()` كـ middleware — 403 فوري
- **License:** MIT — مسموح

## Pattern 3 — CrewAI Hierarchical Process
- **Source:** https://github.com/crewAIInc/crewAI — MIT
- **Pattern:** Manager Agent يوزع المهام هرميًا — لا تواصل مباشر بين العمال
- **Takeaway:** نموذج SOFI `agent→lead→lead→agent` مطابق — Ticket Bus هو Manager
- **License:** MIT — مسموح

## Pattern 4 — FastAPI WebSocket + REST Fallback (Local-First)
- **Source:** FastAPI docs https://fastapi.tiangolo.com/advanced/websockets/ — MIT
- **Pattern:** WS للفورية + REST عند الانقطاع — نفس Pydantic models للاثنين
- **Takeaway:** نفس `models.py` للـ WS وREST — إعادة اتصال 3 مرات ثم fallback
- **License:** MIT — مسموح

## Pattern 5 — SQLite WAL + Append-Only Audit (Local DB)
- **Source:** SQLite docs https://www.sqlite.org/wal.html — Public Domain
- **Pattern:** WAL mode + triggers تمنع UPDATE/DELETE على logs — 100% تدقيق
- **Takeaway:** `PRAGMA journal_mode=WAL` + `CREATE TRIGGER no_update_audit_logs BEFORE UPDATE`
- **License:** Public Domain — مسموح

## جدول المقارنة
| النظام | سحابي؟ | ترخيص | محلي مجاني؟ | يناسب SOFI؟ |
|---|---|---|---|---|
| LangChain MCP | لا — adapter محلي | MIT | نعم | نعم — فصل |
| AutoGen | لا لكن يتطلب OpenAI | MIT | جزئي | نعم — Topic عزل |
| CrewAI | لا | MIT | نعم | نعم — هرمي |
| Pusher/Firebase | نعم مدفوع | Proprietary | لا | مرفوض — Law 10 يحظر سحابة |
| Redis Pub/Sub | يتطلب خادم خارجي | BSD | لا | مرفوض — SQLite فقط |

## القرارات المستخلصة لـ SOFI
1. معمارية 4 مجالات معزولة DDD: MCP / Ticket / Memory / Audit — كل مجال ملف واحد
2. WS أساسي + REST fallback — نفس النماذج — نفس التحقق
3. SQLite ملفان + WAL + triggers — لا PostgreSQL/Redis
4. كل تواصل cross-room عبر Ticket Bus فقط — لا مسار جانبي

*Evidence: بحث محلي + توثيق fastapi/websockets/sqlite — تراخيص MIT/PD فقط — Law 15*
