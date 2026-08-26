# FILE: hq/core/runbooks/incident-response.md
# Consolidated Incident Runbooks — implements Protocol 10 step-by-step
#
# Purpose: pre-written response playbooks so no one improvises mid-crisis.
# Classification and deadlines come from protocols.md P-10.1–P-10.9; this file
# is the executable checklist layer on top of them.
# Infrastructure-specific recovery lives separately in hq/engine/OPERATIONS.md.

## How to use

On detection, the detecting agent runs ONLY Step 0 and Step 1 of the matching
runbook, then hands to its room lead — leads own Steps 2+, per P-10.2.
During SEV-1 the communication blackout applies (P-10.7): emergency traffic only.

---

## RUNBOOK R1 — SEV-1 Critical (system crash · data loss · security breach · constitutional violation)

**Trigger examples:** brain/memory store corrupted or unreadable · unauthorized agent behavior · frozen contract touched · production site down · secret leaked into a delivery.

1. **Freeze & checkpoint (detecting agent):** stop all writes immediately · create brain checkpoint entry in `hq/brain/hippocampus-sessions.md` (P-10.3) · capture evidence (exact command, exit code, file:line).
2. **Notify:** room lead → brd-ceo + brd-cso + brd-cqo (emergency board). Blackout ON.
3. **Contain (lead):** quarantine the failing component/agent · block further merges/deploys via ops-lead · for breaches: revoke exposed credentials first, investigate second.
4. **Assess:** confirm classification (if it is actually SEV-2, downgrade is allowed once, documented — never the reverse silently).
5. **Recover (P-10.5):** restore from last verified checkpoint/backup → verify integrity → resume flow from gtw-intake-reformer → replay lost work through fresh RCCF tickets.
6. **Close:** formal RCA ≤ 20 turns filed to AMYGDALA (P-10.4) · postmortem to LESSONS (P-10.8) · blackout OFF only by brd-ceo order.

**Never do:** delete evidence · "quick-fix then document later" · resume work without integrity verification.

## RUNBOOK R2 — SEV-2 High (agent failure mid-task · pipeline corruption · brain inconsistency)

**Trigger examples:** subagent returns corrupt/partial output twice · gate state machine out of sequence · memory files disagree with each other.

1. Detecting agent: checkpoint (P-10.3) + preserve the failed output verbatim as evidence.
2. Notify room lead within the 3-turn window (P-10.1). Lead notifies brd-ceo.
3. Quarantine the failed agent/task; reassign via fresh RCCF ticket (P-10.6) — no blind third attempt (Law 6 anti-loop: 3 failures of one category = dump logs + escalate).
4. Repair pipeline/brain inconsistency from the authoritative source (registry.yaml · system-state-current.md); if sources conflict, freeze and escalate to brd-arbiter.
5. RCA ≤ 20 turns to AMYGDALA; postmortem if the failure was systemic.

## RUNBOOK R3 — SEV-3 Medium (gate failure · test failure · quality breach)

**Trigger examples:** artifact rejected at its gate · regression suite red · quality verdict fail on a delivered task.

1. Pause the affected stage only — other stages continue.
2. Room notified within 5 turns (P-10.1); brd-cqo + qa-lead review per P-10.2.
3. Fix through normal flow: rejection goes back to the lowest responsible tier via leads' chain (nexus/room-priority.yaml work_order_rules).
4. Two consecutive rejections for the same reason = Law 14 freeze → brd-arbiter within 24h. Do not attempt fix #3 blind.
5. Log outcome; no RCA required unless it recurs three times in a week (then treat as SEV-2 candidate).

## RUNBOOK R4 — SEV-4 Low (minor violation · handoff failure)

Lead handles inline with documentation in the session record. Response ≤ 10 turns. Pattern of recurrence (≥ 3/week) escalates one level.

---

## Drill requirement (P-10.9)

Every 50 agent turns ops-lead runs a tabletop drill: pick one runbook, walk it
end-to-end on paper against the current system state, file gaps found to AMYGDALA.
Drill results feed the Monthly Organizational Report (standards/reporting-cadence.md §Monthly §3).

## Mapping to alerts

Every configured alert must map 1:1 to exactly one runbook above or a dedicated
playbook beside them (gate-8.md:20, KPI K17). Unmapped alert = Gate-8 fails.

*References: protocols.md Protocol 10 · AGENTS.md Laws 6/14 · nexus/room-priority.yaml · standards/reporting-cadence.md · hq/engine/OPERATIONS.md (infra-level recovery). Created 2026-08-26.*
