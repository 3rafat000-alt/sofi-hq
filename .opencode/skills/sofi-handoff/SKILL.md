---
name: sofi-handoff
description: >-
  Builds the official SOFI delivery ticket (RCCF) for hierarchical handoff between agents and rooms (Law 3 + Protocol 02). Triggers — "hand off", "handoff ticket", "RCCF ticket", "deliver to lead", "cross-room handoff", "hand over the task", "delivery ticket", "deliver to the room". Invoked by any agent/lead when handing work upward in the hierarchy.
---

# sofi-handoff — The Handoff Ticket Builder (Hierarchical Handoff / RCCF)

> **Law 3:** agent → their room lead → brd-ceo → user. Direct delivery to the user or to another room is forbidden. Verbal handoff = L2.

## 🎯 When to invoke (When)
- An agent delivers output to their room lead.
- A room lead delivers to brd-ceo.
- Delivery between two rooms (via leads exclusively — Law 2).
- Receiving a delivery (verification + explicit acceptance).

## 📥 Inputs
- The original RCCF work order (Law 5).
- A ready evidence block from `sofi-evidence` (Law 4).
- A checkpoint in `hq/brain/hippocampus-sessions.md` (P-02.1 — no delivering unrecorded work).

## 🔧 Steps
1. **Checkpoint** first: record the state in HIPPOCAMPUS before delivery (P-02.1).
2. Identify the correct destination upward in the hierarchy — no skips, no sideways delivery.
3. Fill the RCCF ticket (below) — attach evidence verbatim (P-02.3: leads relay literally).
4. Send and request **explicit acceptance** (P-02.4 — no implied acceptance).
5. Record the delivery receipt in HIPPOCAMPUS (P-02.5): timestamp, from, to, ticket_id, artifacts, status.

## 📤 Output — the RCCF ticket

```
### RCCF Handoff Ticket
- ticket_id: <PRJ-ID>-<seq>
- from_agent: <id>        to_agent: <lead_id>   (upward only)
- objective: <the work order's original objective>
- success_metric: <the measurable success criterion>
- artifacts: <files/paths>
- evidence: <full sofi-evidence block, verbatim>
- status: ready-for-review
- handoff_note: <context that must not be lost>
```

## 🔗 Acceptance / Rejection
- **Accept:** the receiver verifies the evidence (file:line present, exit codes, screenshots) — P-02.9 — then accepts explicitly.
- **Reject:** specify exactly what's missing (evidence/completeness/quality) — P-02.6. Vague rejection = L1.
- Without acceptance the delivery is "in-flight", not "delivered" (P-02.4).

## 📦 The strict cross-room communication scheme (Strict JSON Handoff Scheme)

Every ticket **crossing a room boundary** travels as a unified compact JSON — no free narrative, no pasted full contexts. Goal: preventing Context Window Bloat:

```json
{
  "v": 1,
  "ticket_id": "PRJ-ID-001",
  "from_agent": "bck-api-engineer",
  "to_agent": "bck-lead",
  "direction": "upward-only",
  "type": "handoff|acceptance|rejection",
  "rccf_ref": "RCCF-2026-0823-NAME",
  "artifacts": ["projects/<name>/app/Domains/X/Actions.php"],
  "evidence_digest": {
    "files_changed": 3,
    "checks": {"static_analysis": "PASS", "tests": "PASS"},
    "exit_codes": [0]
  },
  "context_refs": ["hq/core/standards/api-envelope.md#envelope-v1"],
  "status": "ready-for-review|in-flight|delivered|rejected",
  "note": "<≤280 chars>"
}
```

**Strict schema rules:**
1. `note` ≤ 280 characters — details live in the files referenced via `context_refs`, never inside the ticket.
2. Full evidence stays in the `sofi-evidence` block inside the checkpoint file; the ticket carries **only the evidence fingerprint** (`evidence_digest`) — the receiver reads the source when needed and is not force-fed content automatically.
3. Any field outside the schema = automatic ticket rejection by the receiver (L1) — extension happens by issuing a new `v` with CEO approval only.
4. The same schema serves `type: rejection` tickets for replies — no free-text messages outside `note`.

## ⛔ Constraints
- Direct delivery to the user forbidden (P-01.5 / Law 3) = L3.
- Sideways delivery between two agents across room boundaries forbidden — through leads (P-02.7) = L3.
- Delivering unrecorded work forbidden (P-02.1) = L2.
- The lead relays content verbatim with original citations (P-02.3).
