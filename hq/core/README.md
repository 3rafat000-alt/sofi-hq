# `hq/core/` — The Constitution Material

> **Authoritative source of organizational law.** Every byte in this directory is part of the SOFI
> constitution, governed by `AGENTS.md:1`. Edit only with `brd-ceo` approval recorded in CORTEX.

This directory is the **supreme law of the organization** — protocols, contracts, standards, gates,
pipelines, rooms, tools, and templates. Treat every file as a binding artifact.

---

## What this directory contains

```
hq/core/
├── README.md                        ← you are here
├── protocols.md                     ← 17 protocols (P-01..P-20) — operational law
├── contracts.md                     ← 10 cross-room contracts (Constitution-Article 5)
├── constitution-master.md           ← supreme law of the organization
├── system-state-current.md          ← BINDING current operating state (the only legal source of truth)
├── SOFI-QUICK-REFERENCE.md          ← 1-page map (decision tree)
├── structure-standard.md            ← naming conventions + old←new map (Law 13.5)
│
├── nexus/                           ← the registry nexus (see hq/core/nexus/README.md)
│   ├── registry.yaml                ← 17 rooms · 121 agents (Law 12 — single source of truth)
│   ├── personas.yaml                ← Arabic names + roles per agent
│   ├── pipeline.yaml                ← S1→S6 production line
│   ├── gates.yaml                   ← G0..G8 + DFR (Design-Freeze Review)
│   ├── routing.yaml                 ← model + effort + budget per agent
│   ├── mcp-routing.yaml             ← 27 MCP servers · 100% local
│   ├── models.yaml                  ← LLM model routing per task class
│   ├── room-priority.yaml           ← T0..T4 priority tiers
│   ├── skill-routing.yaml           ← skill → room → lead map
│   ├── rccf-registry.yaml           ← central RCCF ticket tracker (Audit-ALL)
│   └── bus/                         ← ticket bus implementation (if any)
│
├── domain/                          ← DDD domain layer (see hq/core/domain/README.md)
│   ├── context-map.yaml             ← single official inter-room interface
│   └── rooms/                       ← 17 rooms (charter + capsules + agents/)
│
├── standards/                       ← 22 binding standards (see hq/core/standards/README.md)
│
├── gate_checklists/                 ← per-gate criteria (gate-0.md ... gate-8.md + dfr.md)
│
├── design/                          ← system-ddd-blueprint + 9 Mermaid diagrams
│   ├── system-ddd-blueprint.md
│   └── diagrams/                    ← 9 *.mmd (source) + 9 *.svg + 9 *.png
│
├── tech_templates/                  ← template skeletons for new agents/MCPs
│   ├── agent-prompt-template.md
│   └── mcp-agent-annex.md
│
├── templates/                       ← operational templates (report + skill)
│   └── report-template.md
│
├── tooling/                         ← 4 constitutional guards + pre-commit (see hq/core/tooling/README.md)
│
├── archive/                         ← historical + audit-all-phase3 (Law 13.5)
│
├── constitution_articles/           ← Article 00 (The Constitution) + future articles
│
├── protocols/                       ← protocol subdirectory
│
└── runbooks/                        ← operational runbooks
```

---

## How to read this directory

**First-time readers:**
1. `AGENTS.md` (at the repo root) — the 16 binding laws
2. `hq/core/SOFI-QUICK-REFERENCE.md` — 1-page map
3. `hq/core/system-state-current.md` — current state (the only legal source of truth)
4. `hq/core/nexus/registry.yaml` — the official registry
5. Then drill into the subdirectory you care about

**Editors:**
- Every edit must be `file:line`-cited (Law 4)
- Every new file must have `## FILE: <path>` header (Law 13.3)
- Every change must pass the 4 guards (Law 12)
- Any change to `protocols.md` / `contracts.md` / `AGENTS.md` requires `brd-ceo` approval

---

## The 17 protocols (P-01..P-20)

> Source: `protocols.md` — operational law descending from the constitution. P-15 retired.

| ID | Name |
|----|------|
| P-01 | Pipeline (entry → 3 lanes → 24h clarification timeout) |
| P-02 | Handoff (JSON ticket ≤280 chars + checkpoint + acceptance) |
| P-03 | Evidence (file:line + exit code + log) |
| P-04 | Escalation (chain of responsibility) |
| P-05 | Conflict (priority arbitration) |
| P-06 | Memory (with P-06.7 summarizer ritual) |
| P-07 | Communication (ticket bus) |
| P-08 | Security (P-08.1 secrets via gitleaks) |
| P-09 | Quality (K1–K17 thresholds) |
| P-10 | Emergency (incident response + WarRoom + AMYGDALA) |
| P-11 | Tool (4 guards + pre-commit + sofi-audit wrapper) |
| P-12 | Token Economy (model routing per task class) |
| P-13 | Gate (0→1→2→3→4→5→6→7→8 immutable sequence) |
| P-14 | Memory Isolation (Law 7 — org vs project) |
| P-16 | Direct-on-Project (Law 10 v2 — main tree + ephemeral branches ≤72h) |
| P-17 | Context Minimization (JSON ticket + evidence digest) |
| P-18 | Visual Research (research before design + design-system integration) |
| P-19 | Research-to-Design Bridge (mandatory handoff + traceability + joint co-sign) |
| P-20 | Living Docs & Failure Mode (max 1 commit lag + weekly brain backup + monthly failure-mode review) |

**Priority chain:** `Pipeline (01) > Security (08) > Emergency (10) > Handoff (02) > Direct-on-Project (16) > Context Minimization (17) > Quality (09) > Gate (13) > Evidence (03) > Memory Isolation (14) > Escalation (04) > Conflict (05) > Memory (06) > Communication (07) > Tool (11) > Token Economy (12)`

A lower-priority protocol cannot override a higher-priority one. A protocol that contradicts the
constitution is **void**.

---

## The 10 cross-room contracts

> Source: `contracts.md` — Article 5 of the constitution.

| # | Contract | Purpose |
|---|----------|---------|
| 01 | **Intake** | 14-gateway → 00-boardroom → room leads — request intake + classification + dispatch |
| 02 | **Research** | 02-research → 03-design — JTBD + journey + pain-points → UX flows |
| 03 | **Design** | 03-design → 06-frontend + 07-mobile + 08-localization — frozen tokens + DFR |
| 04 | **Data** | 04-architecture → 05-backend + 12-observability — ERD + schema-contract |
| 05 | **API** | 04-architecture → 05-backend → 06-frontend + 07-mobile — frozen OpenAPI |
| 06 | **Security** | 09-security → all rooms — STRIDE + DFR co-sign + veto (per gate) |
| 07 | **Quality** | 10-quality → all engineering rooms — Gate-5 verdict + advisory reports |
| 08 | **Operations** | 11-devops → 12-observability + 13-knowledge — deploy + rollback + observability |
| 09 | **Observability** | 12-observability → 15-warroom (P0) — SLO breach → incident response |
| 10 | **Knowledge** | 13-knowledge → all rooms — CORTEX (decisions) + HIPPOCAMPUS (sessions) + AMYGDALA (incidents) |

---

## See also

- [`hq/brain/`](../../brain/README.md) — organization memory (CORTEX + HIPPOCAMPUS + AMYGDALA)
- [`hq/engine/`](../../engine/README.md) — live publishing layer
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — supreme law
