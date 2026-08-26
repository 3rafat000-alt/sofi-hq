# Observability Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 12-observability
**Code:** obs
**Room lead:** `obs-lead`

---

## | Identity

**Purpose:**
System monitoring, alerting, SRE, incident analysis

**Agent count:** 6

---

## | Agent Roster

- `obs-lead` — lead
- `obs-monitoring-engineer` — monitoring-engineer
- `obs-alerting-engineer` — alerting-engineer
- `obs-sre` — sre
- `obs-incident-commander` — incident-commander
- `obs-insights-analyst` — insights-analyst

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Monitor metrics (SLOs) — measured against the binding catalog `hq/core/standards/kpi-thresholds.md` (K1–K17); red readings alert the owning lead same-session, two consecutive reds escalate to brd-ceo
2. Analyze incidents — response follows the consolidated runbooks `hq/core/runbooks/incident-response.md` (R1–R4 per Protocol 10)
3. Provide recommendations
4. Update dashboards
5. Produce the Daily Ops Digest and feed the Weekly/Monthly reports per `hq/core/standards/reporting-cadence.md`

---

## | Connected Rooms

11-devops (deployment), 05-backend (performance), 08-data (data)

---

## | Gate Ownership

**My stage in production line v2:** S6 — vigilance and metrics (Gate-8) — full map at `nexus/gates.yaml#stage_map`.

Gate-8 (Observe)

---

## | Handoff Protocol

1. The agent completes its task and records evidence
2. The agent hands off to the room lead
3. The room lead reviews and unifies
4. The room lead hands off to brd-ceo
5. brd-ceo delivers to the user

**Forbidden:**
- An agent delivering directly to the user
- An agent addressing another room
- A room lead executing the work personally

---

## | Skills

- **Room playbook:** `obs-incident-response` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Observability Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.
