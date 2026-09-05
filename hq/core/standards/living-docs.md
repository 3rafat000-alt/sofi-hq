# Living Documentation Standard — معيار التوثيق الحي

> **الغرض:** منع الوثائق القديمة — كل وثيقة حية تُحدث مع كل تغيير مصيري/قياسي (max تأخير التزام واحد). الحل لفجوة "عدم وجود معيار موحد للتوثيق الحي" (audit 2026-09-05) + Protocol 20 P-20.1
> **المالك:** `knw-lead` (13-knowledge) — يدقق شهرياً عبر `memory_summarizer.py` + `evidence_guard`
> **القانون:** Law 7 (Memory Binding) + Law 4 (Evidence) — وثيقة قديمة = L1

---

## القاعدة

كل غرفة تُحدث وثائقها المملوكة مع كل تغيير **Fateful أو Standard** يمسها — في نفس الالتزام أو التالي مباشرة (max تأخير = التزام واحد). الوثيقة القديمة = L1 للـ lead المسؤول.

## ما يُعتبر "وثيقة حية"

| الوثيقة | المالك | متى تُحدث |
|---------|--------|-----------|
| `hq/core/nexus/registry.yaml` + `personas.yaml` + `routing.yaml` | `knw-lead` + `gtw-dispatcher` | مع كل وكيل/غرفة جديدة |
| `hq/core/nexus/gates.yaml` + `gate_checklists/*` | `arc-lead` + `qa-lead` | مع كل بوابة جديدة/معدلة |
| `hq/core/standards/*.md` | مالك المعيار | مع كل معيار جديد/معدل |
| `hq/core/domain/rooms/<room>/charter.md` | room lead | مع كل تغيير دور/عدد وكلاء |
| `hq/core/domain/context-map.yaml` | `arc-lead` | مع كل عقد جديد بين الغرف |
| `hq/core/system-state-current.md` | `knw-lead` + `brd-ceo` | مع كل موجة تبسيط/أرشفة |
| `.opencode/skills/INDEX.md` | `knw-lead` | مع كل مهارة جديدة |
| `AGENTS.md` §Final State | `brd-ceo` | مع كل تغيير أعداد ملزمة |
| `hq/brain/cortex-decisions.md` | `knw-lead` (بتفويض CEO) | مع كل قرار مصيري |
| `projects/<slug>/brain/CONTEXT.md` | `str-lead` | مع كل PRD جديد |

## آلية التحقق

- **شهرياً:** `knw-lead` يشغل `python3 hq/core/tooling/evidence_guard.py hq/core --strict` + فحص `git log --since="1 month ago" -- hq/core/standards/*.md` — أي معيار لم يُحدث رغم تغيير يمسه = تقرير L1.
- **عند كل التزام:** `pre-commit` يفحص `evidence_guard` — أي `file:line` قديم مكسور = رفض.
- **القالب:** `hq/core/templates/` — كل وثيقة جديدة تُنشأ من قالب، لا من الصفر.

## الاستثناء

التغييرات **Fast** (قراءات/ملف واحد قابل للعكس) لا تتطلب تحديث وثيقة — فقط سجل HIPPOCAMPUS.

---

## المراجع

- `AGENTS.md:42` Law 7 · `hq/core/protocols.md` P-20.1 · `hq/brain/hippocampus-sessions.md` (سجل التحديثات)
