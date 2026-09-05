# SOFI HQ

> **An AI enterprise organization** — a complete, constitution-governed multi-agent software company:
> **17 rooms · 121 agents · 116 skills · 16 binding laws · 9 gates + DFR · an S1→S6 production line · zero pending warnings.**

SOFI HQ is not a traditional application you "run". It is an *operating organization* for AI coding
harnesses: every request enters through a single gateway, gets classified by criticality, and flows
through specialized agent rooms under binding laws — with evidence discipline, quality gates,
memory isolation, and incident runbooks built in.

> **Status (R3.1 + Audit-ALL-Phase3 — 2026-09-05):** `17 rooms · 121 agents · 116 skills` — all 4
> constitutional guards green · **zero PENDING warnings** · main tree only · every change atomic + auditable.
>
> **Live dashboard:** [`SOFI-INSTITUTION-COMPLETE-REPORT-2026-09-05.md`](./SOFI-INSTITUTION-COMPLETE-REPORT-2026-09-05.md) — 685 lines, the single source of truth for the org state.

---

## Table of Contents

1. [Overview](#overview)
2. [How It Works](#how-it-works)
3. [Repository Structure](#repository-structure)
4. [The Governance Core](#the-governance-core)
5. [The 17 Rooms](#the-17-rooms)
6. [The 121 Agents](#the-121-agents)
7. [The 116 Skills](#the-116-skills)
8. [Tech Stack & Stack Lock](#tech-stack--stack-lock)
9. [Requirements & Dependencies](#requirements--dependencies)
10. [Installation & Setup](#installation--setup)
11. [Running & Usage Examples](#running--usage-examples)
12. [The S1→S6 Production Line](#the-s1s6-production-line)
13. [Gates & Decision Authority](#gates--decision-authority)
14. [Memory: CORTEX / HIPPOCAMPUS / AMYGDALA](#memory-cortex--hippocampus--amygdala)
15. [The MCP Fleet (27 servers, 100% local)](#the-mcp-fleet-27-servers-100-local)
16. [Key Subsystems](#key-subsystems)
17. [The 16 Binding Laws](#the-16-binding-laws)
18. [The 17 Protocols](#the-17-protocols)
19. [The 26 Standards](#the-26-standards)
20. [Extending the System](#extending-the-system)
21. [Developer Guidelines](#developer-guidelines)
22. [Troubleshooting & FAQ](#troubleshooting--faq)
23. [Versioning & History](#versioning--history)
24. [License & Contributing](#license--contributing)

---

## Overview

SOFI HQ treats AI coding as **organizational work**, not chat. Every "user" of SOFI is in fact a
**non-technical owner** (Arabic-speaking, with Law 11 communication standard). Every developer request
becomes a **work order (RCCF)** that flows through specialized **rooms** filled with specialized **agents**,
gated by **constitutional laws** and **quality gates**, and audited by **four machine guards** before
any commit lands on the main tree.

The organization has been re-architected three times in 2026 to eliminate the very things that
make AI harnesses unreliable: drift, hallucination, secret leakage, and unbounded scope creep.
The current state (R3.1 + Audit-ALL-Phase3) is the result.

| Metric | Value | Source |
|--------|-------|--------|
| **Rooms** | 17 | `hq/core/nexus/registry.yaml:11` |
| **Agents** | 121 | `hq/core/nexus/registry.yaml:11` + `.opencode/agent/` |
| **Skills** | 116 | `.opencode/skills/*/SKILL.md` |
| **Laws** | 16 | `AGENTS.md:10` |
| **Protocols** | 17 (P-01..P-20) | `hq/core/protocols.md` |
| **Standards** | 26 | `hq/core/standards/` |
| **Gates** | G0..G8 + DFR | `hq/core/nexus/gates.yaml` |
| **MCP servers** | 27 (100% local) | `hq/core/nexus/mcp-routing.yaml` |
| **MCP-FLEET rules** | 6 | binding for all servers |
| **Constitutional guards** | 4 (registry_guard · count_sync · evidence_guard · gitleaks) | `hq/core/tooling/` |
| **Memory stores** | 2 (org `hq/brain/` + project `projects/<slug>/brain/`) | Law 7 |
| **Visual diagrams** | 9 (Mermaid + SVG + PNG) | `hq/core/design/diagrams/` |
| **Pre-commit hooks** | 5 checks | `hq/core/tooling/hooks/pre-commit` |
| **Templates** | 1 unified report + agent + mcp | `hq/core/templates/` + `skill-forge` |
| **Live project** | sakk (mobile Flutter + web React/Vite + Laravel backend) | `projects/sakk/` |
| **GitHub** | `3rafat000-alt/sofi-hq` (private project ops · public repo) | `git remote -v` |

---

## How It Works

The flow is **strictly hierarchical** and **three-lane proportional** (Law 1):

```
            ┌─────────────────────────────────────────┐
            │            OWNER (Arabic, non-tech)     │  ← Law 11: simple Arabic
            └────────────────┬────────────────────────┘
                             │ "I want X"
                             ▼
            ┌─────────────────────────────────────────┐
            │      gtw-intake-reformer (room 14)      │  ← Law 1: every request enters here
            │  • 5-section prompt reformulation        │
            │  • ambiguity score (Law 16: ≤20% OK)     │
            │  • conflict + budget check                │
            └────────────────┬────────────────────────┘
                             │ Intake Report (5 sections)
                             ▼
            ┌─────────────────────────────────────────┐
            │   P-01.8 lane classification:            │  ← single authoritative text
            │  🟢 Fast  | 🟡 Standard | 🔴 Fateful   │
            └────┬────────────┬─────────────┬──────────┘
                 │            │             │
        (read/scan)  (feature 1-2 rooms)  (money/security/schema)
                 │            │             │
        one lead → delivery    brd-ceo (+ Board on Fateful)
                 │            │             │
        ┌────────┴────────────┴─────────────┴──────────┐
        │  S1 → S2 → S3 → S4 → S5 → S6               │
        │  paper  paper paper  code  code  shield    │
        │  (01)   (04)  (03)  (05)  (06/07)  (09-13) │
        └────────────────────────────────────────────┘
                             │
                             ▼
            ┌─────────────────────────────────────────┐
            │  Memory: CORTEX (ADRs) + HIPPOCAMPUS    │  ← Law 7: org vs project split
            │  (sessions) + AMYGDALA (incidents)      │
            └─────────────────────────────────────────┘
```

**Constitutional guarantees (Law 1):**
- **🟢 Fast** — Gateway auto-authorizes (read/scan/trivial reversible single-file) — no CEO bottleneck
- **🟡 Standard** — features spanning 1–2 rooms, brd-ceo approval, full RCCF + L8 gate
- **🔴 Fateful** — money/security/architecture/production/schema/irreversible — full flow + Board consult + CSO veto
- **Money/Security/Production/Schema = ALWAYS Fateful** (no downgrade — L3 on violation)
- **Doubt escalates upward** (fail-safe) — never sideways, never skip
- **Promotion ascends, never descends** — discovering higher risk mid-execution → immediate promotion

---

## Repository Structure

```
SOFI/
├── README.md                                ← this file
├── AGENTS.md                                ← the constitution (16 binding laws)
├── opencode.json                            ← MCP fleet config + agent routing
├── gitleaks.toml                            ← secret allowlist
│
├── .opencode/                               ← the **operating layer** (sole source of truth per Law 12)
│   ├── agent/                               ← 121 agent files (frontmatter + identity + skills + constraints + handoff + team)
│   └── skills/                              ← 116 skills = one folder per skill, SKILL.md inside
│
├── hq/                                      ← the **headquarters** (governance + runtime)
│   ├── core/                                ← the constitution material — DO NOT EDIT casually
│   │   ├── protocols.md                     ← 17 protocols (P-01 → P-20)
│   │   ├── contracts.md                     ← 10 cross-room contracts
│   │   ├── constitution-master.md           ← supreme law
│   │   ├── constitution_articles/           ← Article 00 + future articles
│   │   ├── system-state-current.md          ← BINDING current operating state
│   │   ├── structure-standard.md            ← naming + old←new map
│   │   │
│   │   ├── domain/                           ← DDD domain layer (rooms, contexts, contracts)
│   │   │   ├── context-map.yaml             ← single official inter-room interface
│   │   │   └── rooms/                       ← 17 rooms with charter + agents/*/capsule
│   │   │
│   │   ├── nexus/                           ← the cross-cutting registry
│   │   │   ├── registry.yaml                ← 14 rooms · 121 agents (Law 12)
│   │   │   ├── personas.yaml                ← Arabic names + roles
│   │   │   ├── pipeline.yaml                ← S1→S6 stages
│   │   │   ├── gates.yaml                   ← G0..G8 + DFR
│   │   │   ├── routing.yaml                 ← model/effort/budget per agent
│   │   │   ├── mcp-routing.yaml             ← 27 MCP servers · 100% local
│   │   │   ├── models.yaml                  ← LLM models per task class
│   │   │   ├── room-priority.yaml           ← T0..T4 tiers
│   │   │   ├── skill-routing.yaml           ← skill → room → lead map
│   │   │   └── rccf-registry.yaml           ← central RCCF tracker (Audit-ALL)
│   │   │
│   │   ├── standards/                       ← 26 standards (api-envelope, ddd-capsule, latest-version-mandatory, …)
│   │   ├── gate_checklists/                 ← per-gate criteria (gate-0.md … gate-8.md + dfr.md)
│   │   ├── design/                          ← system-ddd-blueprint + 9 Mermaid diagrams
│   │   ├── archive/                         ← historical + audit-all-phase3 (Law 13.5)
│   │   ├── tech_templates/                  ← agent-prompt-template + mcp-agent-annex
│   │   ├── templates/                       ← report-template + agent/skill templates
│   │   └── tooling/                         ← the 4 constitutional guards + hooks + wrappers
│   │
│   ├── brain/                               ← organization memory (CORTEX + HIPPOCAMPUS + AMYGDALA)
│   │   ├── cortex-decisions.md              ← ADR log
│   │   ├── hippocampus-sessions.md          ← session log
│   │   ├── amygdala-incidents.md            ← incident log
│   │   └── evidence/                        ← snapshot + audit files
│   │
│   ├── engine/                              ← live publishing layer (Caddy + PHP-FPM + n8n + MCP server)
│   ├── training/                            ← file-discipline + rooms-guide + ddd-full-cycle-playbook
│   └── history/                             ← 2026-08-25 cleanup + future decision history
│
├── projects/                                ← project memories (Law 7: separate from org memory)
│   └── sakk/                                ← the live project (mobile Flutter + web React + Laravel)
│       ├── brain/                           ← CONTEXT (PRD v2.0) + DECISIONS + HANDOFFS + LESSONS
│       ├── backend/                         ← Laravel 11+ code
│       ├── mobile/                          ← Flutter 3.22+ code
│       └── apps/                            ← React 19 + Vite admin/web
│
├── docs/                                    ← non-binding supplementary docs (Mermaid mirror)
│
└── .claude/ .kilo/ .coverage/ .pytest_cache/ .firecrawl/  ← harness internals (NOT part of SOFI constitution)
```

---

## The Governance Core

The **constitution** is `AGENTS.md:1` — 16 binding laws, supreme. Any modification requires `brd-ceo`
approval recorded in `hq/brain/cortex-decisions.md` (Law 12). The constitution defers to P-01.8 in
`hq/core/protocols.md:19` for the single authoritative lane text.

**The 4 Constitutional Guards** (run on every pre-commit + on-demand via `hq/core/tooling/hooks/pre-commit`):

| Guard | File | Purpose | Threshold |
|-------|------|---------|-----------|
| `registry_guard` | `hq/core/tooling/registry_guard.py:1` | `.opencode/agent/*` 1:1 with `registry.yaml` rooms/agents | exit 0 + zero pending |
| `count_sync` | `hq/core/tooling/count_sync.py:1` | derived vs declared vs textual claims in `AGENTS.md` | exit 0 + zero pending |
| `evidence_guard` | `hq/core/tooling/evidence_guard.py:1` | every `file:line` citation resolves to a real file | exit 0 + 0 broken |
| `gitleaks` | `gitleaks.toml:1` (via pre-commit) | no secrets in code (Law 8 + P-08.1) | exit 0 + "no leaks found" |

**`sofi-audit`** is the unified wrapper at `hq/core/tooling/sofi-audit.py` — single invocation that
chains `registry_guard` + `count_sync` for pre-commit. The originals remain callable independently.

---

## The 17 Rooms

> Source: `hq/core/nexus/registry.yaml:1` + `hq/core/domain/rooms/<room>/charter.md` (per-room charter).

| # | Room | Code | Tier | Lead | Domain |
|---|------|------|------|------|--------|
| 00 | Boardroom | 00-boardroom | T0 Spine | `brd-ceo` | governance + board advisory + CSO veto |
| 14 | Gateway | 14-gateway | T0 Spine | `gtw-dispatcher` | mandatory entry · lane classification · routing |
| 01 | Strategy | 01-strategy | T1 Paper | `str-lead` | PRD + MVP + roadmap |
| 02 | Research | 02-research | T1 Paper | `res-lead` | JTBD personas + journey maps + competitive |
| 04 | Architecture | 04-architecture | T1 Paper | `arc-lead` | system design + API freeze + DDD + ERD |
| 03 | Design | 03-design | T1 Paper | `dsn-lead` | UX + design system + DFR sign-off |
| 08 | Localization | 08-localization | T1 Paper | `loc-translation-manager` | Arabic translation + RTL + voice & tone + privacy |
| 16 | Innovation | 16-innovation | T1 Paper | `inn-lab-lead` | tech scouting + PoCs + ML sandbox |
| 05 | Backend | 05-backend | T2 Code | `bck-lead` | Laravel 11+ · S4 |
| 06 | Frontend | 06-frontend | T2 Code | `fnt-lead` | React 18+ + Tailwind 4+ · S5 |
| 07 | Mobile | 07-mobile | T2 Code | `mob-lead` | Flutter 3.22+ + Dart 3+ · S5 |
| 09 | Security | 09-security | T3 Shield | `sec-lead` | STRIDE + pentest + license + secrets |
| 10 | Quality | 10-quality | T3 Shield | `qa-lead` (Lama Al-Tarabulsi) | test plans + automation + Gate-5 + DFR |
| 11 | DevOps | 11-devops | T3 Shield | `ops-lead` | CI/CD + cloud + release + sandbox |
| 12 | Observability | 12-observability | T3 Shield | `obs-lead` | metrics + logs + SLOs + incidents |
| 15 | WarRoom | 15-warroom | T3 Shield | `war-incident-commander` | P0 incident command · on-call |
| 13 | Knowledge | 13-knowledge | T4 Memory | `knw-lead` | CORTEX + HIPPOCAMPUS + AMYGDALA |

**T0 spine (always-on):** rooms 00 + 14 — every request enters via 14, every escalation ends at 00.
**T1 paper:** rooms 01, 02, 03, 04, 08, 16 — no code before DFR signature.
**T2 code:** rooms 05, 06, 07 — backend must complete before UI.
**T3 shield:** rooms 09, 10, 11, 12, 15 — continuous, veto powers anywhere.
**T4 memory:** room 13 — passive, logs every decision.

---

## The 121 Agents

> Source: `hq/core/nexus/registry.yaml:11` + `.opencode/agent/<name>.md` + `hq/core/nexus/personas.yaml`.

**121 agents** distributed across the 17 rooms. Each has:
- a frontmatter (name · description · mode · model)
- an identity (Arabic name + role + skills + mindset)
- 7 responsibilities + a constraints block
- a team-collaboration section (inputs/outputs/escalation)
- 1–3 available skills (constitutionally wired via `sofi-evidence` + `sofi-handoff`)

**Quality room (10) — the only "official testers" all live together in room 10:**

| Agent | Arabic name | Specialty | Acceptance points | Stack |
|-------|-------------|-----------|-------------------|-------|
| `qa-lead` | لمى الطرابلسي | Gate-5 + DFR | — | cross |
| `qa-test-architect` | ياسمين العطاسي | test plans + Pest/PHPUnit | — | cross |
| `qa-automation-engineer` | نمير العطار | Playwright/Cypress | — | cross |
| `qa-manual-explorer` | هنادي النقري | exploratory | — | cross |
| `qa-perf-analyst` | هلال الجزائري | JMeter/k6 | — | cross |
| `qa-design-auditor` | نايا الأسفري | Nielsen + WCAG | — | cross |
| `qa-regression-warden` | وجدان الحلاق | regression suite | — | cross |
| `qa-flutter-architect` | **ريان القاضي** | Flutter 3.22+ + adb/uiautomator/gfxinfo/meminfo | **20** | mobile |
| `qa-react-architect` | **سامر الخليل** | React 18+/Next.js + DDD + Web Vitals | **28** | frontend |
| `qa-laravel-architect` | **يوسف العامري** | Laravel 11+ + DDD + DB + Security (N+1/EXPLAIN/Policies) | **22** | backend |

> **The 3 stack-specialist testers are ADVISORY ONLY** (no gate authority — `qa-lead` + `brd-cqo` decide).
> They feed findings to Gate-5; the verdict belongs to the room lead + Board.

**New in Audit-ALL-Phase3:**
- `inn-ml-engineer` (Bushra Al-Amadi) — Innovation lab ML/AI experimentation
- `loc-privacy-officer` (Dirar Al-Khatib) — Localization privacy (GDPR/LGPD on Arabic copy)

---

## The 116 Skills

> Source: `.opencode/skills/INDEX.md` + `.opencode/skills/*/SKILL.md`.

Skills are the **operating manuals** — each room + each new agent ships with one or more. Categories:

| Category | Count | Examples |
|----------|-------|----------|
| **Foundation** (all rooms) | 6 | `sofi-evidence` · `sofi-handoff` · `sofi-mcp-fleet` · `sofi-boot` · `sofi-project-spawn` · `skill-forge` |
| **Room playbooks** (1/room) | 17 | `brd-decision-gate` · `gtw-intake-route` · `qa-test-plan` · `qa-flutter-architect` · `qa-react-architect` · `qa-laravel-architect` · `bck-feature-build` · `fnt-component-build` · `mob-feature-build` · `dsn-design-handoff` · `arc-adr` · `obs-incident-response` · `sec-threat-model` · `sec-mcp-vetting` · `loc-rtl-adaptation` · `inn-experiment` · `war-incident-runbook` |
| **Official Flutter/Dart pack** | 22 | `flutter-add-widget-test` · `dart-run-static-analysis` · … |
| **LambdaTest pack** | 19 | `playwright-skill` · `phpunit-skill` · `laravel-dusk-skill` · `flutter-testing-skill` · `smartui-skill` · … |
| **Anthropic pack** | 7 | `frontend-design` · `theme-factory` · `webapp-testing` · `skill-creator` · … |
| **SOFI original** | 6 | `systematic-debugging` · `brainstorming` · `writing-plans` · `dsn-design-intelligence` · `qa-agent-browser` · `res-web-scrape` |
| **Absorbed** | 7 | `banner-design` · `brand` · `design` · `design-system` · `slides` · `ui-styling` · `ui-ux-pro-max` |
| **External packs (linked)** | 38+ | `api-*` · `dart-*` · `flutter-*` · `test-frameworks` · … |

**3 new skills added in Audit-ALL-Phase3:**
- `loc-rtl-adaptation` — Arabic localization & RTL protocol
- `inn-experiment` — Innovation experiment protocol
- `war-incident-runbook` — WarRoom P0 incident runbook

---

## Tech Stack & Stack Lock

> Source: `AGENTS.md` §Stack Lock R3 (owner directive 2026-09-04) — **no override without owner order recorded in CORTEX**.

| Layer | **Binding** | **Forbidden** |
|-------|-------------|---------------|
| **Frontend (06)** | **React 18+** (19+ encouraged) · TypeScript 5+ · Tailwind 4+ · Vite 5+ / Webpack 5 · Storybook 8+ · Jest/Vitest/Playwright | Vue · Angular · Svelte · jQuery · Bootstrap · any non-React lib |
| **Backend (05)** | **Laravel 11+** EXCLUSIVE · PHP 8.3+ mandatory · Eloquent · Queues + Horizon · Redis 7+ · PostgreSQL 16+ / MySQL 8+ · PHPUnit 11+ / Pest 3+ · Composer 2+ | Symfony (standalone) · CodeIgniter · Yii · Slim · Lumen-as-main · raw PHP frameworks · PHP < 8.3 |
| **Mobile (07)** | **Flutter 3.22+** · Dart 3+ · Riverpod / Bloc | any non-Flutter framework |
| **Linting/quality** | ESLint · Prettier · Storybook · PHPUnit/Pest | (none — all required) |
| **MCP** | 27 servers, **100% local**, free | paid SaaS / API keys (INT-0003 auto-rejects) |
| **Tone** | All human-time concepts removed from mandates | "daily standup" · "nightly scan" · "weekly retrospective" (Rec #16 — replaced with on-merge / on-incident-close) |

**Latest-Version-Mandatory:** before any code touching a library → **Context7** MCP; for any external
repo claim → **DeepWiki** MCP. No improvising from stale memory. (`hq/core/standards/latest-version-mandatory.md:1`)

---

## Requirements & Dependencies

| Component | Version | Notes |
|-----------|---------|-------|
| **Python** | 3.12+ | required for the 4 constitutional guards |
| **Bash** | 5+ | pre-commit hook is bash |
| **gitleaks** | 8.30+ | secret scanner (free, MIT) |
| **Git** | 2.40+ | for the engine layer + pre-commit hooks |
| **OpenCode** (or compatible harness) | latest | MCP-aware + subagent-capable |
| **Caddy** | 2.7+ | only if running the engine layer locally |
| **PHP 8.3+** | required | only for Laravel projects under `projects/` |
| **Node 20 LTS** | required | only for React projects under `apps/` |

**Optional:**
- Docker — for the MCP server (`hq/engine/mcp_server/`)
- Mermaid CLI ^10.9.0 — for regenerating diagrams (`hq/core/design/diagrams/`)
- n8n — for the orchestrator workflow (`hq/engine/n8n/`)

All tooling is **free** (INT-0003). No paid API keys, ever.

---

## Installation & Setup

```bash
# 1. Clone
git clone https://github.com/3rafat000-alt/sofi-hq.git
cd sofi-hq

# 2. Install system tooling
sudo apt-get install python3.12+ gitleaks bash git
# OpenCode: see https://opencode.ai
# Optional: install npx + Mermaid CLI for diagram regeneration

# 3. Install the SOFI pre-commit hook
bash hq/core/tooling/hooks/install.sh

# 4. Verify the constitutional guards are green
python3 hq/core/tooling/sofi-audit.py
python3 hq/core/tooling/evidence_guard.py hq/core --strict
bash hq/core/tooling/hooks/pre-commit

# 5. (Optional) Run the live project — sakk
ls projects/sakk/brain/CONTEXT.md    # read the PRD
cd projects/sakk/backend && composer install && php artisan migrate
cd projects/sakk/mobile && flutter pub get
cd projects/sakk/apps/admin && pnpm install
```

You should see all 4 guards exit 0 with **zero pending** warnings. If not, see [Troubleshooting](#troubleshooting--faq).

---

## Running & Usage Examples

### 1. Submit a request as the owner (Arabic)

```bash
# Just type in plain Arabic in the OpenCode chat
"أريد تطبيق متجر إلكتروني بسيط"
```

The gateway (`gtw-intake-reformer`) receives it, reformulates into a 5-section Intake Report, and routes
per P-01.8. Nothing bypasses intake (Law 1 → L4 on bypass).

### 2. Add a new agent (full lifecycle, mirror of `qa-react-architect`)

```bash
# 1. Create agent file (frontmatter + identity + constraints + handoff)
cat > .opencode/agent/<name>.md <<'YAML'
---
name: <name>
description: <name> — <role> in the <room> room
mode: subagent
model: opencode/big-pickle
---
...
YAML

# 2. Create capsule (capabilities + senses + memory)
mkdir -p hq/core/domain/rooms/<room>/agents/<name>
for f in capabilities senses memory; do
  cat > hq/core/domain/rooms/<room>/agents/<name>/$f.yaml <<'YAML'
# ... standard content
YAML
done

# 3. Update registry + personas + routing + charter + INDEX + AGENTS
# 4. Bump guards: registry_guard.py:20 + count_sync.py:23

# 5. Commit atomically — pre-commit enforces all 4 guards
git add <files> && git commit -m "feat(<room>): add <name>"
```

### 3. Run a constitutional guard on demand

```bash
python3 hq/core/tooling/sofi-audit.py             # unified
python3 hq/core/tooling/registry_guard.py --strict  # 1:1 check
python3 hq/core/tooling/count_sync.py              # claims check
python3 hq/core/tooling/evidence_guard.py hq/core --strict  # file:line check
gitleaks git --staged --pre-commit --config gitleaks.toml  # secret check
```

### 4. Make a fateful decision (Board consult)

```bash
# Issue RCCF-2026-MM-DD-NAME ticket
# -> brd-ceo consults Board (brd-cpo, brd-cto, brd-cqo, brd-cso)
# -> CSO holds absolute veto on security/safety
# -> deliver via sofi-handoff (JSON ticket ≤280 char note)
# -> record in hq/brain/cortex-decisions.md
```

### 5. Trigger WarRoom (P0 incident)

```bash
# On P0: obs-incident-commander OR sec-incident-responder raises alert
# -> war-incident-commander takes command (Law 14 freeze)
# -> war-forensic-analyst collects evidence (hash before touch)
# -> war-rollback-engineer executes rollback window
# -> war-communication-lead briefs owner every 30 min (Law 11)
# -> AMYGDALA entry within 24h
# -> re-evaluate linked Gate (e.g. security incident → re-open G4)
```

---

## The S1→S6 Production Line

> Source: `hq/core/nexus/pipeline.yaml:8` + `hq/core/standards/pipeline-production-line.md`.

| Stage | Name | Rooms | Lead | Gate | Output |
|-------|------|-------|------|------|--------|
| **S1** | Idea, Strategy & Research | 00·01·14·02 | `str-lead` | G1 | PRD in `projects/<slug>/brain/CONTEXT.md` |
| **S2** | Data & Contract Design (paper) | 04 | `arc-lead` | G3 | ERD + schema-contract + frozen OpenAPI (no code) |
| **S3** | Experience & Visual System | 03 | `dsn-lead` | **DFR** | UX + design system + mockups (signed by 09+10) |
| **S4** | Live Backend Execution | 05 | `bck-lead` | G4 | Working API + migrations + security-checked |
| **S5** | Both Interfaces in Parallel | 06·07 (merged team) | `fnt-lead` + `mob-lead` | G4b | Flutter/Dart for web+mobile on frozen contract |
| **S6** | Shield & Production | 09·10·11·12 | `qa-lead` + `ops-lead` + `obs-lead` | G5·G6·G7·G8 | Tests + deploy + observability + knowledge log |

**4 binding laws:**
1. **OpenAPI-first** — no code without a frozen OpenAPI spec
2. **No transient mocks crossing boundaries** (internal unit tests exempt)
3. **Envelope** per `hq/core/standards/api-envelope.md` — every API response wraps
4. **DDD Capsule** per `hq/core/standards/ddd-capsule.md` — DO/DON'T table for bounded contexts

---

## Gates & Decision Authority

> Source: `hq/core/nexus/gates.yaml:1` + `hq/core/gate_checklists/`.

| Gate | Owner | Triggers | What it checks |
|------|-------|---------|----------------|
| **G0** | 14-gateway + 01-strategy | every intake | ambiguity ≤ 20% · scope classification · fast-track eligibility |
| **G1** | 02-research | S1 → S2 | research dossier signed (JTBD + personas + pain points) |
| **G2** | 01-strategy | S1 → S2 | PRD approved · MVP scope locked |
| **G3** | 04-architecture | S2 → S3 | ERD + schema-contract (paper) + OpenAPI frozen |
| **DFR** | 03-design + 09-security + 10-quality | S3 → S4 | **Design-Freeze Review signed by sec-lead + qa-lead** — zero code before this |
| **G4** | 05-backend | S4 → S5 | live API + migrations + security-checked |
| **G4b / S5** | 06·07 | S5 → S6 | both interfaces on frozen contract |
| **G5** | 10-quality | S6 end | test plan + execution + coverage + design audit (PASS/REJECT) |
| **G6** | 11-devops | G5 → S7 | deploy + rollback plan + health check |
| **G7** | 12-observability | G6 → S8 | tracing + SLOs + alerts live |
| **G8** | 13-knowledge | S6 final | documentation in CORTEX + skills indexed |

**4 owner approval points** (mandatory — INT-EVOL-2):
1. **Scope & plan** (after S1) — what we'll build, what we won't, timeline, technology
2. **Look & design** (after S3) — shapes, colors, fonts as images, no jargon
3. **Technical plan** (after S2/S3) — metaphor, no jargon
4. **DFR + G5** — design freeze + production quality

> Rejecting at any point = return to the owning stage for correction. Writing code before all 4
> points are approved is forbidden (Design-First doctrine, INT-0004).

---

## Memory: CORTEX / HIPPOCAMPUS / AMYGDALA

> Source: `hq/brain/` + `projects/<slug>/brain/` · Law 7 binds these together.

**Two completely separate memories — never mix:**

### Organization memory (`hq/brain/`)

- **`cortex-decisions.md`** — **CORTEX** — the ADR log. Every fateful decision is recorded here with:
  context · decision · consequences · evidence `file:line` · ADR id (e.g. `ADR-20260905-AUDIT-ALL`).
- **`hippocampus-sessions.md`** — **HIPPOCAMPUS** — session log. One entry per session with: date ·
  intake_id · classification · verdict · evidence · status.
- **`amygdala-incidents.md`** — **AMYGDALA** — incident log. Every P0/WarRoom incident with:
  timeline · forensic evidence · rollback actions · postmortem.
- **`evidence/`** — per-task audit + snapshot files (e.g. `surgical-review-*`).

**Auto-summarize (P-06.7):** `hq/core/tooling/memory_summarizer.py:1` runs every 10 turns via `knw-reflector`
(hippocampus >800 lines or amygdala >600 lines → keep last 5 full + summarize older).

### Project memory (`projects/<slug>/brain/`)

For each active project (e.g. `projects/sakk/brain/`):
- `CONTEXT.md` — the PRD (single source of truth)
- `DECISIONS.md` — project-level decisions
- `HANDOFFS.md` — task handoffs
- `LESSONS.md` — lessons learned

> **Law 7 isolation:** org memory and project memory are **strictly separated** — promotion from project to
> org requires explicit `brd-ceo` decision. No agent may write to both stores in one commit.

---

## The MCP Fleet (27 servers, 100% local)

> Source: `hq/core/nexus/mcp-routing.yaml:13` + `hq/core/standards/mcp-registry.md` + `.opencode/skills/sofi-mcp-fleet/SKILL.md`.

**The 6 binding MCP-FLEET rules (apply to every server):**

1. **SOFI-Context before any code touching a library** — Latest-Version-Mandatory
2. **SOFI-Wiki before any external repo claim** — HiveFence lesson
3. **SOFI-Browser for visual delivery evidence** — Kitesurf default (Law 4)
4. **SOFI-Reasoning for complex branching** — Sequential-thinking
5. **`sec-mcp-vetting` for any new server** — no self-enable
6. **Everything is free** — paid keys auto-rejected (INT-0003)

**Distribution:** each room gets 2–3 servers (Filesystem-Scoped + SOFI-Time + SOFI) + access to the
6 fleet servers + 21 organizational servers (SOFI-Consult, SOFI-Research, SOFI-Skills, SOFI-Github,
SOFI-Network, SOFI-MemoryHub, SOFI-EpisodicMemory, SOFI-WorkingMemory, …).

**100% local** — zero external SaaS, zero npx cloud calls. Verified by `SOFI-MCP-FLEET-v2` header.

---

## Key Subsystems

### Visual Layer (9 Mermaid diagrams)

`hq/core/design/diagrams/` — 9 Mermaid + SVG + PNG diagrams covering: Use-Case · Pipeline S1→S6 ·
Gateway Routing · Layered Architecture · Context-Map · Gate State Machine · Ticket-Bus · Deployment ·
Memory Isolation. Generated via Mermaid CLI ^10.9.0 (MIT) + fallback PIL.

Mirror at `docs/diagrams/` (18 files) for the website/presentations. Each SVG has `aria-label` + contrast ≥ 4.5:1.

### Templates (`hq/core/templates/` + `skill-forge`)

- `agent-prompt-template.md` — base for every `.opencode/agent/<name>.md`
- `mcp-agent-annex.md` — MCP section
- `report-template.md` — unified 5-section report (the Audit-ALL standard)
- **`.opencode/skills/skill-forge/`** — meta-skill to author/update any skill under `sofi-evidence`
  guard discipline

### The Hook System (`hq/core/tooling/hooks/pre-commit`)

Installed via `bash hq/core/tooling/hooks/install.sh` into `.git/hooks/pre-commit`. Runs in 5 stages:

1. **gitleaks** — secret scan (Law 8 + P-08.1)
2. **sofi-audit** (unified wrapper) — `registry_guard --strict` + `count_sync`
3. **evidence_guard --staged --strict** — every `file:line` resolves
4. **law13_path_guard** — every cited path has a home (advisory)
5. **license advisory** — reminds to fill `License-check` on manifest changes (Law 15)

Exit 1 on any violation. Zero dependencies beyond Python 3.12+ and gitleaks.

---

## The 16 Binding Laws

> Source: `AGENTS.md:10` — the supreme covenant. Any modification voids the session.

| # | Law | Title | Penalty |
|---|-----|-------|---------|
| 1 | Proportional Flow | every request enters through gateway; 3-lane proportional | L4 bypass / L3 Fateful downgrade |
| 2 | Room Isolation | no cross-room direct addressing (use `context-map.yaml` + ticket bus) | L3 |
| 3 | Hierarchical Handoff | `agent → room lead → brd-ceo → user` | L3/L4 |
| 4 | Evidence Required | every delivery has `file:line` + `exit code` + log/screenshot | L2 |
| 5 | RCCF Mandatory | Request → Clarify → Confirm → Fullfil — no execution without it | L2 |
| 6 | Board Advisory | CEO consults Board on Fateful via Task; final decision is CEO's | L3 |
| 7 | Memory Binding | org `hq/brain/` ↔ project `projects/<slug>/brain/` — never mix | L1 then L2 |
| 8 | Quality Before Speed | no delivery without review; no review without evidence | L1 |
| 9 | Chain of Responsibility | agent → lead → CEO → system halt | escalation |
| 10 | Direct-on-Project (v2) | main tree only; ephemeral branches ≤72h with sandbox + merge-before-close | L2 worktree |
| 11 | Owner Communication Standard | owner is Arabic, non-technical; simple Arabic explaining *why it matters* | L1 then L2 |
| 12 | Registry Invariant | `registry.yaml` = 17 rooms · 121 agents; any generation must match or fail loudly | guard fail |
| 13 | Zero-Randomness | triple engine · continuous `TODO/Phase-NN` numbering · `## FILE: <path>` header · kebab-case · old←new map | L2/L3 |
| 14 | Double-Rejection Protocol | rejection 2× same reason = freeze → `brd-arbiter` 24h binding | L2 |
| 15 | License & IP Gate | no merge without `sec-license-auditor` check (allowed: MIT/Apache/BSD/ISC/MPL; vetoed: GPL/AGPL/SSPL/unknown) | L2 then L3 |
| 16 | Smart Clarification Loop | ambiguity > 20% = halt + 1–3 sharp questions + 24h timeout → `brd-arbiter` | L2 |

**Violation levels:** L1 yellow (warning + immediate correction) · L2 orange (mandate + notify lead) ·
L3 red (freeze + escalate to CEO) · L4 black (system halt + mandatory restart).

---

## The 17 Protocols

> Source: `hq/core/protocols.md` — operational law descending from the constitution.

| ID | Name |
|----|------|
| **P-01** | Pipeline Protocol (10 rules: P-01.1 mandatory entry → P-01.10 24h clarification timeout + anti-paralysis) |
| **P-02** | Handoff Protocol (5 rules + JSON ticket ≤280 chars) |
| **P-03** | Evidence Protocol |
| **P-04** | Escalation Protocol |
| **P-05** | Conflict Protocol |
| **P-06** | Memory Protocol (with P-06.7 summarizer ritual) |
| **P-07** | Communication Protocol |
| **P-08** | Security Protocol (P-08.1 secrets) |
| **P-09** | Quality Protocol |
| **P-10** | Emergency Protocol (incident response) |
| **P-11** | Tool Protocol |
| **P-12** | Token Economy Protocol |
| **P-13** | Gate Protocol (0→1→2→3→4→5→6→7→8 — immutable sequence) |
| **P-14** | Memory Isolation Protocol (Law 7 binding) |
| **P-15** | retired (2026-07-16) |
| **P-16** | Direct-on-Project Protocol (Law 10 v2) |
| **P-17** | Context Minimization Protocol |
| **P-18** | Visual Research Protocol (research before design · no verbatim copying · design-system integration) |
| **P-19** | Research-to-Design Bridge Protocol (P-19.1 mandatory handoff · P-19.5 joint Gate-1/DFR co-sign) |
| **P-20** | Living Documentation & Failure Mode Protocol (P-20.1 living docs · P-20.2 weekly backup · P-20.3 failure mode review) |

**Priority chain:** Pipeline (01) > Security (08) > Emergency (10) > Handoff (02) > Direct-on-Project (16) >
Context Minimization (17) > Quality (09) > Gate (13) > Evidence (03) > Memory Isolation (14) > Escalation (04) >
Conflict (05) > Memory (06) > Communication (07) > Tool (11) > Token Economy (12).

A lower-priority protocol cannot override a higher-priority one. A protocol that contradicts the
constitution is void.

---

## The 26 Standards

> Source: `hq/core/standards/`.

| Standard | Purpose |
|----------|---------|
| `api-envelope.md` | unified API response wrapper — every API uses it |
| `ddd-capsule.md` + `tech_templates/ddd-capsule-protocol.md` | DDD layer rules + DO/DON'T table |
| `deploy-standard.md` | Caddy + PHP-FPM + Cloudflare + Laravel + Flutter/React&Next |
| `latest-version-mandatory.md` | Context7 + DeepWiki before any code |
| `pipeline-production-line.md` | S1→S6 in detail |
| `stacks-tech.md` | R2 legacy + locked stacks |
| `uiux-standard.md` | UI/UX + Protocol 18 (visual feeding) |
| `room-dod-and-execution-rules.md` | per-room DoD + execution rules |
| `kpi-thresholds.md` | K1–K17 (hard rules K6/K11/K14/K16/K17 block Gate-8) |
| `reporting-cadence.md` | on-merge · on-incident-close · on-session-end |
| `structure-standard.md` | naming + old←new map (Law 13.5) |
| `file-discipline.md` (in `hq/training/`) | file discipline |
| `knowledge-cx-uiux.md` | UX + knowledge |
| `living-docs.md` | doc freshness (max 1 commit lag) — Audit-ALL |
| `qa-assessment-matrix.md` | 20/28/22 points + shared criteria (Perf/Security/A11y) — Audit-ALL |
| `installer-standard.md` | env setup rules |
| `room-meetings-standard.md` | meeting cadence |
| `devops-standard.md` | DevOps conventions |
| `mcp-registry.md` | MCP server registry |
| `mcp-communication-standard.md` | MCP bus rules |
| `ddd-full-cycle-playbook.md` (in `hq/training/`) | full DDD cycle |
| `latest-tech-2026.md` | tech currency |
| `glossary-ar.md` (planned in 08-localization) | Arabic glossary |
| `voice-and-tone.md` (planned in 08-localization) | Law 11 voice |
| `design-system-tokens` (planned in 03-design) | tokens schema |
| `permissions/RCCF` | RCCF central registry |

---

## Extending the System

### Adding a new agent

1. Read `hq/core/templates/agent-prompt-template.md`
2. Create `.opencode/agent/<name>.md` with frontmatter (name · description · mode · model)
3. Add capsule: `hq/core/domain/rooms/<room>/agents/<name>/{capabilities,senses,memory}.yaml`
4. Add row to `hq/core/nexus/registry.yaml:200+` (in correct room)
5. Add block to `hq/core/nexus/personas.yaml` (Arabic name + role)
6. Add block to `hq/core/nexus/routing.yaml` (model + effort + budget)
7. Add row to room `charter.md` + bump `Agent count:`
8. Add row to `.opencode/skills/INDEX.md` if new skill
9. Bump `hq/core/tooling/registry_guard.py:20` (SKILLS_BASELINE) + `count_sync.py:23` (AGENTS_HDR_REQUIRED)
10. Bump `AGENTS.md:62,256` + `hq/core/nexus/registry.yaml:3,11` + `room-priority.yaml:11`
11. Record ADR in `hq/brain/cortex-decisions.md` + SES in `hippocampus-sessions.md`
12. Update `SOFI-INSTITUTION-COMPLETE-REPORT-2026-09-05.md` on desktop
13. Commit atomically — pre-commit enforces all 4 guards

### Adding a new skill

1. Read `skill-forge` meta-skill
2. Create `.opencode/skills/<name>/SKILL.md` with frontmatter (name · description · when · inputs · steps · outputs · handoff · constraints · memory · refs)
3. Add row to `.opencode/skills/INDEX.md`
4. Bump `SKILLS_BASELINE` in both guards

### Adding a new MCP server

1. Use `sec-mcp-vetting` skill to vet the server (mandatory — Law + sec gate)
2. Add to `hq/core/nexus/mcp-routing.yaml`
3. Add to `opencode.json`
4. Update `sofi-mcp-fleet` documentation

### Creating a new project

```bash
# Use the project-spawn skill
"sofi-project-spawn my-new-project"
```

→ creates `projects/my-new-project/brain/{CONTEXT,DECISIONS,HANDOFFS,LESSONS}.md` + template stack.

---

## Developer Guidelines

1. **Read the constitution first:** `AGENTS.md:1`
2. **Check the binding state:** `hq/core/system-state-current.md:1`
3. **Check the quick reference:** `hq/core/SOFI-QUICK-REFERENCE.md` (1 page)
4. **For new agents/skills:** use the `skill-forge` meta-skill
5. **For new projects:** use `sofi-project-spawn`
6. **For fateful decisions:** open a Board consult — never decide alone
7. **Run guards before commit:** `bash hq/core/tooling/hooks/pre-commit` (or just commit — hook is installed)
8. **Document in CORTEX:** every fateful decision gets an ADR; every session gets a SES entry
9. **Arabic, simple, owner-facing:** Law 11 — every owner communication explains *why it matters*
10. **No shortcuts:** Law 5 (RCCF) + Law 8 (quality before speed) + Law 4 (evidence) + Law 10 (main tree) + Law 12 (registry invariant) + Law 13 (zero randomness) + Law 15 (license)

---

## Troubleshooting & FAQ

**Q: A guard is red — what do I do?**
A: Read the error message — it tells you exactly which file:line is wrong. Then either:
- Update `registry.yaml` to match the disk
- Add the missing agent file
- Fix the file:line citation
- Revert the offending commit (do not amend force-push)

**Q: `pre-commit` failed mid-commit — what now?**
A: `git status` to see staged files, fix the issue, `git add`, `git commit --amend --no-edit` (only if not pushed yet).

**Q: How do I add a new Law?**
A: You can't (alone) — Law modification requires **brd-ceo approval** + CORTEX record + constitutional review. See AGENTS.md final section.

**Q: How do I get my PR merged faster?**
A: Follow the 4 owner approval points + ensure all 4 guards are green + write a clear PR description with file:line evidence.

**Q: The owner wrote in informal Arabic — do I respond informally?**
A: **Yes** for tone, **no** for substance. Use simple Arabic (Law 11) but keep constitutional precision. The "why it matters" focus is required.

**Q: Can I use Vue.js / Angular / Symfony / raw PHP?**
A: **No.** Stack Lock R3 forbids them. The only path is owner directive recorded in CORTEX. Don't ask twice.

**Q: Why so many protocols? Isn't this bureaucracy?**
A: It's not bureaucracy — it's **legibility**. Every step has a `file:line` proof. When something breaks (and it will), the postmortem is trivial because the trail exists. The alternative is "works on my machine" debugging.

**Q: Can I use a paid API?**
A: **No.** INT-0003 auto-rejects. Every tool must be free. If you need a paid one, the answer is no + find the free alternative.

---

## Versioning & History

| Date | Tag | Summary |
|------|-----|---------|
| 2026-08-25 | `system-state-current` | sakk-only cleanup · root simplification · institutional memory archived |
| 2026-08-26 | `R3 + operational gaps` | +3 agents (str-agile-orchestrator · ops-sandbox-executor · sec-license-auditor) + Laws 14/15/16 |
| 2026-08-26 | `priority & cadence` | T0..T4 tiers · K1–K17 · incident runbooks |
| 2026-08-26 | `core-five rooms` | +2 agents in 04 (security-architect · performance-architect) |
| 2026-08-26 | `visual research` | Protocol 18 + +3 agents (scout/competitive/Arabic-UX) + 3 skills |
| 2026-08-26 | `rejected audit` | 15-room comprehensive audit rejected — already-implemented overlaps + off-stack hires |
| 2026-08-26 | `unified DoD` | standards/room-dod-and-execution-rules.md (derivative reference) |
| 2026-08-31 | `9-axis fix` | registry_guard · count_sync · evidence_guard · gitleaks · bootstrap-live · pre-commit · 16/114/109 |
| 2026-08-31 | `R3.1` | 14 rooms (08-Data merged into 04-Architecture) · 114 → 108 agents · 109 skills · 16 laws |
| 2026-08-31 | `SOFI 1.0` | final R3.1 + Phase-B acceptance (DEC-R3.4) |
| 2026-09-04 | `visual diagrams` | 9 Mermaid diagrams + 18 mirrors |
| 2026-09-05 | `qa-flutter-architect` (Rayan Al-Qadi) | first stack-specialist tester in Room 10 — 20 acceptance points |
| 2026-09-05 | `qa-react-architect` (Samer Al-Khalil) | React/DDD + Web Vitals — 28 points |
| 2026-09-05 | `qa-laravel-architect` (Yousuf Al-Amiri) | Laravel 11+ / DDD / DB / Security — 22 points |
| 2026-09-05 | `Audit-ALL` | SOFI-Quick-Reference · P-19/20 · WarRoom 15 · RCCF Registry · Living Docs · QA Matrix |
| 2026-09-05 | `Audit-ALL-Phase2` | Localization 08 (4) + Innovation 16 (2) — 17 rooms · 121 agents |
| 2026-09-05 | `Audit-ALL-Phase3` | redistribute 04 (ml→inn · privacy→loc) + 3 new skills + zero pending + sofi-audit — 17/121/116 |
| 2026-09-05 | `GitHub merge #1` | first public release on `3rafat000-alt/sofi-hq` (squash commit b585ec9) |

---

## License & Contributing

**License:** see `LICENSE` (project root). SOFI HQ is constitution-governed; contributing requires
following the 4 owner approval points + the 4 constitutional guards + the 16 laws.

**Owner authority:** any modification to the constitution (AGENTS.md) requires the explicit
recorded decision of `brd-ceo` in `hq/brain/cortex-decisions.md`. The owner (highest authority) can
override any decision via direct order, also recorded in CORTEX.

**Contributing:**
1. Fork `3rafat000-alt/sofi-hq`
2. Create a feature branch (`feature/<scope>-<ticket-id>`, ≤72h per Law 10)
3. Follow the 4 owner approval points + 4 constitutional guards
4. Open a PR — CI runs the guards automatically
5. Wait for `brd-ceo` review and merge

**Contact (model):** see `identity/sofi-system-identity.md` for the public-facing identity.

---

> **Final note (Law 11 + AGENTS.md:1):** SOFI is not for you to "run" — SOFI is for you to *operate within*.
> The constitution governs; the laws bind; the guards enforce. When in doubt, escalate upward.
> When angry, escalate upward. When lost, read the **SOFI-Quick-Reference** first
> (`hq/core/SOFI-QUICK-REFERENCE.md`). When you break a law, log it in CORTEX. When you fix one,
> log the fix. Every action has a `file:line` proof. **Welcome to the org.** 🟢
