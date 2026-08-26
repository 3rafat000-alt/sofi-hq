---
name: dsn-design-review
description: >-
  Review and audit an existing design/interface against professional standards: Nielsen's 10 heuristics + a
  6-axis scored evaluation + a P0/P1/P2 findings table + WCAG 2.2 accessibility audit + screening against
  slop patterns, with concrete actionable alternatives. Triggers: "review this design",
  "evaluate the interface", "UX audit", "is this design good?", "screen critique", "design audit",
  "review a React/Flutter screen", "review this design", "UX audit",
  "design critique", "score this UI", "heuristic evaluation". Invoked inside the Design room when professional judgment on an existing design (screen, flow, component) is requested — before approval or before re-delivery to frontend.
---

# dsn-design-review — Design Review & Audit ⬛

> **Value:** turns "it looks nice" into measured professional judgment: scores on known axes, severity-classified findings, and specific fixes — review without criteria = personal taste, not a decision.
> **Scientific source:** the `/design-review` methodology from `plugin87/ux-ui-agent-skills` (Nielsen + 6 axes + findings table) and modeling after `ui-ux-design-review-agent` (code analysis → consistency → alternative palettes).

## 🎯 When to invoke (When) ⬛
- A design/screen/flow is ready and needs professional sign-off before delivery or gate crossing.
- A user complaint or conversion drop on a specific path needs design diagnosis.
- A redesign: audit first, then upgrade without breaking what works.
- Direct UI code review (React/Vue/Flutter): reading components and evaluating structural and visual consistency.

**Do not invoke** for: generating a new design system (that's `dsn-design-system-gen`), building the component itself (that's the Frontend room), or automated functional QA tests (that's `qa-test-plan`).

## 📥 Required inputs (Inputs) ⬛
- **RCCF work order (Law 5)** — no execution without it.
- The review subject in one of its forms: screenshots, Figma file, component code (`file` paths), or a local staging URL (never production).
- Project/audience brief — reviewing without audience context = empty judgments.
- Target accessibility standard: WCAG 2.2 AA minimum.

## 🔧 Steps (Steps) ⬛
1. **Fix the scope:** which screens/components/flows? Who is the audience and what is each page's goal?
2. **Walk Nielsen's ten heuristics** one by one: visibility of system status, match between system and the real world, user control and freedom, consistency and standards, error prevention, recognition rather than recall, flexibility and efficiency of use, aesthetics and minimalist design, error recognition and recovery, help and documentation — per heuristic: applies/violated + exactly where.
3. **Score the six axes** 1–5 with justification: visual consistency · information hierarchy clarity · accessibility (a11y) · interactive feedback (states) · cognitive load · content tone and microcopy.
4. **Run the accessibility audit practically:** measured contrast (4.5:1 text / 3:1 UI / focus 3:1), full keyboard navigation + visible focus, ARIA names and roles, touch targets ≥ 24×24px (44 recommended for primary actions), no color-only information transfer, RTL support if the product is Arabic. Use axe-core via Playwright on available local/staging.
5. **Check the eight states** of every interactive element: default/hover/focus/disabled/loading/error/selected/empty — any missing state = a finding.
6. **Screen for slop patterns** (AI slop tells): default purple→blue gradient, three identical cards without reason, Inter/Roboto at display sizes, dummy names ("John Doe"), emoji as icons, a uniform default 300ms transition everywhere, dominant centered hero, generic salesy copy.
7. **Sort findings into a table:** every row = `P0/P1/P2` + precise location (screen/component:line or screenshot region) + problem + concrete proposed fix + effort (S/M/L).
   - **P0** = blocks usage or breaks WCAG AA or damages trust (must be fixed before any approval).
   - **P1** = clear experience damage (before launch).
   - **P2** = quality improvement (backlog).
8. **Offer alternatives, not bare criticism:** for major problems propose 2–3 concrete treatment directions (alternative palette, restructuring, flow simplification) with a trade-off per option.
9. Review quality (Law 8) then produce the evidence block via `sofi-evidence`.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- **Output:** one review report under `artifacts/<ticket>/design-review.md`:
  - Nielsen table (10 rows) · six-axis scores · findings table classified P0/P1/P2 · proposed alternatives.
- **Evidence (Law 4) — Designer type** via `sofi-evidence`:
  - **screenshot** for every documented visual issue (before).
  - **axe-core results**: violation count + exit code (if run).
  - **Measured contrast table** for suspect color pairs.
  - Issue locations in code: `component/path.tsx:line` or `widget_path.dart:line`.
  - Every axis score justified with at least one line.

## 🔗 Handoff ⬛
- Deliver the report to **your room lead `dsn-lead`** only (Law 3) via the `sofi-handoff` skill.
- P0 = a rework recommendation before crossing the Gate; final decision belongs to `dsn-lead` then `brd-ceo`.
- No direct delivery to the user, no addressing frontend directly (Law 2).

## ⛔ Constraints ⬛
- No score without justification, no finding without location + proposed fix — bare criticism rejected.
- No direct code/design modification: this skill evaluates and recommends only; execution belongs to its room (Law 2).
- Automated testing on local/staging exclusively — never production.
- Taste never overrides standards: any taste recommendation must not break WCAG 2.2 AA.
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Record the approval/rework result and critical P0s in project memory `projects/<name>/brain/DECISIONS.md` (Law 7).

## 📚 References ⬜
- `github.com/plugin87/ux-ui-agent-skills` — design-review methodology + a11y-audit.
- `github.com/Laith0003/ux-skill` — anti-pattern checklist for visual screening.
- Sibling skills: `dsn-design-system-gen` (the cure), `fnt-ux-lint` (fast deterministic check), `frontend-design` (direction).
- **Owner (Law 9):** Design room 03 — `dsn-lead`.

## ⬛ Linear Program v2 (OWNER-DIRECTIVE-2026-0823-R2)
- **Your position:** this skill serves stage S3 before DFR signature — the gate crossing from designs to execution is DFR itself (v2 line).
- **Your contracts:** receive a design and deliver a review report that mandatorily checks: eight-state interface coverage, compliance of three-layer tokens across both modes and RTL, unified Heroicons icon names in `heroicon:<name>` format with size type (outline/solid/mini) per `hq/core/standards/nextjs-standards-legacy.md` §10, and WCAG 4.5:1 contrast.
- **Knowledge reference:** `hq/core/standards/knowledge-cx-uiux.md` — UI branches and states.
- **Laws:** OpenAPI-first, no cross-boundary mocks (internal testing substitutes exempt), Envelope `hq/core/standards/api-envelope.md` for response states, delivery via `sofi-evidence`.
