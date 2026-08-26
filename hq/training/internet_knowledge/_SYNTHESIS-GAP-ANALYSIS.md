# 🧬 Knowledge Harvest Synthesis and Gap Analysis — SOFI Self-Development Initiative
> **Source:** owner order 2026-08-24: "read the entire organization, then learn from the internet, then develop the agents, the rooms, and the way of working step by step"
> **Evidence:** 21 files in this folder (~150KB from lawsofux · microsoft/khalil-stemmler DDD · react.dev · flutter.dev · nextjs.org · anthropic engineering ×2) + the full internal audit (constitution/protocols/contracts/105 agents)

---

## ✅ What We Already Apply at World-Class Level (keep it)
| Anthropic/industry pattern | Our current implementation |
|----------------------|----------------|
| Routing workflow | `gtw-router` + three-track classification |
| Orchestrator–Workers | brd-ceo → room leads → agents |
| Evaluator–Optimizer | quality gates G3/G5 + gtw-external-reviewer |
| Prompt chaining | six-lane pipeline S1..S6 under contract |
| Design-before-code | "design first" doctrine INT-0004 (predates their recommendation!) |
| Skills/MCP wiring | ‏105/105 agents wired |

## 🔴 P0 — Critical Gaps (affect every working session)
| # | Gap | External evidence | Proposed fix |
|---|--------|----------------|------------------|
| **1** | **No systematic evaluation of the agents themselves** — we measure products, not workers | Anthropic: LLM-as-judge + rubric evals as a maturity pillar | add a "self-evaluation criteria" section to every room lead + a periodic agent-review protocol (simple rubric: law compliance / evidence quality / accuracy) |
| **2** | **Token economy without numbers** — Article Four mentions economy but with no numeric budgets | multi-agent teams consume ~15× a normal conversation; without a cap cost explodes | assign default token budgets per track in gtw-budget-warden (fast/standard/critical) + automatic warnings on breach |
| **3** | **Context engineering undocumented** — agent prompts are huge and there is no guide for "what loads and when" | Compaction + sub-agent contexts are the core of Anthropic's efficiency | a "minimum context" annex in STRUCTURE or PROTOCOLS: every agent starts with the least sufficient context and expands on demand |

## 🟡 P1 — High-Value Knowledge Enrichment (from the harvest itself)
| # | Opportunity | Harvested source | Fix |
|---|--------|----------------|----------|
| 4 | inject the six UX laws into knowledge-cx-uiux.md (Fitts·Jakob·Miller·Peak-End·Aesthetic-Usability·Serial-Position) with practical store applications | lawsofux.com | new section "Tree 4 — Laws" + linking dsn/res to the source |
| 5 | enrich DDD-STANDARDS: Aggregate boundaries + Ubiquitous Language | stemmler 19KB + MS 14KB | two new paragraphs with a DO/DON'T table |
| 6 | enrich the React engineer prompt with the react.dev mental model (composition/state/isolation) | stack-react-learn 14KB | update fnt-react-engineer |
| 7 | enrich mob-flutter-engineer with the official app-architecture layers | stack-flutter 4KB | update the agent + link mob-flutter-kb |
| 8 | update res-web-scrape: ‏Crawl4AI is now actually installed (remove the lazy-install wording) + ready crwl examples | today's achievement | edit the skill |
| 9 | document the access rule: NN/g and Baymard block bots ← scraped manually via 🪁 Kitesurf only | today's experience recorded in _harvest.log | note in res-web-scrape |

## 🟢 P2 — Sustainable Organizational Development
| # | Opportunity | Fix |
|---|--------|---------|
| 10 | a "quarterly harvest" ritual — periodically re-scrape the elite sources (the script is ready: harvest*.sh as inspiration for an official skill) | new `knw-knowledge-harvest` skill owned by room 13 |
| 11 | terminology alignment: a table mapping Anthropic patterns ↔ our protocols in protocols.md (documentation, not change) | reference appendix |
| 12 | Next.js knowledge applies to legacy projects only (R2 retired it for new ones) — documented inside the harvest file itself | partially done by this document |

## ❌ What the Network Refused (transparency)
nngroup.com and baymard.com/martinfowler.com block bots (450b/791b/113b empty) — our alternative: manual scraping with 🪁, already in place, with evidence in `projects/_intake/`.
