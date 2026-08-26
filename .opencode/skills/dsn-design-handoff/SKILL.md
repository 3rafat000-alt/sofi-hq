---
name: dsn-design-handoff
description: >-
  When preparing a design package ready for frontend. Triggers — Arabic: "hand the design to frontend",
  "UI delivery package", "design tokens ready", "interaction specs", "before we build the interface",
  "the design is done — package it for implementation". English: "hand off design to frontend",
  "prepare UI spec", "design tokens package", "interaction specs ready",
  "design-to-dev handoff", "package screens for build". Invoked inside the Design room before crossing Contract 03 to frontend — never for designing a screen from scratch.
---

# dsn-design-handoff — The Design-to-Frontend Handoff Playbook ⬛

> Converts an approved design into an execution package that tolerates no interpretation: UI spec + tokens + interaction specs + a11y audit + before/after screenshots — frontend receives it and executes literally (Contract 03).

## 🎯 When to invoke (When) ⬛
- Design completed and approved inside the Design room, ready for delivery to frontend (06) via Contract 03.
- Screens + states + tokens + motion need assembling into one executable package.
- Frontend requested a formal specification before starting interface build (Gate-2/Gate-4).
**Do not invoke** for: designing a screen/identity from scratch (that's `dsn-ui-designer`/`dsn-brand-designer`), or implementing interface code (that's the Frontend room).

## 📥 Required inputs (Inputs) ⬛
- RCCF work order (Law 5) — no execution without it; defines scope and required screens.
- The approved design: Figma/HTML reference for screens and their states.
- Identity and system: the design tokens source (colors, typography, spacing, motion).
- Required responsive breakpoints and target a11y criteria (WCAG 2.2 AA minimum).

## 🔧 Steps (Steps) ⬛
1. Read the RCCF; fix the screen list and the mandatory **eight states**: Default / Hover / Focus / Selected / Loading / Success / Empty / Error.
2. Write the **UI spec** per screen: structure, elements, breakpoints, source reference — into `artifacts/<ticket>/specs/`.
3. Export **design tokens** (colors, typography, spacing, motion) as a unified file into `artifacts/<ticket>/tokens/`.
4. Author **interaction specs**: transitions, motion timing/easing, behavior per state — into `specs/`.
5. Run the **a11y audit**: contrast, focus order, ARIA names, touch targets; record results in the audit report.
6. Capture **before/after screenshots** per screen into `artifacts/<ticket>/screens/` (before/after design or baseline vs approved state).
7. Review completeness internally (Law 8): any screen lacking interaction states → returned before delivery.
8. Produce the evidence block (see below) via the `sofi-evidence` skill.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: one unified design package under `artifacts/<ticket>/` with three folders matching Contract 03: `screens/` + `tokens/` + `specs/`, plus the a11y audit report.
- **Evidence (Law 4) — Designer type:** use the `sofi-evidence` skill:
  - **screenshot before/after** per screen (file path inside `artifacts/<ticket>/screens/`).
  - **design tokens** exported (tokens file path + values).
  - **a11y audit**: audit results (contrast/focus/ARIA) with pass/fail per item.
  - The covered screens-and-states list (eight-state coverage).

## 🔗 Handoff ⬛
- Deliver the package to the **room lead `dsn-lead`** only (Law 3) via the `sofi-handoff` skill as an RCCF ticket.
- Only `dsn-lead` crosses Contract 03 to frontend lead `fnt-lead`. Never address the Frontend room directly (Law 2).
- No direct delivery to the user. Explicit delivery acceptance (P-02.4) closes Gate-2 and prepares Gate-4.

## 🔬 a11y automation + token sourcing (Automation & Token Sourcing) ⬛
- **Reading tokens:** use `get_variable_defs` to extract (colors/typography/spacing/motion) → export into a unified file in `tokens/`; use `get_design_context`/`search_design_system` for context. The **fallback**: the approved tokens file in the repo when MCP is unavailable.
- **A11y automation:** after packaging, run axe-core via Playwright on **local/staging only (never production URLs)** → read the report → fix color contrast (WCAG 2.1 AA) and missing ARIA before delivery. Log exit code + violation count as evidence inside the `sofi-evidence` block.

## ⛔ Constraints ⬛
- No delivery without the eight states per interactive screen — state-incomplete designs return (Contract 03).
- No overriding frontend's executive decisions; no interface code implementation — the handoff is specification only.
- All assets inside the project's main tree under `artifacts/` — no worktrees or isolated copies (Law 10).
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Record the final package decision (screens, tokens version, a11y result) in `hq/brain/cortex-decisions.md` (Law 7).

## 📚 References ⬜
- `hq/core/contracts.md` → Contract 03 (Design Handoff to Frontend).
- `hq/core/protocols.md` → P-02.4 (delivery acceptance), P-03.8 (evidence types).
- Shared skills: `sofi-evidence`, `sofi-handoff`.
- Design skills feeding the package: `frontend-design` (visual direction), `theme-factory` (themes), `brand-guidelines` (identity), `canvas-design` (visual assets).
- **Owner (Law 9):** Design room 03-design — `dsn-lead`.

## ⬛ Linear Program v2 (OWNER-DIRECTIVE-2026-0823-R2)
- **Position:** this skill executes the Contract 03 crossing gate from stage S2 to S5 within the six-stage line S1→S6 — no delivery package before crossing the review.
- **Mandatory package content:** three-layer tokens exportable to Tailwind semantic + Flutter ThemeData two modes, every screen spec with its eight states, a component list with unified Heroicons names and size types per `hq/core/standards/nextjs-standards-legacy.md §10`, and a mapping of each screen to its endpoints in the OpenAPI contract issued by S4 where present.
- **Consumers:** `fnt-component-build` for web and `mob-feature-build` for mobile.
- **Laws:** OpenAPI-first, cross-boundary mocks forbidden (internal testing substitutes exempt), Envelope `hq/core/standards/api-envelope.md`, capsule `hq/core/standards/ddd-capsule.md`, `sofi-evidence` file:line delivery.
