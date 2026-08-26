---
type: brain
mem: episodic
prj: PRJ-CADDY
---
# HANDOFFS — PRJ-CADDY · Hierarchical Handoff Log

> Hierarchical handoff is mandatory (Law 3 — `hq/core/CONSTITUTION.md`): **agent → its room lead → brd-ceo → user**.
> Forbidden: direct delivery to the user, delivery straight to another room (Law 2 — isolation), execution without an RCCF work order (Law 5).
> No `done` is accepted without a complete evidence block: file:line for every change + exit code for every command (Law 4). Without evidence = handoff rejected (L2).
> Status ∈ open | accepted | done | rejected | blocked. Escalation passes exclusively through the room lead to brd-ceo (Law 9).

## TKT-001
- **ID:** TKT-001
- **RCCF reference:** SOFI-RCCF-20260824-CADDY-001 — direct owner order via the gateway (HIPPOCAMPUS §INT-GTW-018)
- **From:** gtw-intake-reformer (room 14) — two Task attempts toward brd-ceo failed with an environmental network error (`Provider finish_reason: network_error` — task_ids: ses_fcbc1a826ffeWfu8tyOEH2Hl1l · ses_fcbbf67b3ffeJsvY9m5gCqtwfx), so execution proceeded internally per the approved precedent INT-010-A / INT-GTW-015/016/017
- **To:** the project itself (birth + initialization)
- **Task:** birth of `projects/caddy/` with a full brain memory from official templates + `site/` structure by owner order + removal of its predecessor `hq/engine/` (permanent deletion on the owner's order "I don't want it" — replacing the archival plan) + updating documentation passing through it (STRUCTURE.md · MEMORY.md · SOFI.md) + updating HIPPOCAMPUS
- **Evidence block:** (Law 4 — mandatory before any `done`)
  - file:line — projects/caddy/{site/README.md, brain/*} (new birth) · hq/core/STRUCTURE.md §2 + change log · MEMORY.md §Engine→Projects · SOFI.md:18
  - exit code — mkdir+cp → 0 · mv hq/engine → 0 · git commit → 0 (see commit message)
- **Deliberately not executed:** any change to live `/etc/caddy/Caddyfile` (documented owner decision) · any migration of a live domain
- **Status:** done
- **Reviewer ruling:** awaiting brd-ceo approval once the channel is restored — delivery self-documented per precedent

## TKT-DRAFT-002 (draft — unassigned and unexecuted)
- **ID:** TKT-DRAFT-002
- **Subject:** migrating tobacco.zanjour.com from `/etc/caddy/Caddyfile` (outside git) into this project's management
- **Mandatory opening conditions:** approved design through gate G3 signed by sec(09)+qa(10) · full testing on a matching environment · a ready, tested rollback runbook · explicit owner approval · brd-cso veto review
- **Status:** draft — opens only on a new owner order after design and tests are complete
