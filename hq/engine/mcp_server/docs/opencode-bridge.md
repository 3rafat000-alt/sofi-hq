## FILE: hq/engine/mcp_server/docs/opencode-bridge.md
# جسر opencode ↔ الحافلة (SOFI MCP) — دليل واختبار حي

> Author: gtw-intake-reformer · 2026-08-29 · type Gateway/Infrastructure
> Authority: مكدّس `hq/core/standards/mcp-communication-standard.md` v1.2 + `hq/core/standards/room-meetings-standard.md` + `structure-standard.md` v4.7

## ما هذا؟
جسر MCP (stdio) يفتح حافلة SOFI (`127.0.0.1:8765`) داخل opencode نفسه — أي وكيل من الوكلاء الـ 114 يرى الخادم `SOFI` ويستدعي أدواته مباشرة بدل (أو بالإضافة إلى) SDK البايثون.

**الملف:** `hq/engine/mcp_server/mcp_bridge/server.py` — مسجل في `opencode.json` (`mcp.SOFI`) — داخل المحرك (owner directive: "المجلد في المحرك engine")

## الأدوات (13)

| الأداة | الوظيفة |
|---|---|
| `sofi_org_structure` | الغرف الـ 15 وقادتها ووكلاؤها — مصدر الحقيقة `hq/core/nexus/registry.yaml` (Law 12) |
| `sofi_who_is(agent_id)` | غرفة الوكيل + قائده + زملاؤه + هل هو قائد — **قائد مجلس الإدارة = brd-ceo** (إصلاح brd-lead) |
| `sofi_health` | حالة الحافلة |
| `sofi_send` | إرسال رسالة منضبطة — يرفض بدون task_id/context/evidence (لا عمل أعمى) |
| `sofi_ticket` | إنشاء تذكرة من الأنواع الخمسة |
| `sofi_clarify` | نقص/غموض → أسئلة حادة 1-3 (clarification_request) — لا تخمين (Law 16) |
| `sofi_escalate` | تصعيد فوري إلى brd-ceo |
| `sofi_tickets` | عرض التذاكر بحالة اختيارية |
| `sofi_audit` | قراءة سجل التدقيق غير القابل للتعديل |
| `sofi_consult` | استشارة المجلس بعد تسليم البوابة (Law 6) — تذكرة `consultation_request` |
| `sofi_meeting_new` | جدولة اجتماع غرفة (meetings.db — scheduled) |
| `sofi_meetings` | عرض الاجتماعات (status/room) |
| `sofi_meeting_minutes` | إغلاق الاجتماع بالمحضر → القرارات إلى CORTEX (Law 7) |

## اختبار حي (2026-08-29 06:02 +03 — بعد النقل إلى المحرك)

```
① MCP initialize OK — server: sofi v1.27.2
② tools/list — 13/13 ظاهرة
③ sofi_who_is('brd-ceo') — is_lead True · room 00-boardroom · lead brd-ceo (إصلاح)
④ sofi_consult — consultation_request open → brd-cso (HTTP 201)
⑤ sofi_meeting_new → meeting_id 2 · scheduled
⑥ sofi_meeting_minutes → closed · decisions 2 → كتبت في hq/brain/cortex-decisions.md
⑦ sofi_meetings(status=closed) → 2
```

أدلة الحافلة: `GET /api/v1/audit` — `consult_opened` ، `meeting_created` ، `meeting_minutes` مسجلة.

## النقل إلى المحرك (خريطة old←new — structure-standard v4.7/v4.8)
- `mcp-server/` (جذر المشروع، باسم الواصلة) → **`hq/engine/mcp_server/`** (داخل المحرك — بلا واصلة)
- **v4.8: حُذف الـ symlink نهائياً (لا تكرار)** — المجلد الوحيد `hq/engine/mcp_server` وهو حزمة بايثون حقيقية يستوردها النظام مباشرة
- systemd أُعيد توليده من `hq/engine/mcp_server/install-service.sh` — الخدمة سليمة بعد إعادة التشغيل
- `opencode.json` — أمر SOFI → `hq/engine/mcp_server/mcp_bridge/server.py`
- السجلات التاريخية في `hq/brain/*` لم تُحرر (Law 13) — المرجع الدائم في `structure-standard.md` v4.6/v4.7/v4.8

## الحالة
- ✅ موضع المحرك وخدمة: صحية (health OK بعد restart + 13 أداة عبر stdio)
- ✅ تسجيل opencode: `opencode.json` JSON صالح — SOFI فعّال
- ✅ ملفات الوكلاء: 114/114 بكتلة `<!-- SOFI-BUS-MCP-v2 -->`
- ✅ الحوكمة: استشارة المجلس (Law 6) + اجتماع الغرف حيّان عبر الحافلة — معيار `hq/core/standards/room-meetings-standard.md`
- ✅ عدم التكرار: تدقيق registry↔ملفات = 114/114 بلا فواصل ولا أيتام
- ✅ الاختبارات: governance 4 + integration 14 = 18/18 معاً (المجلد الجديد) — كامل المجموعة 31 نجح + 3 تقلبية بيئية معروفة (تنفرد بالنجاح منفردة)
- ✅ الذاكرة: قرارات في `hq/brain/cortex-decisions.md` (03:02-03:03 UTC) + جلسة في `hippocampus-sessions.md`