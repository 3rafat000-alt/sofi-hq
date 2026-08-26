---
name: str-gate0-classify
description: >-
  The Strategy Gate-0 playbook — invoked when a new ticket/request arrives at a room and before any work, to classify the request (type/risk/size), propose fast-track eligibility (approved by CEO only), frame priority, draft a measurable success metric, and set the resource envelope. Triggers — "gate 0", "classify request", "triage request", "fast-track eligibility", "priority framing", "success metric", "resource envelope", "sizing".
---

# str-gate0-classify — The Gate 0 Playbook (Strategy Intake Classification) ⬛

> **Value:** no request enters the pipeline before being classified, measured, and framed. Gate 0 prevents starting work on the unknown.

## 🎯 When to invoke (When) ⬛
- When a new ticket/request arrives from brd-ceo at the Strategy room and before any assignment or execution.
- When re-classifying a request whose scope or risk changed.
- When a request needs a fast-track proposal, success metric, or resource envelope.

**Do not invoke** for: executing strategic analysis itself (market/business/risk — those are agents' tasks after passing the gate), nor approving fast-track (CEO decision exclusively).

## 📥 Required inputs (Inputs) ⬛
- A formal RCCF work order from brd-ceo (Law 5) — no classification without it.
- The raw/rephrased request text + any attached context (goal, constraints, deadline).
- If an essential element is missing (measurable goal, scope, owner) → escalate to brd-ceo immediately; never guess.

## 🔧 Steps (Steps) ⬛
1. **Classify type:** feature / research / fix / strategy-pivot / compliance / experiment. Tie each classification to evidence from the request text (a quote).
2. **Classify risk:** low / medium / high / critical across the axes: financial impact, security/privacy, user impact, reversibility. The highest axis sets the level.
3. **Classify size:** XS / S / M / L / XL by effort estimate and expected room involvement (count rooms, don't address them — Law 2).
4. **Propose fast-track eligibility:** preliminarily eligible only if (risk ≤ low) and (size ≤ S) and (no security/privacy impact). Write it as an explicit **proposal** — approval belongs to the CEO exclusively.
5. **Frame priority:** compute an approximate score via a value/effort framework (e.g., RICE or Value×Risk) with the values used, ranked against in-flight requests.
6. **Draft a measurable success metric:** number/threshold + unit + time horizon + measurement source (never vague "improve performance").
7. **Set the resource envelope:** candidate rooms, effort estimate, dependencies, and proposed deadline.
8. Produce the evidence block (see below) via the `sofi-evidence` skill.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- **Output:** one unified Gate-0 classification card:
  ```
  ### Gate 0 — <request-id>
  Type: <type> | Risk: <level> | Size: <size>
  Fast-track: PROPOSED <yes/no> (CEO decision)
  Priority: <score> via <framework> (values: ...)
  Success metric: <number+unit+horizon+measurement source>
  Resource envelope: <rooms> | <effort> | <dependencies> | <deadline>
  Open questions / gaps: <if any>
  ```
- **Evidence (Law 4) — Researcher/Analyst type** via `sofi-evidence`:
  - A source quote per classification: request/document text + literal extract.
  - Estimation methodology: the framework used (RICE/Value×Risk) + input values + calculation.
  - Source/backing for every number in the success metric and resource envelope (no unsupported numbers).
  - Confidence level (high/medium/low) per classification + reason for any uncertainty.

## 🔗 Handoff ⬛
- Deliver the Gate-0 card + evidence block to **brd-ceo** only (Law 3) via the `sofi-handoff` skill.
- Fast-track is a **proposal** approved by the CEO; never start execution based on it.
- No direct delivery to the user. No addressing another room (Law 2) — only count rooms in the envelope.

## ⛔ Constraints ⬛
- **Owner (Law 9):** str-lead — Strategy room (01). Accountable for every classification's accuracy.
- No classification without RCCF (Law 5). No delivery without evidence (Law 4).
- Never self-approve fast-track — exceeding authority = L3.
- A success metric without number/unit/horizon = rejected (redo it — Law 8, quality before speed).
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Record the classification decision and fast-track proposal in `hq/brain/cortex-decisions.md` (Law 7) after CEO approval.

## 📚 References ⬜
- `hq/core/contracts.md` (Strategy↔CEO contract), `hq/core/protocols.md` (gates), the `sofi-evidence` and `sofi-handoff` skills.

> **Scope settlement (INT-GTW-029):** track classification inside the gate (fast|standard|fateful before RCCF) = gtw-intake-reformer's own authority. Proposing **fast-track with reduced G1-G3 gate crossing** inside a room ticket = an offer approved exclusively by brd-ceo. No conflict: different time, different place.
