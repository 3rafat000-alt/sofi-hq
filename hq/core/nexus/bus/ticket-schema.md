# RCCF Ticket Schema — Unified Handoff Format

> The previous `TKT-NNN` schema (id/gate/from/to/task/consumes/expected/route) was retired 2026-07-17 by owner order — it contradicted actual practice. This file codifies the RCCF handoff ticket actually emitted by `.opencode/skills/sofi-handoff/SKILL.md` and recorded per `hq/brain/brain_templates/HANDOFFS.md`. gtw-gatekeeper validates THIS format.

## Fields

| Field | Required | Format |
|-------|----------|--------|
| ticket_id | yes | `<PRJ-ID>-<seq>` — recorded as a `TKT-NNN` heading in the project's HANDOFFS.md |
| rccf_ref | yes | `WO-YYYY-MM-DD-XXX` — the brd-ceo-approved work order (Law 5: no execution without RCCF) |
| from_agent | yes | agent-id from `hq/core/nexus/registry.yaml` |
| to_agent | yes | agent-id from registry — upward only (agent → own Lead → brd-ceo; cross-room via both Leads, P-02.7) |
| objective | yes | original objective from the work order, one line |
| success_metric | yes | measurable success criterion |
| artifacts | yes | delivered files/paths |
| evidence | yes for `ready-for-review`/`done` | full `sofi-evidence` block, verbatim (Law 4: file:line per change + exit code per command) |
| status | yes | open \| accepted \| ready-for-review \| done \| rejected \| blocked |
| handoff_note | no | context that must not be lost |

## Status vocabulary

- `open` — ticket issued, not yet accepted (P-02.4: no default acceptance).
- `accepted` — receiver explicitly accepted the handoff.
- `ready-for-review` — work delivered upward with evidence attached, awaiting reviewer decision.
- `done` — reviewer verified evidence (P-02.9: file:line exists, exit codes, screenshots) and closed.
- `rejected` — reviewer specified exactly what is missing (P-02.6; vague rejection → L1).
- `blocked` — escalation in flight (see `bus/escalation.md`); resumes only after decision recorded.

## Validation (checked by gtw-gatekeeper)

- from_agent/to_agent must be valid agent IDs in registry.
- Room boundary: same room, agent→Lead, Lead→Lead, or boardroom/gateway→Lead (P-02.7).
- Exactly one PRJ-ID per ticket (P-14.3); ambiguous PRJ-ID → rejected by gtw-intake-reformer.
- Status must be in the allowed set above.
- `ready-for-review` and `done` require the evidence block attached (Law 4).
- rccf_ref must reference an existing approved work order (Law 5).

---

*Old schema retired 2026-07-17. Single source of the emitted format: `.opencode/skills/sofi-handoff` + `hq/brain/brain_templates/HANDOFFS.md`.*
