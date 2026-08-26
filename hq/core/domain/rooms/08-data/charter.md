# Data Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 08-data
**Code:** dat
**Room lead:** `dat-lead`

---

## | Identity

**Purpose:**
Databases, analytics, machine learning, privacy

**Agent count:** 7

---

## | Agent Roster

- `dat-lead` — lead
- `dat-db-engineer` — db-engineer
- `dat-cache-engineer` — cache-engineer
- `dat-etl-engineer` — etl-engineer
- `dat-analytics-engineer` — analytics-engineer
- `dat-ml-engineer` — ml-engineer
- `dat-privacy-officer` — privacy-officer

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Receive requirements from brd-ceo or arc-lead
2. Design the data schema
3. Run the migration
4. Test
5. Hand off to brd-ceo

---

## | Connected Rooms

04-architecture (design), 05-backend (API), 11-devops (deployment), 12-observability (monitoring)

---

## | Gate Ownership

**My stage in production line v2:** S2 (ERD/schema contribution) · S4 (activating live databases) — full map at `nexus/gates.yaml#stage_map`.

Schema contribution to G3/G4 (ownership per gates.yaml — this room owns no gate)

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

- **Room playbook:** `dat-schema-migration` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **External room skills:** `xlsx` · `pytest-skill` · `unittest-skill` · `api-compliance-checker`
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Data Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.
