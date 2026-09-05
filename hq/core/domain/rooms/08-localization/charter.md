# Localization Room — غرفة الترجمة والتعريب

> **⚡ Created 2026-09-05 — deferred Audit-ALL — owner directive "نفّذ المؤجل" — ADR-20260905-AUDIT-ALL-Phase2**
> **Room:** 08-localization
> **Code:** loc
> **Room lead:** `loc-translation-manager`

---

## | Identity

**Purpose:**
الترجمة والتكيف الثقافي — تجربة مستخدم عربية مكتملة — الحل لفجوة "غياب غرفة الترجمة والتعريب" (audit P1). تُعيد تعريف الكود 08 بعد دمجه في 04 (R3.1) — التاريخ محفوظ في `hq/core/archive/r3.1-reconciliation/` per Law 13.

**Tier:** T1 Paper (مع 01/02/03/04) — تعمل قبل التصميم وبعده
**Stage:** S1 (بحث سوق عربي) + S3 (تدقيق RTL/ثقافي قبل DFR)

**Agent count:** 4

---

## | Agent Roster

- `loc-translation-manager` — translation-manager (مدير الترجمة — يملك القاموس الموحد)
- `loc-cultural-adapter` — cultural-adapter (مكيف ثقافي — يكيّف الأمثلة والصور)
- `loc-rtl-specialist` — rtl-specialist (خبير RTL — يطبق `rtl-mirror-validator`)
- `loc-voice-tone-expert` — voice-tone-expert (خبير نبرة الصوت — يوحد لهجة SOFI)

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. **Research:** `res-ux-researcher` + `loc-cultural-adapter` يحددان الجمهور العربي (لهجة/ثقافة/اتجاه)
2. **Translation:** `loc-translation-manager` يترجم كل واجهة عبر قاموس موحد `hq/core/standards/glossary-ar.md`
3. **RTL:** `loc-rtl-specialist` يطبق `rtl-mirror-validator` + يوقع DFR مع `dsn-arabic-ux-specialist`
4. **Voice:** `loc-voice-tone-expert` يوحد النبرة (Law 11 — عربي مبسّط)
5. **QA:** `qa-design-auditor` + `loc-rtl-specialist` يفحصان 3 أحجام شاشات RTL

---

## | Connected Rooms

- **Talks to:** 02-research (جمهور) · 03-design (RTL) · 06-frontend/07-mobile (تطبيق RTL) · 10-quality (تدقيق)
- **Requires:** research findings + design tokens
- **Provides:** localized strings + RTL specs + voice guide

---

## | Gate Ownership

**Co-signs DFR** مع 03+09+10 — لا تصميم عربي يُجمد بلا توقيع `loc-rtl-specialist`.

---

## | Handoff Protocol

1. `loc-translation-manager` يستلم RCCF من `str-lead` أو `dsn-lead`
2. كل ترجمة `file:line` + `exit code` (glossary check)
3. `loc-rtl-specialist` يوقع DFR
4. التسليم `loc → dsn-lead → brd-ceo → user` (Law 3)

---

## | Skills

- **Room playbook:** `loc-rtl-adaptation` (مخطط — يورث من `rtl-mirror-validator` — يُنشأ Phase 3)
- **Shared:** `sofi-evidence` (Law 4) + `sofi-handoff` (Law 3)
- **Full map:** `.opencode/skills/INDEX.md`

---

## | Room Law

T1 Paper — لا كود قبل اكتمال الترجمة والـ RTL — Law 13 (kebab-case + `## FILE: <path>`) + Law 11 (عربي مبسّط).
