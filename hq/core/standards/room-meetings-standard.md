## FILE: hq/core/standards/room-meetings-standard.md
# معيار اجتماع الغرف ودورة استشارة المجلس (Owneer-Directive 2026-08-29)

> **أمر المالك:** تواصل مجلس الإدارة والتشاور بعد رفع البوابة وتسليم العمل · عقد اجتماعات الغرف كمنظمة صحيحة كاملة · التحقق من عدم التكرار · المجلد في المحرك (hq/engine). هذا المعيار يكمّل القوانين ولا يلغيها.

## 1. دورة استشارة المجلس بعد تسليم البوابة (Law 6 — مكتملة)

كل تسليم عمل من البوابة (intake/route) يمر بهذه الدورة قبل التوزيع:

```
gtw-dispatcher ──(Intake Report + Gate + Budget + Lane)──▶ brd-ceo
   brd-ceo ──sofi_consult(consultee=brd-*)──▶ Board advisor (brd-cpo/brd-cto/brd-cqo/brd-cso/brd-arbiter/brd-chief-of-staff)
   Advisor ──(APPROVE/REJECT/CONDITIONS)──▶ brd-ceo
   brd-ceo ──(القرار النهائي + توزيع RCCF)──▶ room lead(s)
```

- **متى تُستشار المجموعة:** أي قرار مصيري (مال/أمان/بنية/إنتاج/مخطط/غير قابل للإرجاع) أو قرار يتجاوز غرفة واحدة — استشارة إلزامية.
- **الأداة:** `sofi_consult` (تفتح تذكرة `consultation_request` في الحافلة + سجل تدقيق `consult_opened`).
- **أعضاء المجلس:** brd-cpo · brd-cto · brd-cqo · brd-cso (فيتو مطلق) · brd-arbiter · brd-chief-of-staff.
- **قائد مجلس الإدارة هو brd-ceo** (السجل الرسمي 00-boardroom بلا مفتاح lead — AGENTS.md الجدول: brd-ceo).
- **النتيجة:** قرار حاسم من brd-ceo → توزيع على قادة الغرف عبر RCCF (Law 3/5) → تسليم للمالك (Law 11) مع الأدلة (Law 4).

## 2. اجتماعات الغرف (اجتماع الغرف) — الإيقاع والمسؤوليات

| عنصر | القاعدة |
|---|---|
| الاجتماع الدوري | **اجتماع أسبوعي لمجلس الإدارة** (boardroom) يجمع brd-ceo + رؤساء الغرف (leads) — + اجتماعات داخل الغرف حسب الحاجة |
| من يعقد | brd-ceo أو قائد غرفة (organizer) |
| الدعوة | `sofi_meeting_new` — العنوان + أجندة واضحة + الحضور (attendees) |
| الأجندة القياسية | 1) حالة العمل الجاري 2) العوائق والكتل (str-agile-orchestrator يرفعها يومياً) 3) القرارات المطلوبة 4) المخاطر |
| الحد الأدنى | اجتماع دون أجندة = اجتماع ملغى قبل عقده (L1 للداعي) |
| المحضر | `sofi_meeting_minutes` — قرارات + إجراءات + أدلة — **القرارات تُكتب إلى CORTEX (Law 7)** عبر الحافلة |
| الإلزام | القرارات المعتمدة في المحضر ملزمة (تنفيذ عبر RCCF) — عدم تنفيذ إجراء معتمد = L2 |
| الأدلة | كل اجتماع يُسجل: الوقت، الحضور، القرارات، الإجراءات، مرجع CORTEX |

## 3. القنوات التقنية (الحافلة — hq/engine/mcp_server)

| الأداة/المسار | الوظيفة |
|---|---|
| `sofi_consult` / `POST /api/v1/consult` | فتح استشارة مع عضو مجلس أو قائد — تذكرة `consultation_request` |
| `sofi_meeting_new` / `POST /api/v1/meetings` | جدولة اجتماع غرفة (meetings.db — status scheduled) |
| `sofi_meetings` / `GET /api/v1/meetings` | عرض الاجتماعات (حسب status/room) |
| `sofi_meeting_minutes` / `POST /api/v1/meetings/{id}/minutes` | إغلاق الاجتماع بالمحضر → القرارات إلى CORTEX |

الجميع ضمن مغلف الاستجابة الموحد `{success, data, message}` (api-envelope.md) ومحميون بمفتاح API.

## 4. عدم التكرار

- السجل الرسمي الوحيد للغرف والوكلاء: `hq/core/nexus/registry.yaml` (Law 12) — أي وكيل جديد يُضاف إليه أولاً ثم تُحدّث الملفات.
- كل وكيل له معرّف واحد فريد في غرفة واحدة (لا ازدواج أدوار عبر الغرف) — أي تكرار يُرفع إلى brd-ceo.
- المرجع الهيكلي: `hq/core/structure-standard.md` (خريطة old←new دائمة — Law 13).

*Evidence: hq/engine/mcp_server/main.py:post_consult — meetings.py:create_meeting/close_meeting_with_minutes — leads_mcp.py:create_consultation — registry.yaml:00-boardroom — AGENTS.md:Law6/Law12 — هذا المعيار مكمل للقوانين، لا يلغيها — **محدّث 2026-09-01: جسر mcp_bridge محذوف**.*