# Article 11 — Intake & Orchestration (the hierarchy protocol)

Foundation: serves Teaching II (Hierarchical Flow) and Teaching IV (Token Economy). Read `hq/core/constitution-master.md` and `01-work-order.md` first.

> Coordination model set by owner order 2026-07-16: **live hierarchy**. The flat "wear-the-hierarchy / leaf-spawn one hop" model is retired.

## The protocol — live hierarchy

Every delegation follows the chain of command, each hop via Task with an RCCF Work Order:

```
user → gtw-intake-reformer → brd-ceo → room Lead → room agents
```

- **CEO delegates to Leads.** brd-ceo spawns room Leads via Task. The CEO never spawns a specialist directly and never executes work (CEO Covenant).
- **Leads delegate to their own agents.** Each Lead spawns its own room's agents via Task. A Lead never spawns another room's agent (Room Isolation Law) — cross-room needs go Lead → Lead.
- **Agents spawn no one.** A specialist executes and reports back to its Lead. Delegation by a specialist → Level 2.
- **Parallelism.** brd-ceo may spawn multiple Leads in one message; a Lead may spawn multiple of its agents in one message — always behind frozen input (Article 10).
- **RCCF bindings.** Every spawn carries Role·Context·Command·Format (Article 01). No spawn without all four.

## Return path

```
agent → its Lead (merge + evidence review) → brd-ceo (consolidation) → user
```

Hierarchical handoff is mandatory (Protocol 02). No agent delivers directly to the user (P-01.5).

## Intake flow

```
raw human input → gtw-intake-reformer (the translator) → structured ticket → brd-ceo
```

`gtw-intake-reformer` — the semantic gateway, referred to as "the translator" — refines raw human intent into structured work: project, gate, agent, intent. The CEO then produces the RCCF Work Order and delegates to the room Leads. Full roster: 106 agents across 15 rooms (`hq/core/nexus/registry.yaml`).
