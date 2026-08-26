---
name: brd-decision-gate
description: >-
  Board decision + gate playbook — when brd-ceo turns a fateful decision into Board consultation then opens/rejects a gate. Triggers — Arabic: "fateful decision", "consult the board", "board opinion", "open the gate", "gate decision", "security veto", "can we pass the gate?". English: "board decision", "consult the board", "board opinion", "open the gate", "gate decision", "security veto", "can we pass the gate?". Invoked by brd-ceo on every fateful decision or Gate crossing needing Board counsel.
---

# brd-decision-gate — The Board Decision Gate ⬛

> **Law 6:** the CEO consults the Board on fateful decisions; the final decision is his. This playbook converts a fateful decision into documented consultation then a formal gate open/reject — no improvisation, no fateful decision without the Board and evidence.

## 🎯 When to invoke (When) ⬛
- A fateful decision: major architectural change, stack choice, budget/resources, security or legal risk.
- Crossing a formal gate (Gate 0–8) requiring Board signature before passing the artifact. + **DFR** (the design-freeze gate at end of S3: sec-lead and qa-lead signature then CEO approval — source `gates.yaml#dfr`)
- A dispute between two rooms reaching the CEO needing arbitration (via brd-arbiter).
- Any situation where the constitution mandates Board counsel before proceeding.

**Do not invoke** for: routine work assignment to a room lead, a simple informational reply, or a decision within one room lead's authority — those never reach the Board.

## 📥 Required inputs (Inputs) ⬛
- **RCCF work order (Law 5)** — no consultation nor gate without it (PRJ-ID, objective, success criterion, constraints).
- The fateful decision's formulation: proposed options + trade-offs + known risks.
- The relevant gate number/name and its crossing condition (from `hq/core/nexus/gates.yaml`).
- Initial supporting evidence per option (from involved rooms via their leads).

## 🔧 Steps (Steps) ⬛
1. **Frame the decision:** draft one decisive question + options (A/B/C) + a measurable settlement criterion.
2. **Consult the Board via Task (Law 6):** send the same frame to relevant members — brd-cpo (product/gates 0–2), brd-cto (tech/gates 3–4), brd-cqo (quality/gate 5), brd-cso (security — all gates), brd-arbiter (dispute), brd-chief-of-staff (conversion into a work order). Each replies with one **Board Opinion** block: `APPROVE | REJECT | CONDITIONS` justified with evidence.
3. **Assemble opinions (Board Opinion Matrix):** table of member ← opinion ← justification ← conditions.
4. **Check the security veto (brd-cso):** if brd-cso's opinion is `REJECT` → **absolute veto**, the gate is rejected and opens only with brd-cso's own consent or CEO + Board consensus (P-08.4 / Contract 06). Document justification.
5. **CEO final decision:** weigh by evidence, not voting. Log: decision, chosen option, dissenting opinions and why overridden, binding conditions.
6. **Open/reject the gate (Gate verdict):** `GATE-OPEN` (with conditions) or `GATE-REJECT` (with exactly what's missing for resubmission).
7. Produce the evidence block (Decision Record/ADR) and log it in CORTEX before any passing.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- **Output:** fateful decision record + Board Opinion Matrix + gate verdict `GATE-OPEN`/`GATE-REJECT`.
- **Evidence (Law 4) — Decision Record/ADR type (governance):** use the `sofi-evidence` skill:
  - ADR: context, options, decision, consequences, dissenting opinions.
  - Board Opinion Matrix: each member's opinion verbatim + evidence-based justification.
  - Security veto status (brd-cso) explicit: triggered/not triggered + justification.
  - Gate reference (Gate #) and crossing condition from `gates.yaml`, plus the CORTEX decision id.

```
### Board Decision Record
- decision_id: <PRJ-ID>-DEC-<seq>     gate: <Gate-N>
- question: <the decisive question>            options: A|B|C
- board_matrix:
    brd-cpo: APPROVE  — <reason+evidence>
    brd-cto: CONDITIONS — <the condition>
    brd-cso: REJECT   — <security reason>  → VETO ACTIVE
- ceo_decision: <option> + <why it was preferred> + <which opinion was overridden and why>
- verdict: GATE-REJECT (security veto — corrected and resubmitted)
- cortex_ref: <link to CORTEX entry>
```

## 🔗 Handoff ⬛
- The verdict distributes **downward** to relevant room leads via Task (the CEO's role in distributing work) — hierarchical delivery (Law 3): CEO ← room lead, no jumping to agents.
- During consultation: brd-* members stay inside the Board room only — no addressing executive rooms directly (Law 2).
- Final delivery to the user remains a separate step within the flow (P-01.2), never part of this verdict.

## ⛔ Constraints ⬛
- No fateful decision nor gate opening without Board consultation (ignoring the Board = L3).
- brd-cso's veto is bypassed only by brd-cso himself or CEO + Board consensus (bypassing it = L4).
- No acceptance without Decision Record/ADR evidence (Law 4 = L2). A Board Opinion without justification = returned.
- Never override any of the thirteen laws; the CEO executes through leads, not personally.

## 🧠 Memory ⬜
- Record every fateful decision and gate verdict in `hq/brain/cortex-decisions.md` (Law 7) — decisions/ADRs are always preserved (P-06).
- Document sessions in `hq/brain/hippocampus-sessions.md`, and any security veto/emergency in `hq/brain/amygdala-incidents.md`.

## 📚 References ⬜
- `hq/core/protocols.md` (P-01 flow, P-06 memory, P-08.4 security veto).
- `hq/core/contracts.md` (Contract 06 — security review at every gate).
- `hq/core/nexus/gates.yaml` — gate definitions and crossing conditions.
- The `sofi-evidence` and `sofi-handoff` skills for evidence and delivery.
