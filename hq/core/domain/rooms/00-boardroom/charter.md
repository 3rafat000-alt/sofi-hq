# Board Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 00-boardroom
**Code:** brd
**Room lead:** `brd-ceo`

---

## | Identity

**Purpose:**
Executive leadership, governance, and strategic decision-making

**Agent count:** 7

---

## | Agent Roster

- `brd-ceo` — ceo
- `brd-cpo` — cpo
- `brd-cto` — cto
- `brd-cqo` — cqo
- `brd-cso` — cso
- `brd-chief-of-staff` — chief-of-staff
- `brd-arbiter` — arbiter

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. CEO receives the report from intake
2. CEO consults the Board via Task
3. The Board decides or recommends
4. CEO distributes work to room leads

---

## | Connected Rooms

01-strategy (direction), 14-gateway (request intake)

---

## | Gate Ownership

**My stage in production line v2:** S1 (approval) · every decisive stage — full map at `nexus/gates.yaml#stage_map`.

Fast-track delegation at Gate 0 (exclusive to brd-ceo — owned by 01-strategy) · approval of decisive gate rulings and DFR once the signatories have signed

---

## | Handoff Protocol

1. The member completes its task and records evidence
2. The member hands off to brd-ceo (room lead)
3. brd-ceo reviews and unifies
4. brd-ceo delivers to the user

**Forbidden:**
- An agent delivering directly to the user
- An agent addressing another room
- A room lead executing the work personally

---

## | Skills

- **Room playbook:** `brd-decision-gate` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Board Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.
