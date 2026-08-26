---
name: qa-test-plan
description: Quality gate playbook (Gate 5) — a test plan then execution (unit/e2e/manual) then a coverage report, regression status, and design audit, ending in a documented evidence-backed gate pass/reject decision. Triggers — "quality gate", "Gate 5", "test plan", "pass or fail the gate", "regression check", "coverage report", "audit the design before delivery", "QA sign-off". Invoked when finished outputs arrive needing a documented decision on crossing the quality gate before delivery upward.
---

# qa-test-plan — The Quality Gate Playbook (Gate 5)

> **Law 8:** no delivery without review, no review without evidence. The quality gate is the last line before escalation — it passes by evidence or is rejected by evidence.

## 🎯 When to invoke (When) ⬛
- A ready output (code/screen/API) arrives needing a quality-gate crossing decision before delivery to brd-ceo.
- A comprehensive test plan (unit + e2e + manual) requested for a feature or fix.
- A coverage report or documented regression status needed before launch.
- Auditing design/interface behavior against the reference before approval.

**Do not invoke** for: writing the feature code itself (that's the engineering rooms), building the raw evidence block (use `sofi-evidence`), or building the delivery ticket (use `sofi-handoff`).

## ⬛ DFR mode — reviewing designs before freeze (INT-GTW-024)
You are the second signer of the design-freeze gate (`gates.yaml#dfr`). Before signing: check ux-flows against the frozen openapi-spec, schema-contract, and design-tokens literally — any deviation = signature refusal and return to S3. Your output on approval: dfr-signoff.

## 📥 Required inputs (Inputs) ⬛
- Formal RCCF work order (Law 5) — no gate execution without it.
- Output under test: code path/branch, environment URL, or build artifact.
- Acceptance criteria and gate thresholds: coverage threshold, critical paths list, design reference.
- A runnable execution environment (test commands, test data).

## 🔧 Steps (Steps) ⬛
1. **Test plan** — receive the RCCF and write the plan: scope, risks, critical paths, case matrix (happy/edge/negative), pass criterion per type. Distribute across room specialists via Task by specialization (never execute yourself — Law 3/9).
2. **Unit execution** — run unit suites (`qa-test-architect`/`qa-automation-engineer`). Log exit code + passed/failed count per suite.
3. **E2E execution** — run automated scenarios for critical paths (`qa-automation-engineer`). Log results + logs/screenshots.
   Approved tools: E2E via `playwright-skill` or `cypress-skill`; visual audit via `smartui-skill`; browser exploration via `webapp-testing`; test-framework migration via `test-framework-migration-skill`.
4. **Manual exploration** — execute non-automatable cases (`qa-manual-explorer`). Document reproduction steps per observation.
5. **Coverage report** — collect coverage percentage against threshold; identify gaps in critical paths (`qa-perf-analyst` for performance when needed).
6. **Regression status** — compare against baseline (`qa-regression-warden`): did existing behavior break? Log the results diff.
7. **Design audit** — match interface/behavior against reference and a11y (`qa-design-auditor`). Record before/after.
8. **Gate decision** — review all evidence. Assemble the evidence block (below). Issue PASS only if every criterion holds; otherwise FAIL with a reason per failed item.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: the **quality gate decision** — `PASS ✅` or `FAIL ❌` — with justification per criterion and a fixes list on rejection.
- **Evidence (Law 4) — QA type:** use the `sofi-evidence` skill. Four elements mandatory:
  - **Test plan** — scope + case matrix + pass criterion per type.
  - **Execution results** — per suite: command + exit code + `N passed / M failed` + log/screenshot.
  - **Coverage** — actual percentage vs threshold + critical-path gaps.
  - **Regression status** — baseline comparison: `no regressions` or the regression list with `file:line`.

```
### Gate 5 Decision — qa-lead — <timestamp>
- Decision: PASS ✅ | FAIL ❌
- Test plan: <scope> — cases: 24 (12 happy / 8 edge / 4 negative)
- Unit: `<cmd>` → exit 0 → 120 passed / 0 failed
- E2E: `<cmd>` → exit 0 → 18 passed / 0 failed — log: artifacts/e2e.log
- Coverage: 87% (threshold 80% ✅) — gaps: none on critical paths
- Regression: baseline <ref> → no regressions
- Design audit: ref <link> → match, a11y AA ✅ — artifacts/before-after.png
- Blockers (if FAIL): <criterion> — reason — file:line
```

## 🔗 Handoff ⬛
- Deliver decision + evidence block to **brd-ceo through the quality chain** only (Law 3) using `sofi-handoff`. Agents deliver to qa-lead; qa-lead consolidates and delivers upward.
- No direct delivery to the user. No addressing another room directly (Law 2) — any missing requirement escalates to brd-ceo.

## ♿ The a11y gate and multi-state testing (Accessibility & Multi-State Gate) ⬛

> CEO approval (after Board consultation, RCCF-2026-0719-UIUX-STANDARD): 4 UI/UX tactics became permanent quality standards — the a11y gate and multi-state testing are never exempted from Gate 5 for any user-visible screen.

### 1) The a11y gate (WCAG 2.1 AA — non-negotiable)
**Operation:** via `@axe-core/playwright` (the official dequelabs package — not a less-maintained community substitute) on **local/staging only**:

```ts
// a11y.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('a11y scan — <screen name>', async ({ page }) => {
  await page.goto('http://localhost:3000/<path>'); // local/staging only — production URLs forbidden
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .withRules(['target-size']) // not enabled by default within wcag21aa tags
    .analyze();
  expect(results.violations).toEqual([]);
});
```
Run command: `npx playwright test a11y.spec.ts`

**⛔ Critical condition (Law 10):** local/staging only. Any live production URL is forbidden as a direct testing target regardless of reason — targeting production with an a11y command = immediate L3 (freeze + CEO escalation).

**Mandatory checks:**
- **Color contrast (1.4.3 / 1.4.11 — AA):** normal text ≥4.5:1, large text (≥18pt or ≥14pt bold) ≥3:1, non-text interface elements (field borders/active icons) ≥3:1.
- **ARIA roles and labels:** correct `role` for every interactive element, a non-empty accessible name (`aria-label`/`aria-labelledby`), logical `heading` order without skipped levels.
- **Keyboard navigation (2.1.1 / 2.1.2):** every mouse function has a keyboard equivalent, no focus traps, logical `Tab` order, `Enter` activates and `Esc` closes. **Note:** axe-core only checks static DOM rules — actual navigation is tested additionally with explicit keyboard simulation via Playwright (`page.keyboard.press(...)`), as a complement not a substitute for axe.
- **Visible focus (2.4.7 — AA):** visible outline during keyboard navigation; `outline: none` without a visual alternative = FAIL.
- **Touch targets:** the automatically checkable minimum is **24×24 CSS px** (2.5.8 Target Size Minimum — WCAG **2.2** AA; deliberate extension beyond literal 2.1 because WCAG 2.1 contains no AA-level target-size criterion at all). **44×44px remains the recommended best practice (matching 2.5.5 AAA), not a mandatory pass condition.** Enable the `target-size` rule explicitly in axe — disabled within default `wcag21aa` tags.
- **Dynamic status messages (4.1.3 Status Messages — AA):** the `Loading`/`Error` states (next section) must be announced to screen readers without forcibly stealing focus: `Loading` → `role="status" aria-live="polite"`; `Error` → `role="alert"` or `aria-live="assertive"`.

**Pass evidence:** command + exit code + **violation count as an explicit number**. Any unjustified violation lacking written justification = **FAIL**.

### 2) Multi-state component testing
Every interactive element (button/field/component) is tested in the **eight mandatory states**: `Default` / `Hover` / `Focus` / `Selected` / `Loading` / `Success` / `Empty` / `Error` — via `jest` or `vitest` (nearly identical syntax; vitest is API-compatible with jest):

```ts
import { describe, test, expect } from 'vitest'; // or jest per project
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

describe('Button — multi-state coverage', () => {
  test.each([
    ['default', {}],
    ['hover', { hovered: true }],
    ['focus', { focused: true }],
    ['loading', { loading: true }],
    ['success', { status: 'success' }],
    ['error', { status: 'error' }],
  ])('renders correctly in %s state', (stateName, props) => {
    render(<Button {...props} />);
    expect(screen.getByRole('button')).toBeInTheDocument();
    // additional assertions per state: aria-busy when loading, role=alert and aria-invalid when error
  });
});
```
**Any uncovered state = FAIL.** Record the result explicitly as `N/6 states`.

### 3) Proportionality (a mirror of Law 1 — proportional flow)
| Lane | a11y gate | Multi-State |
|---|---|---|
| **Standard/fateful** | full axe-core on every new screen in the flow (all tags + `target-size`) | 6/6 states per new/modified interactive component in the flow |
| **Fast (lite)** | never dropped — narrows to the changed screen/component only (not the whole flow) | narrows to states actually touched by the change (minimum: `Default` + modified state + `Focus`) |

**The precise difference:** what lite reduces is the **scope** of checking (number of screens/states), never **the gate itself**. Zero runs on any user-visible screen = automatic FAIL regardless of lane.

### 4) Crossing items within the Gate 5 decision
In actual use, two lines are added to the "Gate 5 Decision" block above (after the `Design audit` line and before `Blockers`) — **items added at usage time, without modifying the existing block template**:
```
- a11y gate: `npx playwright test a11y.spec.ts` → exit 0 → 0 violations ✅
- Multi-state coverage: <component> → 6/6 states ✅
```
Full gate PASS requires passing **both** with evidence (command + exit code + explicit number) — either failing = FAIL with reason and file:line under Blockers.

## ⛔ Constraints ⬛
- No PASS without complete evidence for the four elements — missing evidence = delivery rejected (L2).
- No PASS under speed pressure; the sole exception is CEO-declared emergencies (Law 8).
- The lead never executes tests personally — distributes and reviews by evidence (Law 3/9).
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Record the gate decision and justification in `hq/brain/cortex-decisions.md`, and evidence/session in `hq/brain/hippocampus-sessions.md` (Law 7).

## 📚 References ⬜
- `sofi-evidence` (evidence block) · `sofi-handoff` (RCCF ticket) · `hq/core/protocols.md` (Protocol 03) · `hq/core/contracts.md`.
- Owner: Quality room (10-quality) — qa-lead (Law 9).

## ⬛ Linear Program v2 (OWNER-DIRECTIVE-2026-0823-R2)
- **Position:** this skill executes the quality gate in S6 and governs stage crossings within the six-stage line S1→S6.
- **Add to its mandatory plan:**
  - (1) A coverage matrix for every endpoint of the OpenAPI contract issued by S4.
  - (2) Testing responses against the Envelope of `hq/core/standards/api-envelope.md` field by field.
  - (3) The eight interface states on both unified Flutter/Dart interfaces (R2); Next.js legacy for existing projects only.
  - (4) The installer scenario fully per `hq/core/standards/installer-standard.md`: clean install + a post-lock access attempt must fail 403.
  - (5) Design tokens compliance and unified Heroicons icons.
  - (6) Refusing passage without exit-code evidence.
- **Laws:** OpenAPI-first; cross-boundary mocks forbidden (internal unit testing exempt); capsule of `hq/core/standards/ddd-capsule.md` DO/DON'T table.
- **Delivery:** via `sofi-evidence` with a documented crossing report per stage.
