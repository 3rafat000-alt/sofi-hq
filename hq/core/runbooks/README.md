# `hq/core/runbooks/` — Operational Runbooks

> Step-by-step runbooks for handling specific operational events (incidents, deployments, etc.).
> Per `reporting-cadence.md`, runbooks are triggered **on event** (incident, deploy, error) — not on
> a schedule (Rec #16 — no human-time concepts).

Owned by `obs-lead` (12-observability) + `ops-lead` (11-devops).

---

## Files

| File | Purpose | Trigger | Owner |
|------|---------|---------|-------|
| `incident-response.md` | P0/SEV-1 incident response — detection → triage → containment → recovery → postmortem | `obs-incident-commander` declares SEV-1 | `obs-lead` + `war-incident-commander` |

> More runbooks may be added as needed (e.g. `disaster-recovery.md`, `compliance-audit.md`,
> `monthly-archaeology.md`).

---

## The incident-response runbook (current)

> Source: `incident-response.md` — the canonical SEV-1 response procedure.

**Phases:**
1. **Detect:** `obs-monitoring-engineer` dashboard spike + `obs-alerting-engineer` page
2. **Declare:** `obs-incident-commander` declares SEV-1
3. **Triage:** `obs-sre` assesses impact + scope
4. **Handoff to WarRoom:** if P0 → `brd-ceo` issues emergency RCCF → `war-incident-commander` takes
   command (Law 14 freeze)
5. **Contain:** `war-rollback-engineer` activates rollback window
6. **Recover:** service restored + health checks pass
7. **Communicate:** `war-communication-lead` briefs owner every 30 min (Law 11)
8. **Postmortem:** within 24h, AMYGDALA entry + root cause + actions + Gate re-eval
9. **Re-eval:** P-20.3 — failure mode analysis + re-open the linked Gate

**Reporting cadence (per `reporting-cadence.md`):**
- On detect: alert fires → incident commander
- On declare: SEV-1 announcement to all-rooms
- Every 30 min during incident: status update (owner + teams)
- On recovery: closure + brief postmortem
- Within 24h: full postmortem in AMYGDALA
- Within 7 days: full failure-mode review (P-20.3)

---

## Rec #16 — Event-Driven Policy

> Per `AGENTS.md` + `reporting-cadence.md`, all runbooks are **on-event triggered** — no
> "daily standup" or "nightly scan" or "weekly retrospective". Human-time concepts are removed
> from agent mandates.

Runbooks activate when:
- An alert fires (SLO breach · error spike · anomaly)
- An RCCF is issued
- A commit lands (on-merge scans)
- An incident is closed (postmortem)

**Forbidden:** scheduled runbook executions (no cron, no daily, no weekly).

---

## How to add a new runbook

1. Create the `.md` file with the standard format (trigger + phases + reporting cadence + owner)
2. Add a row to the table above
3. Cross-reference from `hq/core/standards/reporting-cadence.md` if it's on-merge or on-incident
4. Commit atomically — pre-commit enforces all 4 guards
5. Record ADR in CORTEX if the new runbook changes constitutional behavior

**Forbidden:** scheduled runbook executions.

---

## See also

- [`../README.md`](../README.md) — `hq/core/` parent
- [`../standards/reporting-cadence.md`](../standards/reporting-cadence.md) — on-merge / on-incident-close
- [`../protocols.md:P-10`](../protocols.md) — Emergency Protocol
- [`../nexus/gates.yaml`](../nexus/gates.yaml) — gates
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 11
