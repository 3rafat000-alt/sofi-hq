# Backend Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 05-backend
**Code:** bck
**Room lead:** `bck-lead`

---

## | Identity

**Purpose:**
Server development, APIs, business logic, integration

**Agent count:** 8

---

## | Agent Roster

- `bck-lead` — lead
- `bck-api-engineer` — api-engineer
- `bck-domain-engineer` — domain-engineer
- `bck-blade-engineer` — blade-engineer
- `bck-queue-engineer` — queue-engineer
- `bck-integration-engineer` — integration-engineer
- `bck-code-reviewer` — code-reviewer
- `bck-refactoring-surgeon` — refactoring-surgeon

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Receive specifications from arc-lead
2. Develop code (TDD)
3. Test
4. Review code
5. Hand off to brd-ceo (consulting arc-lead is allowed without delivering)

---

## | Connected Rooms

04-architecture (design), 08-data (data), 09-security (security), 11-devops (deployment)

---

## | Gate Ownership

**My stage in production line v2:** S2 (design) · S4 — live backend execution (Gate-4a) — full map at `nexus/gates.yaml#stage_map`.

Gate-4 (Build)

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

- **Room playbook:** `bck-feature-build` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **External room skills:** `phpunit-skill` · `laravel-dusk-skill`⭐(Blade) · `behat-skill` · `api-designer/analyzer/documentation/fetcher`
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Backend Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.
