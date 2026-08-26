---
name: mobbin-scraper
description: >-
  Extracts UI patterns and user flows from curated visual platforms (Mobbin, Page Flows, Land-book,
  Awwwards, Ilham.io) per Protocol 18. Triggers — "scout patterns", "find UI examples", "checkout flow
  examples", "onboarding patterns", "visual research", "Mobbin search", "pattern scout". Invoked by
  res-visual-pattern-scout (room 02) under RCCF work orders.
---

# mobbin-scraper — Visual Platform Pattern Extraction

> **Protocol 18 feed:** outputs land in `projects/<slug>/brain/visual-patterns/` with the mandatory
> five fields (P-18.2). Max 3–5 examples per request — curation over volume.

## 🎯 When to invoke (When)
- A design task needs real-world pattern evidence before `dsn-ui-designer` starts (P-18.1).
- Periodic trends refresh every 40 agent turns (P-18.5).

## 📥 Inputs (Inputs)
| Field | Type | Notes |
|---|---|---|
| `pattern_type` | string | e.g. "checkout", "onboarding", "dashboard", "login" |
| `platform` | enum | ios · android · web |
| `industry` | string (optional) | e.g. "ecommerce", "fintech", "realestate" |

## 📤 Outputs (Outputs)
1. `screenshots` — array of source URLs (evidence, Law 4).
2. `user_flow` — step-by-step flow description entry → goal.
3. `elements` — UI components used per step (buttons, forms, navigation).
4. `best_practices` — the UX rationale: why this pattern works.

## 🛠️ Procedure (How)
1. Resolve platform priority for the request type: apps → Mobbin first; flows → Page Flows; web → Land-book/Awwwards; Arabic/RTL → Ilham.io.
2. Search and shortlist candidates; capture screenshots via browser tooling (Playwright/Kitesurf).
3. For each candidate record the four output fields above — no field may be empty (P-18.2).
4. Classify by industry + component taxonomy; write files to `projects/<slug>/brain/visual-patterns/<pattern>.md`.
5. Deliver compiled report to `res-lead` within 2 agent turns.

## 🚫 Rules
- Never strip attribution: every example keeps its source URL.
- Never exceed 5 examples per request without an explicit lead override.
- Findings are evidence only — adaptation into SOFI's design system is room 03's job (P-18.4).

*Owner order 2026-08-26 · assigned room: 02-research · ledger: domain/SKILLS-ASSIGNMENT.md*
