# Frontend Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 06-frontend
**Code:** fnt
**Room lead:** `fnt-lead`

---

## | Identity

**Purpose:**
UI development, interaction, performance, accessibility

**Agent count:** 8

---

## | Agent Roster

- `fnt-lead` — lead
- `fnt-vue-engineer` — vue-engineer
- `fnt-react-engineer` — react-engineer
- `fnt-css-artisan` — css-artisan
- `fnt-interaction-engineer` — interaction-engineer
- `fnt-performance-engineer` — performance-engineer
- `fnt-a11y-engineer` — a11y-engineer
- `fnt-code-reviewer` — code-reviewer

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Receive designs from dsn-lead
2. Develop components
3. Test accessibility and performance
4. Review
5. Hand off to brd-ceo (consulting dsn-lead is allowed without delivering)

---

## | Connected Rooms

03-design (design), 05-backend (API), 10-quality (quality)

---

## | Gate Ownership

**My stage in production line v2:** S5 — merged Flutter/Dart team (Gate-4b); locked until S4 is complete — full map at `nexus/gates.yaml#stage_map`.

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

- **Room playbook:** `fnt-component-build` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **External room skills:** `frontend-design`⭐ · `web-artifacts-builder` · `theme-factory` · `jest-skill` · `vitest-skill` · `mocha-skill`
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Frontend Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.
