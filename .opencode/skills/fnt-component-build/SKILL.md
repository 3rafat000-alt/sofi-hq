---
name: fnt-component-build
description: >-
  Playbook for building a frontend component from an approved design specification (Contract 03) through to evidence-backed delivery.
  Triggers — Arabic: "build a component", "implement this design as a component", "component from Figma", "build a React button/modal/table", "turn the design spec into code", "implement a Vue screen". English: "build a component", "implement this design", "code the Figma spec", "build React/Vue component", "turn design tokens into UI", "implement screen from design". Invoked inside the Frontend room when an approved design spec arrives needing conversion into a shippable component.
---

# fnt-component-build — Building a Frontend Component from the Design Specification ⬛

> We convert a Contract 03 spec into a literally faithful React/Vue component, backed by a11y + performance evidence + screenshot + tests — no creative improvisation.

## 🎯 When to invoke (When) ⬛
- An approved design spec arrived from the Design room via Contract 03 (`screens/ tokens/ specs/`) and needs implementation as a component.
- An RCCF work order requests building or modifying a React/Vue component from defined tokens and interaction states.
**Do not invoke** for: designing a component from scratch without a spec (that's the Design room's work — Law 2), nor modifying the design spec itself (requires dsn-lead approval through leads).

## 📥 Required inputs (Inputs) ⬛
- Formal RCCF work order (Law 5) — no execution without it.
- Contract 03 design package: Figma/HTML references + `tokens/` (colors, typography, spacing, motion) + breakpoints + all interaction states (hover, focus, error, loading, disabled, empty). A spec without interaction states → returned; never start.
- The project main tree and target component path (Law 10 — work directly on it).

## 🔧 Steps (Steps) ⬛
1. Verify spec completeness: every interaction state + every breakpoint present. Missing → return to lead before any code (never guess).
2. Work **directly on the project main tree** (Law 10). Worktrees, isolated copies, or long-lived branches forbidden.
3. Bind design tokens to code variables (never hard-coded values) and build the React/Vue component matching the spec literally. When Design guidance is absent: `frontend-design` for visual direction and `theme-factory` for theming.
4. Apply all specified interaction states and breakpoints — none missing, none added.
5. Verify a11y: ARIA roles/labels, contrast, keyboard navigation, visible focus (run axe/lighthouse a11y).
6. Measure performance: component bundle size, re-renders, CLS/LCP where applicable (run actual measurement, never estimate).
7. Take before/after screenshots of states into `artifacts/`.
8. Write/run the component test (unit + interaction) via `jest-skill`/`vitest-skill` and log exit code and results.
9. **Pass output through `fnt-ux-lint`** (the deterministic checker) — zero critical/high is a continue condition; any finding gets fixed then re-scanned.
10. Produce the evidence block via `sofi-evidence` (see below).

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: a spec-faithful React/Vue component on the main tree + its tests + its screenshots.
- **Evidence (Law 4) — extended Engineer type, via `sofi-evidence`:**
  - `file:line` for every component/test change + exit code for build/test commands + test output (passed/failed).
  - **Screenshot:** `artifacts/<component>-<state>.png` before/after per major interaction state.
  - **a11y:** axe/lighthouse report (violations = 0 or justified) + contrast + focus verification.
  - **Perf:** bundle size measurement + applicable Core Web Vitals (LCP/CLS/INP) with actual figures.
  - Token compliance: proof that values come from `tokens/`, not hard-coded.

## 🔗 Handoff ⬛
- Deliver component + evidence block to **fnt-lead only** (Law 3) via the `sofi-handoff` skill.
- No direct delivery to the user. No addressing the Design room or any other room directly (Law 2) — any fidelity question goes through fnt-lead.

## 🧱 Atomic Design standard + multi-state testing (Atomic + Multi-State) ⬛
- **Atomic build order:** Atoms → Molecules → Organisms → Pages.
- **Multi-State Testing:** test every component in its six states (Default/Hover/Focus/Loading/Success/Error) via jest/vitest — any uncovered state = incomplete.
- **A11y gate:** axe (0 violations or justified) on **local/staging only** — never production URLs.
- **Token source:** Figma MCP `get_variable_defs` as base; **runtime truth + fallback = the tokens file inside the repo** (tailwind.config/CSS variables). No hard-coded values.
- **Per-stack binding:** React→shadcn/ui, Vue→shadcn-vue/reka-ui — neither imposed on the other.
- **Golden rule:** start from "the goal", not "the look".

## ⛔ Constraints ⬛
- No modifying the design spec without dsn-lead approval through leads — execution is literal (Contract 03).
- Worktree / isolated copy / forgotten branch forbidden — work directly on the main tree (Law 10). Any temporary technical branch merges and deletes before task closure.
- No delivery without review and complete evidence (a11y + perf + screenshot + test) — Law 8.
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Record important implementation decisions (justified deviation, token choice) in `hq/brain/cortex-decisions.md` (Law 7).

## 📚 References ⬜
- `hq/core/contracts.md` → Contract 03 (Design Handoff to Frontend).
- Shared skills: `sofi-evidence`, `sofi-handoff`.

## ⬛ Linear Program v2 (OWNER-DIRECTIVE-2026-0823-R2)
- Position: S5 exclusively — merged team 06·07 on the unified Flutter/Dart stack for web and mobile.
- Operating conditions: frozen openapi-spec from S2 + signed dfr-signoff + **S4 complete (live security-checked backend)** — no component before it (backend_complete_before_ui).
- Default platform: Flutter/Dart from the approved design system (ThemeData receives design-tokens) — official Material icons.
- Legacy-only path (existing projects non_retroactive): Next.js per hq/core/standards/nextjs-standards-legacy.md with @heroicons/react icons and src/features capsule.
- Data via Envelope hq/core/standards/api-envelope.md with one unified adapter — cross-boundary mocks forbidden (internal unit testing exempt).
- The eight interface states mandatory for every data component.
- Delivery sofi-evidence file:line.
