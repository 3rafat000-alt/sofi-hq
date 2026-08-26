# Knowledge Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 13-knowledge
**Code:** knw
**Room lead:** `knw-lead`

---

## | Identity

**Purpose:**
Knowledge management, documentation, institutional memory, reflection

**Agent count:** 6

---

## | Agent Roster

- `knw-lead` — lead
- `knw-brain-query` — brain-query
- `knw-doc-writer` — doc-writer
- `knw-historian` — historian
- `knw-memory-curator` — memory-curator
- `knw-reflector` — reflector

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Document major decisions
2. Organize knowledge
3. Answer agent inquiries
4. Reflect and review lessons learned
5. Update CORTEX

---

## | Connected Rooms

All rooms

---

## | Gate Ownership

**My stage in production line v2:** supports all stages — CORTEX documentation at closures — full map at `nexus/gates.yaml#stage_map`.

All stages (support)

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

- **Room playbook:** `knw-brain-write` + `skill-forge` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **External room skills:** `skill-creator` · `docx` · `pdf`⚠️High · `pptx` · `xlsx` · `doc-coauthoring`
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Knowledge Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.
