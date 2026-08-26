# Strategy Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 01-strategy
**Code:** str
**Room lead:** `str-lead`

---

## | Identity

**Purpose:**
Market analysis, product planning, risk management, growth strategy

**Agent count:** 8

---

## | Agent Roster

- `str-lead` — lead
- `str-product-strategist` — product-strategist
- `str-business-analyst` — business-analyst
- `str-market-analyst` — market-analyst
- `str-roadmap-planner` — roadmap-planner
- `str-risk-analyst` — risk-analyst
- `str-monetization-strategist` — monetization-strategist
- `str-agile-orchestrator` — agile-orchestrator *(2026-08-26: flow tracking · cross-room blocker alerts · WIP ≤ 2 enforcement)*

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Receive direction from brd-ceo
2. Analyze data and trends
3. Present strategic recommendations
4. Hand off to brd-ceo

---

## | Connected Rooms

00-boardroom (reporting), 02-research (data), 03-design (direction)

---

## | Gate Ownership

**My stage in production line v2:** S1 — stage lead (PRD) — full map at `nexus/gates.yaml#stage_map`.

Gate-0 (Inception)

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

- **Room playbook:** `str-gate0-classify` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Strategy Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.

**Shift-left security rule (Law owner order 2026-08-26):** no roadmap is approved without `sec-threat-modeler` (room 09, via leads' chain) signing off on the expected risks of its major items — risk analysis happens before sequencing is frozen, never after build starts.

**Debt-capacity rule (owner decision 2026-08-26):** `str-roadmap-planner` reserves ≥15% of every Phase tree's capacity for tech-debt tasks, and `str-agile-orchestrator` enforces the reserve during board sweeps; `brd-cto` audits it in his monthly engineering-excellence review.
