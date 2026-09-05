# `hq/core/constitution_articles/` — Articles of the Constitution

> The **articles** that make up the SOFI HQ constitution (alongside `AGENTS.md`). Each article
> is a deep-dive into one area of organizational law. The articles are referenced by the
> protocols and the gates.

These are **supreme law** — any change requires `brd-ceo` approval recorded in CORTEX. The
articles are **constitution** (not operational law) and bind every agent.

---

## The 11 articles

| # | Article | Topic | One-line summary |
|---|---------|-------|------------------|
| 00 | `00-operating-system.md` | **Operating System** | SOFI HQ as an operating system for AI harnesses — the meta-article |
| 01 | `01-work-order.md` | **Work Order** | The RCCF flow (Request → Clarify → Confirm → Fullfil) — Law 5 binding |
| 02 | `02-grounding.md` | **Grounding** | How agents ground their claims (file:line + Context7/DeepWiki) — Law 4 |
| 03 | `03-verification.md` | **Verification** | The 4 constitutional guards + pre-commit — Law 12 |
| 04 | `04-reflection.md` | **Reflection** | How the organization learns (HIPPOCAMPUS + knw-reflector) — Law 7 |
| 05 | `05-token-economy.md` | **Token Economy** | Model routing per task class (workhorse / gatekeeper) — P-12 |
| 07 | `07-security-law.md` | **Security Law** | STRIDE + DFR + License + Secrets — Laws 8 + 15 |
| 08 | `08-handoff-law.md` | **Handoff Law** | The hierarchical path + JSON ticket — Laws 2 + 3 + P-02 |
| 09 | `09-research-law.md` | **Research Law** | Research before design (P-18) + Research-to-Design Bridge (P-19) — Law 4 |
| 10 | `10-lifecycle-gates.md` | **Lifecycle Gates** | S1→S6 + 9 gates + DFR + 4 owner approval points — Laws 1 + 11 |
| 11 | `11-intake-orchestration.md` | **Intake Orchestration** | gtw-intake-reformer + 5-section reformulation + Law 16 clarification loop |

> **Note:** articles 06 (and any missing numbers) are reserved for future use.

---

## The article vs. protocol distinction

- **Article** = supreme law (constitutional) — binds every agent — changes only with `brd-ceo`
  approval
- **Protocol** = operational law (procedural) — applies in specific contexts — may be amended
  within the article's framework

For example: `08-handoff-law.md` (article) defines the principle; `protocols.md:P-02` (protocol)
defines the operational rules (JSON ticket + checkpoint + acceptance).

---

## How to read this directory

**First-time readers:**
1. `00-operating-system.md` — the meta-article (the constitution in 1 page)
2. Then drill into the article you care about

**Editors:**
- New article = `brd-ceo` approval + ADR in CORTEX
- Amending an article = same process (supreme law)
- Adding a new protocol that references an article = lighter ceremony (knw-lead)

---

## The constitution as a whole

```
AGENTS.md                           ← supreme law (16 laws)
└── hq/core/constitution_articles/   ← 11 articles — deep-dive per topic
    ├── 00-operating-system.md      ← the meta-article
    ├── 01-work-order.md
    ├── ...
    └── 11-intake-orchestration.md
```

```
hq/core/protocols.md                ← 17 protocols (P-01..P-20) — operational law
hq/core/contracts.md                ← 10 contracts (Constitution-Article 5)
hq/core/standards/                  ← 22 standards
hq/core/nexus/                      ← registry + personas + pipeline + gates + routing + MCP
hq/core/domain/                     ← DDD rooms + context-map
hq/core/tooling/                    ← 4 constitutional guards + pre-commit
```

---

## See also

- [`../README.md`](../README.md) — `hq/core/` parent
- [`../../../AGENTS.md`](../../../AGENTS.md) — supreme law
- [`../protocols.md`](../protocols.md) — operational law
- [Top-level README](../../../README.md)
