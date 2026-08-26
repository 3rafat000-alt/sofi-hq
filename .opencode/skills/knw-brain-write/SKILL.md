---
name: knw-brain-write
description: >-
  When knowledge must be recorded into SOFI's six-area brain enforcing Law 7. Triggers — "write to
  brain", "record decision", "log an ADR", "where do I record this", "add lesson", "log incident",
  "update CORTEX", "document session", "approve routine", "memory binding". Invoked for every decision/session/emergency/routing/planning/routine
  that must be immortalized — not for reading (that's knw-brain-query) nor project documents (knw-doc-writer).
---

# knw-brain-write — The Brain Writing Playbook ⬛

> Law 7 made executable: directs every knowledge type to its correct brain area among the six, with the authorized writer, moment, and correct template — no documentation = L1, repetition = L2.

## 🎯 When to invoke (When) ⬛
- A fateful/architectural decision must be immortalized (ADR) → CORTEX.
- Closing a session → HIPPOCAMPUS.
- Emergency/incident (occurrence, update, or closure) → AMYGDALA.
- Changing a routing rule or gate → THALAMUS.
- Opening/closing a work order or strategic review → PREFRONTAL.
- Approving/modifying an approved routine → BASAL-GANGLIA.
- WO closure or alert and lesson maturation → org/LESSONS.

**Do not invoke** for: reading/querying the brain (that's `knw-brain-query`), or drafting a project document (that's `knw-doc-writer`).

## 📥 Required inputs (Inputs) ⬛
- RCCF work order (Law 5) — no brain writing without it.
- Knowledge type + its ready content (the decision/lesson/incident/routine text).
- CEO approval of the write — every brain write is hierarchical through the CEO (Law 3).

## 🔧 Steps (Steps) ⬛
1. Classify the knowledge into its type (decision/session/emergency/routing/planning/routine/lesson).
2. Identify the area, authorized writer, and moment from the write matrix (table below).
3. Verify you are the authorized writer; if not, escalate to the authorized writer via the CEO — never write on their behalf.
4. Apply the correct template from `hq/brain/brain_templates/` (DECISIONS/LESSONS/HANDOFFS/CONTEXT).
5. Write the entry with a unique identifier (ADR-NNN / LES-NNN·sig) + date + WO reference.
6. Review quality before delivery (Law 8), and record `file:line` for the new entry.
7. Produce the evidence block (see below).

## 🧭 Write Matrix ⬛
| Type | Area (file) | Authorized writer | Moment |
|-------|-----------------|----------------|--------|
| Decision/ADR | `hq/brain/cortex-decisions.md` | brd-ceo (documentation delegated to knw-lead) | every fateful decision, before closing the ticket |
| Session | `hq/brain/hippocampus-sessions.md` | brd-ceo | closing each session (cap 10, oldest archived) |
| Emergency | `hq/brain/amygdala-incidents.md` | the reporting lead via the CEO | emergency occurrence/update/closure |
| Routing | `hq/brain/thalamus-routing.md` | gtw-dispatcher via the CEO | changing a routing rule/gate |
| Planning | `hq/brain/prefrontal-frameworks.md` | str-lead via the CEO | WO open/close + periodic review |
| Routine | `hq/brain/basal-ganglia-routines.md` | knw-lead with CEO approval | approving/modifying a routine |
| Lesson | `brain/hq/brain/org_lessons/LESSONS.md` | knw-reflector | every WO closure and every alert |

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: one complete brain entry with its identifier in its correct area.
- **Evidence (Law 4):** use the `sofi-evidence` skill (Knowledge/Docs type):
  - `file:line` for every new brain entry (area + line number) — proof of writing.
  - Entry identifier (ADR-NNN / LES-NNN·sig) + date + WO reference.
  - Before/after of the modified file, and the template name used from `templates/`.
  - Confirmation by the reviewer authorized in the write matrix (knw-lead / sec-lead / brd-ceo).

## 🔗 Handoff ⬛
- Deliver entry + evidence block to **knw-lead** only (Law 3) via the `sofi-handoff` skill.
- knw-lead reviews then escalates to brd-ceo for write approval. No direct delivery to the user.
- No addressing another room directly (Law 2) — any coordination through leads.

## ⛔ Constraints ⬛
- Never write in an area whose authorized writer you are not — escalate to the writer via the CEO.
- Never delete from CORTEX (permanent); HIPPOCAMPUS is cumulative with cap 10, oldest moved to archive.
- No writing without identifier/date/WO reference. No writing into `hq/archive/` (history only).
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- This skill *is* Law 7's mechanism — every invocation produces documentation in its correct area.
- The decision adopting this skill itself is recorded in `hq/brain/cortex-decisions.md` as an ADR (by brd-ceo's hand).

## 📚 References ⬜
- `hq/brain/brain-index.md` — the index + full write matrix and six-area rules.
- `hq/brain/brain_templates/` — DECISIONS / LESSONS / HANDOFFS / CONTEXT.
- `hq/brain/owners-matrix.yaml` — owner of every live brain file (Law 9).
