# Gateway Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 14-gateway
**Code:** gtw
**Room lead:** `gtw-dispatcher`

---

## | Identity

**Purpose:**
Request intake, routing, budget management, conflict resolution

**Agent count:** 7

---

## | Agent Roster

- `gtw-dispatcher` — dispatcher
- `gtw-router` — router
- `gtw-gatekeeper` — gatekeeper
- `gtw-budget-warden` — budget-warden
- `gtw-conflict-resolver` — conflict-resolver
- `gtw-external-reviewer` — external-reviewer
- `gtw-intake-reformer` — intake-reformer

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. gtw-intake-reformer receives the request
2. gtw-dispatcher routes to the appropriate room
3. gtw-gatekeeper verifies permissions
4. gtw-budget-warden manages the budget
5. gtw-conflict-resolver resolves conflicts

---

## | Connected Rooms

All rooms + external parties

---

## | Gate Ownership

**My stage in production line v2:** S1 — intake, classification, and routing — full map at `nexus/gates.yaml#stage_map`.

Gate-0 — intake only (owner: 01-strategy)

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

- **Room playbook:** `gtw-intake-route` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Gateway Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.

**Smart Clarification Loop (Law 16 · owner order 2026-08-26 — amended 2026-08-31 P-01.10):** `gtw-intake-reformer` computes an ambiguity score for every incoming request (missing inputs · conflicting constraints · undefined scope). Above **20%**, processing halts immediately — no routing, no work orders — and a clarification card of 1–3 sharply specific questions is emitted to the owner with an explicit **24-hour deadline**. The loop repeats until the score drops below threshold; guessing past ambiguity is forbidden at every level. **Timeout & anti-paralysis:** if the owner does not answer within 24h, `gtw-intake-reformer` auto-escalates via `gtw-conflict-resolver` to `brd-arbiter` (room 00) whose binding decision is due within 24h (Law 14 window): proceed with assumptions, freeze, or split. **Max 2 clarification rounds** without arbiter — third round = mandatory escalation (P-01.10).

**Fast Track Delegation & Post-Audit (Law 1 · P-01.8 — amended 2026-08-31 Axis 4):** Fast Track 🟢 is **fully delegated** to the competent room Lead: `gtw-intake-reformer` → single room lead → delivery (no per-task brd-ceo hop). This removes the brd-ceo bottleneck at S1 for trivial reversible work. Guard: `gtw-dispatcher` runs a **weekly post-audit** over the batch log `hq/brain/cortex-decisions.md` (fast-lane batch entries) and flags any misclassification to `brd-ceo` within 3 turns; misclassified Fast → immediate promotion + L2 for gateway. No quality gate / evidence / memory step is ever skipped — only redundant management hops collapse.
