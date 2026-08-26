# 🏛️ SOFI AI — A Complete Software Organization Built from AI

> **A unified operating framework that turns AI agents from a scattered bunch into an organized enterprise:**
> 15 specialized rooms · 106 agents · one intake gateway · 9 quality gates · memory that never forgets.
> One entry point, one registry, one brain — built entirely on top of [opencode](https://opencode.ai).

---

## Why SOFI?

Working with AI agents today often resembles a workshop without a manager: every agent acts from its own point of view, no one is held accountable, decisions get lost between sessions, and the same mistake repeats because nobody remembers the lessons.

**SOFI solves this by building a complete "company" on top of the language model:**

- **One gateway for everything:** no request enters the system except through the intake agent, which understands it, classifies it, and routes it — no chaos, no random paths.
- **Strict specialization:** every agent masters exactly one mission, and every room is led by a single lead accountable for their team. No room meddles outside its domain.
- **Binding laws that cannot be bypassed:** constitutional laws govern every session — mandatory evidence for every delivery, hierarchical handoffs with no jumps, and no work without a formal work order.
- **Memory that never forgets:** decisions, lessons, and every incident are documented and consulted — the system never reinvents the wheel and never repeats its mistakes.
- **Quality before speed:** nine numbered inspection gates (G0–G8); no stage moves forward until it passes its gate.

The result: you talk to the system in your natural language, while behind the scenes a full organization operates with the discipline of a real company.

---

## A Look at the Architecture

Every request travels through the same hierarchy — from you into the system, and back out to you:

```
                        ┌──────────────────────┐
                        │         YOU          │
                        │   (owner / user)     │
                        └──────────┬───────────┘
                                   │ write your request in natural language
                                   ▼
                        ┌──────────────────────┐
                        │    Gateway (14)      │  gtw-intake-reformer
                        │ understand →         │  mandatory first point of entry
                        │ classify → route     │
                        └──────────┬───────────┘
                                   ▼
                        ┌──────────────────────┐
                        │  Board Room (00)     │  brd-ceo
                        │ final decision and   │  (+ Board consultation on
                        │ work distribution    │   critical matters)
                        └──────────┬───────────┘
              ┌────────────────────┼──────────────────────┐
              ▼                    ▼                      ▼
     ┌────────────────┐   ┌────────────────┐     ┌────────────────┐
     │ Executive rooms│   │ Review rooms   │     │ Support rooms  │
     │ 01–08          │   │ 09–10–12       │     │ 11–13          │
     │ strategy…data  │   │ security ·     │     │ operations ·   │
     │                │   │ quality · obs. │     │ knowledge      │
     └───────┬────────┘   └────────────────┘     └────────────────┘
             ▼ inside each room: the lead assigns agents (via Task)
             ▼ delivery returns up the same chain: agent → lead → CEO → you
```

### The 15 Rooms

| Code | Room | Lead | Agents | Role in one line |
|------|--------|--------|---------|-------------|
| `brd` | 00 · Board Room | `brd-ceo` | 7 | Leadership, governance, decisive decision-making, and work distribution |
| `str` | 01 · Strategy | `str-lead` | 7 | Market analysis, product planning, and prioritization |
| `res` | 02 · Research | `res-lead` | 7 | User and competitor research plus fact verification |
| `dsn` | 03 · Design | `dsn-lead` | 8 | Crafting screen appearance, visual identity, and the design system |
| `arc` | 04 · Architecture | `arc-lead` | 7 | System structure design and technology selection before building |
| `bck` | 05 · Backend | `bck-lead` | 8 | Building the server, communication channels, and behind-the-scenes business logic |
| `fnt` | 06 · Frontend | `fnt-lead` | 8 | Building everything the user sees and touches in the browser |
| `mob` | 07 · Mobile | `mob-lead` | 6 | Phone applications built with Flutter for Android and iOS |
| `dat` | 08 · Data | `dat-lead` | 7 | Databases, analytics, and privacy protection |
| `sec` | 09 · Security | `sec-lead` | 8 | Penetration testing and secrets protection — its lead holds an absolute veto |
| `qa` | 10 · Quality | `qa-lead` | 7 | Inspecting every delivery before acceptance: approve or block |
| `ops` | 11 · DevOps | `ops-lead` | 7 | Provisioning environments, releasing versions, and cutting operating costs |
| `obs` | 12 · Observability | `obs-lead` | 6 | Vigilance after deployment: health metrics and incident handling |
| `knw` | 13 · Knowledge | `knw-lead` | 6 | Preserving memory: documenting decisions and lessons and answering "why?" |
| `gtw` | 14 · Gateway | `gtw-dispatcher` | 7 | First stop for any request: understanding it, classifying its track, routing it |

> **Total:** 15 rooms and 106 agents — per the official registry [`hq/core/nexus/registry.yaml`](hq/core/nexus/registry.yaml).
> A detailed explanation of each room, its agents, and how it works appears in the [Rooms Guide](hq/training/rooms-guide.md).

---

## How Does the System Work?

### The Three Tracks — Work Depth Matches Task Criticality

Every request is classified by the gateway at entry into one of three tracks:

#### 🟢 Fast Track
**For what?** Reads, checks, and queries, documentation research, or a trivial single-file reversible fix — never touching money, security, or the data schema.
**Flow:** intake gateway → one room lead → delivery to you.

> **Example:** "How many rooms are in the system?" or "Open this file and explain it." A direct answer backed by evidence, without extra ceremony.

#### 🟡 Standard Track
**For what?** A new feature or medium change engaging one or two rooms.
**Flow:** gateway → CEO → room leads → agents → leads → CEO → you, crossing the quality gate.

> **Example:** "Add an About page to the site." Design, then build, then a full quality pass before delivery.

#### 🔴 Critical Track
**For what?** Anything touching money, security, live production, or the data schema — any irreversible change.
**Flow:** the complete path with zero shortcuts: gateway → CEO → Board consultation (the security lead holds an absolute veto) → rooms → gates → CEO → you.

> **Example:** "Change how payment data is stored" or "Deploy a new version to the live site." However small the work may look, it stays critical.

**Rules protecting classification:** doubt always escalates upward · money, security, and production are always critical · if higher risk emerges mid-execution the task promotes immediately — promotion only ascends, never descends.

### The Core Governing Laws

The full constitution ([AGENTS.md](AGENTS.md)) carries the binding laws — the most important:

| Law | What it means for you |
|---------|---------------|
| **Single gateway** (1) | every request enters through the intake agent — no other path exists, and violating this halts the system |
| **Hierarchical handoff** (3) | agent → room lead → CEO → you. No one jumps over anyone |
| **Mandatory evidence** (4) | every delivery arrives with its proof: the changed file and line, the result of every command run, and a record of the outcome. No evidence = delivery rejected |
| **RCCF work order** (5) | nothing executes without a formal work order answering: what? why? who executes? and how do we know it succeeded? |
| **Quality before speed** (8) | no delivery without review, no review without evidence — nine inspection gates guard the road |
| **Two memories** (7) | one memory for the organization and an independent memory for each project — they never mix |
| **Clear communication** (11) | everything you receive is written in clear simple Arabic, with no unexplained technical jargon |

---

## The Memory System

SOFI never starts a session from scratch. It has **organization memory** — seven regions inside `hq/brain/` (their files are private to the owner, stored locally, and not published in this public repository), each region with its own function:

> **State as of 2026-08-25:** these regions' records were archived through full local archiving by owner decision (nothing destroyed); the live index `hq/brain/brain-index.md` documents where the archive lives and how to retrieve any part of it. The table below describes the memory system's design as such.

| Region | Function |
|---------|----------|
| **HIPPOCAMPUS** | the unified session log — written by the CEO at the close of every session |
| **CORTEX** | permanent memory — architectural decisions, lessons, and structure. Additions only, never deletions |
| **THALAMUS** | routing and coordination — tracks, gates, and the room registry |
| **AMYGDALA** | alerts and emergencies — detection, escalation, and post-incident analysis |
| **PREFRONTAL** | planning and decisions — goals, risks, and trade-offs |
| **BASAL-GANGLIA** | routines and habits — recurring approved procedures |
| **TOOLS** | central capability registry — which room owns which tool and when it is used |

### Per-Project Memory — Fully Separate

Every project under `projects/<name>/` gets its own exclusive `brain/` folder with four files:

- **CONTEXT.md** — the project's living context and identity
- **DECISIONS.md** — this project's decisions only
- **HANDOFFS.md** — the log of delivery tickets between agents
- **LESSONS.md** — this project's lessons

**The strict separation rule:** a decision or lesson belonging to one project is never written straight into organization memory. Promotion happens only with the CEO's approval once a lesson recurs across different projects, or once a decision touches SOFI's own structure.

---

## Skills

Agents gain their extra capabilities from **Skills** — specialized instruction packs invoked on demand, documented in [.opencode/skills/INDEX.md](.opencode/skills/INDEX.md). Total: **106 skills** on disk (audited 2026-08-24), across main categories:

| Category | Examples |
|-------|-------|
| **Organization core** (3) | `sofi-evidence` builds the evidence block · `sofi-handoff` creates the hierarchical handoff ticket · `skill-forge`, the self-building skill factory |
| **Room playbooks** (one or more per room) | `str-gate0-classify` classifies requests · `sec-threat-model` models threats · `qa-test-plan` runs quality gates · `ops-deploy-runbook` ships safe deployments |
| **Official Flutter/Dart suite** (22+) | from the official Flutter team repository — testing, architecture, performance, localization |
| **Security-vetted external packs** | from Anthropic official and LambdaTest — UI, automated testing, Office/PDF documents |
| **Local MCP layer** | free keyless tool servers (`playwright` · `context7` · `sequential-thinking` · `ddg-search`) — system policy: no server with a key or subscription, and every new server must pass the security vetting gate |

---

## Requirements

To run SOFI on your machine you need:

- **A computer running Linux, macOS, or Windows** with a terminal
- **[opencode](https://opencode.ai)** — the runtime environment the entire system stands on
- **An account with an AI model provider** — linked to opencode once at first launch
- **git** — optional, for cloning the repository or keeping backups (and a GitHub account is fully optional too — you need it only if you want to publish your copy online)

No cloud services or extra subscriptions required — the system runs entirely locally.

---

## Step-by-Step Installation

```bash
# 1) Clone the repository onto your machine
git clone https://github.com/3rafat000-alt/sofi-hq.git SOFI
cd SOFI

# 2) Install opencode (choose either method)
curl -fsSL https://opencode.ai/install | bash
# or via npm:
npm i -g opencode-ai@latest

# 3) Link your model provider with your account key (once only)
opencode auth login

# 4) Launch the system from inside the SOFI folder
cd ~/Desktop/SOFI
opencode
```

### What Happens at Launch?

- An opencode session opens **directly on the intake gateway agent `gtw-intake-reformer`** — this is the default mode configured in [`opencode.json`](opencode.json), and the mandatory first entry point for every request.
- **Operating modes** (switch between them with Tab inside the interface):
  - **plan** — read-only mode: explore and draft plans without modifying any file.
  - **build** — execution mode: build and modify directly on the project's main tree.
- **You never invoke the 106 agents yourself** — they work behind the scenes: the CEO and the room leads automatically call each room's agents according to specialty, and work cascades hierarchically until the final delivery reaches you.

---

## How Do You Use It?

You write in your natural language — the system handles the rest:

### Example 1 — a simple request (fast track 🟢)

> **You:** "How many rooms do you have in the system? And what exactly does the security room do?"

**Behind the scenes:** the intake gateway understands the question and fast-classifies it → routes it to the right room lead → the answer comes grounded in the official registry → it reaches you within moments, backed by evidence from the system's files.

### Example 2 — a medium request (standard track 🟡)

> **You:** "Add an About page to my project's site."

**Behind the scenes:** the gateway classifies the request as standard → the CEO receives and distributes → the design room designs the page within the project identity → frontend builds it in code → quality inspects compliance and performance at the review gate → the CEO hands you the final result in understandable language with evidence of every step.

### Example 3 — a sensitive request (critical track 🔴)

> **You:** "Deploy the new version to the live site."

**Behind the scenes:** the gateway immediately classifies the request as critical → the CEO consults the Board, where the security lead holds an absolute veto if danger appears → DevOps deploys with a ready rollback plan → observability keeps watch after deployment → delivery is documented with complete evidence. No step is skipped no matter how long it takes.

---

## Folder Structure

```
SOFI/
├── identity/public-readme.md                  ← you are here
├── identity/sofi-system-identity.md           ← system identity and principles
├── AGENTS.md                  ← constitution: the 13 laws and boot sequence
├── memory_index/memory-index.md  ← memory index [private local — unpublished]
├── opencode.json              ← runtime config: default agent and permissions
│
├── hq/                        ← general headquarters ("HQ")
│   ├── core/                  ← governance: constitution, protocols, contracts, room charters
│   │   ├── nexus/             ← official registries: registry.yaml (15 rooms · 106 agents) and gates.yaml
│   │   ├── domain/            ← DDD domain layer: the 15 rooms as capsules with contracts (context-map)
│   │   ├── system-state-current.md  ← reference state of how the system works now
│   │   ├── tech_templates/    ← binding engineering templates alongside standards
│   │   └── tooling/           ← HQ tools (agent migration · law guards)
│   ├── brain/                 ← organization memory (locally archived — index: brain-index.md) [private local]
│   ├── engine/                ← live deployment layer (Caddy): sites/ one file per domain · php-fpm · scripts
│   └── hq/training/              ← training guides (ROOMS-GUIDE — guide to the 15 rooms)
│
├── projects/                  ← live projects — sakk only currently      [private local — unpublished]
│   └── sakk/
│       └── brain/             ← the project's separate memory: its context, decisions, lessons
│
└── .opencode/                 ← the operating layer above opencode
    ├── agent/                 ← definitions of the 106 agents (each agent's persona and specialty)
    └── skills/                ← 106 approved skills + their INDEX.md
```

---

## Roadmap and Future Ideas

A flexible section that evolves through the owner's decisions via the same formal flow — the leading directions currently proposed:

- **Expanding individual skills:** deriving specialized skills for specific agents within each room (such as a standalone penetration-testing skill for the pentester), derived from the room playbooks.
- **Expanding the local tool fleet:** adding free keyless MCP servers, each mandatorily passing the security vetting gate before activation.
- **Enriching the training library:** more annotated guides in `hq/training/`, written plainly for the owner and team.

---

## License and Contributing

### License

The repository license has not yet been chosen — the decision belongs to the owner at public release. Until then all contents are all rights reserved.

### Contributing

- Open an **Issue** in the repository to propose a feature or report a problem — preferably in Arabic.
- Every suggestion travels through SOFI's formal flow: the intake gateway classifies it, leadership reviews it, and nothing executes outside the binding laws.
- Code contributions will be welcomed after public release, subject to the same quality and security gates the internal team's work goes through.

---

## Deeper Documentation

| # | Document | What it answers |
|---|---------|-----------|
| 1 | [`identity/sofi-system-identity.md`](identity/sofi-system-identity.md) | system identity: who we are and what we run |
| 2 | [`AGENTS.md`](AGENTS.md) | the constitution: the 13 laws, three tracks, and boot sequence |
| 3 | [`hq/core/constitution-master.md`](hq/core/constitution-master.md) | the supreme law in detail |
| 4 | [`hq/core/protocols.md`](hq/core/protocols.md) | 16 living protocols (+1 retired) |
| 5 | [`hq/core/contracts.md`](hq/core/contracts.md) | inter-room contracts: handoff and escalation |
| 6 | [`hq/core/nexus/registry.yaml`](hq/core/nexus/registry.yaml) | the official registry: 15 rooms and 106 agents |
| 7 | `hq/brain/brain-index.md` *(private local — unpublished)* | the full memory structure |
| 8 | [`hq/training/rooms-guide.md`](hq/training/rooms-guide.md) | a room-by-room guide to the 15 rooms in plain language |
| 9 | [`.opencode/skills/INDEX.md`](.opencode/skills/INDEX.md) | index of the 106 skills |
