# Research Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 02-research
**Code:** res
**Room lead:** `res-lead`

---

## | Identity

**Purpose:**
UX research, competitor analysis, fact checking

**Agent count:** 8

---

## | Agent Roster

- `res-lead` — lead
- `res-ux-researcher` — ux-researcher
- `res-journey-architect` — journey-architect
- `res-competitor-analyst` — competitor-analyst
- `res-data-researcher` — data-researcher
- `res-fact-checker` — fact-checker
- `res-web-scout` — web-scout
- `res-visual-pattern-scout` — visual-pattern-scout (added 2026-08-26, owner order)

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Receive research direction from brd-ceo or str-lead
2. Execute the research
3. Deliver a findings report
4. Hand off to brd-ceo

---

## | Connected Rooms

01-strategy (analysis), 03-design (design), 13-knowledge (documentation)

---

## | Gate Ownership

**My stage in production line v2:** S1 — market and competitor research feeds the PRD — full map at `nexus/gates.yaml#stage_map`.

Gate-1 (Discovery — owner)

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

- **Room playbook:** `res-journey-map` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Research Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.
