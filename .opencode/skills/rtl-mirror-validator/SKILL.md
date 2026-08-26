---
name: rtl-mirror-validator
description: >-
  Validates RTL layout correctness for Arabic (and other RTL) interfaces: mirroring logic, Arabic
  typography legibility, spacing behavior, icon/direction semantics, cultural fit. Triggers — "RTL
  check", "validate Arabic layout", "mirror validation", "RTL approved", "Arabic UX check", "قبل
  اعتماد التصميم بالعربي". Invoked by dsn-arabic-ux-specialist (room 03); signature gates DFR.
---

# rtl-mirror-validator — RTL Layout Validation

> **Binding gate:** no design passes DFR without the `RTL-Approved` signature from
> `dsn-arabic-ux-specialist` (Protocol 18, P-18.1 — complements rooms 09+10 signatures).

## 🎯 When to invoke (When)
- Any new screen/mockup before Design-Freeze Review.
- Any layout change touching direction-sensitive elements (nav, arrows, progress, tables).

## 📥 Inputs (Inputs)
| Field | Type |
|---|---|
| `design_artifact` | mockup/screenshots or implemented screen captures |
| `language` | enum: arabic (default) · hebrew · persian |
| `breakpoints` | mobile · tablet · desktop (test all three minimum) |

## 📤 Outputs (Outputs)
Validation report — one row per element:
| element | expected_direction | actual_direction | status | fix_suggestion |
|---|---|---|---|---|

Verdict: **RTL-Approved** (all PASS) or **Returned** (any FAIL, with precise fixes through `dsn-lead`).

## 🛠️ Checklist (How)
1. [ ] Navigation, back-arrows, progress indicators mirrored correctly (direction semantics, not blind flip — media/play controls stay LTR).
2. [ ] Mixed-direction content handled: Latin words/numbers inside Arabic text render correctly (bidi isolation).
3. [ ] Arabic body text ≥ 16px, line-height comfortable, diacritics not clipped.
4. [ ] Spacing does not crowd Arabic glyphs (Arabic needs slightly more vertical breathing room).
5. [ ] Icons with directional meaning flipped; culturally neutral icons unchanged.
6. [ ] Cultural fit: symbols/colors/date-number formats appropriate for the region.
7. Test at mobile/tablet/desktop in RTL mode; capture evidence screenshots per breakpoint.

## 🚫 Rules
- One FAIL returns the whole artifact — partial approval does not exist.
- Every FAIL row carries a concrete fix suggestion (file:line when implementation exists).
- Evidence attached per Law 4: screenshots + file:line references.

*Owner order 2026-08-26 · assigned room: 03-design · ledger: domain/SKILLS-ASSIGNMENT.md*
