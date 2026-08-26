---
name: bck-feature-build
description: Playbook for leading end-to-end backend feature builds in the Backend room — API/domain/queue/blade design, execution, actually-run tests, and code evidence, distributed across room agents by specialization. Triggers — "build backend feature", "implement API endpoint", "add service/queue/domain", "Laravel feature", "backend build playbook", "implement a new endpoint", "add an API or service or queue". Invoked when a backend feature ticket arrives at bck-lead from brd-ceo needing distribution, execution, and unified delivery.
---

# bck-feature-build — The Backend Feature Build Playbook ⬛

> Leading a backend feature from design to code evidence: smart distribution across room agents, direct execution on the main tree, testing, unified consolidation.

## 🎯 When to invoke (When) ⬛
- Receiving a backend feature ticket from `brd-ceo` (endpoint, domain service, job/queue, Blade page).
- A substantial change to existing backend logic requiring design + execution + testing.
- Wiring an external integration or async queue within a feature.

**Do not invoke** for: one-line bug fixes without design (use a direct track), frontend/mobile work (another room), or abstract code review without building.

## 📥 Required inputs (Inputs) ⬛
- **RCCF work order (Law 5)** — no execution or distribution without it. Request it from `brd-ceo` if missing.
- **The frozen OpenAPI contract from S2 + DFR signature (design-freeze gate)** — never build without both (openapi_first · design_before_code). Request them via brd-ceo if absent.
- Feature contract: inputs/outputs, scope rules, acceptance criteria — derived from the frozen contract and never contradicting it.
- Project path on the **main tree** (Law 10) — no worktree, no isolated branch.
- Architecture references if any (schema, ADR) relayed via `brd-ceo`.

## 🔧 Steps (Steps) ⬛
1. **Understand the ticket fully** before distribution: decompose the feature into components (API, domain, queue, blade, integration).
2. **Verify the frozen contract:** read the approved openapi-spec from S2 letter by letter — endpoints, signatures, and queue contracts derive exclusively from it; any uncovered need returns to the gate and is never invented in code.
3. **Distribute via Task by specialization** (every agent directly on the main tree, Law 10):
   - `bck-api-engineer` → API layer (routes, controllers, requests, resources).
   - `bck-domain-engineer` → domain logic (services, actions, models, migrations).
   - `bck-queue-engineer` → jobs, queues, async events.
   - `bck-blade-engineer` → Blade templates and server-side rendering.
   - `bck-integration-engineer` → external integrations and clients.
4. **Bind every agent to tests:** feature/unit tests written and actually run (no claims) — via `phpunit-skill` for tests and `laravel-dusk-skill` for browser tests on Blade pages; use `api-designer`/`api-documentation` when designing/documenting endpoints.
5. **Mandatory review:** pass output through `bck-code-reviewer`; on technical debt move in `bck-refactoring-surgeon`.
6. **Verify every agent's evidence** (`file:line` + exit codes) before acceptance — no evidence = rework (Law 8).
7. **Consolidate outputs** into one delivery + evidence block (see below) via the `sofi-evidence` skill.

## 🎛️ Mandatory API-UX (user experience starts in the backend) ⬛
> The interface cannot deliver good experience over a slow backend with chaotic contracts. Every API feature is built under these controls:
1. **Unified Response Envelope:** one shape for all successes and errors (`{ success, data, error: { code, message, field? } }`) via Exception Handler + unified Resources — so React/Flutter handle errors and loading states with one logic instead of one state per endpoint.
2. **Actionable error codes:** the error tells users what to do ("code expired, resend") not just a generic 500 — microcopy agreed with Design.
3. **No N+1:** queries with documented `eager loading` (`with(...)` / `load(...)`); any list endpoint proves its query count in tests (`DB::enableQueryLog` or assertCount) before acceptance.
4. **State-friendly contracts:** fields feeding loading/empty/invalidity indicators already present in responses (pagination meta, counts, statuses) — frontend never guesses.
5. **Balanced response time:** list endpoints ≤ 300ms on staging (p95) or a documented exception reason + caching plan.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- **Output:** a backend feature built on the main tree (API + domain + queue/blade as needed) with green tests, consolidated into one delivery.
- **Evidence (Law 4) — Engineer type** (via `sofi-evidence`, per agent then aggregated):
  - **code diff `file:line`** for every change (route/controller/service/migration/job/blade).
  - **test output** — actual feature/unit run results: `X passed / Y failed`.
  - **build/command exit code** — `php artisan test` / `migrate` → exit 0 + last lines.
  - **API-UX evidence:** a sample unified response (success + error) + query count for a list endpoint (proving no N+1).
- No complete evidence block = delivery rejected (L2).

## 🔗 Handoff ⬛
- Room agents deliver only to me (bck-lead) — they never address another room (Law 2).
- I deliver the consolidated result + evidence **upward to `brd-ceo`** exclusively (Law 3) via the `sofi-handoff` skill.
- No direct delivery to the user. No addressing another room directly.

## ⛔ Constraints ⬛
- **Law 10:** all work directly on the main tree. `.opencode/worktrees/` or any long-lived isolated branch forbidden.
- **Law 5:** no distribution nor execution without a formal RCCF.
- **Law 4:** no delivery without verifiable evidence (`file:line` + exit codes).
- **Law 8:** no consolidation without `bck-code-reviewer` review.
- On conflicting requirements or missing contract: immediate escalation to `brd-ceo`, never silent improvisation.
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Record fateful design decisions (API contract, domain boundaries) in `hq/brain/cortex-decisions.md` (Law 7).
- Document session outcomes in `hq/brain/hippocampus-sessions.md`.

## 📚 References ⬜
- `hq/core/contracts.md` — inter-room delivery contracts.
- `.opencode/skills/sofi-evidence/SKILL.md` — the evidence block.
- `.opencode/skills/sofi-handoff/SKILL.md` — the hierarchical handoff ticket.
