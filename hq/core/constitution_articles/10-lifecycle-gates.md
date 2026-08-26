# Article 10 — Lifecycle Gates (the 9 gates)

Foundation: serves Teaching II (Hierarchical Flow) and Teaching V (Continuous Metamorphosis). Machine twin: `hq/core/nexus/gates.yaml`.

## The 9 gates

| # | Gate | Owner | Output | Exit bar |
|---|------|-------|--------|----------|
| 0 | Inception | 01-strategy | Blueprint + Problem Statement | Project charter exists |
| 1 | Discovery | 02-research | Personas + Journey Map (Mermaid) | Evidence-grounded, cited |
| 2 | Solution Design | 03-design | Prototype Spec + Content Strings | WCAG 2.2 AA · every screen traces to journey |
| 3 | Architecture | 04-architecture (+08-data, 09-security) | Schema + ERD + OpenAPI + Threat Model | Schema↔screens traceable · migrations reversible |
| 4 | Build | 05-backend · 06-frontend · 07-mobile | Code per frozen contract | All states built · leads merge at close |
| 5 | Quality | 10-quality | Test reports + Design Audit | ONE PASS/BLOCK · coverage >90% · TTI <2s |
| 6 | Staging / UAT | 11-devops | Staging URL + UAT log | UAT pass · pass^k on critical paths |
| 7 | Production | 11-devops | Prod confirmation + tested rollback | Blue/Green healthy |
| 8 | Observe | 12-observability | SLO report + journey drop-off insights | SLO breach → re-enters Gate 1 |

## Gate discipline

- No skip. Gate numbers move monotonically, never jump more than +1 — except brd-ceo-authorized Fast-Track per P-01.8 (collapses Gates 1–3). *_(Amendment INT-GTW-024 · 2026-08-24 — v2: S2 crosses Gate-3 on paper and S3 is sealed with the Design-Freeze Review (DFR) signature; map: `nexus/gates.yaml#stage_map`.)*
- Advance = gtw-gatekeeper adversarial check.
- Tag at close: the gate owner records the passage in `hq/brain/cortex-decisions.md` (P-13.6; gate-tag tooling retired 2026-07-16 → hierarchical enforcement).
- Journey-less → Backlog.
- Two tracks: Fast-Track collapses Gates 1–3 (authorized exclusively by brd-ceo — single text: PROTOCOLS P-01.8); Deep-Audit takes all 9.

## Parallelism

Squads fan out only behind frozen input:
- Gate 3: schema · API · security — behind frozen prototype
- Gate 4: backend · frontend · mobile — behind frozen Gate-3 bundle
- Gate 5: automation · manual · perf · pentest — behind merged build
