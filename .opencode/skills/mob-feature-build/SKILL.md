---
name: mob-feature-build
description: >
  When building or modifying a mobile feature end-to-end. Triggers — Arabic: "build mobile feature",
  "new Flutter screen", "add app state", "profile app performance", "prep store release",
  "test on Android/iOS". English: "build mobile feature", "new Flutter screen",
  "add app state management", "profile app performance", "prep store release",
  "test on Android/iOS". Invoked when a complete mobile feature is required spanning build + state + performance + platform + release.
---

# mob-feature-build — The Mobile Feature Build Playbook ⬛

> A unified production line for a mobile feature: from Flutter/native code to state to perf profile to platform testing to release check — with evidence and hierarchical delivery.

## 🎯 When to invoke (When) ⬛
- Building a new mobile feature (screen/flow) in Flutter or platform native code.
- Modifying an existing feature touching state, performance, or store compliance.
- Requesting a perf profile or release readiness check for a mobile feature.
**Do not invoke** for: purely visual UI design (Design room), backend APIs (Backend room), or merely asking about build status without execution.

## 📥 Required inputs (Inputs) ⬛
- RCCF work order (Law 5) — no execution without it.
- Feature description: flow, screens, acceptance criteria.
- Target platform(s) (Android / iOS) and acceptable performance thresholds (fps, jank, startup time).
- Mobile project path on the main tree (Law 10 — no isolated copy, no worktree).

## 🔧 Steps (Steps) ⬛
1. Read the feature and acceptance criteria from the RCCF; fix platforms and thresholds before any code.
2. **Consult official knowledge (`mob-flutter-kb`):** before writing any unfamiliar pattern (architecture/state/platform-integration/perf), query the local official Flutter/Dart knowledge base and attach a `file:line` reference for every adopted pattern — no unsourced improvisation in critical patterns.
3. **Build (mob-flutter-engineer / mob-platform-engineer):** implement the widget/screen in Flutter or native channel code directly on the project tree; record `file:line` for every change.
4. **State management (mob-state-engineer):** wire the feature into the approved state solution (Bloc/Riverpod/Provider); reinforce leak-free disposal and lifecycle management.
5. **Perf profile (mob-perf-profiler):** run the profiler (DevTools) on the platform; measure fps, frame jank, startup time, memory; save perf profile + screenshot.
6. **Platform testing (mob-flutter-engineer):** run `flutter analyze` and `flutter test`; install the feature on at least one device/emulator per platform and capture a result screenshot.
   Invoke `flutter-testing-skill` (widget/integration/golden); native testing via `espresso-skill` (Android) / `xcuitest-skill` (iOS) by mob-platform-engineer; `detox-skill` for React Native; `appium-skill` ⚠️ blocked until sec-lead review.
7. **Release check (mob-release-engineer):** verify version bump, package signing, store permissions, and Play/App Store rules before delivery.
8. Produce the evidence block (see below) via the `sofi-evidence` skill.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: a built mobile feature wired to state, with a perf profile and release check report ready for review.
- **Evidence (Law 4)** — Engineer type via the `sofi-evidence` skill:
  - `file:line` for every code change (Dart/native).
  - Exit codes for `flutter analyze` and `flutter test` + test outputs.
  - **perf profile:** fps/jank/startup/memory figures from DevTools before/after.
  - **screenshot:** the feature running on the platform + the performance result capture.
  - Release check line: version/signing/permissions + store rules outcome.

## 🔗 Handoff ⬛
- Deliver output to **mob-lead** (Mobile room lead) only (Law 3) via the `sofi-handoff` skill.
- No direct delivery to the user. No addressing another room directly (Law 2) — coordination through leads.

## ⛔ Constraints ⬛
- Work directly on the project's main tree only (Law 10): worktrees, isolated copies, or forgotten branches forbidden.
- No delivery without perf profile + screenshot + exit codes (Laws 4 + 8).
- No execution without RCCF (Law 5). Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Record important feature decisions (state solution choice, performance thresholds, store exception) in `hq/brain/cortex-decisions.md` (Law 7).

## 📚 References ⬜
- `hq/core/contracts.md` — the Mobile room's delivery contract.
- Room agents: mob-flutter-engineer, mob-platform-engineer, mob-state-engineer, mob-perf-profiler, mob-release-engineer.

## ⬛ Linear Program v2 (OWNER-DIRECTIVE-2026-0823-R2)
- Position: S5 exclusively — partner of merged team 06·07 on the unified Flutter/Dart stack (web and mobile from the same code and design).
- Operating condition: the frozen openapi-spec from S2 + DFR signature + **S4 completed with a live security-checked backend** — no screen before that.
- Contracts: receive openapi-spec + approved design-tokens; deliver screens under `lib/features/<f>/{domain,application,infrastructure,presentation}` per the Flutter branch of `hq/core/standards/ddd-capsule.md`.
- Data: a unified dio interceptor receiving the Envelope of `hq/core/standards/api-envelope.md` and mapping its states onto the eight interface states.
- Theming from design tokens via ThemeData with two modes (light/dark) — official Material icons.
- Cross-boundary mocks forbidden (internal unit testing exempt).
- Delivery via `sofi-evidence` with file:line evidence for every change.
