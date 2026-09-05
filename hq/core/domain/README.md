# `hq/core/domain/` — DDD Domain Layer

> The DDD domain layer. Every bounded context (room) has its own **charter** + **capsules** + a
> shared **context-map** that defines the single official interface between rooms (Law 2).

This directory is **not** editable casually — every change must pass through a gate and be recorded
in CORTEX. Contracts are **frozen between gates**.

---

## The reading rules (from `context-map.yaml:8-10`)

```
provides = what the room commits to produce for the system
requires = what it needs by name, not by source
talks-to = legitimate neighbors, via tickets only
forbidden = explicit prohibitions
```

Any communication outside what is defined here = **leakage** (Law 2 violation → L3).

---

## Layout

```
domain/
├── context-map.yaml                ← THE single official inter-room interface (Law 2)
└── rooms/                          ← 17 rooms
    ├── 00-boardroom/
    │   ├── charter.md              ← room identity + SOP + connected rooms + gate ownership
    │   └── agents/
    │       ├── brd-ceo/{capabilities,senses,memory}.yaml
    │       ├── brd-cpo/...
    │       └── brd-arbiter/...
    ├── 01-strategy/
    ├── 02-research/
    ├── 03-design/
    ├── 04-architecture/
    ├── 05-backend/
    ├── 06-frontend/
    ├── 07-mobile/
    ├── 08-localization/
    ├── 09-security/
    ├── 10-quality/                 ← 10 testers
    ├── 11-devops/
    ├── 12-observability/
    ├── 13-knowledge/
    ├── 14-gateway/
    ├── 15-warroom/                 ← P0 incident command
    └── 16-innovation/              ← sandbox + ML
```

---

## The context-map (Law 2)

> Source: `context-map.yaml` — single source of truth for **who talks to whom**.

The map has a versioned `boundary note` at the top (current: **v1.1** — added 2026-09-05 in
Audit-ALL). The 3 critical boundaries are:

1. **04 OWNS api-design + data-design** — sole designer of OpenAPI + ERD
2. **09 REVIEWS/VETO** — security aspects of every design/release — via gates only — never designs APIs
3. **10 VERIFIES** — testability + contract-conformance + DFR tokens — via tickets only — never fixes code or designs APIs

**No overlap:** design ownership is 04, security gate is 09, quality gate is 10 — all via tickets only.

---

## Per-room: charter

Every `rooms/<room>/charter.md` follows this template:

```markdown
# <Room Name>
> ⚡ Created/updated YYYY-MM-DD — context note

**Room:** NN-name
**Code:** <prefix>
**Room lead:** <lead-agent>

---

## | Identity
**Purpose:** <one-line>
**Tier:** T0/T1/T2/T3/T4
**Stage:** <S1..S6> or N/A

**Agent count:** <N>

## | Agent Roster
- <agent> — <role>  (one per line)

## | Standard Operating Procedure (SOP)
1. <step>
2. <step>

## | Connected Rooms
- Talks to: ...
- Requires: ...
- Provides: ...

## | Gate Ownership
<which gates this room owns / co-signs>

## | Handoff Protocol
<how outputs flow upward>

## | Skills
- **Room playbook:** <name>
- **Shared:** sofi-evidence, sofi-handoff
```

---

## Per-agent: capsule (3 files)

Every `rooms/<room>/agents/<agent>/` has exactly 3 files:

```
capabilities.yaml    # tools whitelist + skills reference
senses.yaml          # what inputs this agent accepts + escalation rule
memory.md            # pointers to org + project memory stores
```

These are **the** capsule contract (Law 12). The `registry_guard` enforces that every agent in
`registry.yaml` has a capsule here — and every capsule here has an agent file in `.opencode/agent/`.

---

## How to add a new room (or expand an existing one)

**Add a new agent:**
1. Write `.opencode/agent/<name>.md`
2. Create the 3 capsule files
3. Update `registry.yaml` (add row under the room block + bump `meta.total_agents`)
4. Update `personas.yaml` (Arabic name + role)
5. Update `routing.yaml` (model + effort + budget)
6. Update `mcp-routing.yaml` if MCP access changes
7. Update room `charter.md` (Agent count + roster)
8. Bump `AGENTS.md:62,256` + `room-priority.yaml:11` + `count_sync.py:23`
9. ADR + SES in CORTEX + HIPPOCAMPUS
10. Commit — pre-commit enforces all 4 guards

**Add a new room (requires `brd-ceo` approval — owner order recorded in CORTEX):**
1. Create `rooms/<NN>-<name>/{charter.md, agents/}` tree
2. Add `- code: NN-<name>` block to `registry.yaml` + bump `meta.total_rooms`
3. Update `context-map.yaml` (provides / requires / talks-to / forbidden for the new room)
4. Update `room-priority.yaml` (which tier + rooms list)
5. Update `mcp-routing.yaml` (add room to per-room MCP distribution)
6. Update `personas.yaml` + `routing.yaml` + `skill-routing.yaml`
7. ADR + context map version bump (Law 13 — old ← new map)

---

## See also

- [`hq/core/README.md`](../README.md) — parent
- [`hq/core/nexus/registry.yaml`](../nexus/registry.yaml) — the registry
- [`hq/core/standards/ddd-capsule.md`](../standards/ddd-capsule.md) — DO/DON'T table
- [`hq/core/context-map.yaml`](./context-map.yaml) — the interface map
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md)
