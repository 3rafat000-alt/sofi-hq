# Design Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 03-design
**Code:** dsn
**Room lead:** `dsn-lead`

---

## | Identity

**Purpose:**
Visual design, design system, branding, UX

**Agent count:** 8

---

## | Agent Roster

- `dsn-lead` — lead
- `dsn-ui-designer` — ui-designer
- `dsn-design-system` — design-system
- `dsn-brand-designer` — brand-designer
- `dsn-content-strategist` — content-strategist
- `dsn-motion-designer` — motion-designer *(scope extended 2026-08-26, owner order: also owns interaction-behavior design)*
- `dsn-a11y-specialist` — a11y-specialist
- `dsn-ux-architect` — ux-architect

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Receive requirements from brd-ceo
2. Research and gather inspiration
3. Design and iterate
4. Present for review
5. Hand off to brd-ceo

---

## | Connected Rooms

02-research (research), 06-frontend (implementation), 07-mobile (implementation)

---

## | Gate Ownership

**My stage in production line v2:** S3 — stage lead + hosting the design-freeze gate signature (DFR) — full map at `nexus/gates.yaml#stage_map`.

Gate-2 (Design)

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

- **Room playbook:** `dsn-design-handoff` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **External room skills:** `frontend-design`⭐ · `theme-factory` · `canvas-design` · `brand-guidelines` · `internal-comms` · `algorithmic-art`⚠️Med · `smartui-skill`
- **Full map:** `.opencode/skills/INDEX.md`.

**Shift-left data-privacy rule (owner order 2026-08-26):** no UX flow, screen, or mockup passes the Design-Freeze Review without `dat-privacy-officer` (room 08, via the leads' chain) signing off on every personal-data collection, storage, and display point — a privacy defect caught on paper costs nothing; caught in production it is an SEV-1 incident (runbook R1).

**Interaction-design ownership rule (owner order 2026-08-26):** `dsn-motion-designer` owns not only visual motion but the full interaction-behavior spec — press/hold/drag/scroll states, transitions between states, and micro-feedback — documented per component before handoff to the merged S5 team; `fnt-interaction-engineer` implements the spec and returns deviations through the leads' chain.

---

## | Room Law

The Design Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.
