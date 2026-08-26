---
name: fnt-ux-lint
description: >-
  A fast deterministic checker for interface code against slop patterns and AI fingerprints
  (anti-slop) plus core a11y rules — no interpretation, no taste judgments: fixed rules runnable in CI,
  emitting a findings table with severity levels and blocking merges at Critical/High. Triggers:
  "scan the code for slop", "lint the UI", "does the code look AI-generated?",
  "pre-approval check", "slop scan", "quick a11y check". English: "ux lint", "anti-slop scan", "check AI
  fingerprints in UI", "pre-merge UI check". Invoked inside the Frontend room after generating/modifying any interface code and before human review or merging.
---

# fnt-ux-lint — The Deterministic UI Slop Linter (Anti-Slop UX Linter) ⬛

> **Value:** the first mechanical gate before any taste judgment: a quick fixed-rule sweep capturing slop fingerprints and basic a11y violations — same input always yields the same result, and zero Critical/High findings is a merge condition.
> **Scientific source:** the deterministic linter concept from `Laith0003/ux-skill` (152 regex rules without LLM) + hardcodes/contrast gates from `plugin87/ux-ui-agent-skills`.

## 🎯 When to invoke (When) ⬛
- After generating or modifying interface code (React/Vue/HTML/CSS/Flutter) before handing it to review.
- As a pre-merge gate: `Critical/High = blocks merge`.
- A quick sweep of a large codebase before tasking `dsn-design-review` with deep auditing.
- Verifying a previous round's fixes introduced no new violations.

**Do not invoke** for: taste judgment and aesthetics (that's `dsn-design-review`), building components (that's `fnt-component-build`), or functional E2E tests (that's QA).

## 📥 Required inputs (Inputs) ⬛
- **RCCF work order** of the parent task (Law 5) — the check runs within its cycle.
- Target code paths (folder/files) — default: the project's interface folders.
- The approved tokens file if present (to detect hardcoded values).

## 🔧 Steps (Steps) ⬛
1. **Set the scan scope** excluding: `node_modules`, `.git`, `dist`, `build`, `.next`, `vendor`.
2. **Scan the nine categories** (per rule: file:line location + literal evidence):
   | Category | Example rules |
   |-------|-------------|
   | A11y | image without `alt`, button as `<div onClick>`, input without label, removed focus outline (`outline: none` without alternative), interactive icon < 24px |
   | Content | dummy text ("Lorem", "John Doe", "Test User"), emoji as icon/status dot, generic CTA ("Click here", lone "Submit") |
   | Layout | 3 identical cards as a lazy template without content reason, stereotypical centered hero, unintended horizontal overflow |
   | Typography | Inter/Roboto/Arial at display sizes, no declared type scale (scattered random px sizes) |
   | Color | hardcoded colors outside tokens (raw `#hex` in components), default purple→blue gradient, dark text on dark background |
   | Quality | CSS selectors conflicting and overriding each other, duplicated copy-paste of an existing component |
   | Visual | shadow/radius borders inconsistent with tokens, icons from multiple sources |
   | Motion | uniform default 300ms on every transition, animation ignoring `prefers-reduced-motion` |
   | Performance | large image without lazy loading, full font instead of subsets |
3. **Classify every finding:** `critical / high / medium / cosmetic` — critical/high break a11y AA or make the UI look machine-generated.
4. **Emit the report:** ordered critical→cosmetic then by location, with a counter per severity + **exit code**: 0 clean, non-zero when critical/high exist.
5. **Never fix inside the check** — the linter reports only; fixing returns to `fnt-component-build` then **re-run the scan** until clean.
6. Produce the evidence block via `sofi-evidence`.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- **Output:** lint report under `artifacts/<ticket>/ux-lint-report.md`: findings table (category, rule, file:line location, evidence, severity) + counter summary + verdict (PASS/FAIL).
- **Evidence (Law 4) — Engineer type** via `sofi-evidence`:
  - The executed command + full exit code.
  - Counters: `critical=N high=M medium=K cosmetic=J`.
  - Finding locations with `file:line` + quoted literal line.
  - Final PASS/FAIL verdict with the applied criterion (fail-on: high).

## 🔗 Handoff ⬛
- Deliver the report to **your room lead `fnt-lead`** only (Law 3) via the `sofi-handoff` skill.
- FAIL → fixing inside the room via `fnt-component-build` then re-scan — a FAIL never travels upward except with a documented fix plan.
- No direct delivery to the user and no addressing the Design room directly (Law 2) — pattern recommendations travel through leads.

## ⛔ Constraints ⬛
- **Strict determinism:** same code = same result always. No taste judgment inside the scan.
- The linter reports and never modifies — any code change is outside this skill's scope.
- Rules serve standards: any "taste" rule must have its reason documented in this file before enforcement.
- No exceptions without logging: overriding a rule requires a written note with the reason in the report.
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Record recurring critical patterns (the same finding across multiple sessions) as a lesson in project memory `projects/<name>/brain/LESSONS.md` (Law 7).
- Proposing a permanent new rule → through your lead to `skill-forge` (updating this skill), never local improvisation.

## 📚 References ⬜
- `github.com/Laith0003/ux-skill` — the deterministic LLM-free linter philosophy + nine-category classification.
- `github.com/plugin87/ux-ui-agent-skills` — no-hardcode/no-emoji rules and contrast gates.
- Sibling skills: `dsn-design-review` (deep audit after scanning), `dsn-design-system-gen` (tokens source), `fnt-component-build` (the fix).
- **Owner (Law 9):** Frontend room 06 — `fnt-lead`.

## ⬛ Linear Program v2 (OWNER-DIRECTIVE-2026-0823-R2)
- **Your position:** this skill is a quality gate inside S5, before any human review or merge within the six-stage line S1→S6.
- **Fixed deterministic rules added:**
  - (1) Any raw color value outside tokens = Critical.
  - (2) Any icon not from `@heroicons/react` or duplicated manual SVG = High per `hq/core/standards/nextjs-standards-legacy.md` §10.
  - (3) A data component without the eight states = High.
  - (4) Business logic in `src/app` or presentation instead of features/domain = Critical — breaking the capsule of `hq/core/standards/ddd-capsule.md`.
  - (5) Hard mocks crossing room boundaries = Critical (internal unit testing exempt).
  - (6) A response not matching the Envelope `hq/core/standards/api-envelope.md` = Critical.
- **Laws:** OpenAPI-first • Delivery via `sofi-evidence` with a findings report.
