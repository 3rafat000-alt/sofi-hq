# Architecture Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 04-architecture
**Code:** arc
**Room lead:** `arc-lead`

---

## | Identity

**Purpose:**
System design, architecture, integration planning

**Agent count:** 9

---

## | Agent Roster

- `arc-lead` — lead
- `arc-system-architect` — system-architect
- `arc-api-architect` — api-architect
- `arc-data-architect` — data-architect
- `arc-infra-architect` — infra-architect
- `arc-integration-architect` — integration-architect
- `arc-review-architect` — review-architect
- `arc-security-architect` — security-architect (added 2026-08-26, owner order)
- `arc-performance-architect` — performance-architect (added 2026-08-26, owner order)

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Receive requirements from brd-ceo
2. Analyze architectural options
3. Document decisions (ADRs)
4. Present the implementation plan
5. Hand off to brd-ceo

---

## | Connected Rooms

05-backend (build), 06-frontend (build), 08-data (data), 11-devops (deployment)

---

## | Gate Ownership

**My stage in production line v2:** S2 — stage lead (ERD + OpenAPI on paper, via Gate-3) — full map at `nexus/gates.yaml#stage_map`.

Gate-3 (Architecture)

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

- **Room playbook:** `arc-adr` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **External room skills:** `api-designer` · `api-documentation` · `mcp-builder` · `api-ai-augmented`
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Architecture Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.

**Shift-left quality rule (owner order 2026-08-26):** no API contract is frozen without `qa-test-architect` (room 10, via leads' chain) reviewing it for testability — a contract that cannot be tested cheaply is a defect at design time, not at QA time.
