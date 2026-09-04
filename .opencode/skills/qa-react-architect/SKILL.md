## FILE: .opencode/skills/qa-react-architect/SKILL.md
---
name: qa-react-architect
description: >-
  React/Next.js + DDD end-to-end QA architecture protocol — five mandatory phases, 28 acceptance points measured against approved documents (frozen OpenAPI, DFR design tokens, S5/S6 criteria), browser-fingered Web-Vitals + bundle evidence, and a unified advisory report. Triggers — "run the React QA architecture review", "verify the React/Next.js app against the contract", "5-phase React check", "28 acceptance points", "review the React architecture and performance", "DDD layer conformance", "Web Vitals / Lighthouse / bundle analysis", "WCAG 2.1 AA + ARIA + RTL review". Invoked by qa-lead (room 10) assigning a React/Next.js delivery to the React/DDD QA Architect — never for general test strategy (qa-test-plan), Flutter/mobile (qa-flutter-architect), or gate verdicts (qa-lead / brd-cqo).
---

# qa-react-architect — The React/DDD QA Architecture Protocol

> **Core value:** an end-to-end React/Next.js + DDD review protocol whose every acceptance point is measured against SOFI's approved documents — the report advises, the room lead decides. **No gate verdicts, no verdicts, no security classification (C3).**

## 🎯 When to invoke (When) ⬛
- A React/Next.js delivery (SSR/SSG via Next.js App Router, or SPA via Vite/CRA legacy) arrives needing architecture + performance + accessibility + UX verification in one coherent review.
- qa-lead needs browser-fingered Web-Vitals + bundle evidence (Lighthouse · `@next/bundle-analyzer` / `vite-plugin-bundle-analyzer` · React Profiler · Chrome DevTools Performance) before assembling Gate-5 evidence.
- A frozen-contract + DDD-layer cross-check is required: does this React/Next.js screen/feature conform to the approved OpenAPI + DDD context map + DFR design tokens?
**Do not invoke** for: general test strategy or Gate-5 decision (use `qa-test-plan`, decided by qa-lead) · Flutter/mobile (qa-flutter-architect owns that — C4) · Vue/Angular/Svelte/jQuery/Bootstrap (Stack Lock R3 — wrong stack, return to qa-lead) · security classification (sec-lead → brd-cso) · running any forbidden op (C6).

## 📥 Required inputs (Inputs) ⬛
- Formal RCCF work order from `qa-lead` (Law 5) — no execution without it.
- The delivery under review: project path, feature/screen scope, build/run target (Next.js or Vite).
- The approved references: frozen OpenAPI / schema-contract (S2) + DFR design tokens (S3) + S5/S6 gate criteria — each with a locatable `file:line`.
- An approved live target (production URL, staging URL, or local `next dev`/`vite` dev server) — else the report records a documented exit-0 skip (C7).

## 🔧 Steps (Steps) ⬛

### Phase 1 — Reference & Environment Verification
1. Verify the RCCF (Law 5) and locate every approved reference with `file:line` (C5). **Missing reference → stop: return to qa-lead with a gate-return note — never invent an in-report standard.**
2. Target pre-check (C7): detect the approved live target. Present → capture fingerprint (Next.js version · React version · Node version · browser + version · viewport size · network profile · Lighthouse version). Absent → record a documented skip (`exit 0`, `no-target`), report without runtime phases, never fake measurement.

### Phase 2 — Architecture Review (paper + code, against documents)
3. Verify DDD layer separation: `src/domain/{entities,value-objects,aggregates,repositories}` · `src/application/{hooks,services,dto}` · `src/infrastructure/{api,storage}` · `src/presentation/{pages,components,layouts}`. Any layer bleeding = P0 finding.
4. State management review: identify tool (Redux Toolkit / Zustand / Jotai / React Context / React Query) · check slice/store alignment with bounded contexts · check React Query staleTime/cacheTime for server state · check useState/useReducer overuse in large components.
5. Code splitting: `React.lazy` + `Suspense` at route level; main bundle ≤ 200KB gzipped.
6. Memoization discipline: `React.memo` on heavy components with stable props · `useCallback` for handlers passed to children · `useMemo` for expensive computations.
7. Render batching: state changes in async handlers must be batched.
8. Network: detect duplicate API calls (over-fetching/under-fetching) · Error Boundaries present · cache headers reviewed.
9. TypeScript: no `any` except where strictly justified (and commented).
10. Map every screen/feature to its frozen OpenAPI contract point — **no code path without a contract point** (OpenAPI-first).
11. Verify no transient mocks cross boundaries (internal unit tests exempt); API responses follow `hq/core/standards/api-envelope.md`; structure follows `hq/core/standards/ddd-capsule.md` DO/DON'T.
12. Check state management / navigation / DI against the project's approved `projects/<slug>/brain/DECISIONS.md` + CONTEXT.
13. Any design question surfacing during review → document as a **gate return** (S2/S3), never resolved inside the report (Design-First · C5).

### Phase 3 — Performance Measurement (C6 + C7)
14. Run `lighthouse <url>` (desktop + mobile profiles: mobile = 4× CPU slowdown + Slow 3G) → record Performance/Accessibility/Best Practices/SEO scores and the binding Web Vitals (LCP < 2.5s · FID/INP < 100ms · CLS < 0.1 · FCP < 1.8s · TTI < 3.8s) **with fingerprint + exit code**.
15. Run Chrome DevTools Performance recording for page load (desktop + mobile throttling) → record frame timing, main-thread long tasks, layout shifts **with fingerprint**.
16. Run bundle analysis: `@next/bundle-analyzer` for Next.js, `vite-plugin-bundle-analyzer` for Vite. Identify top 5 largest chunks. Main bundle ≤ 200KB gzipped is binding.
17. Run React Profiler: record a session (scroll, button click, menu open). Identify slow components. Count unnecessary re-renders.
18. Only the whitelisted commands run — any other need returns to qa-lead unexecuted (C6).

### Phase 4 — Accessibility & UX Verification (C6 + C7)
19. Run Axe DevTools or Lighthouse a11y scan → verify zero serious/critical violations.
20. Manual keyboard nav: Tab/Shift+Tab/Enter/Space traverse all interactive elements in logical order.
21. Screen reader spot-check (NVDA/VoiceOver): at least the primary user flow.
22. Semantic HTML: header/nav/main/section/article/aside/footer used correctly; no div-button/div-anchor.
23. ARIA: roles correct · aria-label on icon-only buttons · aria-describedby for fields · aria-live for dynamic messages.
24. Contrast: text ≥ 4.5:1 · large text ≥ 3:1 · non-text elements ≥ 3:1.
25. Focus visible: outline not hidden.
26. RTL: layout mirrored via `dir="rtl"` or library; Arabic typography legible; icons direction-correct.
27. Responsive: tested at 360/768/1024/1440 widths.
28. States covered: loading (Skeleton/Spinner) · error (human message) · empty (no-data UI) · offline (network error UI) · dark mode if supported · fonts preloaded (no CLS).
29. Cross-check visual conformity to the DFR design tokens (colors/typography/spacing) — deviations are a point finding with `file:line`, never an aesthetic opinion.

### Phase 5 — Unified Advisory Report & Delivery
30. Score the **28 acceptance points** (table below) — each measured **against its approved document** (C5); each claim carries `file:line` + `exit code` + browser/device/network fingerprint (C7).
31. **Advisory verdict only (C3):** per-point pass / fail-with-reason — no gate decisions, no security classification, no release sign-off.
32. Sanitize transient output (identifiers, screenshots) before including any evidence — nothing leaves the working tree (C6).
33. Produce the evidence block (Law 4) and hand off to `qa-lead` (Law 3).

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: the **unified advisory report** (template below) + the 28-point score table + evidence block. Report = consultation for qa-lead's Gate-5 decision and brd-cqo.
- **Evidence (Law 4) — QA type:** use the `sofi-evidence` skill. Mandatory per claim: `file:line` · command + `exit code` · **browser/device/network fingerprint per Lighthouse/bundle/Profiler/a11y phase (C7)** · sanitized logs/dumps. Target absence = documented skip with exit 0 (C7).

### Unified Advisory Report Template (compact — full example in `references/acceptance-and-report.md`)
```
### React/DDD QA Architecture — Unified Advisory — <ticket-id> — <timestamp>
- Reviewed: <project/feature> · Scope: <screens/flows> · Stack: <Next.js/Vite + React + Node versions>
- References: OpenAPI <file:line> · DFR tokens <file:line> · S5/S6 criteria <file:line>
- Target: <url or dev-server> · Browser <ver> · Viewport <size> · Network <profile>   (per phase where applicable)
- Phases: 1 refs ✅ · 2 architecture: <n findings> · 3 perf: <n findings> · 4 a11y/UX: <n findings>
- 28 acceptance points: <pass-count>/28 advisory pass — <fail-count> findings (see score table)
- Web Vitals: LCP <lt> · FID/INP <lt> · CLS <lt> · FCP <lt> · TTI <lt> · main bundle <kb>
- Gate returns: <list of deviations returned to S2/S3 — never resolved here>
- Advisory: <overall consultation for qa-lead — NOT a gate verdict>
- Evidence: <evidence block per sofi-evidence — file:line · exit codes · fingerprints · sanitized dumps>
- Escalations: <any security-classified observation → qa-lead → sec-lead → brd-cso>
```

### The 28 Acceptance Points (scored against approved documents — C5)
**UI/UX & Design System (10):**
| # | Point | Measured against |
|---|-------|------------------|
| 1 | Harmony with design system (colors/typography/spacing tokens) | DFR design tokens |
| 2 | Visual hierarchy (heading scale · contrast · spacing rhythm) | DFR design tokens · WCAG 2.1 AA |
| 3 | 4/8pt spacing grid adherence | DFR design tokens · knowledge-cx-uiux |
| 4 | Responsive across ≥ 3 viewports (360/768/1024/1440) | DFR design tokens · uiux-standard |
| 5 | Loading states (Skeleton/Spinner) covered | knowledge-cx-uiux · uiux-standard |
| 6 | Error states (human message) covered | knowledge-cx-uiux · uiux-standard |
| 7 | Empty states (no-data UI) covered | knowledge-cx-uiux · uiux-standard |
| 8 | Dark mode support (if declared in design) | DFR design tokens |
| 9 | Fonts preloaded (no CLS from font swap) | DFR design tokens · Web Vitals |
| 10 | RTL correctness (mirroring · Arabic typography · icons direction) | rtl-mirror-validator · knowledge-cx-uiux |

**Performance & Web Vitals (6):**
| # | Point | Measured against |
|---|-------|------------------|
| 11 | LCP < 2.5s | Web Vitals · Lighthouse |
| 12 | FID/INP < 100ms | Web Vitals · Lighthouse |
| 13 | CLS < 0.1 | Web Vitals · Lighthouse |
| 14 | Main bundle ≤ 200KB gzipped | bundle-analyzer · stack tech budget |
| 15 | No unnecessary re-renders (React Profiler) | React Profiler · memoization discipline |
| 16 | Memoization in the right places (`memo`/`useCallback`/`useMemo`) | code review · React docs |

**Accessibility WCAG AA (6):**
| # | Point | Measured against |
|---|-------|------------------|
| 17 | ARIA labels on icon-only buttons + form fields | WCAG 2.1 AA · Axe |
| 18 | Keyboard navigation traverses all interactive elements | WCAG 2.1 AA · WCAG 2.4.7 |
| 19 | ARIA roles correct (no div-button/div-anchor) | WCAG 2.1 AA · WCAG 4.1.2 |
| 20 | Contrast 4.5:1 text · 3:1 large/non-text | WCAG 2.1 AA · WCAG 1.4.3 |
| 21 | Focus visible (outline not hidden) | WCAG 2.1 AA · WCAG 2.4.7 |
| 22 | Live regions for dynamic changes (toast/validation/async) | WCAG 2.1 AA · WCAG 4.1.3 |

**Code Quality & DDD Architecture (6):**
| # | Point | Measured against |
|---|-------|------------------|
| 23 | TypeScript — no unjustified `any` | TypeScript docs · projects/<slug>/brain |
| 24 | DDD layer separation (Domain/Application/Infrastructure/Presentation) | ddd-capsule.md |
| 25 | State management choice appropriate for bounded contexts | projects/<slug>/brain/DECISIONS |
| 26 | Tests present (unit + integration) | projects/<slug>/brain/DECISIONS |
| 27 | Public APIs documented (JSDoc/TSDoc) | TS docs · projects/<slug>/brain |
| 28 | Folders organized by bounded contexts | ddd-capsule.md · projects/<slug>/brain |

## 🔗 Handoff ⬛
- Deliver the advisory report + evidence block to **`qa-lead` only** (Law 3) via the `sofi-handoff` skill; qa-lead consolidates into Gate-5 and delivers upward.
- No direct delivery to the user. No addressing another room (Law 2). Security observations escalate only through qa-lead → sec-lead → brd-cso.

## ⛔ Constraints ⬛
- **Advisory only (C3, verbatim intent):** outputs are consultation feeding qa-lead's Gate-5 decision (and brd-cqo); no gate openings/rejections, no verdicts, no security classification; no direct delivery; no other-room addressing (Laws 2-3); escalation through qa-lead (security → sec-lead → brd-cso).
- **Scope (C4, verbatim intent):** React/Next.js products only — SSR/SSG (Next.js App Router) and SPA (Vite/CRA legacy) under the non-retroactive R2 contract; no Flutter/mobile (qa-flutter-architect owns that); no Vue/Angular/Svelte/jQuery/Bootstrap (Stack Lock R3 — wrong stack, return to qa-lead).
- **Command whitelist (C6, verbatim):** allowed: `lighthouse <url>` · `npx next build` (read-only on local) · `npx vite build` · `npm run analyze` · `npx @next/bundle-analyzer` · Chrome DevTools via MCP if available · Playwright `npx playwright test` for live E2E spot-checks (read-only, no destructive ops) · React DevTools/Profiler recording. Forbidden: any `npm publish` · any `git push --force` · any environment variable write · any cookie/storage tampering · any key access · any paid API · any destructive DB ops (INT-0003). Outputs sensitive/transient: sanitized before any documentation/evidence; never leave the tree.
- **Browser/Device/Network fingerprint (C7, verbatim):** every performance/accessibility report carries the browser/device/network/version fingerprint per Lighthouse/bundle/Profiler/a11y phase + pre-check: no target → documented skip with exit-0 (Law 4 executable on any environment).
- **License gate (Law 15):** any dependency suggestion cites `package + version + license evidence (file:line)`. Allowed: MIT · Apache-2.0 · BSD-2/3 · ISC · MPL-2.0. Vetoed: GPL/AGPL/SSPL and unknown.
- **Latest-Version-Mandatory:** before any code touching a library → Context7 MCP first; for any external repo claim → DeepWiki MCP.
- Never override any of the sixteen laws; a skill "saving time" by skipping the lead is rejected.

## 🧠 Memory ⬜
- Important decisions and findings patterns → recorded per Law 7 through the room (CORTEX for org-level records; `projects/<slug>/brain/` for project-level).

## 📚 References 📚
- `references/acceptance-and-report.md` — expanded 28-point acceptance matrix (measurement recipe per point) + full worked example of the unified report + the C6 whitelist/forbidden table.
- `hq/core/nexus/gates.yaml` (Gate-5 · DFR) · `hq/core/standards/api-envelope.md` · `hq/core/standards/ddd-capsule.md` · `hq/core/standards/knowledge-cx-uiux.md` · `hq/core/standards/stacks-tech.md` (R2) · `hq/core/system-state-current.md` · `hq/brain/cortex-decisions.md` (ADR-20260905-GTW-REACT-DDD-ARCHITECT).