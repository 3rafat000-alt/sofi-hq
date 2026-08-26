---
name: obs-incident-response
description: >-
  For when an operational incident ignites or a metric breaks and needs detection → alerting → response → analysis. Triggers —
  "incident", "service is down", "SLO breach", "alert fired", "there is an
  incident", "the metric broke", "page fired", "on-call response", "postmortem",
  "log the incident", "declare incident", "error spike",
  "latency spike", "MTTR". Invoked inside the Observability room (12)
  upon detecting a live fault or alert — not for building dashboards from scratch nor routine threshold tuning.
---

# obs-incident-response — The Incident & Monitoring Playbook ⬛

> Turns a live fault signal into a disciplined response: metric-based detection → confirmed alerting → timeline-driven incident command → root cause analysis → recording the emergency in AMYGDALA — no improvisation and no lost evidence.

## 🎯 When to invoke (When) ⬛
- A monitoring metric broke (errors/latency/saturation/availability) or an SLO/error-budget was breached and response is needed.
- An alert fired from the monitoring system and needs triage, confirmation, then incident command.
- A postmortem/root cause analysis of an incident is requested, or an emergency must be recorded in the emotional memory.
**Do not invoke** for: building a dashboard/monitoring board from scratch (routine `obs-monitoring-engineer` work), non-emergency alert threshold tuning (`obs-alerting-engineer` work), or long-term product analysis with no incident (`obs-insights-analyst` work).

## 📥 Required inputs (Inputs) ⬛
- RCCF work order (Law 5) — no execution without it; it defines the affected service, the response scope, and authority.
- The signal: name of the fired metric/alert + its current value against the threshold/SLO.
- Time window: deviation start (timestamp) and the examination time range.
- Measurement sources: metrics/logs/traces links + service/environment (prod/staging).

## 🔧 Steps (Steps) ⬛
1. Read the RCCF; fix the affected service, incident severity (SEV1–SEV4), and the relevant SLO.
2. **Detection (monitoring):** task `obs-monitoring-engineer` via Task to collect metrics (error rate, p95/p99 latency, saturation, availability) before/after deviation start with screenshots.
3. **Alerting:** task `obs-alerting-engineer` with confirming the alert (real, not false-positive), linking it to the metric, and documenting fire time.
4. **Response (incident command):** task `obs-incident-commander` with declaring the incident, opening a timeline, executing mitigation/rollback, and logging MTTA/MTTR.
5. **Analysis (insights):** task `obs-insights-analyst` (and when needed `obs-sre`) with root cause analysis (RCA), impact, error-budget lesson, and recommendations.
6. Review agent results and verify evidence (metrics + alert + timeline) — any gap is redone before consolidation (Law 8).
7. **Emergency → AMYGDALA (Law 7):** record the incident in `hq/brain/amygdala-incidents.md` (time, severity, impact, root cause, mitigation, lesson).
8. Produce the evidence block (see below) via the `sofi-evidence` skill, then consolidate a unified result.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: unified incident report = summary + timeline + RCA + mitigation actions + recommendations, plus the AMYGDALA entry for the emergency.
- **Evidence (Law 4) — DevOps/SRE type:** use the `sofi-evidence` skill:
  - **metrics**: indicator values before/after (error rate, p95/p99, saturation, availability) with screenshots/links and their sources.
  - **alert**: fired alert text + fire time + breached threshold + resolution status.
  - **timeline**: timestamped timeline (detection → declaration → mitigation → resolution) with MTTA/MTTR.
  - **exit codes**: for every executed mitigation/health-check command, with outputs.
  - **rollback/health**: rollback plan/result and the post-recovery health check.

## 🔗 Handoff ⬛
- Agents deliver to me (`obs-lead`) inside the room; I consolidate, review evidence, then deliver the unified result to `brd-ceo` only (Law 3) via the `sofi-handoff` skill.
- No direct delivery to the user. No addressing another room directly (Law 2) — any Security/Operations escalation goes through `brd-ceo`.
- Immediate escalation to `brd-ceo` at SEV1, a critical SLO breach, or conflicting/missing requirements.

## ⛔ Constraints ⬛
- No response without the three evidence items (metrics + alert + timeline) — evidence-incomplete delivery is rejected (L2).
- No impactful mitigation on prod without RCCF and explicit authority; only CEO-authorized emergencies break the speed hierarchy (Law 8).
- No skipping a lead/CEO and no user delivery (Laws 1/3); inter-room communication through leads (Law 2).
- Work directly on the project's main tree — no worktrees or isolated copies (Law 10).
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Every emergency → `hq/brain/amygdala-incidents.md` (Law 7), mandatory per incident.
- Important response decision/lesson learned → `hq/brain/cortex-decisions.md`; session documentation → `hq/brain/hippocampus-sessions.md`.

## 📚 References ⬜
- `hq/core/protocols.md` → P-03.8 (evidence types), the incident response protocol.
- `hq/core/contracts.md` → the Observability room's (12) contracts with the Board.
- Shared skills: `sofi-evidence`, `sofi-handoff`.
- **Owner (Law 9):** Observability room 12-observability — `obs-lead`.
