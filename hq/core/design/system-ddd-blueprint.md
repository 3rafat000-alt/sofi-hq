# System DDD Blueprint — the strict structural blueprint per Domain-Driven Design

> **Purpose:** restructure the SOFI system so that rooms, agents, skills, and tools become true domain entities inside strictly bounded contexts, with layers of clear dependency, encapsulated capsules, and documented contracts — no scattering, no leakage.
> **Date:** 2026-08-25 · **Authority:** owner directive · **Status:** approved design for phased execution (no code before the owner's signature — the DFR gate)
> **Home:** `hq/core/design/system-ddd-blueprint.md` — this file is the governing source; any conflict with older documents is interpreted through it.

---

## 1) Governing principles (merging DDD with SOFI's 13 laws)

| DDD Principle | Its embodiment in SOFI |
|----------|----------------|
| Ubiquitous Language | One unified Arabic–English language: room/agent names are fixed technical identifiers, and the governance prose is maintained in English (Law 13) |
| Bounded Contexts | Every room = a bounded context with a single owner per concept — Law 2 (Room Isolation) |
| Context Mapping / Contracts | provides/requires contracts + the ticket bus — Law 3 (Hierarchical Handoff) |
| Aggregate Root | The room is the aggregate root; the agent is an entity inside it; no agent exists outside its mother room |
| Dependency Rule | Presentation depends on Application, which depends on Domain; infrastructure serves through Ports and never sneaks into the domain |
| Encapsulation | The agent capsule: its inputs, memory, and capabilities live in one closed home |
| Design Before Code | No execution before this blueprint is approved and frozen — production-line stages S2/S3 |

---

## 2) The Ubiquitous Language — core entities

| Entity | Precise definition | Example |
|--------|---------------|------|
| **Room** | An Aggregate Root: a bounded context owning exactly one institutional mission, one Lead, and one charter | `05-backend` |
| **Agent** | An entity inside a room: an executive persona with identity, role, and authority boundaries; crosses to another room only via contract | `bck-api-engineer` |
| **Skill** | An invocable cognitive capability owned by a single room, with its invocation documented in its agent's definition | `sec-threat-model` |
| **Tool** | An external execution capability (an MCP server or script), licensed to a room through a vetting gate, invoked by name only | `Context7` · `port-agents.mjs` |
| **Ticket** | A value object/event passing between contexts over the bus — the only permitted form of cross-room communication | `TKT-SAKK-FE-001` |
| **Gate** | A domain service: a mandatory checkpoint before crossing a state | `gate-3` (design freeze) |
| **Evidence** | A value object: `file:line`, `exit code`, or screenshot — without evidence the delivery does not exist (Law 4) | `Caddyfile:42 · exit 0` |

**Strict ownership rule:** every skill and tool carries a single `owner-room` in its registry entry. Whoever does not find it in their room's registry must not invoke it — requesting it from another room happens via a ticket through the contract.

---

## 3) The four layers (Layered Architecture) and the dependency rules

```
┌──────────────────────────────────────────────────────────────┐
│  PRESENTATION — the presentation layer                        │
│  What the operator and tools see: generated runtime adapters  │
│  .kilo/agent (mirror) · .opencode/agent (load adapters)       │
│  opencode.json (MCP wiring) · identity/public-readme          │
├──────────────────────────────────────────────────────────────┤
│  APPLICATION — the application layer (orchestration)          │
│  Workflow, not logic: intake gateway, classification, routing │
│  RCCF work orders · gate runner · ticket bus                  │
│  Agent build line (porter v2) · deploy flow deploy.sh         │
├───────────────────────────────────┬──────────────────────────┤
│  DOMAIN — the domain layer (heart)│  INFRASTRUCTURE — infra  │
│  hq/core/domain/                  │  (serves through ports)  │
│  rooms/<15 contexts>:             │  hq/engine (Caddy deploy)│
│   charter · agent capsules        │  hq/brain + the archive  │
│   capabilities (skills/tools)     │   (fingerprint stores)   │
│  shared-kernel: identity·terms    │  actual MCP servers      │
│  context-map · contracts          │  training corpus         │
│                                   │  backups · tooling       │
└───────────────────────────────────┴──────────────────────────┘
```

**The binding dependency rule (downward only):**
1. Presentation knows Application, and Application knows Domain — the reverse is forbidden.
2. The domain imports nothing from infrastructure; infrastructure implements "ports" defined by the application layer.
3. Horizontal communication between two contexts in the domain layer is **textually forbidden** — it happens exclusively through contracts in `context-map` and executes over the bus in the application layer (this is Laws 2 and 3 rendered as engineering).

| Layer | Role in brief | Home |
|--------|--------------|-------|
| **Domain** | Who we are and what we own: rooms, agents, capabilities, contracts, rules of the game — zero dependence on operational tooling | `hq/core/domain/` |
| **Application** | How the work cycle is managed: intake → classification → work order → gates → delivery → memory | `hq/core/application/` |
| **Infrastructure** | How things practically happen: deployment, storage, tool servers, schools of knowledge | `hq/engine/` + `hq/core/tooling/` + `hq/training/` |
| **Presentation** | How everything is presented to the engine and the operator: generated adapters + public identity | `.opencode/` · `.kilo/` · `identity/` |

---

## 4) The complete target tree

```
SOFI/
├── AGENTS.md                          ← the constitution (untouched — referenced through existing bridges)
├── opencode.json                      ← MCP wiring and tool servers (Presentation wiring)
├── identity/                          ← public identity (Presentation)
│
├── hq/
│   ├── core/
│   │   ├── domain/                    ★ the domain layer
│   │   │   ├── shared-kernel/          what everyone shares with no private ownership:
│   │   │   │   ├── glossary.md          the ubiquitous language (§2)
│   │   │   │   ├── evidence-rule.md     the unified evidence law
│   │   │   │   ├── envelope.md          the unified message/delivery shape
│   │   │   │   └── identity.md          the reference SOFI identity
│   │   │   ├── context-map.yaml        the context map: who addresses whom and under which contract
│   │   │   └── rooms/                  the 15 bounded contexts:
│   │   │       ├── 00-boardroom/
│   │   │       │   ├── charter.md            the room charter (from room_charters)
│   │   │       │   ├── contracts/
│   │   │       │   │   ├── provides.yaml     what this room offers the system
│   │   │       │   │   └── requires.yaml     what it needs from others (by name, not by source)
│   │   │       │   ├── capabilities/         the room's capability registry (source of truth):
│   │   │       │   │   ├── skills.yaml        every skill: name · owner-agent · when
│   │   │       │   │   └── tools.yaml         every tool: name · type · license · vetting gate
│   │   │       │   └── agents/               agent capsules ↓ §5
│   │   │       ├── 01-strategy/ … 14-gateway/
│   │   ├── application/               ★ the application layer
│   │   │   ├── gateway/                intake-reformer flow: classification → routing
│   │   │   ├── rccf/                   the work-order template and its lifecycle
│   │   │   ├── gates/                 the gate runner (checklists referenced here)
│   │   │   ├── bus/                    ticket-schema · escalation (the inter-context bus)
│   │   │   └── build/                  porter v2: capsules → presentation adapters
│   │   ├── nexus/                      official registries (registry/gates/models/personas/routing)
│   │   ├── standards/                  engineering standards (remain as-is)
│   │   ├── tech_templates/ · templates/ · tooling/
│   │   ├── structure-standard.md · system-state-current.md
│   │   └── design/                     this blueprint and design documents
│   ├── brain/                          organization memory repository (Repository — archived with its primer)
│   ├── engine/                         deployment infrastructure (sites/ · php-fpm/ · scripts/)
│   └── hq/training/                       the reference schools of knowledge
│
├── projects/<slug>/                    a project = an independent bounded context with its own memory (brain/) — the Law 7 pattern
│
├── .opencode/                          Presentation runtime:
│   ├── agent/*.md                      load adapters generated from domain capsules (never hand-edited)
│   └── skills/                         capability installation area (INDEX generated from room manifests)
├── .kilo/                              generated mirror + operator commands (command/)
├── caddy/                              the temporary /etc bridge
└── backups/                            encrypted — untouched
```

---

## 5) Agent capsule anatomy — professional encapsulation

Every agent = one closed folder of four fixed files (no deep trees — discipline):

```
rooms/05-backend/agents/bck-api-engineer/
├── agent.md          Identity: full frontmatter (name/description/mode/model) + purpose, role, responsibilities
├── senses.yaml       Its senses: what it receives — events/tickets/files/commands it runs, and its allowed read sources
├── memory.md         Its private memory: live working notes + pointers into repository memories (never copies from them)
└── capabilities.yaml Its capabilities: skills[] and tools[] **by name only**, and they must exist in its room's manifests
```

**Real-world example (excerpt):**

```yaml
# senses.yaml — bck-api-engineer
listens:
  - tickets: { from: bck-lead, type: RCCF-task }
  - files:    [ projects/*/backend/**/*.php ]     # reads within its task scope only
forbidden-inputs: [ direct-owner-chat, other-room-tickets ]
```

```yaml
# capabilities.yaml — bck-api-engineer
skills: [ bck-feature-build, sec-mcp-vetting:read-only ]
tools:  [ Context7, DeepWiki, Dart-Flutter:no ]
note: every item here must be a line in rooms/05-backend/capabilities/*.yaml, otherwise it is a leak.
```

**The strict capsule rules:**
1. The agent sees only its own capsule + shared-kernel + its room's contracts — all other paths fall outside its read scope (W1: the audit applies the same "suspect" logic).
2. `capabilities.yaml` ⊆ `rooms/<room>/capabilities/*` always — the verifier (build/porter) fails the build on any orphan element.
3. `memory.md` holds pointers, not content: permanent memories live in their repositories (hq/brain · projects/*/brain) — preventing 106 scattered memories.

---

## 6) Binding skills and tools to the room (leak prevention)

- **The sole ownership source:** `rooms/<room>/capabilities/{skills,tools}.yaml`.
- `.opencode/skills/INDEX.md` becomes **generated**: built by merging the manifests of the 15 rooms (the total count of 106 is preserved as a verification constraint in the registry).
- The MCP tool server (`opencode.json`) is a general-purpose infrastructure license; **who uses it and why** is decided by each room's tools.yaml — a tool with no owner in the registry is forbidden to invoke.
- A skill genuinely shared between two rooms? Either it moves into `shared-kernel` by documented decision, or it remains owned by one room while the other invokes it **through a contract** (requires) — never duplicated copies.

---

## 7) Contracts and the Context Map

```yaml
# context-map.yaml — registration pattern (excerpt)
05-backend:
  provides: [ api-contract, migrations-runbook ]
  requires: [ ui-spec from 03-design, data-model from 08-data ]
  talks-to: [ 10-quality (tickets), 09-security (gates) ]
  forbidden: [ direct chat with 06-frontend ]   # via 04/brd-ceo exclusively — Law 3
```

- `provides/requires` use the official names from the ubiquitous language — no file paths inside contracts (a contract is an interface, not an implementation).
- The bus `application/bus/` is the sole executor of cross-context communication: inbound ticket → outbound ticket → evidence.
- Every change to any contract passes through a gate and gets its decision recorded — contracts are frozen between gates.

---

## 8) Three-layer memory (Repository Pattern)

| Level | Home | Who writes |
|---------|-------|-------------|
| Capsule memory | `agents/<x>/memory.md` | The agent itself — live notes and pointers |
| Organization memory | `hq/brain/` (primer + fingerprint archive) | brd-ceo/knw only — cross-project decisions |
| Project memory | `projects/<slug>/brain/` | The project team through its Lead — Law 7 literally |

**Rule:** no agent writes directly into organization memory, nor into the memory of a project it does not belong to — promotion between layers happens by documented CEO decision (Law 7 + leak prevention).

---

## 9) Mapping current assets → target (migration map)

| Today's asset | Target home | Migration method |
|-------------|----------------|--------------|
| `hq/core/room_charters/*.md` (15) | `domain/rooms/*/charter.md` | move + update links |
| `.opencode/agent/*.md` (106 source files) | `domain/rooms/*/agents/*/agent.md` | gradual move (P2) + adapters generated |
| `.opencode/skills/*` (106) | remains the installation area + ownership recorded in manifests | P3: generate INDEX from the registries |
| `nexus/{registry,routing,gates,personas,models,pipeline}.yaml` | `nexus/` (official registries serving the domain) | stay — they are the counting and verification source |
| `gate_checklists/` | `application/gates/` | reference move |
| `contracts.md` + `bus/*` | `context-map.yaml` + `application/bus/` | documented decomposition |
| `standards/` · `tech_templates/` · `tooling/` | their current places in core | no movement |
| `hq/engine/` · `hq/training/` · `hq/brain/` | Infrastructure | no movement |
| `.kilo/command/` · kilo.jsonc · node_modules | Presentation/harness | no movement |

**Invariants that must not break during migration:**
1. The registry.yaml counter = number of generated adapters = always 106 (porter fails loudly on any mismatch).
2. `/etc/caddy` and the live publishing chain remain unaffected (engine sits outside P1–P4 scope).
3. `projects/sakk/**` is fully protected — a parallel session is working on it right now.
4. Compatibility bridges (the hq/core/hq/brain/training symlinks + the caddy bridge) remain until migration completes and the owner signs acceptance.

---

## 10) Phased execution plan (nothing executes before your signature)

| Phase | What it does | Exit gate |
|---------|-----------|--------------|
| **P0 Freeze** | Approve this blueprint with your comment ("approved") + a safety commit of the current tree | a documented approval line |
| **P1 Structure** | Create the `domain/` skeleton: the 15 empty rooms with their templates + shared-kernel + an initial context-map | check: every context has charter/contracts/capabilities placeholders |
| **P2 Capsules** | Migrate agents in batches (the 15 leads first, then the rest) + porter v2 generates the adapters | 106/106 generated and matching + a healthy counter |
| **P3 Capabilities** | Skill/tool manifests per room + INDEX generation + tool licensing | zero orphan skill and zero ownerless tool |
| **P4 Contracts & Closure** | Full context-map + system-state/public-readme updates + reference sweep + final report | checks: zero broken references · zero capability leaks · validate the deployment |

Every phase: archive before moving (restore.sh ready) · a file-lock log · a sub-report — the same discipline as the purge operations.

---

## 11) Risks and protections

| Risk | Protection |
|-----|-------|
| The engine reads only flat files (.opencode/agent) | Adapters are always generated — capsules are the source, adapters are the view (P2 proves it before rollout) |
| Breaking constitution references during migration | The existing symbolic bridges remain until P4, and the final sweep comes after your signature |
| Bloat of 106 capsule folders | The capsule is 4 fixed files — no deep trees, expected total size < 3MB |
| Conflict with the parallel sakk session | Zero touches to projects/** in every phase + a safety commit before P1 |
| Losing the official agent counter | The invariant of 106 in registry.yaml judges every generation (loud failure, never silence) |
