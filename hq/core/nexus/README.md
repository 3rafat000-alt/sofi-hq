# `hq/core/nexus/` — The Registry Nexus

> The **single official interface** between the constitution and the runtime. This is where the
> **Law 12 Registry Invariant** lives: `registry.yaml` is the official registry of 17 rooms ·
> 121 agents; any generation must match it or fail loudly.

Every file here answers **who exists, what they do, and how they connect**. Touching these files
without `brd-ceo` approval is a Law 12 violation.

---

## Files

| File | Purpose | Owner | Update trigger |
|------|---------|-------|----------------|
| `registry.yaml` | **THE official registry** — 17 rooms · 121 agents (Law 12) | `knw-lead` | every new agent / room |
| `personas.yaml` | Arabic names + roles per agent (public-facing) | `knw-lead` | every new agent |
| `pipeline.yaml` | **S1→S6 production line** — stages + lead + gate + output | `str-lead` | every pipeline change |
| `gates.yaml` | **G0..G8 + DFR** (Design-Freeze Review) — per-gate criteria | `qa-lead` + `arc-lead` | every gate change |
| `routing.yaml` | Model + effort + budget per agent (P-12 Token Economy) | `gtw-dispatcher` | every new agent |
| `mcp-routing.yaml` | **27 MCP servers · 100% local** — room distribution + 6 binding rules | `gtw-dispatcher` | every new server |
| `models.yaml` | LLM model selection per task class (workhorse / gatekeeper) | `gtw-dispatcher` | every model change |
| `room-priority.yaml` | **T0..T4 priority tiers** — execution order + escalation rules | `gtw-dispatcher` | every priority change |
| `skill-routing.yaml` | Skill → room → lead map (who owns which skill) | `knw-lead` | every new skill |
| `rccf-registry.yaml` | **Central RCCF ticket tracker** (Audit-ALL) | `brd-chief-of-staff` | every RCCF |
| `bus/` | Ticket bus implementation (transport layer) | `gtw-dispatcher` | (reserved for future) |

---

## The binding artifact: `registry.yaml`

> **Source of truth for Law 12.** Every `.opencode/agent/*.md` must 1:1 match a row here. Every
> `hq/core/domain/rooms/<room>/agents/<name>/` capsule must exist for every row. The 4 constitutional
> guards enforce this on every commit.

**Schema (R3.1):**

```yaml
meta:
  total_rooms: 17       # bumped to 16/17/18 only on owner order
  total_agents: 121     # bumped by exactly +1 per new agent

- code: 00-boardroom    # room identifier (NN-name)
  tier: T0              # T0 / T1 / T2 / T3 / T4
  name_en: Boardroom    # public name
  prefix: brd           # agent name prefix (e.g. brd-ceo, brd-cto)
  role: <one-line>      # purpose
  agents:
    - { name: ceo, skills: [...] }    # 1+ agents, each with kebab-case name
```

**Currently:** 17 rooms · 121 agents (see `meta:` block at top of `registry.yaml`).

---

## The flow: 4 protocols that read this directory

| Protocol | File | What it does |
|----------|------|--------------|
| **P-01** | `protocols.md:P-01.2` | 3-lane proportional flow reads `routing.yaml` |
| **P-09** | `protocols.md:P-09` + `kpi-thresholds.md` | quality gates read `gates.yaml` |
| **P-11** | `tooling/registry_guard.py:1` | guard reads `registry.yaml` and `.opencode/agent/` |
| **P-13** | `protocols.md:P-13` | gate sequence reads `pipeline.yaml` + `gates.yaml` |

---

## How to add a new entry here

**Add a new agent** (the most common change):
1. Write `hq/core/domain/rooms/<room>/agents/<name>/{capabilities,senses,memory}.yaml`
2. Write `.opencode/agent/<name>.md` (frontmatter + identity + skills + constraints + handoff)
3. Add row to `registry.yaml` under the correct room block
4. Add persona block to `personas.yaml` (Arabic name + role)
5. Add routing block to `routing.yaml` (model + effort + budget)
6. Bump `meta.total_rooms` / `meta.total_agents` if needed
7. Bump `hq/core/tooling/registry_guard.py:20` (SKILLS_BASELINE) + `count_sync.py:23` (AGENTS_HDR_REQUIRED)
8. Bump `AGENTS.md:62,256` + `room-priority.yaml:11`
9. Update room charter `Agent count:`
10. Add to `.opencode/skills/INDEX.md` if new skill
11. Record ADR in `hq/brain/cortex-decisions.md` + SES in `hippocampus-sessions.md`
12. Commit atomically — pre-commit enforces all 4 guards

**Add a new room** (requires `brd-ceo` approval):
1. Add `- code: NN-<name>` block to `registry.yaml`
2. Create `hq/core/domain/rooms/<room>/{charter.md, agents/}` directory tree
3. Add tier to `room-priority.yaml`
4. Update `personas.yaml` + `routing.yaml` + `mcp-routing.yaml` + `skill-routing.yaml`
5. Bump `meta.total_rooms`
6. Update `context-map.yaml` (per `hq/core/domain/README.md`)
7. ADR in CORTEX

---

## The bus (`nexus/bus/`)

> Reserved directory for ticket bus implementation. Currently empty. The **Strict JSON Handoff
> Scheme** (P-02) lives in `protocols.md:P-02` — see also `nexus/registry.yaml` for the bus
> contract. Future implementations: Redis streams, RabbitMQ, or in-process (Law 17 keeps the
> ticket `note` ≤ 280 chars).

---

## See also

- [`hq/core/README.md`](../README.md) — parent
- [`hq/core/tooling/README.md`](../tooling/README.md) — 4 constitutional guards
- [`hq/core/domain/`](../domain/README.md) — DDD rooms + context-map
- [`hq/brain/`](../../brain/README.md) — CORTEX decisions + HIPPOCAMPUS sessions + AMYGDALA incidents
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — supreme law
