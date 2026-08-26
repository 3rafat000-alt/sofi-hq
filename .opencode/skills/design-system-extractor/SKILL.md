---
name: design-system-extractor
description: >-
  Analyzes competitor screenshots to extract design tokens (color palette, typography scale, spacing
  grid, component inventory) and compares them against the SOFI design system. Triggers — "extract
  design tokens", "analyze competitor UI", "competitive UI analysis", "palette from screenshot",
  "typography scale analysis", "spacing grid detection". Invoked by dsn-competitive-ui-analyst
  (room 03) under RCCF work orders.
---

# design-system-extractor — Competitor Design-Token Extraction

> **Protocol 18:** extracts principles, never pixels (P-18.3). Verbatim copying = L3.

## 🎯 When to invoke (When)
- Competitive UI teardown requested by `dsn-lead`.
- Feeding `dsn-design-system-gen` with adoptable opportunities (P-18.4).

## 📥 Inputs (Inputs)
| Field | Type |
|---|---|
| `screenshot_url` / captured screens | string[] (browser capture via Chrome-DevTools/Playwright) |
| `focus_area` | enum: colors · typography · spacing · components · all |

## 📤 Outputs (Outputs)
1. `color_palette` — {primary, secondary, accent, neutral} with hex values sampled from evidence.
2. `typography_scale` — {h1, h2, h3, body, caption} sizes/weights as observed.
3. `spacing_grid` — detected rhythm (e.g. [4, 8, 16, 24, 32]) with confidence note.
4. `components_used` — component inventory per screen (cards, modals, nav patterns).
5. `comparison` — strengths · gaps · opportunities vs the SOFI design system.

## 🛠️ Procedure (How)
1. Capture key screens of each competitor (login → core loop → goal) at consistent viewport.
2. Extract tokens screen-by-screen using zoomed inspection; cite screenshot URL per token claim.
3. Build the triad comparison against current SOFI tokens/components.
4. File raw analyses under `projects/<slug>/brain/visual-patterns/competitive/`; deliver report to `dsn-lead`.

## 🚫 Rules
- Every extracted value must trace to a cited screenshot — no eyeballed claims (Law 4).
- Recommendations state the principle ("why it works"), never just the shape.
- Output feeds integration decisions; `dsn-design-system-gen` performs any system change.

*Owner order 2026-08-26 · assigned room: 03-design · ledger: domain/SKILLS-ASSIGNMENT.md*
