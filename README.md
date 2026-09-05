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

### Part 1 — Orientation
1. [What is SOFI HQ?](#1-what-is-sofi-hq)
2. [The Big Picture (Visual)](#2-the-big-picture)
3. [The 3-Lane Proportional Flow](#3-the-3-lane-proportional-flow-law-1)
4. [Key Metrics](#4-key-metrics)

### Part 2 — The Constitution
5. [The 16 Binding Laws](#5-the-16-binding-laws)
6. [The 17 Protocols](#6-the-17-protocols)
7. [The 4 Constitutional Guards](#7-the-4-constitutional-guards)

### Part 3 — The Organization Structure
8. [The 17 Rooms (Complete Table)](#8-the-17-rooms)
9. [The 4 Priority Tiers (T0–T4)](#9-the-4-priority-tiers)
10. [The 121 Agents (Per-Room Inventory)](#10-the-121-agents)
11. [The 116 Skills (Catalog)](#11-the-116-skills)

### Part 4 — How It Works
12. [The S1→S6 Production Line](#12-the-s1s6-production-line)
13. [The 9 Gates + DFR](#13-the-9-gates--dfr)
14. [The 4 Owner Approval Points](#14-the-4-owner-approval-points)
15. [The 26 Standards](#15-the-26-standards)

### Part 5 — Operations
16. [Memory: CORTEX / HIPPOCAMPUS / AMYGDALA](#16-memory)
17. [The MCP Fleet (27 servers, 100% local)](#17-the-mcp-fleet)
18. [The Hierarchical Handoff Path](#18-the-hierarchical-handoff-path)
19. [Tickets: RCCF + the JSON Bus](#19-tickets-rccf--the-json-bus)

### Part 6 — Stack & Domain
20. [Tech Stack & Stack Lock R3](#20-tech-stack--stack-lock-r3)
21. [The Latest-Version-Mandatory Rule](#21-the-latest-version-mandatory-rule)
22. [The 27 MCP Servers (Room Distribution)](#22-the-27-mcp-servers)

### Part 7 — Room-by-Room Deep Dives
23. [Room 00 — Boardroom](#23-room-00--boardroom)
24. [Room 14 — Gateway](#24-room-14--gateway)
25. [Room 01 — Strategy](#25-room-01--strategy)
26. [Room 02 — Research](#26-room-02--research)
27. [Room 04 — Architecture](#27-room-04--architecture)
28. [Room 03 — Design](#28-room-03--design)
29. [Room 08 — Localization](#29-room-08--localization)
30. [Room 16 — Innovation](#30-room-16--innovation)
31. [Room 05 — Backend](#31-room-05--backend)
32. [Room 06 — Frontend](#32-room-06--frontend)
33. [Room 07 — Mobile](#33-room-07--mobile)
34. [Room 09 — Security](#34-room-09--security)
35. [Room 10 — Quality (10 testers)](#35-room-10--quality-10-testers)
36. [Room 11 — DevOps](#36-room-11--devops)
37. [Room 12 — Observability](#37-room-12--observability)
38. [Room 15 — WarRoom](#38-room-15--warroom)
39. [Room 13 — Knowledge](#39-room-13--knowledge)

### Part 8 — Worked Scenarios
40. [Scenario 1: The Owner Wants an Online Store](#40-scenario-1-the-owner-wants-an-online-store)
41. [Scenario 2: A P0 Production Incident](#41-scenario-2-a-p0-production-incident)
42. [Scenario 3: Adding a New Specialist Tester](#42-scenario-3-adding-a-new-specialist-tester)
43. [Scenario 4: A Fateful Decision (Board Consult)](#43-scenario-4-a-fateful-decision-board-consult)
44. [Scenario 5: Smart Clarification Loop (Owner Asks Vague Question)](#44-scenario-5-smart-clarification-loop)

### Part 9 — Setup, Run, Extend
45. [Requirements & Dependencies](#45-requirements--dependencies)
46. [Installation & Setup](#46-installation--setup)
47. [Running & Usage Examples](#47-running--usage-examples)
48. [Extending the System](#48-extending-the-system)
49. [Developer Guidelines](#49-developer-guidelines)

### Part 10 — Reference & History
50. [Versioning & History (Full Timeline)](#50-versioning--history)
51. [Troubleshooting & FAQ](#51-troubleshooting--faq)
52. [License & Contributing](#52-license--contributing)

---

# Part 1 — Orientation

## 1. What is SOFI HQ?

SOFI HQ is **a complete AI software company** simulated inside a single Git repository. It is not
a chatbot, not a coding assistant, not an IDE plugin. It is an *organization* with:

- A **constitution** (16 binding laws) at `AGENTS.md:10` that every agent must obey
- **17 rooms** (specialized departments) with charters and capsule contracts
- **121 agents** (employees) with identity, responsibilities, constraints, and team-collaboration rules
- **116 skills** (operating manuals) for every room and most agents
- A **4-tier priority** system (T0 spine → T1 paper → T2 code → T3 shield → T4 memory)
- An **S1→S6 production line** that takes a raw idea and ships it without code-before-design
- **9 gates + DFR** (Design-Freeze Review) that block bad work
- **4 constitutional guards** (machine-checked) that block bad commits
- **2 memory stores** (org + project) that are strictly isolated
- **27 MCP servers** (all local, no paid API) for context, planning, and tooling

**The owner is Arabic-speaking and non-technical** (Law 11). The constitution guarantees that every
direct communication to the owner is in **simple Arabic explaining why it matters**, not jargon.

## 2. The Big Picture

```
                   ┌──────────────────────────────────────┐
                   │  OWNER (Arabic, non-technical)      │  ← Law 11
                   └──────────────────┬───────────────────┘
                                      │ "I want X"
                                      ▼
                   ┌──────────────────────────────────────┐
                   │  gtw-intake-reformer  (room 14)      │  ← Law 1: every request enters here
                   │  · 5-section reformulation           │
                   │  · Law 16 ambiguity score (≤20%)    │
                   │  · budget + conflict check            │
                   └──────────────────┬───────────────────┘
                                      │ Intake Report
                                      ▼
                   ┌──────────────────────────────────────┐
                   │  P-01.8 lane classification:          │  ← single authoritative text
                   │  🟢 Fast  🟡 Standard  🔴 Fateful    │
                   └────┬──────────┬──────────┬──────────┘
                        │          │          │
                  (read/scan)  (feature  (money/security)
                              1-2 rooms)
                        │          │          │
                  one lead   brd-ceo   brd-ceo + Board
                        │          │          │
                        └──────────┴──────────┘
                                      │
                                      ▼
            ┌────────────────────────────────────────────────────┐
            │  S1 → S2 → S3 → S4 → S5 → S6                       │
            │  paper  paper paper  code  code  shield            │
            │  (01)   (04)  (03)   (05)  (06/07)  (09-13)        │
            │  PRD    ERD   DFR    API   UI    deploy+monitor   │
            │  G1     G3    DFR    G4    G4b    G5/G6/G7/G8      │
            └─────────────────────┬──────────────────────────────┘
                                  │
                                  ▼
            ┌────────────────────────────────────────────────────┐
            │  Memory:                                            │
            │  · CORTEX  (decisions/ADRs)         hq/brain/       │
            │  · HIPPOCAMPUS (sessions)           hq/brain/       │
            │  · AMYGDALA  (incidents)            hq/brain/       │
            │  · projects/<slug>/brain/ (separate, per project)  │
            └────────────────────────────────────────────────────┘
```

## 3. The 3-Lane Proportional Flow (Law 1)

The flow is **strictly hierarchical and 3-lane proportional**. Not every request needs the full pipeline.

| Lane | Trigger | Flow | Token Budget | Gates |
|------|---------|------|--------------|-------|
| 🟢 **Fast** | read/scan/query · trivial reversible single-file change | `intake → 1 lead → delivery` | 10K | evidence only |
| 🟡 **Standard** | feature/change spanning 1–2 rooms | `intake → brd-ceo → lead(s) → agents → lead → brd-ceo → user` | 100K | L8 quality |
| 🔴 **Fateful** | money / security / architecture / production / schema / irreversible | full flow + Board consult + CSO veto | 500K | complete |

**Hard guardrails:**
- **Money / Security / Production / Schema = ALWAYS Fateful**, never Fast, regardless of size (violation = L3)
- **Doubt escalates upward** (fail-safe toward rigor)
- **Promotion ascends, never descends** — discovering higher risk mid-execution → immediate promotion
- **Skip the room lead = L3** on any lane
- **Skip the CEO on Standard/Fateful = L3**
- **Responding without intake = L4**

## 4. Key Metrics

| Metric | Value | Source |
|--------|-------|--------|
| **Rooms** | 17 | `hq/core/nexus/registry.yaml:11` |
| **Agents** | 121 (1:1 with disk) | `registry.yaml:11` + `.opencode/agent/*.md` |
| **Skills** | 116 | `.opencode/skills/*/SKILL.md` |
| **Laws** | 16 | `AGENTS.md:10` |
| **Protocols** | 17 (P-01..P-20) | `hq/core/protocols.md` |
| **Standards** | 26 | `hq/core/standards/` |
| **Gates** | G0..G8 + DFR | `hq/core/nexus/gates.yaml` |
| **MCP servers** | 27 (100% local) | `hq/core/nexus/mcp-routing.yaml` |
| **Constitutional guards** | 4 (registry · count_sync · evidence · gitleaks) | `hq/core/tooling/` |
| **Memory stores** | 2 (org `hq/brain/` + project `projects/<slug>/brain/`) | Law 7 |
| **Visual diagrams** | 9 Mermaid (3 sets: source + SVG + PNG) | `hq/core/design/diagrams/` |
| **Active project** | sakk (mobile Flutter + web React/Vite + Laravel) | `projects/sakk/` |
| **GitHub** | `3rafat000-alt/sofi-hq` (public) | `git remote -v` |
| **PENDING warnings** | **0** (zero — all 4 guards green) | post-Audit-ALL-Phase3 |
| **Audit score** | ~96/100 | constitutional self-audit |

---

# Part 2 — The Constitution

## 5. The 16 Binding Laws

> Source: `AGENTS.md:10` — the supreme covenant. Any modification requires `brd-ceo` approval
> recorded in `hq/brain/cortex-decisions.md` (Law 12).

| # | Law | Title | One-line summary | Penalty |
|---|-----|-------|------------------|---------|
| 1 | Proportional Flow | `gtw-intake-reformer` for every request, 3-lane proportional | L4 bypass / L3 Fateful downgrade |
| 2 | Room Isolation | No cross-room direct addressing — use `context-map.yaml` + ticket bus | L3 |
| 3 | Hierarchical Handoff | `agent → room lead → brd-ceo → user` — no skip, no sideways | L3/L4 |
| 4 | Evidence Required | Every delivery: `file:line` + `exit code` + log/screenshot | L2 |
| 5 | RCCF Mandatory | Request → Clarify → Confirm → Fullfil — no execution without it | L2 |
| 6 | Board Advisory | CEO consults Board (`brd-*`) on Fateful via Task; final decision is CEO's | L3 |
| 7 | Memory Binding | org `hq/brain/` ↔ project `projects/<slug>/brain/` — never mix | L1 → L2 |
| 8 | Quality Before Speed | No delivery without review; no review without evidence | L1 |
| 9 | Chain of Responsibility | agent → lead → CEO → system halt (escalation chain) | escalation |
| 10 | Direct-on-Project (v2) | main tree only; ephemeral branches ≤72h with sandbox + merge-before-close | L2 worktree |
| 11 | Owner Communication Standard | owner is Arabic, non-technical; simple Arabic explaining *why it matters* | L1 → L2 |
| 12 | Registry Invariant | `registry.yaml` = 17 rooms · 121 agents; any generation must match or fail loudly | guard fail |
| 13 | Zero-Randomness | triple engine · continuous `TODO/Phase-NN` numbering · `## FILE: <path>` header · kebab-case · old←new map | L2/L3 |
| 14 | Double-Rejection Protocol | rejection 2× same reason = freeze → `brd-arbiter` 24h binding | L2 |
| 15 | License & IP Gate | no merge without `sec-license-auditor` check (allowed: MIT/Apache/BSD/ISC/MPL; vetoed: GPL/AGPL/SSPL/unknown) | L2 → L3 |
| 16 | Smart Clarification Loop | ambiguity > 20% = halt + 1–3 sharp questions + 24h timeout → `brd-arbiter` | L2 |

**Violation levels:** L1 yellow (warning + immediate correction) · L2 orange (mandate + notify lead) ·
L3 red (freeze + escalate to CEO) · L4 black (system halt + mandatory restart).

## 6. The 17 Protocols

> Source: `hq/core/protocols.md` — operational law descending from the constitution. P-15 retired.

| ID | Name | Purpose | One-line trigger |
|----|------|---------|------------------|
| **P-01** | Pipeline Protocol | 10 rules: P-01.1 mandatory entry · P-01.2 3-lane proportional · P-01.8 single authoritative text · P-01.10 24h clarification timeout + anti-paralysis | every session starts at intake |
| **P-02** | Handoff Protocol | 5 rules + JSON ticket ≤280 chars + checkpoint before handoff (P-02.1) + explicit acceptance (P-02.4) | every agent→lead handoff |
| **P-03** | Evidence Protocol | every delivery has `file:line` + `exit code` + log | every delivery |
| **P-04** | Escalation Protocol | agent → lead → CEO → system halt (Law 9) | every escalation |
| **P-05** | Conflict Protocol | request conflict detected → `gtw-conflict-resolver` settles | duplicate requests |
| **P-06** | Memory Protocol | with P-06.7 summarizer ritual (knw-reflector every 10 turns) | memory writes |
| **P-07** | Communication Protocol | ticket bus + JSON + `note` ≤280 chars | cross-room comm |
| **P-08** | Security Protocol | P-08.1 secrets (gitleaks pre-commit) | every commit |
| **P-09** | Quality Protocol | K1–K17 thresholds · Gate-5 verdict (qa-lead + brd-cqo) | S6 |
| **P-10** | Emergency Protocol | incident response · WarRoom · AMYGDALA log within 24h | P0 incident |
| **P-11** | Tool Protocol | `sofi-audit` wrapper · 4 guards · pre-commit hook | every commit |
| **P-12** | Token Economy | model routing per task class (workhorse/gatekeeper) | every agent |
| **P-13** | Gate Protocol | 0→1→2→3→4→5→6→7→8 — immutable sequence; Fast-Track may collapse 1–3 with brd-ceo | every stage transition |
| **P-14** | Memory Isolation | Law 7 binding — org vs project | every memory write |
| **P-16** | Direct-on-Project | Law 10 v2 — main tree only · ephemeral branches ≤72h | every commit |
| **P-17** | Context Minimization | JSON ticket ≤280 chars + evidence digest | every ticket |
| **P-18** | Visual Research | research before design · no verbatim copying · design-system integration (P-18.1–18.5) | every new screen |
| **P-19** | Research-to-Design Bridge | P-19.1 mandatory handoff · P-19.2 traceability `file:line` · P-19.3 persona→flow · P-19.5 joint Gate-1/DFR co-sign | every 02→03 handoff |
| **P-20** | Living Docs & Failure Mode | P-20.1 living docs (max 1 commit lag) · P-20.2 weekly brain backup · P-20.3 monthly failure mode review | every Fateful/Standard change |

**Priority chain:** `Pipeline (01) > Security (08) > Emergency (10) > Handoff (02) > Direct-on-Project (16) > Context Minimization (17) > Quality (09) > Gate (13) > Evidence (03) > Memory Isolation (14) > Escalation (04) > Conflict (05) > Memory (06) > Communication (07) > Tool (11) > Token Economy (12)`

A lower-priority protocol cannot override a higher-priority one. A protocol that contradicts the
constitution is **void**.

## 7. The 4 Constitutional Guards

Every commit is checked by 4 machine guards (`hq/core/tooling/hooks/pre-commit`). Each one enforces
a specific law.

| Guard | File | Law | What it checks | Threshold |
|-------|------|-----|----------------|-----------|
| `registry_guard` | `hq/core/tooling/registry_guard.py:1` | Law 12 | `.opencode/agent/*` ↔ `registry.yaml` rooms/agents **1:1** | exit 0 + zero pending |
| `count_sync` | `hq/core/tooling/count_sync.py:1` | Law 12/13 | derived vs declared (registry meta) vs textual claims (AGENTS.md) vs disk | exit 0 + zero pending |
| `evidence_guard` | `hq/core/tooling/evidence_guard.py:1` | Law 4 | every `file:line` citation in the codebase resolves to a real file:line | exit 0 + 0 broken |
| `gitleaks` | `gitleaks.toml:1` (via pre-commit) | Law 8 + P-08.1 | no secrets in any staged file | exit 0 + "no leaks found" |

**Unified wrapper:** `hq/core/tooling/sofi-audit.py` chains `registry_guard` + `count_sync` into a
single command — used by pre-commit since Audit-ALL-Phase3. The originals remain callable independently.

**Law 13 path guard (advisory):** `hq/core/tooling/law13_path_guard.py` — every cited path has a home.

---

# Part 3 — The Organization Structure

## 8. The 17 Rooms

> Source: `hq/core/nexus/registry.yaml:1` + `hq/core/domain/rooms/<room>/charter.md` (one charter per room).

| # | Room | Code | Tier | Lead | Domain | Agents |
|---|------|------|------|------|--------|--------|
| 00 | **Boardroom** | 00-boardroom | T0 Spine | `brd-ceo` | governance + board advisory + CSO veto | 7 |
| 14 | **Gateway** | 14-gateway | T0 Spine | `gtw-dispatcher` | mandatory entry · lane classification · routing | 7 |
| 01 | **Strategy** | 01-strategy | T1 Paper | `str-lead` | PRD + MVP + roadmap | 8 |
| 02 | **Research** | 02-research | T1 Paper | `res-lead` | JTBD personas + journey maps + competitive | 6 |
| 04 | **Architecture** | 04-architecture | T1 Paper | `arc-lead` | system design + API freeze + DDD + ERD | 13 |
| 03 | **Design** | 03-design | T1 Paper | `dsn-lead` | UX + design system + DFR sign-off | 8 |
| 08 | **Localization** | 08-localization | T1 Paper | `loc-translation-manager` | Arabic translation + RTL + voice & tone + privacy | 5 |
| 16 | **Innovation** | 16-innovation | T1 Paper | `inn-lab-lead` | tech scouting + PoCs + ML sandbox | 3 |
| 05 | **Backend** | 05-backend | T2 Code | `bck-lead` | Laravel 11+ · S4 | 8 |
| 06 | **Frontend** | 06-frontend | T2 Code | `fnt-lead` | React 18+ + Tailwind 4+ · S5 | 7 |
| 07 | **Mobile** | 07-mobile | T2 Code | `mob-lead` | Flutter 3.22+ + Dart 3+ · S5 | 6 |
| 09 | **Security** | 09-security | T3 Shield | `sec-lead` | STRIDE + pentest + license + secrets | 9 |
| 10 | **Quality** | 10-quality | T3 Shield | `qa-lead` (Lama Al-Tarabulsi) | test plans + automation + Gate-5 + DFR | 10 |
| 11 | **DevOps** | 11-devops | T3 Shield | `ops-lead` | CI/CD + cloud + release + sandbox | 8 |
| 12 | **Observability** | 12-observability | T3 Shield | `obs-lead` | metrics + logs + SLOs + incidents | 6 |
| 15 | **WarRoom** | 15-warroom | T3 Shield | `war-incident-commander` | P0 incident command · on-call | 4 |
| 13 | **Knowledge** | 13-knowledge | T4 Memory | `knw-lead` | CORTEX + HIPPOCAMPUS + AMYGDALA | 6 |

**Total: 17 rooms · 121 agents · 121 capsule directories** (1:1 with registry).

## 9. The 4 Priority Tiers

> Source: `hq/core/nexus/room-priority.yaml:v2`.

| Tier | Order | Description | Activation | Exit |
|------|-------|-------------|------------|------|
| **T0 Spine** | always-on | The sovereign spine: 14 (intake) + 00 (board). Every request enters via 14; every escalation ends at 00. | `any inbound request or escalation` | Never — spine is permanent |
| **T1 Paper** | 1 | Paper stages only. No executable code may exist while any T1 artifact is open. Sequence: 01→02→04→03 (with 08 + 16 in parallel). | `lane classification complete` | DFR signed (09 + 10 stamps) |
| **T2 Code** | 2 | Code stages. Activate only after T1 exits clean. HARD RULE: backend (05) complete, running, security-checked BEFORE any UI line. Frontend (06) and Mobile (07) start together as one merged team on the FROZEN OpenAPI contract. | `DFR signed + OpenAPI frozen` | all routes implemented + security passed + tests green |
| **T3 Shield** | continuous | Continuous shield across ALL tiers. Veto powers apply ANYWHERE: 09 (security), 10 (quality Gate-5), 11 (deploy), 12 (observability), 15 (WarRoom P0). | `any change touching security/data/production/schema` | Never — shield is permanent |
| **T4 Memory** | passive | Room 13 logs every decision/session/incident. | `every decision` | Never — memory is permanent |

**Lane → Tier mapping:**
- 🟢 Fast → `T0 → single lead → delivery` (may skip DFR for trivial docs)
- 🟡 Standard → `T0 → T1 subset → T2 (1-2 rooms) → T3 gate → delivery` (DFR + Gate-5 for non-trivial)
- 🔴 Fateful → `Full S1→S6 flow + Board (cso veto) + zero shortcuts` (all gates + all evidence + all memory)

## 10. The 121 Agents

> Source: `hq/core/nexus/registry.yaml:11` + `.opencode/agent/<name>.md` + `hq/core/nexus/personas.yaml`.

Each agent has:
- a **frontmatter** (name · description · mode · model)
- an **Identity** (Arabic name + role + skills + mindset)
- 7 **Responsibilities**
- a **Constraints** block (advisory/no-gate · scope · command whitelist · no other-room)
- a **Team Collaboration** section (inputs / outputs / escalation)
- 1–3 **available skills** (constitutionally wired: `sofi-evidence` + `sofi-handoff` + room playbook)

### Room 00 — Boardroom (7 agents)
| Agent | Role |
|-------|------|
| `brd-ceo` | Chief Executive · system governance · final decisions · Arabic owner liaison |
| `brd-cpo` | Chief Product · product vision · Gates 0-2 · feature priority · market fit |
| `brd-cto` | Chief Technology · technology strategy · Gates 3-4 · **architecture veto** · **stack lock** |
| `brd-cqo` | Chief Quality · quality standards · Gate 5 · coverage thresholds · test design |
| `brd-cso` | Chief Security · **security veto (absolute)** · threat review · **DFR sign-off** · license audit |
| `brd-chief-of-staff` | Chief of Staff · decision-to-work-order conversion · RCCF drafting · cross-room coordination |
| `brd-arbiter` | Arbiter · **Law-14 disputes** · inter-room arbitration · **binding verdict within 24h** |

### Room 14 — Gateway (7 agents)
| Agent | Role |
|-------|------|
| `gtw-dispatcher` | **room lead** — supervises intake apparatus · tunes THALAMUS routing · team accountability |
| `gtw-router` | track selection (Fast/Standard/Fateful) · room assignment · conflict escalation |
| `gtw-gatekeeper` | **Law-16 ambiguity scoring** · clarification cards (1-3 questions) · threshold enforcement |
| `gtw-budget-warden` | resource envelope · spend limits · cost-aware routing |
| `gtw-conflict-resolver` | request conflict detection · priority arbitration · downgrade prevention |
| `gtw-external-reviewer` | third-party request vetting · external MCP review · trust scoring |
| `gtw-intake-reformer` (Kaisar Al-Ribat) | **5-section prompt reformulation** · Law-1 classification · **first touchpoint** |

### Room 01 — Strategy (8 agents)
| Agent | Role |
|-------|------|
| `str-lead` | **room lead** · MVP scoping · PRD sign-off |
| `str-product-strategist` | product vision · PRD authoring · feature decomposition |
| `str-business-analyst` | requirements elicitation · process modeling · stakeholder mapping |
| `str-market-analyst` | market sizing · TAM/SAM/SOM · trend signals |
| `str-roadmap-planner` | release sequencing · dependency mapping · milestone framing |
| `str-risk-analyst` | risk register · mitigation plans · fateful detection |
| `str-monetization-strategist` | revenue models · pricing tiers · unit economics |
| `str-agile-orchestrator` | WIP limits · cross-room blocker detection · flow metrics |

### Room 02 — Research (6 agents)
| Agent | Role |
|-------|------|
| `res-lead` | **room lead** · research dossier sign-off · **Gate-1 owner** |
| `res-ux-researcher` | personas (JTBD) · pain points · behavioral data |
| `res-journey-architect` | user journey maps · touchpoint analysis · usability scripts |
| `res-competitor-analyst` | market research pipeline · competitive matrix · SearXNG/Crawl4AI |
| `res-fact-checker` | evidence verification · source triangulation · claim validation |
| `res-visual-pattern-scout` | Mobbin/Page Flows scraping · pattern libraries · visual feeding (Protocol 18) |

### Room 04 — Architecture (13 agents — was 15, redistributed 2 in Phase 3)
| Agent | Role |
|-------|------|
| `arc-lead` | **room lead** · **ADR sign-off** · **Gate-3/4 owner** |
| `arc-system-architect` | system decomposition · bounded contexts · ADR authoring |
| `arc-api-architect` | **OpenAPI contract freeze** · REST/GraphQL design · envelope wrapper |
| `arc-data-architect` | **ERD design (paper-only)** · schema contract · **DDD context map** · On-event triggered |
| `arc-infra-architect` | cloud topology · network design · IaC patterns |
| `arc-integration-architect` | cross-context contracts · anti-corruption layer · event flows |
| `arc-review-architect` | design review · trade-off evaluation · migration plans |
| `arc-security-architect` | **STRIDE review (DFR mode)** · threat surface · zero-trust design |
| `arc-performance-architect` | **SLO design** · capacity planning · latency budgets |
| `arc-db-engineer` | PostgreSQL/MySQL design · index strategy · query plans |
| `arc-cache-engineer` | Redis 7+ patterns · cache invalidation · TTL strategy |
| `arc-etl-engineer` | pipeline design · batch/stream ETL · data contracts |
| `arc-analytics-engineer` | metrics pipelines · event taxonomy · dashboards |

### Room 03 — Design (8 agents)
| Agent | Role |
|-------|------|
| `dsn-lead` | **room lead** · **DFR owner** · sign-off authority |
| `dsn-ui-designer` | screen design · mockups · component specs |
| `dsn-design-system` | **3-layer tokens** · Tailwind theme · Storybook docs |
| `dsn-brand-designer` | brand identity · logo systems · visual language |
| `dsn-a11y-specialist` | **WCAG 2.2 audit** · a11y patterns · screen reader flows |
| `dsn-ux-architect` | UX flows · info architecture · interaction specs |
| `dsn-competitive-ui-analyst` | competitor UI teardown · design extraction |
| `dsn-arabic-ux-specialist` | **RTL mirror validation** · Arabic typography · cultural fit |

### Room 08 — Localization (5 agents — created Phase 2)
| Agent | Arabic name | Role |
|-------|-------------|------|
| `loc-translation-manager` | Noura Al-Hassan | **room lead** — translation memory · glossary · Arabic copy |
| `loc-cultural-adapter` | Khalid Al-Masri | cultural adaptation · imagery · examples |
| `loc-rtl-specialist` | Hadi Al-Quds | RTL validation · mirror · typography |
| `loc-voice-tone-expert` | Rana Al-Shami | voice & tone · **Law 11 Arabic simple** |
| `loc-privacy-officer` | Dirar Al-Khatib | **GDPR/LGPD** · PII Arabic copy · DPIA (added Phase 3) |

### Room 16 — Innovation (3 agents — created Phase 2 + Phase 3)
| Agent | Arabic name | Role |
|-------|-------------|------|
| `inn-lab-lead` | Ziad Al-Hariri | **room lead** — experiment design · ADR drafting · PoC |
| `inn-tech-scout` | Maya Al-Nouri | tech scouting · trend signals · PoC |
| `inn-ml-engineer` | Bushra Al-Amadi | **ML/AI experimentation** · Python 3.12+ · model serving · sandbox (added Phase 3 — moved from 04) |

### Room 05 — Backend (8 agents)
| Agent | Role |
|-------|------|
| `bck-lead` | **room lead** · API distribution · **S4 close-out** |
| `bck-api-engineer` | **Laravel 11+ controllers** · Form Requests · API resources |
| `bck-domain-engineer` | Eloquent models · domain services · DDD aggregates |
| `bck-blade-engineer` | Blade components · email views · server-rendered UI |
| `bck-queue-engineer` | Horizon jobs · Redis queues · retry/backoff |
| `bck-integration-engineer` | third-party APIs · webhooks · external adapters |
| `bck-code-reviewer` | PHP code review · Pint enforcement · PR quality gate |
| `bck-refactoring-surgeon` | legacy modernization · safe refactors · test-preserving edits |

### Room 06 — Frontend (7 agents)
| Agent | Role |
|-------|------|
| `fnt-lead` | **room lead** · component distribution · **S5 owner** |
| `fnt-react-engineer` | **React 18+ components** · hooks · state |
| `fnt-css-artisan` | **Tailwind 4+** utility composition · design tokens · responsive layouts |
| `fnt-interaction-engineer` | motion design · micro-interactions · GSAP/Framer |
| `fnt-performance-engineer` | **Core Web Vitals** · bundle audit · INP optimization |
| `fnt-a11y-engineer` | WCAG 2.2 · keyboard nav · screen reader · aria patterns |
| `fnt-code-reviewer` | React code review · ESLint rules · slop/AI-fingerprint scan |

### Room 07 — Mobile (6 agents)
| Agent | Role |
|-------|------|
| `mob-lead` | **room lead** · Flutter distribution · release coordination |
| `mob-flutter-engineer` | **Flutter 3.22+ widgets** · Dart 3+ · Riverpod/Bloc |
| `mob-platform-engineer` | Android/iOS native bridges · permissions · store config |
| `mob-state-engineer` | Riverpod/Bloc patterns · offline-first |
| `mob-perf-profiler` | frame analysis · jank detection · DevTools profiling |
| `mob-release-engineer` | store submission · versioning · OTA channels |

### Room 09 — Security (9 agents)
| Agent | Role |
|-------|------|
| `sec-lead` | **room lead** · cso delegate · **veto coordination** |
| `sec-pentester` | manual pen-testing · exploit PoC · attack surface mapping |
| `sec-appsec-engineer` | SAST/DAST · secure code review · **OWASP Top 10** |
| `sec-authn-engineer` | OAuth2/OIDC · JWT/Session · MFA design |
| `sec-compliance-auditor` | GDPR/SOC2/PCI · audit trails · data residency |
| `sec-incident-responder` | breach triage · forensics · postmortem |
| `sec-threat-modeler` | **STRIDE** · **DFR-mode mandatory review** · abuse cases |
| `sec-secrets-warden` | secrets scanning · vault hygiene · rotation policy |
| `sec-license-auditor` | **dependency license check (Law-15)** · copyleft veto · SBOM |

### Room 10 — Quality (10 agents — the testers)
| Agent | Arabic name | Specialty | Acceptance points | Stack |
|-------|-------------|-----------|-------------------|-------|
| `qa-lead` | لمى الطرابلسي | **Gate-5 + DFR** | — | cross |
| `qa-test-architect` | ياسمين العطاسي | test plans + Pest/PHPUnit | — | cross |
| `qa-automation-engineer` | نمير العطار | Playwright/Cypress | — | cross |
| `qa-manual-explorer` | هنادي النقري | exploratory | — | cross |
| `qa-perf-analyst` | هلال الجزائري | JMeter/k6 | — | cross |
| `qa-design-auditor` | نايا الأسفري | Nielsen + WCAG | — | cross |
| `qa-regression-warden` | وجدان الحلاق | regression suite | — | cross |
| `qa-flutter-architect` | **ريان القاضي** | Flutter 3.22+ + adb/uiautomator/gfxinfo/meminfo | **20** | mobile |
| `qa-react-architect` | **سامر الخليل** | React 18+/Next.js + DDD + Web Vitals | **28** | frontend |
| `qa-laravel-architect` | **يوسف العامري** | Laravel 11+ + DDD + DB + Security (N+1/EXPLAIN/Policies) | **22** | backend |

> **The 3 stack-specialist testers (qa-flutter / qa-react / qa-laravel) are ADVISORY ONLY.**
> They feed findings to Gate-5; the verdict belongs to `qa-lead` + `brd-cqo`. Never to them.
> This is the **C3 advisory-only clause** in every one of their agent files.

### Room 11 — DevOps (8 agents)
| Agent | Role |
|-------|------|
| `ops-lead` | **room lead** · ephemeral branch governance · **rollback owner** |
| `ops-cicd-engineer` | GitHub Actions/Jenkins · pipeline-as-code · **on-merge scans** |
| `ops-cloud-engineer` | AWS/GCP/Azure · Terraform/IaC · cost-aware scaling |
| `ops-cost-optimizer` | spend dashboards · rightsizing · reserved capacity |
| `ops-domain-warden` | DNS/TLS · edge config · domain hygiene |
| `ops-migration-runner` | DB migrations · safe rollout · **rollback windows** |
| `ops-release-manager` | release runbooks · change windows · comms |
| `ops-sandbox-executor` | isolated build/syntax gates · pre-QA sandboxing |

### Room 12 — Observability (6 agents)
| Agent | Role |
|-------|------|
| `obs-lead` | **room lead** · SLO governance · incident commander delegate |
| `obs-monitoring-engineer` | Prometheus/Grafana · metric design · dashboards |
| `obs-alerting-engineer` | alert rules · noise reduction · paging policy |
| `obs-sre` | SLO/SLI · error budgets · reliability reviews |
| `obs-incident-commander` | incident declaration · MTTR drive · **postmortem owner** |
| `obs-insights-analyst` | anomaly detection · cohort analysis · trend signals |

### Room 15 — WarRoom (4 agents — created Phase 1)
| Agent | Arabic name | Role |
|-------|-------------|------|
| `war-incident-commander` | Firas Al-Najjar | **room lead** — incident command · MTTR drive · **Law-14 freeze** · postmortem |
| `war-forensic-analyst` | Layla Al-Halabi | forensic evidence · log/trace preservation · timeline reconstruction |
| `war-rollback-engineer` | Omar Al-Khani | rollback windows · service revival · health checks |
| `war-communication-lead` | Salma Al-Rashid | crisis comms · **Arabic Law-11 liaison** · stakeholder updates |

### Room 13 — Knowledge (6 agents)
| Agent | Role |
|-------|------|
| `knw-lead` | **room lead** · brain-index owner |
| `knw-brain-query` | brain search (Law-7) · context recall |
| `knw-doc-writer` | ADR/RFC drafting · decision docs · RFC process |
| `knw-historian` | session log · audit trail · evolution records |
| `knw-memory-curator` | **CORTEX/HIPPOCAMPUS/AMYGDALA maintenance** · project vs org split |
| `knw-reflector` | on-incident-close lessons · retrospectives · Law-6 anti-loop feeds |

## 11. The 116 Skills

> Source: `.opencode/skills/INDEX.md` + `.opencode/skills/*/SKILL.md`.

Skills are **operating manuals** — each room + each new agent ships with one or more.

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

**3 skills added in Audit-ALL-Phase3:**
- `loc-rtl-adaptation` — Arabic localization & RTL protocol
- `inn-experiment` — Innovation experiment protocol
- `war-incident-runbook` — WarRoom P0 incident runbook

---

# Part 4 — How It Works

## 12. The S1→S6 Production Line

> Source: `hq/core/nexus/pipeline.yaml:8` + `hq/core/standards/pipeline-production-line.md`.

| Stage | Name | Rooms | Lead | Gate | Output | Can it ship code? |
|-------|------|-------|------|------|--------|-------------------|
| **S1** | Idea, Strategy & Research | 00·01·14·02 | `str-lead` | G1 | **PRD** in `projects/<slug>/brain/CONTEXT.md` | NO (paper only) |
| **S2** | Data & Contract Design (paper) | 04 | `arc-lead` | G3 | **ERD + schema-contract + frozen OpenAPI** (no code, no live DB) | NO (paper only) |
| **S3** | Experience & Visual System | 03 | `dsn-lead` | **DFR** | UX + design system + mockups + web/mobile mockups | NO (mockups only) |
| **S4** | Live Backend Execution | 05 | `bck-lead` | G4 | Working API + migrations + **security-checked** | YES (backend only) |
| **S5** | Both Interfaces in Parallel | 06·07 (merged team) | `fnt-lead` + `mob-lead` | G4b | Flutter/Dart for web+mobile on frozen contract | YES (UI on live backend) |
| **S6** | Shield & Production | 09·10·11·12 | `qa-lead` + `ops-lead` + `obs-lead` | G5·G6·G7·G8 | Tests + deploy + observability + knowledge log | YES (deploy + monitor) |

**4 binding laws of the pipeline:**
1. **OpenAPI-first** — no code without a frozen OpenAPI spec
2. **No transient mocks crossing boundaries** (internal unit tests exempt)
3. **Envelope** per `hq/core/standards/api-envelope.md` — every API response wraps
4. **DDD Capsule** per `hq/core/standards/ddd-capsule.md` — DO/DON'T table for bounded contexts

## 13. The 9 Gates + DFR

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

## 14. The 4 Owner Approval Points

> Source: `AGENTS.md` + `INT-EVOL-2`.

The owner (Arabic, non-technical) must approve at **4 explicit checkpoints**. Rejecting at any
point = return to the owning stage for correction. Writing code before all 4 points are approved
is **forbidden** (Design-First doctrine INT-0004).

| # | When | What is presented | How it's presented |
|---|------|--------------------|---------------------|
| 1 | after S1 (research + analysis) | what we'll build + what we won't + timeline + technology (candidates) | simple plan in Arabic |
| 2 | after S3 (wireframes + mockups) | screen shapes + colors + fonts as understandable images | mockup images, no jargon |
| 3 | after S2/S3 (architecture + contract) | how it works inside, explained by metaphor | Arabic metaphor, no jargon |
| 4 | DFR + G5 | design freeze signature + production quality verdict | Arabic summary + test report |

## 15. The 26 Standards

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
| `reporting-cadence.md` | on-merge · on-incident-close · on-session-end (Rec #16 — no human-time) |
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
| `+ SOFI-QUICK-REFERENCE.md` (in `hq/core/`) | 1-page map |

---

# Part 5 — Operations

## 16. Memory: CORTEX / HIPPOCAMPUS / AMYGDALA

> Source: `hq/brain/` + `projects/<slug>/brain/` · Law 7 binds these together.

**Two completely separate memories — never mix:**

### Organization memory (`hq/brain/`)

- **`cortex-decisions.md`** — **CORTEX** — the ADR log. Every fateful decision is recorded here:
  ```
  ## ADR-YYYYMMDD-NAME — title
  - date
  - context
  - decision
  - consequences
  - evidence refs (file:line)
  - guards state
  ```
  Key ADRs: `ADR-20260831-9AXIS-FIX` · `ADR-20260831-VISUAL-DIAGRAMS` · `ADR-20260831-SAKK-DOUBLE-VERIFY` ·
  `ADR-20260905-GTW-FLUTTER-QA-ARCHITECT` · `…-REACT-DDD-…` · `…-LARAVEL-DDD-…` ·
  `ADR-20260905-AUDIT-ALL` · `…-Phase2` · `…-Phase3` · `DEC-R3.4-PHASEB-ACCEPT` · `DEC-R6-…ARCHIVE-LEGACY-AGENTS`

- **`hippocampus-sessions.md`** — **HIPPOCAMPUS** — session log. One entry per session:
  ```
  ## SES-YYYYMMDD-…
  - session
  - intake_id
  - classification
  - what
  - evidence
  - status
  ```

- **`amygdala-incidents.md`** — **AMYGDALA** — incident log. Every P0/WarRoom incident with:
  timeline · forensic evidence · rollback actions · postmortem.

- **`evidence/`** — per-task audit + snapshot files (e.g. `surgical-review-*`).

**Auto-summarize (P-06.7):** `hq/core/tooling/memory_summarizer.py:1` runs every 10 turns via
`knw-reflector` — when `hippocampus >800` or `amygdala >600`, keep last 5 full + summarize older.

### Project memory (`projects/<slug>/brain/`)

For each active project (e.g. `projects/sakk/brain/`):
- `CONTEXT.md` — the PRD (single source of truth)
- `DECISIONS.md` — project-level decisions
- `HANDOFFS.md` — task handoffs
- `LESSONS.md` — lessons learned

> **Law 7 isolation:** org memory and project memory are **strictly separated** — promotion from
> project to org requires explicit `brd-ceo` decision recorded in CORTEX.

## 17. The MCP Fleet (27 servers, 100% local)

> Source: `hq/core/nexus/mcp-routing.yaml:13` + `hq/core/standards/mcp-registry.md` + `.opencode/skills/sofi-mcp-fleet/SKILL.md`.

**The 6 binding MCP-FLEET rules (apply to every server):**

1. **SOFI-Context before any code touching a library** — Latest-Version-Mandatory
2. **SOFI-Wiki before any external repo claim** — HiveFence lesson
3. **SOFI-Browser for visual delivery evidence** — Kitesurf default (Law 4)
4. **SOFI-Reasoning for complex branching** — Sequential-thinking
5. **`sec-mcp-vetting` for any new server** — no self-enable
6. **Everything is free** — paid keys auto-rejected (INT-0003)

## 18. The Hierarchical Handoff Path

```
agent (any room)        — receives RCCF from lead
        │                  executes within scope + constraints
        ▼
room lead (e.g. qa-lead) — reviews + unifies + takes responsibility
        │
        ▼
brd-ceo (00-boardroom)  — final sign-off + owner communication
        │
        ▼
owner (Arabic)          — receives in simple Arabic (Law 11)
```

**Forbidden:**
- agent → another room directly (Law 2)
- agent → user directly (Law 3)
- lead → user directly (Law 3)
- any sideways delivery (Law 2)

## 19. Tickets: RCCF + the JSON Bus

**RCCF work order** (Law 5): Request → Clarify → Confirm → Fullfil.
No execution without one. Central registry: `hq/core/nexus/rccf-registry.yaml`.

**JSON bus** (P-02 — Strict JSON Handoff Scheme):

```json
{
  "v": 1,
  "ticket_id": "PRJ-ID-001",
  "from_agent": "bck-api-engineer",
  "to_agent": "bck-lead",
  "direction": "upward-only",
  "type": "handoff|acceptance|rejection",
  "rccf_ref": "RCCF-2026-0823-NAME",
  "artifacts": ["projects/<name>/app/Domains/X/Actions.php"],
  "evidence_digest": {
    "files_changed": 3,
    "checks": {"static_analysis": "PASS", "tests": "PASS"},
    "exit_codes": [0]
  },
  "context_refs": ["hq/core/standards/api-envelope.md#envelope-v1"],
  "status": "ready-for-review|in-flight|delivered|rejected",
  "note": "≤280 characters"
}
```

**Strict rules:**
- `note` ≤ 280 chars
- Full evidence stays in `sofi-evidence` block (Law 4)
- Schema extension = new `v` with `brd-ceo` approval
- Rejecting requires explicit `rejection` ticket with reason

---

# Part 6 — Stack & Domain

## 20. Tech Stack & Stack Lock R3

> Source: `AGENTS.md` §Stack Lock R3 (owner directive 2026-09-04) — **no override without owner order recorded in CORTEX**.

| Layer | **Binding (only allowed)** | **Forbidden** |
|-------|-------------|---------------|
| **Frontend (06)** | **React 18+** (19+ encouraged) · TypeScript 5+ · Tailwind 4+ · Vite 5+ / Webpack 5 · Storybook 8+ · Jest/Vitest/Playwright | Vue · Angular · Svelte · jQuery · Bootstrap · any non-React lib |
| **Backend (05)** | **Laravel 11+** EXCLUSIVE · PHP 8.3+ mandatory · Eloquent · Queues + Horizon · Redis 7+ · PostgreSQL 16+ / MySQL 8+ · PHPUnit 11+ / Pest 3+ · Composer 2+ | Symfony (standalone) · CodeIgniter · Yii · Slim · Lumen-as-main · raw PHP frameworks · PHP < 8.3 |
| **Mobile (07)** | **Flutter 3.22+** · Dart 3+ · Riverpod / Bloc | any non-Flutter framework |
| **Linting/quality** | ESLint · Prettier · Storybook · PHPUnit/Pest | (all required) |
| **MCP** | 27 servers, **100% local**, free | paid SaaS / API keys (INT-0003 auto-rejects) |
| **Tone** | All human-time concepts removed from mandates | "daily standup" · "nightly scan" · "weekly retrospective" (Rec #16 — replaced with on-merge / on-incident-close) |

**Latest-Version-Mandatory:** before any code touching a library → **Context7** MCP; for any external
repo claim → **DeepWiki** MCP. No improvising from stale memory. (`hq/core/standards/latest-version-mandatory.md:1`)

## 21. The Latest-Version-Mandatory Rule

Before writing any line of code that imports a library, you **must** invoke:
- **Context7 MCP** — fetches the latest official documentation
- **DeepWiki MCP** (if external repo claim) — verifies against actual repository state

This prevents:
- Hallucinated APIs (from stale model memory)
- Outdated syntax (from old training data)
- Wrong license attributions (from invented package names)

Failure to use Context7/DeepWiki = L1 first time, L2 on repetition.

## 22. The 27 MCP Servers (Room Distribution)

> Source: `hq/core/nexus/mcp-routing.yaml:13`.

**6 fleet servers (universal):**

| Server | Used by |
|--------|---------|
| SOFI-Context | every code-touching task (Latest-Version-Mandatory) |
| SOFI-Wiki | every external repo claim |
| SOFI-Browser | every visual evidence / screenshot |
| SOFI-Reasoning | every complex branching problem |
| SOFI-Time | timing (Asia/Riyadh) |
| SOFI-Security | new MCP server vetting |

**21 organizational servers (per-room):**

| Server | Used by |
|--------|---------|
| Filesystem-Scoped | every room (3 MCP tools: read/write/edit) |
| SOFI-Consult | 00-boardroom for Board consults |
| SOFI-Research | 01/02 for market + research |
| SOFI-Skills | 13-knowledge for skills registration |
| SOFI-Github | 11/14 for git ops |
| SOFI-Network | 11/12/14 for network status |
| SOFI-MemoryHub | 13 for memory ops |
| SOFI-EpisodicMemory | 13 for episode tracking |
| SOFI-WorkingMemory | 13 for context |
| SOFI-Dart | 07 (Flutter/Dart) |
| SOFI-Broker | 14 for task delegation |
| SOFI-Consult | 00 for board opinions |
| + 9 more | distributed per room needs |

**Room allocation per the routing rules:** each room gets 3 core servers (Filesystem-Scoped + SOFI-Time
+ SOFI) + access to all 6 fleet + relevant organizational servers. Full map: `hq/core/nexus/mcp-routing.yaml:13`.

---

# Part 7 — Room-by-Room Deep Dives

> Each room has its own charter at `hq/core/domain/rooms/<room>/charter.md` and capsule at
> `hq/core/domain/rooms/<room>/agents/<name>/{capabilities,senses,memory}.yaml`.

## 23. Room 00 — Boardroom

**Tier:** T0 Spine · **Lead:** `brd-ceo` · **Agents:** 7

**Purpose:** Supreme governance + Board advisory + final arbitration. The CEO holds the constitutional
authority for system-wide decisions. The CSO holds **absolute veto** on security/safety. The Arbiter
is the binding judge for Law-14 disputes.

**Provides:** RCCF work orders · final arbitration · security veto (CSO only)
**Requires:** escalations from all rooms
**Talks to:** all-room leads · gtw-dispatcher
**Forbidden:** direct task execution (Boardroom decides, doesn't do)

**When you need the Board:**
- Money decisions
- Architecture/lock changes
- Security/privacy questions
- Law-14 dispute (same task rejected twice for same reason)
- Cross-room conflicts the gateway can't resolve

**Workflow:** agent escalates → `brd-ceo` consults relevant `brd-*` via Task → `brd-chief-of-staff`
converts decision to RCCF work order → `brd-ceo` signs → distributed downward.

## 24. Room 14 — Gateway

**Tier:** T0 Spine · **Lead:** `gtw-dispatcher` · **Agents:** 7

**Purpose:** The **only** entry point for any request. Classifies into Fast/Standard/Fateful.
Enforces Law 1, Law 11, Law 16. Routes to the correct room/lead.

**Provides:** Intake Reports (5 sections) · lane classification · conflict resolution
**Requires:** owner/user input
**Talks to:** all rooms (via tickets) · brd-ceo (Fateful)
**Forbidden:** execution (gateway prepares & routes, never executes)

**SOP:**
1. `gtw-intake-reformer` receives raw input
2. 5-section prompt reformulation (Executive Summary · Full Context · Specific Request ·
   Constraints & Considerations · Expected Deliverables)
3. Ambiguity score (Law 16 — ≤20% PASS; >20% emit 1-3 sharp questions + 24h timeout)
4. Budget + conflict check
5. Lane classification per P-01.8
6. Route to room lead (Fast) or brd-ceo (Standard/Fateful)

**Tools available:** `gtw-intake-route` (playbook) + `sofi-evidence` + `sofi-handoff` (mandatory for all rooms).

## 25. Room 01 — Strategy

**Tier:** T1 Paper · **Lead:** `str-lead` · **Agents:** 8

**Purpose:** Define what to build (PRD), what NOT to build (MVP scope), and when to ship (roadmap).
Owns Gate-0 (intake classification support) and Gate-2 (PRD approval).

**Provides:** PRD in `projects/<slug>/brain/CONTEXT.md` · MVP scope · roadmap · risk register
**Requires:** market research from 02-research · business context from 00
**Talks to:** 02-research · 03-design · 04-architecture
**Forbidden:** implementation decisions (Strategy plans, doesn't code)

**Workflow:** owner intent → `str-business-analyst` elicits requirements → `str-product-strategist`
authors PRD → `str-market-analyst` sizes market → `str-monetization-strategist` prices →
`str-risk-analyst` flags risks → `str-roadmap-planner` sequences → `str-agile-orchestrator` WIP-limits
→ `str-lead` signs Gate-2.

## 26. Room 02 — Research

**Tier:** T1 Paper · **Lead:** `res-lead` · **Agents:** 6

**Purpose:** The empirical foundation. JTBD personas, journey maps, competitor analysis, fact
verification, visual patterns. Owns Gate-1.

**Provides:** research dossier (journey map + JTBD personas + pain points + behavioral data + usability scripts)
**Requires:** questions from 01-strategy and 03-design
**Talks to:** 01-strategy · 03-design
**Forbidden:** design decisions (Research finds, doesn't design)

**Protocol 19 (P-19):** every UX decision in 03-design must cite its source research `file:line`.
`res-ux-researcher` personas map 1:1 to `dsn-ux-architect` user flows via
`projects/<slug>/brain/research-to-design-bridge.md` (P-19.3). Joint Gate-1/DFR co-sign per P-19.5.

**Skill:** `res-journey-map` (the research dossier skill) + Protocol 18 (visual feeding via
`res-visual-pattern-scout` + `mobbin-scraper`).

## 27. Room 04 — Architecture

**Tier:** T1 Paper · **Lead:** `arc-lead` · **Agents:** 13

**Purpose:** The structural foundation. System decomposition, API contracts, ERD, DDD context maps,
security architecture, performance budgets. Owns Gates 3-4.

**Provides:** ERD (paper) + schema-contract + frozen OpenAPI + DDD context map + ADR chain
**Requires:** PRD from 01-strategy · designs from 03-design
**Talks to:** 05-backend · all engineering leads
**Forbidden:** bypassing DFR (Architecture freezes contract, doesn't ship without DFR)

**4 binding output artifacts:**
1. ERD (paper) — `arc-data-architect` + `arc-db-engineer`
2. Schema-contract (paper) — `arc-data-architect` (DDD context map)
3. Frozen OpenAPI spec — `arc-api-architect` (G3 gate)
4. ADR chain — `arc-system-architect` (every fateful decision)

**3 security/performance specialists:**
- `arc-security-architect` — STRIDE review (DFR mode mandatory) — threat surface — zero-trust design
- `arc-performance-architect` — SLO design — capacity planning — latency budgets
- (was) `arc-ml-engineer` — moved to 16-innovation in Phase 3
- (was) `arc-privacy-officer` — moved to 08-localization in Phase 3

**Context-map boundaries (clarified in Phase 1):**
- **04 OWNS api-design + data-design** — sole designer of OpenAPI + ERD
- **09 REVIEWS/VETO** — security aspects of every design/release — via gates only — **never designs APIs**
- **10 VERIFIES** — testability + contract-conformance + DFR tokens — via tickets only — **never fixes code or designs APIs**

**Skill:** `arc-adr` (the ADR authoring skill) + `sofi-evidence` (every ADR cites file:line).

## 28. Room 03 — Design

**Tier:** T1 Paper · **Lead:** `dsn-lead` · **Agents:** 8

**Purpose:** Translate research into UX flows, components, design system, and visual language.
Owns DFR (Design-Freeze Review) co-sign with 09 + 10.

**Provides:** UX flows · design system · mockups · DFR sign-off
**Requires:** research findings from 02-research · data-model from 04-architecture · API contract from 04-architecture
**Talks to:** 02-research · 04-architecture · 06-frontend · 07-mobile · 08-localization (Arabic copy)
**Forbidden:** code commits before DFR gate

**DFR signature:** `dsn-lead` + `sec-lead` + `qa-lead` (and `res-lead` per P-19.5) — without these
signatures, no code may be written.

**Skill:** `dsn-design-handoff` (the design-to-dev handoff package) + `sofi-evidence` (every
design token cites `file:line`).

## 29. Room 08 — Localization

**Tier:** T1 Paper · **Lead:** `loc-translation-manager` (Noura Al-Hassan) · **Agents:** 5

**Purpose:** Arabic translation, cultural adaptation, RTL mirror validation, voice & tone, and
PII-privacy for Arabic copy. Co-signs DFR (Hadi Al-Quds) for RTL correctness.

**Provides:** localized strings + RTL specs + voice guide + privacy audit
**Requires:** research findings + design tokens
**Talks to:** 02-research · 03-design · 06-frontend · 07-mobile · 10-quality
**Forbidden:** skipping RTL validation · leaking PII in Arabic copy

**Workflow:** 02-research identifies Arabic audience → 03-design produces tokens → `loc-rtl-specialist`
applies `rtl-mirror-validator` skill → `loc-translation-manager` translates via glossary →
`loc-cultural-adapter` reviews imagery → `loc-voice-tone-expert` unifies tone (Law 11) →
`loc-privacy-officer` audits PII → co-sign DFR.

**Skill:** `loc-rtl-adaptation` (the new Phase-3 protocol) + `rtl-mirror-validator` (shared).

## 30. Room 16 — Innovation

**Tier:** T1 Paper (innovation track) · **Lead:** `inn-lab-lead` (Ziad Al-Hariri) · **Agents:** 3

**Purpose:** Tech scouting + PoCs in isolated sandbox. Pre-Production innovation track with explicit
`brd-cto` approval per experiment.

**Provides:** innovation ADRs + PoCs
**Requires:** `brd-cto` + `brd-cso` approval per experiment
**Talks to:** 02-research (scout) · 04-architecture (evaluate) · 09-security (veto) · 13-knowledge (log)
**Forbidden:** touching production without promotion via fateful ADR

**Workflow:** `inn-tech-scout` writes tech brief → `inn-lab-lead` writes experimental ADR →
`brd-cto` approves → experiment in `hq/engine/sandbox/<tech>/` or `projects/innovation-lab/<slug>/` →
`inn-ml-engineer` runs PoC → ADR draft with go/no-go → archive or promote to fateful ADR.

**Skill:** `inn-experiment` (the new Phase-3 protocol).

## 31. Room 05 — Backend

**Tier:** T2 Code · **Lead:** `bck-lead` · **Agents:** 8

**Purpose:** S4 — live Laravel 11+ backend execution. Activates schemas from S2 + codes against
frozen OpenAPI. Security-checked before UI starts.

**Provides:** working API + migrations + backend-security-hardening
**Requires:** frozen OpenAPI from 04-architecture + approved schema from 04-architecture
**Talks to:** 10-quality (tickets) · 09-security (gates)
**Forbidden:** direct chat with 06-frontend · UI code (backend only) · schema changes without 04-architecture approval

**Law 11 means:** all responses use the api-envelope standard. **No chat directly with frontend**
— tickets only.

**Skill:** `bck-feature-build` (the backend feature playbook) + `sofi-evidence` (every endpoint cites `file:line`).

## 32. Room 06 — Frontend

**Tier:** T2 Code · **Lead:** `fnt-lead` · **Agents:** 7

**Purpose:** S5 — React 18+ + Tailwind 4+ web apps. Coded against the frozen OpenAPI on a live
backend. Together with 07-mobile as a merged team (S5 parallel).

**Provides:** web apps on approved design system
**Requires:** frozen OpenAPI from 04-architecture · live backend via 11-devops · designs from 03-design
**Talks to:** 10-quality (tickets) · 07-mobile (unified UI lane)
**Forbidden:** backend code · schema changes

**Skill:** `fnt-component-build` (the React component playbook) + `fnt-ux-lint` (anti-slop + a11y
check before merge) + `sofi-evidence`.

## 33. Room 07 — Mobile

**Tier:** T2 Code · **Lead:** `mob-lead` · **Agents:** 6

**Purpose:** S5 — Flutter 3.22+ + Dart 3+ for web + mobile (unified standard per R2). On the same
frozen contract as 06. Uses the unified design system with 06.

**Provides:** Flutter apps (web + mobile unified)
**Requires:** frozen OpenAPI from 04-architecture · designs from 03-design
**Talks to:** 06-frontend (unified UI lane) · 10-quality
**Forbidden:** divergent design system (must align with 06)

**Skill:** `mob-feature-build` (the mobile feature playbook) + `mob-flutter-kb` (official Flutter
knowledge gateway) + `sofi-evidence`.

**The Unified UI Lane (R2):** 06 + 07 are a **merged team** for S5. `mob-state-engineer` owns state
architecture for the whole merged team.

## 34. Room 09 — Security

**Tier:** T3 Shield · **Lead:** `sec-lead` · **Agents:** 9

**Purpose:** Continuous security shield — STRIDE + pentest + license + secrets + compliance. Holds
**absolute veto** on security/safety. Co-signs DFR.

**Provides:** threat models · pentest reports · DFR signature · absolute veto
**Requires:** review access to every design and release
**Talks to:** all-rooms (gates only) · 00-boardroom
**Forbidden:** implementation duties (Security reviews, doesn't implement) · API design · data design

**Workflow:** any room can request security review via ticket → `sec-threat-modeler` runs STRIDE →
`sec-appsec-engineer` SAST/DAST → `sec-pentester` manual pentest → `sec-compliance-auditor` regulatory check
(DFR mode mandatory) → `sec-license-auditor` Law-15 check → `sec-incident-responder` if breach →
`sec-secrets-warden` continuous → `sec-lead` vetoes or signs.

**Skill:** `sec-threat-model` (the threat modeling playbook) + `sec-mcp-vetting` (gate for any new MCP server).

## 35. Room 10 — Quality (10 testers)

**Tier:** T3 Shield · **Lead:** `qa-lead` (Lama Al-Tarabulsi) · **Agents:** 10

**Purpose:** The official testers. 7 generalists + 3 stack-specialist. **Owns Gate-5** + co-signs DFR.

**Provides:** test plans · zero-bug evidence · release verdicts
**Requires:** testable builds via bus · acceptance criteria from leads
**Talks to:** 05-backend · 06-frontend · 07-mobile · 11-devops
**Forbidden:** fixing code (Quality tests, doesn't code) · API design · data design

**The 3 stack-specialist testers (ADVISORY ONLY — C3):**

| Tester | Specialty | Tools | Acceptance points |
|--------|-----------|-------|-------------------|
| **Rayan Al-Qadi** — `qa-flutter-architect` | Flutter 3.22+ | adb screencap · uiautomator dump · gfxinfo · meminfo · flutter run --profile | **20** |
| **Samer Al-Khalil** — `qa-react-architect` | React 18+/Next.js + DDD | Lighthouse · @next/bundle-analyzer · React Profiler · Chrome DevTools · Axe | **28** |
| **Yousuf Al-Amiri** — `qa-laravel-architect` | Laravel 11+ + DDD + DB + Security | php artisan · EXPLAIN · Telescope · Pest/PHPUnit | **22** |

**Unified assessment matrix (Phase 2):** `hq/core/standards/qa-assessment-matrix.md` — common criteria
(Performance / Security / A11y) + 20/28/22 stack-specific points.

**The verdict hierarchy:** qa-flutter-architect / qa-react-architect / qa-laravel-architect produce
**advisory reports** → `qa-lead` consolidates → `brd-cqo` signs Gate-5 → `brd-ceo` ships.
**Never the specialist tester.**

**Skill:** `qa-test-plan` (Gate-5 playbook) + `qa-flutter-architect` + `qa-react-architect` +
`qa-laravel-architect` + `sofi-evidence`.

## 36. Room 11 — DevOps

**Tier:** T3 Shield · **Lead:** `ops-lead` · **Agents:** 8

**Purpose:** CI/CD + cloud + release + sandbox + ephemeral branches (Law 10). Owns the
production deployment window + rollback.

**Provides:** deployments · live-infra health · rollback plans
**Requires:** QA-passed artifacts from 10-quality · runbooks from standards
**Talks to:** 10-quality · 12-observability · 09-security
**Forbidden:** deploying without QA pass or owner order

**Law 10 enforcement:**
- Default: all work on main tree
- Allowed: ephemeral branches `feature/<scope>-<ticket-id>` ≤72h with sandbox + merge-before-close
- Unmerged at 72h → `ops-lead` escalates to `brd-arbiter`
- Long-lived isolated branches (>24h unmerged) and permanent worktrees = L2

**Workflow:** S6 done (Gate-5 PASS) → `ops-cicd-engineer` triggers pipeline (`on-merge` automated) →
`ops-cloud-engineer` provisions (Terraform) → `ops-migration-runner` runs migrations with rollback
window → `ops-release-manager` ships → `ops-domain-warden` manages DNS/TLS → `ops-sandbox-executor`
validates inside container if needed → `ops-cost-optimizer` watches spend.

**Skill:** `ops-deploy-runbook` (the deploy playbook) + `sofi-evidence`.

## 37. Room 12 — Observability

**Tier:** T3 Shield · **Lead:** `obs-lead` · **Agents:** 6

**Purpose:** Continuous observability — metrics + logs + traces + SLOs + incident detection.
The eyes and ears of the system.

**Provides:** health metrics · incident alerts · postmortems
**Requires:** access to live signals via engine layer
**Talks to:** 11-devops · 00-boardroom (incidents)
**Forbidden:** config changes (Observability monitors, doesn't modify)

**Rec #16 — Event-Driven Policy:** Observability runs **on event** (SLO breach, error spike, anomaly),
not on schedule. No "nightly scans" — that's human-time.

**Workflow:** `obs-monitoring-engineer` designs metrics + dashboards → `obs-alerting-engineer`
designs alert rules + paging → `obs-sre` designs SLOs + error budgets → `obs-incident-commander`
declares incidents on SLO breach → `obs-insights-analyst` finds trends → `obs-lead` reports to
00-boardroom.

**Skill:** `obs-incident-response` (the SEV-1 incident response playbook) + `sofi-evidence`.

## 38. Room 15 — WarRoom

**Tier:** T3 Shield · **Lead:** `war-incident-commander` (Firas Al-Najjar) · **Agents:** 4

**Purpose:** P0 incident command — the last line of defense when a SEV-1 strikes. On-call, not
scheduled. Owns the **Law-14 freeze** for the affected scope.

**Provides:** incident command · forensic evidence · rollback windows · crisis communications
**Requires:** emergency RCCF from `brd-ceo` · or alert from `obs-incident-commander` or `sec-incident-responder`
**Talks to:** 11-devops (rollback) · 09-security (security) · 00-boardroom (closure)
**Forbidden:** hiding incidents (immediate AMYGDALA) · direct owner contact (via `war-communication-lead`)

**Law 14 freeze:** when a WarRoom is active, affected RCCFs are **frozen** — no third blind attempt
per the broken-loop countermeasure.

**Workflow:** SEV-1 detected → `obs-incident-commander` raises → `war-incident-commander` takes
command (Law 14 freeze) → `war-forensic-analyst` collects evidence (hash before touch) →
`war-rollback-engineer` activates rollback window → `war-communication-lead` briefs owner every 30 min
(Law 11) → recovery → within 24h, postmortem in AMYGDALA → re-evaluate linked Gate.

**Skill:** `war-incident-runbook` (the new Phase-3 protocol) + `obs-incident-response` (inherited).

## 39. Room 13 — Knowledge

**Tier:** T4 Memory · **Lead:** `knw-lead` · **Agents:** 6

**Purpose:** The institutional memory. CORTEX (decisions) · HIPPOCAMPUS (sessions) ·
AMYGDALA (incidents). Maintains the brain, registers skills, and audits the docs.

**Provides:** memory curation · skills-forge · documentation
**Requires:** decisions input via CEO promotion
**Talks to:** all-room memory contracts · 00-boardroom
**Forbidden:** unilateral law edits (Knowledge documents, doesn't legislate)

**Workflow:** every fateful decision → CORTEX ADR (knw-doc-writer) · every session → HIPPOCAMPUS
SES (knw-historian) · every incident → AMYGDALA (knw-memory-curator) · every skill →
`skill-forge` → knw-brain-query indexes · knw-reflector runs the P-06.7 summarizer ritual.

**Skill:** `knw-brain-write` (the brain-writing playbook) + `knw-knowledge-harvest` (quarterly
harvest from elite sources via Crawl4AI/Kitesurf) + `skill-forge` (meta) + `sofi-evidence`.

---

# Part 8 — Worked Scenarios

## 40. Scenario 1: The Owner Wants an Online Store

**Owner utterance (in Arabic, plain):**
> "أريد متجر إلكتروني بسيط"

**Flow:**

1. **14-gateway · `gtw-intake-reformer` (Kaisar Al-Ribat)** receives the raw Arabic. He reformulates
   it into a 5-section Intake Report:
   - **Executive Summary:** Owner wants a simple online store.
   - **Full Context:** no current product, no PRD, no design. Cold start.
   - **Specific Request:** build an e-commerce platform — scope TBD.
   - **Constraints:** Law 11 (owner is Arabic, non-technical). Law 12 (no rooms can be skipped).
   - **Expected Deliverables:** an online store.

2. **Law 16 ambiguity check:** score 0.35 (35%) — **above 20% threshold**. Gatekeeper issues 1-3
   sharp questions + 24h timeout:
   - Who sells what? (products, services, digital goods?)
   - Who buys? (B2C, B2B, regional?)
   - Payment methods? (Mada, Apple Pay, Stripe?)

3. **Owner responds** (within 24h): "Physical products (Saudi market), B2C, Mada + Apple Pay + COD".

4. **Lane classification:** Standard (e-commerce spans 5+ rooms: 01/02/04/03/05/06/07/10/11/12 — but
   the M3 stacking rule: anything involving payment is **Fateful** by default). → 🔴 **Fateful**
   → `brd-ceo`.

5. **`brd-ceo` consults Board via Task:**
   - `brd-cso` — security: payment gateway (Mada) is high-stakes, need PCI-DSS-aware architecture
   - `brd-cto` — stack: Laravel 11+ backend, React 18+ web, Flutter mobile (Stack Lock compliant)
   - `brd-cqo` — quality: payment paths need extra Gate-5 rigor
   - `brd-cpo` — product: scope clarification
   - `brd-chief-of-staff` — converts to RCCF-2026-0905-ECOMMERCE

6. **S1 — Strategy (01):** `str-product-strategist` authors PRD (MVP scope: catalog + cart +
   checkout + payment + order tracking + admin). `str-market-analyst` sizes the Saudi e-commerce
   market. `str-risk-analyst` flags payment gateway + Mada PCI-DSS risk. `str-roadmap-planner`
   sequences 6 sprints. `str-lead` signs Gate-2.

7. **S1 → S2 — Research (02):** `res-ux-researcher` builds JTBD personas (Saudi shopper, COD
   preferer, Mada-user, Apple-Pay-user). `res-journey-architect` maps journeys. `res-fact-checker`
   verifies Mada + Apple Pay APIs. `res-competitor-analyst` analyzes 3 Saudi competitors. `res-lead`
   signs Gate-1.

8. **S2 — Architecture (04):** `arc-data-architect` drafts ERD (users, products, categories,
   carts, orders, payments, shipments). `arc-api-architect` freezes OpenAPI for the 47 endpoints.
   `arc-security-architect` runs STRIDE on payment paths. `arc-system-architect` authors 4 ADRs
   (architecture, payment, Mada integration, scaling). `arc-lead` signs Gate-3.

9. **S3 — Design (03):** `dsn-ux-architect` produces user flows. `dsn-ui-designer` produces mockups.
   `dsn-design-system` defines 3-layer tokens. `dsn-a11y-specialist` audits WCAG 2.1 AA. `dsn-arabic-ux-specialist`
   signs RTL. `dsn-lead` co-signs DFR with `sec-lead` + `qa-lead` + `res-lead` (P-19.5).

10. **S4 — Backend (05):** `bck-api-engineer` codes 47 endpoints against the frozen OpenAPI.
    `bck-domain-engineer` implements Eloquent models + DDD aggregates. `bck-queue-engineer` implements
    the payment-webhook + email-job with Horizon. `bck-integration-engineer` integrates Mada +
    Apple Pay. `bck-lead` signs G4.

11. **S5 — Frontend + Mobile (06‖07):** `fnt-react-engineer` + `mob-flutter-engineer` (merged
    team) build on the live backend. Unified design system. `fnt-performance-engineer` audits Core
    Web Vitals. `mob-perf-profiler` audits jank. G4b passes.

12. **S6 — Shield (09-13):**
    - `qa-laravel-architect` (Yousuf Al-Amiri) runs 22-point review on backend → advisory PASS
    - `qa-react-architect` (Samer Al-Khalil) runs 28-point review on web → advisory PASS
    - `qa-flutter-architect` (Rayan Al-Qadi) runs 20-point review on mobile → advisory PASS
    - `qa-lead` consolidates + `brd-cqo` signs Gate-5
    - `ops-cicd-engineer` triggers CI → all 4 guards green
    - `ops-migration-runner` runs migrations with rollback window
    - `ops-release-manager` ships to production
    - `obs-monitoring-engineer` activates dashboards + alerts
    - `knw-doc-writer` records the full ADR chain in CORTEX

13. **Delivery to owner:** `brd-ceo` writes in simple Arabic (Law 11):
    > "المتجر جاهز يا صاحب المنزل — جاهز للإطلاق مع 47 نقطة نهاية، 4 وكلاء متخصصين راجعوا، 3 حراس خضراء. يحمي بيانات الدفع مع Mada + Apple Pay + الدفع عند الاستلام. جاهز للسوق السعودي."

**Time:** ~6 sprints (each 2 weeks = 12 weeks).

## 41. Scenario 2: A P0 Production Incident

**Trigger:** SLO breach — payment error rate > 5% in production.

1. **12-observability · `obs-monitoring-engineer`** dashboard shows spike → `obs-alerting-engineer`
   fires page → `obs-incident-commander` (Maya Al-Naqri equivalent) declares SEV-1.

2. **WarRoom 15 activates:**
   - `brd-ceo` issues emergency RCCF-2026-0905-INCIDENT-001
   - `war-incident-commander` (Firas Al-Najjar) takes command — **Law-14 freeze** on all
     payment-related RCCFs (no third blind attempt)
   - `war-forensic-analyst` (Layla Al-Halabi) collects logs (hash before touch), traces, dumps —
     file:line per piece of evidence

3. **15-WarRoom + 11-DevOps coordinated:**
   - `war-rollback-engineer` (Omar Al-Khani) sees the issue is Mada API change — activates
     rollback to last known-good Laravel version
   - `obs-sre` confirms Mada API deprecation notice
   - Rollback succeeds — payment error rate drops to 0.1%

4. **15-WarRoom + 09-Security coordinated:**
   - `sec-incident-responder` reviews for breach — no breach (Mada change was unannounced)
   - `sec-appsec-engineer` confirms no data leak

5. **Communication:**
   - `war-communication-lead` (Salma Al-Rashid) briefs owner every 30 min in simple Arabic
     (Law 11):
     - T+0: "حدث خلل في الدفع — جاري التحقيق"
     - T+15: "وجدنا السبب (Mada API) — جاري التراجع"
     - T+30: "التراجع نجح — الخدمة عادت طبيعية"
   - All team leads notified via ticket bus

6. **Postmortem (within 24h):**
   - `obs-incident-commander` writes postmortem → `hq/brain/amygdala-incidents.md`
   - Lessons learned:
     - Subscribe to Mada API changelog (action: `sec-incident-responder`)
     - Add synthetic Mada payment test (action: `bck-domain-engineer`)
     - Reduce rollback window from 30min to 10min (action: `ops-rollback-engineer`)
   - `brd-arbiter` records → no Law-14 dispute (single incident)
   - **G4 re-opened** (P-20.3 — failure mode → Gate re-evaluation)

7. **Re-eval (G4):** `sec-threat-modeler` re-runs STRIDE with Mada-deprecation scenario. `bck-domain-engineer`
   adds synthetic test. `bck-queue-engineer` adds Mada health-check job. G4 re-passes.

**Time:** incident TTR = ~35 minutes. Postmortem within 24h.

## 42. Scenario 3: Adding a New Specialist Tester

**The owner wants to add a `qa-node-express-architect` for legacy Node.js projects.**

1. **14-gateway · `gtw-intake-reformer`** receives the Arabic request. Reformulates. Computes
   ambiguity (low — clear scope). Lane = Fateful (registry modification = Law 12).

2. **brd-ceo consults Board:**
   - `brd-cto`: "Node.js is **not** in Stack Lock R3. Only Laravel, React, Flutter are."
   - `brd-cso`: "No security issue per se."
   - `brd-cpo`: "Strategic question — do we want to expand Stack Lock?"
   - **brd-ceo** decides: defer until owner explicitly expands Stack Lock + amend R3.

3. **If owner expands Stack Lock:** then proceed:
   - ADR-2026-0905-ADD-NODE-EXPRESS-TESTER in CORTEX
   - Create `.opencode/agent/qa-node-express-architect.md` (mirror the 3 existing stack testers)
   - Add skill `.opencode/skills/qa-node-express-architect/SKILL.md`
   - Add capsule `hq/core/domain/rooms/10-quality/agents/qa-node-express-architect/`
   - Add row to `hq/core/nexus/registry.yaml:200+`
   - Add block to `hq/core/nexus/personas.yaml`
   - Add block to `hq/core/nexus/routing.yaml`
   - Bump `registry_guard.py:20` + `count_sync.py:23`
   - Bump `AGENTS.md:62,256` + `registry.yaml:3,11` + `room-priority.yaml:11`
   - Update room 10 charter `Agent count: 8 → 9`
   - Add row to `.opencode/skills/INDEX.md`
   - Atomic commit — pre-commit enforces all 4 guards
   - `brd-ceo` signs acceptance in CORTEX (DEC-...-ACCEPT)

**Time:** ~30 minutes.

## 43. Scenario 4: A Fateful Decision (Board Consult)

**The CTO wants to migrate from PostgreSQL to a graph database.**

1. **`brd-cto`** issues a fateful proposal: "Migrate to Neo4j for relationship-heavy data."

2. **`brd-ceo`** opens a Board consult via Task:
   - `brd-cto` (proposer): rationale + benchmarks
   - `brd-cso` (security): graph DB security model
   - `brd-cqo` (quality): migration risk + testing
   - `brd-cpo` (product): impact on roadmap
   - `brd-cso` (veto holder): if vetoed, no migration

3. **Board consult happens in Task (parallel):**
   - Each board member gives an opinion in their domain
   - `brd-cso` raises concerns about Neo4j's access control model
   - `brd-cqo` raises concerns about migration testing (no Pest equivalent for Neo4j)
   - `brd-cto` revises proposal to add Cypher security review + extended testing

4. **`brd-ceo` decides:** Conditional approval — "Approve pilot on non-critical path with security
   review first."

5. **ADR recorded:** `hq/brain/cortex-decisions.md:ADR-YYYYMMDD-NEO4J-PILOT` with full context +
   board opinions + CEO decision + conditions.

6. **RCCF issued:** `RCCF-YYYY-MM-DD-NEO4J-PILOT` from `brd-chief-of-staff`.

7. **Distributed:** `bck-lead` + `sec-lead` execute pilot with `ops-sandbox-executor` first.

**The CSO's veto power is absolute** — if `brd-cso` says "no security," the migration cannot proceed
even if everyone else agrees. This is constitutional.

## 44. Scenario 5: Smart Clarification Loop

**Owner:** "اعمل لي شيء حلو"

1. **`gtw-intake-reformer`** reformulates. Computes Law-16 ambiguity: **0.95 (95%)** — extremely
   vague. "حلو" means "nice" — but what is "nice"? For whom? For what purpose?

2. **Gatekeeper issues 3 sharp questions** + 24h timeout:
   - "حلو لمن؟ (children, professionals, family)"
   - "حلو أين؟ (web app, mobile, desktop)"
   - "حلو لـ ماذا؟ (productivity, entertainment, education)"

3. **Owner has 24h** to respond. If silent → `brd-arbiter` auto-escalated with full intake + clarification
   history. `brd-arbiter` has 24h window (Law 14) to decide:
   - (a) reformulate with best-available assumptions and proceed at higher lane
   - (b) freeze pending owner
   - (c) split into smaller unambiguous sub-tasks

4. **Max 2 clarification rounds** without arbiter — third round = mandatory escalation (anti-paralysis).

5. **If owner responds** (e.g. "لعبة تعليمية للأطفال على الموبايل"):
   - Reformulate again → ambiguity drops to 0.15 (15%) → proceed
   - Route per P-01.8 → likely Fateful (mobile game for children = privacy + security + UX heavy)

**This loop prevents the most common failure mode:** an AI assistant guessing what the owner means
and building the wrong thing for weeks.

---

# Part 9 — Setup, Run, Extend

## 45. Requirements & Dependencies

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

## 46. Installation & Setup

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

You should see all 4 guards exit 0 with **zero pending** warnings. If not, see Troubleshooting.

## 47. Running & Usage Examples

### 1. Submit a request as the owner (Arabic)
```bash
"أريد تطبيق متجر إلكتروني بسيط"
```
→ gateway receives, reformulates, classifies, routes.

### 2. Add a new agent (full lifecycle)
See [Scenario 3](#42-scenario-3-adding-a-new-specialist-tester).

### 3. Run a constitutional guard on demand
```bash
python3 hq/core/tooling/sofi-audit.py             # unified
python3 hq/core/tooling/registry_guard.py --strict  # 1:1 check
python3 hq/core/tooling/count_sync.py              # claims check
python3 hq/core/tooling/evidence_guard.py hq/core --strict  # file:line check
gitleaks git --staged --pre-commit --config gitleaks.toml  # secret check
```

### 4. Make a fateful decision (Board consult)
See [Scenario 4](#43-scenario-4-a-fateful-decision-board-consult).

### 5. Trigger WarRoom (P0 incident)
See [Scenario 2](#41-scenario-2-a-p0-production-incident).

## 48. Extending the System

### Adding a new agent
1. Read `hq/core/templates/agent-prompt-template.md`
2. Create `.opencode/agent/<name>.md` with frontmatter (name · description · mode · model)
3. Add capsule: `hq/core/domain/rooms/<room>/agents/<name>/{capabilities,senses,memory}.yaml`
4. Add row to `hq/core/nexus/registry.yaml:200+` (in correct room)
5. Add block to `hq/core/nexus/personas.yaml` (Arabic name + role)
6. Add block to `hq/core/nexus/routing.yaml` (model + effort + budget)
7. Add row to room `charter.md` + bump `Agent count:`
8. Add row to `.opencode/skills/INDEX.md` if new skill
9. Bump `hq/core/tooling/registry_guard.py:20` + `count_sync.py:23`
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
1. Use `sec-mcp-vetting` skill to vet the server (mandatory)
2. Add to `hq/core/nexus/mcp-routing.yaml`
3. Add to `opencode.json`
4. Update `sofi-mcp-fleet` documentation

### Creating a new project
```bash
# Use the project-spawn skill
"sofi-project-spawn my-new-project"
```
→ creates `projects/my-new-project/brain/{CONTEXT,DECISIONS,HANDOFFS,LESSONS}.md` + template stack.

## 49. Developer Guidelines

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

# Part 10 — Reference & History

## 50. Versioning & History (Full Timeline)

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
| 2026-09-05 | `README full rewrite` | 830 lines · 24 sections · 100% Law 4 evidence · commit 98900ef |

## 51. Troubleshooting & FAQ

**Q: A guard is red — what do I do?**
A: Read the error message — it tells you exactly which file:line is wrong. Then either:
- Update `registry.yaml` to match the disk
- Add the missing agent file
- Fix the file:line citation
- Revert the offending commit (do not amend force-push)

**Q: `pre-commit` failed mid-commit — what now?**
A: `git status` to see staged files, fix the issue, `git add`, `git commit --amend --no-edit`
(only if not pushed yet).

**Q: How do I add a new Law?**
A: You can't (alone) — Law modification requires **brd-ceo approval** + CORTEX record +
constitutional review. See AGENTS.md final section.

**Q: How do I get my PR merged faster?**
A: Follow the 4 owner approval points + ensure all 4 guards are green + write a clear PR
description with file:line evidence.

**Q: The owner wrote in informal Arabic — do I respond informally?**
A: **Yes** for tone, **no** for substance. Use simple Arabic (Law 11) but keep constitutional
precision. The "why it matters" focus is required.

**Q: Can I use Vue.js / Angular / Symfony / raw PHP?**
A: **No.** Stack Lock R3 forbids them. The only path is owner directive recorded in CORTEX.
Don't ask twice.

**Q: Why so many protocols? Isn't this bureaucracy?**
A: It's not bureaucracy — it's **legibility**. Every step has a `file:line` proof. When something
breaks (and it will), the postmortem is trivial because the trail exists. The alternative is
"works on my machine" debugging.

**Q: Can I use a paid API?**
A: **No.** INT-0003 auto-rejects. Every tool must be free. If you need a paid one, the answer
is no + find the free alternative.

**Q: PENDING warnings appeared — what do I do?**
A: This means the disk + registry + textual claims have drifted. Read the warning — it tells you
which one. Then:
- If 08-data exists → run the Phase-3 migration to remove it
- If r3.1-reconciliation exists → remove it (already complete)
- If `archive/audit-all-phase3/` has stale source.md → remove (no longer needed)
- If `system-state-current.md` mentions "114 agents" or "15 rooms" without "historical" marker → re-mark

**Q: I'm a new developer — where do I start?**
A: In this order:
1. `AGENTS.md:1` (the constitution)
2. `hq/core/SOFI-QUICK-REFERENCE.md` (1-page map)
3. `hq/core/system-state-current.md:1` (binding state)
4. `SOFI-INSTITUTION-COMPLETE-REPORT-2026-09-05.md` (on your desktop) — the live dashboard
5. `hq/core/standards/pipeline-production-line.md` (the S1→S6 map)
6. Run `bash hq/core/tooling/hooks/pre-commit` to see the guards in action
7. Open one issue for a small improvement + follow the full pipeline

## 52. License & Contributing

**License:** see `LICENSE` (project root). SOFI HQ is constitution-governed; contributing
requires following the 4 owner approval points + the 4 constitutional guards + the 16 laws.

**Owner authority:** any modification to the constitution (AGENTS.md) requires the explicit
recorded decision of `brd-ceo` in `hq/brain/cortex-decisions.md`. The owner (highest authority)
can override any decision via direct order, also recorded in CORTEX.

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
