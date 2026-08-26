# SOFI HQ

> **An AI enterprise organization** — a complete, constitution-governed multi-agent software company:
> **15 rooms · 114 agents · 16 binding laws · 9 gates · an S1→S6 production line.**
>
> SOFI HQ is not a traditional application you "run". It is an *operating organization* for AI coding
> harnesses: every request enters through a single gateway, gets classified by criticality, and flows
> through specialized agent rooms under binding laws — with evidence discipline, quality gates,
> memory isolation, and incident runbooks built in.

---

## Table of Contents

1. [Overview](#overview)
2. [How It Works](#how-it-works)
3. [Repository Structure](#repository-structure)
4. [The Governance Core](#the-governance-core)
5. [Tech Stack](#tech-stack)
6. [Requirements & Dependencies](#requirements--dependencies)
7. [Installation & Setup](#installation--setup)
8. [Running & Usage Examples](#running--usage-examples)
9. [Key Subsystems](#key-subsystems)
10. [Extending the System](#extending-the-system)
11. [Developer Guidelines](#developer-guidelines)

---

## Overview

SOFI HQ models a real software company as an agent hierarchy:

| Concept | Implementation |
|---|---|
| **Rooms** | 15 departments (`00-boardroom` → `14-gateway`), each with its own charter |
| **Agents** | 114 specialist agents defined as Markdown specs in `.opencode/agent/` |
| **Constitution** | `AGENTS.md` at the root — 16 binding laws, violation levels L1–L4 |
| **Production line** | Six stages S1–S6: idea → data/contract design → experience → backend → unified UI → shield & production |
| **Gates** | 0–8 quality gates; artifacts cannot skip stages |
| **Memory** | Organization memory (`hq/brain/`) and per-project memory (`projects/<slug>/brain/`) are strictly separated |
| **Publishing layer** | A live Caddy-based engine (`hq/engine/`) serving approved sites |

The current operating baseline is a **zeroed system**: all historical memory was purged by owner
order on 2026-08-26. Memory folders exist with `ZEROED.md` markers and start fresh from that date.
Amendment (3) on the same date added two dedicated architects to room 04 (`arc-security-architect`,
`arc-performance-architect`) and wired three scope rules into charters: interaction-behavior
ownership in Design, state ownership for the merged S5 Flutter/Dart team, and mandatory
builder-authored tests verified by Quality (no duplicate test agents). Amendment (4) added the
**Visual Research Protocol 18** + visual feeding system: `res-visual-pattern-scout` (room 02),
`dsn-competitive-ui-analyst` + `dsn-arabic-ux-specialist` (room 03, RTL signature gates DFR),
three skills (`mobbin-scraper`, `design-system-extractor`, `rtl-mirror-validator`), a binding
platform list in `uiux-standard.md`, and pattern documentation under
`projects/<slug>/brain/visual-patterns/`.

### The 15 Rooms

| # | Room | Lead | Role |
|---|------|------|------|
| 00 | Boardroom | `brd-ceo` | CEO + CPO/CTO/CQO/CSO + chief-of-staff + arbiter (advisory board) |
| 01 | Strategy | `str-lead` | Product strategy, PRD, roadmaps, Agile flow tracking |
| 02 | Research | `res-lead` | Market/user/technical research · visual pattern scouting (Mobbin/PageFlows) |
| 03 | Design | `dsn-lead` | UX flows, design systems, mockups, interaction-behavior specs · competitive UI analysis · Arabic/RTL sign-off gates DFR |
| 04 | Architecture | `arc-lead` | DDD architecture, API contracts, review · secure-design & performance-by-design architects |
| 05 | Backend | `bck-lead` | Laravel domain engineering |
| 06 | Frontend | `fnt-lead` | Web interfaces (Flutter R2 unified standard) |
| 07 | Mobile | `mob-lead` | Flutter mobile engineering |
| 08 | Data | `dat-lead` | Schemas, migrations, analytics, privacy officer |
| 09 | Security | `sec-lead` | AppSec, threat modeling, license/IP gate |
| 10 | Quality | `qa-lead` | Test architecture, automation, verdicts |
| 11 | DevOps | `ops-lead` | CI/CD, deployments, sandbox executor |
| 12 | Observability | `obs-lead` | Monitoring, KPIs, incident analysis |
| 13 | Knowledge | `knw-lead` | CORTEX decisions, lessons, historian |
| 14 | Gateway | `gtw-dispatcher` | Intake reforming, lane classification, routing |

Full registry: [`hq/core/nexus/registry.yaml`](hq/core/nexus/registry.yaml) — any generation or
migration must match it exactly or fail loudly (**Law 12 — Registry Invariant**).

---

## How It Works

Every request follows one mandatory lifecycle (**Law 1 — Proportional Flow**):

```
 User request
      │
      ▼
 gtw-intake-reformer ── ambiguity ≥20%? ──► clarification card (1–3 questions), halt
      │ Law 16 loop until clarity
      ▼
 Lane classification (gtw-dispatcher + str-gate0-classify)
   🟢 Fast       reads/trivial fixes        → intake ← room lead ← delivery
   🟡 Standard   feature-sized work         → intake ← CEO ← leads ← agents ← lead ← CEO
   🔴 Critical   money/security/schema/prod → full flow + Board + all gates, zero shortcuts
      │
      ▼
 RCCF work order issued (Law 5 — no execution without one)
      │
      ▼
 Room(s) execute under T0–T4 priority tiers (nexus/room-priority.yaml)
      │  · evidence required: file:line + exit codes (Law 4)
      │  · quality gate review before anything ships (Law 8)
      ▼
 Lead reviews → brd-ceo delivers → user (simple-Arabic summaries, Law 11)
```

Hard guarantees: intake is sovereign on every track · lanes only ascend, never descend ·
money/security/production/schema work is always Critical · cross-room contact happens only through
documented contracts and the ticket bus (**Law 2**).

---

## Repository Structure

```
SOFI/
├── AGENTS.md                  # The constitution — 16 binding laws + boot sequence (read first)
├── opencode.json              # Harness config: default agent = gateway, MCP servers, LSP, permissions
├── identity/                  # System identity documents
│   ├── sofi-system-identity.md
│   └── public-readme.md
│
├── hq/
│   ├── core/                  # ALL governance
│   │   ├── constitution-master.md        # Supreme law, detailed edition
│   │   ├── constitution_articles/        # Individual constitutional articles
│   │   ├── protocols.md                  # 18 operational protocols (incl. Protocol 10 emergencies · 18 visual research)
│   │   ├── contracts.md                  # Inter-room contract deeds
│   │   ├── domain/                       # DDD layer: context-map.yaml + rooms/<room>/ capsules
│   │   │   └── rooms/<room>/             # charter.md · agents/<name>/ capsules (senses/capabilities/memory)
│   │   ├── nexus/                        # Machine-readable routing brain
│   │   │   ├── registry.yaml             # ⭐ official registry: 15 rooms · 114 agents
│   │   │   ├── routing.yaml              # model routing grid (aliases, budgets)
│   │   │   ├── pipeline.yaml             # S1–S6 stage/gate machine
│   │   │   ├── gates.yaml                # gate map & stage_map
│   │   │   ├── room-priority.yaml        # ⭐ T0–T4 priority tiers + escalation order
│   │   │   └── bus/                      # ticket bus
│   │   ├── gate_checklists/              # gate-0 … gate-8 checklists
│   │   ├── standards/                    # stacks-tech · devops · deploy · pipeline-production-line
│   │   │                                 # reporting-cadence · kpi-thresholds (K1–K17)
│   │   ├── runbooks/                     # incident-response.md — R1–R4 SEV playbooks
│   │   ├── tech_templates/               # ddd-capsule-protocol.md · auth-rbac-stack
│   │   ├── templates/                    # document templates (project brain etc.)
│   │   ├── tooling/                      # Python/Node utilities (see below)
│   │   ├── design/                       # system-ddd-blueprint.md
│   │   ├── structure-standard.md         # canonical naming + legacy path map
│   │   └── system-state-current.md       # ⭐ reference operating state (amendments log)
│   │
│   ├── brain/                 # Organization memory — ZEROED 2026-08-26 (ZEROED.md marker)
│   ├── training/              # Training guides: rooms-guide · file-discipline · playbooks
│   └── engine/                # Live publishing layer
│       ├── Caddyfile          # primary config (snippets + 404 guard + import)
│       ├── sites/<domain>.caddy          # one file per domain
│       ├── php-fpm/           # pool definitions (+ disabled/)
│       ├── cloudflare/        # DNS/tunnel assets
│       ├── OPERATIONS.md      # infrastructure runbook
│       └── scripts/           # validate.sh · deploy.sh · status.sh · diff-live.sh · bootstrap-live.sh
│
├── memory_index/              # Memory primer location — ZEROED 2026-08-26 (path locked by articles)
├── projects/<slug>/           # Actual software projects (gitignored here — private code)
│   └── <slug>/brain/          # Project memory: CONTEXT · DECISIONS · HANDOFFS · LESSONS
│
├── .opencode/                 # Operating layer — source of truth for agents & skills
│   ├── agent/*.md             # 114 agent definitions (legal spec source)
│   └── skills/                # 109 skill packages
│
└── .kilo/                     # Mirror layer: generated agent mirrors + commands + local config
```

---

## The Governance Core

### The 16 Binding Laws (digest)

| # | Law | One-line essence |
|---|-----|------------------|
| 1 | Proportional Flow | Every request enters via the gateway; depth ∝ criticality |
| 2 | Room Isolation | Rooms never talk directly — contracts + ticket bus only |
| 3 | Hierarchical Handoff | agent → lead → brd-ceo → user; no shortcuts |
| 4 | Evidence Required | `file:line` for changes, exit codes for commands, logs for results |
| 5 | RCCF Mandatory | No execution without a formal work order |
| 6 | Board is Advisory | CEO consults `brd-*`; final call is the CEO's; anti-loop rule after 3 failures |
| 7 | Memory Binding | Org memory vs project memory never mix; promotion needs a CEO decision |
| 8 | Quality Before Speed | No delivery without review; no review without evidence |
| 9 | Chain of Responsibility | Agent owns output · lead owns team · CEO owns system |
| 10 | Direct-on-Project | Work on the main tree; worktrees forbidden |
| 11 | Owner Communication | Owner-facing text = clear simple Arabic; internal docs = English |
| 12 | Registry Invariant | `registry.yaml` must always match reality (15 rooms · 114 agents) |
| 13 | Zero-Randomness | Triple engine for critical work · `## FILE:` path headers · kebab-case naming |
| 14 | Double-Rejection | Same task rejected twice → freeze → binding arbitration ≤24h |
| 15 | License Gate | No dependency merge without recorded license verdict |
| 16 | Smart Clarification | Ambiguity ≥20% → halt and ask 1–3 sharp questions before routing |

Violations escalate L1 (warning) → L2 (mandate) → L3 (freeze) → L4 (system halt).

### Production Line (S1–S6) and Gates

```
S1 Idea & Strategy ──► S2 Data & Contract Design (paper) ──► S3 Experience & Visual System
                                                                            │
                                                        DFR gate ◄──────────┘ (signatures: 09 + 10)
                                                                │ zero code before signature
                              S4 Live Backend Execution ◄───────┘
                                          │ closes only when fully running + security-checked
                              S5 Unified UI (Flutter R2, web+mobile in parallel)
                                          │
                              S6 Shield & Production (qa · ops · obs · knw)
```

Gates 0–8 checklist every transition; Gate-3 collapses only under CEO-authorized Fast-Track;
Gate-8 requires live telemetry, alert↔runbook 1:1 mapping, and postmortems.

### Priority Tiers & Escalation (`nexus/room-priority.yaml`)

| Tier | Rooms | Rule |
|---|---|---|
| **T0 Spine** | 14 · 00 | Always-on; gateway classifies before anything else runs |
| **T1 Paper-first** | 01→02→04+08→03 | No code while a paper artifact is open; exits at frozen schema + OpenAPI + DFR |
| **T2 Execution** | 05 then 06+07 | Backend complete & security-checked before any UI line |
| **T3 Shield** | 09·10·11·12 | Continuous veto power across all tiers |
| **T4 Memory** | 13 | Logs everything; never blocks a stage |

Escalation wins in order: SEV-1 incident → Law-14 arbitration → blocking gate failure → scheduled reporting.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Governance corpus | Markdown + YAML (constitution, charters, registries, pipelines) |
| Agent runtime | OpenCode-compatible harness / Kilo Code VS Code extension |
| Agent specs | Markdown definitions + YAML capsule manifests (senses/capabilities) |
| Tooling scripts | Node.js (ESM) + Python 3 (stdlib-only tools) |
| Skill dependencies | Python package set (`requirements.txt`: lxml, pypdf, playwright, anthropic, mcp, …) |
| Publishing engine | Caddy v2 + PHP-FPM pools + Cloudflare tunnel assets |
| Project stacks (per-project) | Laravel (backend) · Flutter/Dart R2 (web+mobile) · Tailwind CSS · Three.js |
| MCP integrations | Context7 · DeepWiki · Sequential-Thinking · Chrome-DevTools · Playwright · Dart-Flutter · Filesystem-Scoped |

---

## Requirements & Dependencies

| Requirement | Purpose | Notes |
|---|---|---|
| Git | version control | fresh history starts 2026-08-26 |
| Node.js ≥ 18 | tooling + npx-based MCP servers | `port-agents.mjs`, MCP launches |
| Python 3.10+ | guard tools & skills | tooling/* is stdlib-only; skills need requirements.txt |
| OpenCode CLI **or** Kilo Code (VS Code) | running the organization | `opencode.json` is the entry config |
| Caddy v2 + PHP-FPM *(optional)* | live publishing layer | only if you serve real domains |
| Dart SDK *(optional)* | Dart LSP / Flutter MCP | used when working on Flutter projects |

---

## Installation & Setup

```bash
# 1) Clone the clean baseline
git clone https://github.com/3rafat000-alt/sofi-hq.git
cd sofi-hq

# 2) Install skill-level Python dependencies (tooling itself needs nothing)
python3 -m pip install -r hq/core/tooling/requirements.txt

# 3) Install .kilo mirror-layer dependencies (if using Kilo Code)
cd .kilo && npm install && cd ..

# 4) Point the filesystem-scoped MCP at your checkout (one line in opencode.json):
#    "@modelcontextprotocol/server-filesystem", "<absolute-path-to-sofi-hq>"
# 5) Optional — machine-specific paths in opencode.json (dart_mcp_server) can be disabled
#    safely if you do not do Flutter work.
```

No global services are required to *use* the governance system — it activates inside the AI harness
when you open the folder. The publishing engine is opt-in infrastructure.

---

## Running & Usage Examples

### Start the organization (inside OpenCode or Kilo Code)

Opening the folder boots chat exclusively on the gateway (`default_agent: gtw-intake-reformer`).
Just talk to it in natural language:

```
You:   أريد إضافة صفحة تسجيل دخول جديدة للمشروع
Gateway: (classifies) → Standard lane → issues work order → routes to 01-strategy → …
```

Harness modes configured in `opencode.json`:

| Mode | Behavior |
|---|---|
| *(default)* | Chat opens on `gtw-intake-reformer` — mandatory first entry point |
| `plan` | Read-only planning mode — explore/draft without modifying files |
| `build` | Direct execution on the main tree after gateway routing (laws still binding) |

Subagents (room specialists) are invoked hierarchically via Task calls — max depth 6
(`subagent_depth`). You never address rooms directly; the gateway does the routing.

### Regenerate the `.kilo` agent mirrors from the source of truth

```bash
node hq/core/tooling/port-agents.mjs     # .opencode/agent → .kilo/agent mirror sync
python3 hq/core/tooling/count_sync.py    # verify counts match the registry (114 expected)
```

### Run the constitutional path guard (Law 13)

```bash
python3 hq/core/tooling/law13_path_guard.py --help   # checks naming/kebab-case/path headers
```

### Operate the publishing engine

```bash
# add a site: create hq/engine/sites/<domain>.caddy, then:
bash hq/engine/scripts/validate.sh <domain>     # lint the Caddyfile + site file
bash hq/engine/scripts/deploy.sh <domain>       # reload Caddy safely
bash hq/engine/scripts/status.sh               # what is live right now
sudo bash hq/engine/scripts/bootstrap-live.sh   # one-time root bootstrap of the live layer
```

### Verify repository health

```bash
grep -m1 '15 rooms' hq/core/nexus/registry.yaml   # Registry Invariant header (Law 12)
ls hq/core/runbooks/incident-response.md          # incident runbooks present (R1–R4)
cat hq/core/system-state-current.md               # current operating state + amendments
```

---

## Key Subsystems

### Memory Architecture (Law 7) — currently zeroed

| Store | Path | Contents |
|---|---|---|
| Organization memory | `hq/brain/` | CORTEX (decisions) · HIPPOCAMPUS (sessions) · AMYGDALA (incidents) · LESSONS |
| Memory primer | `memory_index/` | retrieval index (path fixed by constitutional articles) |
| Project memory | `projects/<slug>/brain/` | CONTEXT · DECISIONS · HANDOFFS · LESSONS + evidence |

Both org stores carry a `ZEROED.md` marker dated 2026-08-26: all prior content was purged by owner
order together with git history and backups. Everything from that date forward starts fresh.
Recording a new decision recreates the target file under the same name.

### Incident Response (`hq/core/runbooks/incident-response.md`)

Four pre-written runbooks implementing Protocol 10 — no improvisation mid-crisis:

| Runbook | Severity | Trigger examples |
|---|---|---|
| **R1** | SEV-1 Critical | crash · data loss · breach · constitutional violation → freeze, checkpoint, emergency board, blackout, RCA ≤20 turns |
| **R2** | SEV-2 High | agent failure mid-task · pipeline corruption → quarantine, reassign via fresh RCCF |
| **R3** | SEV-3 Medium | gate/test/quality failures → pause stage, fix via normal flow; 2× same reason → Law-14 freeze |
| **R4** | SEV-4 Low | minor violations → lead handles inline with documentation |

Plus mandatory tabletop drills every 50 agent turns (P-10.9).

### KPI Catalog (`hq/core/standards/kpi-thresholds.md`)

17 measurable indicators (K1–K17) with green/yellow/red thresholds computed from real artifacts —
intake cycle time, gate pass rate, rework rate, license-check compliance (hard 100%), MTTR,
drill compliance, deployment rollback-plan presence, test coverage, alert↔runbook mapping.
Hard rules block Gate-8 automatically. Red readings alert owning leads same-session.

### Reporting Cadence (`hq/core/standards/reporting-cadence.md`)

Daily Ops Digest · Weekly Performance Review · Monthly Organizational Report — fixed skeletons,
owner-facing summaries in simple Arabic, stored under `hq/brain/org_reports/<yyyy>/<mm>/`.

---

## Extending the System

| Want to… | Do this |
|---|---|
| **Add an agent** | Create `.opencode/agent/<name>.md` + its capsule under `hq/core/domain/rooms/<room>/agents/<name>/` → update `registry.yaml` (count must match!) → run `port-agents.mjs`. Capsule capabilities must stay ⊆ room manifests (zero leakage). |
| **Add a room skill** | Assign via `SKILLS-ASSIGNMENT.md` deed + room `capabilities/skills.yaml`. Never duplicate across rooms — shared code becomes shared-kernel by documented decision. |
| **Add a domain site** | Create `hq/engine/sites/<domain>.caddy` → `validate.sh` → `deploy.sh`. Unknown hosts hit the 404 guard by default. |
| **Change governance** | Propose through the flow (gateway → CEO). Constitution changes require brd-ceo approval; amendments are appended to `system-state-current.md`, never rewritten silently. |
| **Start a project** | Follow S1: intake → MVP scope → research → PRD lands in `projects/<slug>/brain/CONTEXT.md`. Paper stages precede any code. |

---

## Developer Guidelines

Binding for anyone (human or agent) working in this tree:

1. **Read the boot sequence** in `AGENTS.md` before touching anything — it loads identity,
   constitution, brain index, protocols, contracts, and the skills index in order.
2. **Evidence or it didn't happen** — every change cites `file:line`, every command reports its
   exit code (Law 4).
3. **Real paths only** — deliverables open with their actual `## FILE: <path>` header; imagining a
   path is forbidden; folders/files use English kebab-case (technical identifiers excepted) (Law 13).
4. **No worktrees, ever** — all work happens directly on the main tree (Law 10).
5. **Internal texts in English**, owner-facing communication in clear simple Arabic (Law 11).
6. **The registry is law** — 15 rooms · 114 agents must always reconcile (Law 12).
7. **Never edit historical record texts** — append amendments instead; old paths resolve through
   `structure-standard.md`.
8. **Secrets safety net** — `projects/**/*.env`, `backups/`, vendor and node artifacts are
   gitignored; keep it that way. This public repo contains governance only — private project code
   stays untracked by design.

---

*Baseline: clean-zeroed system · first commit 2026-08-26 · upstream: https://github.com/3rafat000-alt/sofi-hq*
