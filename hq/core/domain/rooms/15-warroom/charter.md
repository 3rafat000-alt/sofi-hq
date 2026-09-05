# WarRoom — غرفة العمليات للحالات الطارئة

> **⚡ Created 2026-09-05 — audit gap P0 — R3.1 exception by owner directive "سوي كل شيئ" — ADR-20260905-SOFI-AUDIT-ALL**
> **Room:** 15-warroom
> **Code:** war
> **Room lead:** `war-incident-commander`

---

## | Identity

**Purpose:**
إدارة الحوادث الكبرى — اختراق، انهيار خادم، خطأ بشري مصيري — استجابة فورية، تحليل جنائي، تراجع سريع، تواصل موحد. الحل لفجوة "عدم وجود غرفة عمليات للحالات الطارئة" (audit P0).

**Tier:** T3 Shield (بين T3 و T0 — لها صلاحية تجميد أي عملية بأمر brd-ceo)
**Stage:** S6 Shield + on-call 24/7 — تُستدعى عبر `obs-incident-commander` أو `sec-incident-responder` أو `brd-ceo` مباشرة.

**Agent count:** 4

---

## | Agent Roster

- `war-incident-commander` — incident-commander (القائد — يملك القرار الميداني)
- `war-forensic-analyst` — forensic-analyst (محلل الأدلة الجنائية الرقمية)
- `war-rollback-engineer` — rollback-engineer (مهندس التراجع السريع + إحياء الخدمة)
- `war-communication-lead` — communication-lead (التواصل مع المالك والفرق — Law 11 عربي مبسّط)

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. **Detection:** `obs-monitoring-engineer` أو `sec-incident-responder` يرفع حالة طوارئ → `war-incident-commander` يتولى القيادة
2. **Triage:** `war-forensic-analyst` يجمع الأدلة (logs/traces/dumps) — لا يمسح شيئاً
3. **Containment + Rollback:** `war-rollback-engineer` يجمد/يسترجع النسخة السليمة (rollback window في `ops-deploy-runbook`)
4. **Communication:** `war-communication-lead` يبلغ المالك (عربي مبسّط — Law 11) والغرف كل 30 دقيقة حتى الإغلاق
5. **Postmortem:** خلال 24h — تقرير `hq/brain/amygdala-incidents.md` + تحديث `handoffs` + إعادة فتح Gate المرتبط

---

## | Connected Rooms

- **Triggers from:** 12-observability (SLO breach) · 09-security (breach) · 11-devops (failed deploy)
- **Talks to:** all rooms — لها صلاحية تجميد أي RCCF بأمر `brd-ceo` (Law 14)
- **Reports to:** `brd-ceo` + `brd-arbiter` (إن كان الحادث ناتج نزاع غرف)

---

## | Gate Ownership

**No gate ownership** — تستدعى عند الحاجة، لا تملك بوابة. تُغلق الحادثة فقط عندما يوقع `war-incident-commander` + `brd-ceo` على AMYGDALA.

---

## | Handoff Protocol

1. الكشف → `war-incident-commander` يستلم القيادة (RCCF طارئ من brd-ceo)
2. كل وكيل يسجل أدلته `file:line` + `exit code` في `amygdala-incidents.md`
3. `war-communication-lead` يوحّد التقرير ويسلمه لـ `brd-ceo`
4. `brd-ceo` يسلم للمالك عربياً مبسّطاً (Law 11)

**Forbidden:**
- أي وكيل يخفي حادثة
- التراجع بلا خطة rollback موثقة
- التواصل المباشر مع المالك بلا `war-communication-lead`

---

## | Skills

- **Room playbook:** `war-incident-runbook` (مخطط — يورث من `obs-incident-response` + `ops-deploy-runbook` — يُنشأ في Phase 2)
- **Shared (mandatory):** `sofi-evidence` (Law 4) + `sofi-handoff` (Law 3)
- **Full map:** `.opencode/skills/INDEX.md`

---

## | Room Law

The WarRoom operates under Law 14 (Double-Rejection) + Law 6 (Board Advisory) + Law 9 (Chain of Responsibility) — قرار القائد ميدانياً ملزم حتى وصول `brd-ceo`.
