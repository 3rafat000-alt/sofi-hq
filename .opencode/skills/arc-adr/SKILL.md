---
name: arc-adr
description: >-
  Architecture decision playbook for gates 3–4 — ADR documentation + system design + diagram + migration plan. Triggers — "architecture decision", "write an ADR", "system design", "choose the stack", "architecture diagram", "migration plan", "gate 3", "gate 4", "evaluate trade-offs", "architectural decision", "document an ADR". Invoked whenever a critical architectural decision requires weighed options and documented consequences.
---

# arc-adr — The Architecture Decision Playbook ⬛

> An architectural decision without an ADR = technical debt of unknown origin. This skill produces a decision documented with options and consequences + design + diagram + migration plan, ready for gates 3–4.

## 🎯 When to invoke (When) ⬛
- When choosing between two or more architectural alternatives (stack, pattern, service boundaries, storage).
- At gate 3 (system design) or gate 3 — the paper Architecture bundle (ERD+OpenAPI+threat-model within S2), which requires a documented ADR.
- For an architectural change touching more than one component that needs a migration and rollback plan.
- For an architectural dispute requiring an evidence-based decision before escalation.

**Do not invoke** for: direct code execution (backend/frontend rooms), cosmetic changes, or a decision inside one component with no boundary impact — those need no ADR.

## 📥 Required inputs (Inputs) ⬛
- An RCCF work order (Law 5) — no execution without it; it defines scope and the target gate (3 or 4).
- The problem/decision at hand + constraints (performance, security, cost, time).
- The current architectural state (components, boundaries, affected dependencies).
- Acceptance criteria for the target gate (from `hq/core/contracts.md`).

## 🔧 Steps (Steps) ⬛
1. **Context:** write the problem, forces at play, constraints, and acceptance criteria. No solutions yet.
2. **Options:** enumerate ≥2 realistic alternatives. For each: how it works + trade-offs (performance/security/cost/complexity/time) backed by evidence, not opinion.
3. **Decision:** pick exactly one option explicitly and state **why** this one over the others (the decisive criterion).
4. **Consequences:** positives + negatives + accepted technical debt + what becomes harder later.
5. **System design:** component boundaries, contracts between them, failure points, non-functional requirements. (Optional: when endpoint specifications are needed at gate 4, use the installed `api-designer` skill to draft initial REST specs reviewed within the design.)
6. **Diagram:** draw a `mermaid` diagram (components/flow) reflecting the decision — reviewable text, never a vague image.
7. **Migration plan:** transition steps + rollback point + data impact + a verification gate for each step.
8. Produce the evidence block (see below) through `sofi-evidence` before delivery.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: one ADR file structured `[Context · Options · Decision · Consequences]` + system design + mermaid diagram + migration/rollback plan.
- **Evidence (Law 4) — Architect type** (P-03.8) via the `sofi-evidence` skill:
  - **Architecture diagram** — a mermaid diagram of components and boundaries after the decision.
  - **ADR** — the complete document with its four sections, each option with its evidence-backed trade-offs.
  - **Migration plan** — numbered steps + rollback point + data impact per step.
- Every element independently verifiable (`file:line` for affected files, no LLM claims).

## 🔗 Handoff ⬛
- Deliver the ADR + evidence to **arc-lead (Architecture room lead)** only (Law 3) via the `sofi-handoff` skill.
- arc-lead consolidates and escalates upward to `brd-ceo`; the CEO consults `brd-cto` on gates 3–4.
- No direct delivery to the user. No addressing another room directly (Law 2) — contracts flow through leads.

## ⛔ Constraints ⬛
- An ADR without ≥2 weighed options = rejected (a decision without alternatives is not a decision).
- Without a rollback plan = does not cross the migration gate.
- No executing the migration inside this skill — this is documentation and design; execution is a separate work order for the Operations room via leads.
- Never override any of the thirteen laws (especially 2/3/4/5/7).

## 🧠 Memory ⬜
- Record every approved ADR in `hq/brain/cortex-decisions.md` (Law 7): identifier, decision, rejected alternative, reason, approval date — so it becomes a reference precedent.
- Architectural incidents (migration divergence/failure) → `hq/brain/amygdala-incidents.md`.

## 📚 References ⬜
- `hq/core/contracts.md` — acceptance criteria for gates 3–4.
- `hq/core/protocols.md` — Protocol 03 (§P-03.8 Architect evidence).
- The `sofi-evidence` and `sofi-handoff` skills — evidence and hierarchical delivery.
