# DevOps Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 11-devops
**Code:** ops
**Room lead:** `ops-lead`

---

## | Identity

**Purpose:**
CI/CD, infrastructure, cloud, deployment, cost management

**Agent count:** 8

---

## | Agent Roster

- `ops-lead` — lead
- `ops-cicd-engineer` — cicd-engineer
- `ops-cloud-engineer` — cloud-engineer
- `ops-cost-optimizer` — cost-optimizer
- `ops-domain-warden` — domain-warden
- `ops-migration-runner` — migration-runner
- `ops-release-manager` — release-manager
- `ops-sandbox-executor` — sandbox-executor *(2026-08-26: isolated-container build gate before QA · Hard Rule #11)*

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Receive infrastructure from arc-lead
2. Provision the environment
3. Build the pipeline
4. Deploy
5. Monitor
6. Hand off to brd-ceo

---

## | Connected Rooms

04-architecture (design), 05-backend (build), 12-observability (monitoring)

---

## | Gate Ownership

**My stage in production line v2:** S6 — deployment (staging/production · Gate-6/7) — full map at `nexus/gates.yaml#stage_map`.

Gate-6 (Staging), Gate-7 (Production)

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

- **Room playbook:** `ops-deploy-runbook` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **External room skills:** `cicd-pipeline-skill`
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The DevOps Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.
