# Innovation Lab — مختبر الابتكار

> **⚡ Created 2026-09-05 — deferred Audit-ALL — owner directive "نفّذ المؤجل" — ADR-20260905-AUDIT-ALL-Phase2**
> **Room:** 16-innovation
> **Code:** inn
> **Room lead:** `inn-lab-lead`

---

## | Identity

**Purpose:**
تجربة تقنيات جديدة بلا تأثير على الإنتاج — الحل لفجوة "عدم وجود غرفة الابتكار" (audit P2). مرتبطة بـ 02-research و 04-architecture — تجاربها بموافقة `brd-cto` فقط.

**Tier:** T1 Paper (innovation track — موازٍ لـ T1)
**Stage:** S1/S2 تجريبي — لا يلمس S4/S5 إلا بعد ADR مصيري

**Agent count:** 2

---

## | Agent Roster

- `inn-lab-lead` — lab-lead (قائد المختبر — يملك التجارب)
- `inn-tech-scout` — tech-scout (كشاف تقني — يرصد التقنيات الناشئة)

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. **Scout:** `inn-tech-scout` يرصد تقنية ناشئة (AI/Vector-DB/Streaming/AR-VR) — تقرير `hq/brain/knowledge/innovations/<tech>.md`
2. **Proposal:** `inn-lab-lead` يكتب ADR تجريبي — يعرضه على `brd-cto` + `brd-cso` (veto)
3. **Experiment:** تجربة معزولة في `hq/engine/sandbox/` أو `projects/innovation-lab/` — لا تمس `SOFI` الرئيسي
4. **Evaluation:** `qa-perf-analyst` + `sec-threat-model` يقيمان — إما أرشفة أو ترقية لـ ADR مصيري

---

## | Connected Rooms

- **Talks to:** 02-research (رصد) · 04-architecture (تقييم) · 09-security (veto) · 13-knowledge (توثيق)
- **Requires:** brd-cto approval per experiment
- **Provides:** innovation ADRs + PoCs

---

## | Gate Ownership

**No gate ownership** — تجاربها لا تفتح بوابة — الترقية للإنتاج تحتاج ADR مصيري جديد.

---

## | Handoff Protocol

1. `inn-tech-scout` يكتشف → `inn-lab-lead` يكتب ADR تجريبي
2. `brd-cto` يوافق/يرفض (مع `brd-cso` veto)
3. التجربة معزولة — لا تسليم مباشر للإنتاج
4. النتيجة تُسجل في `hq/brain/cortex-decisions.md` (تجربة) أو تُرقى لمصيري

---

## | Skills

- **Room playbook:** `inn-experiment` (مخطط — يُنشأ Phase 3)
- **Shared:** `sofi-evidence` + `sofi-handoff`
- **Full map:** `.opencode/skills/INDEX.md`

---

## | Room Law

T1 innovation — لا تأثير على الإنتاج بلا موافقة `brd-cto` — Law 10 (main tree) + Law 15 (license) — كل تجربة مجانية (INT-0003).
