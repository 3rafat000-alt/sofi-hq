# The Capsule Protocol — The Binding Rules for Building and Modifying Everything
### Backend · Frontend · Mobile — in the unified DDD Capsule format · foundational release 2026-08-24 · INT-GTW-031

> **Authority:** this document is the **operational contract** governing how the team actually works when building a project, or modifying a feature, interface, or backend.
> Detailed technical standard: `hq/core/standards/ddd-capsule.md` · lifecycle: `hq/training/ddd-full-cycle-playbook.md`
> **The sole exception:** an ADR signed by brd-ceo — no individual improvisation.

---

## Article 0 — The Capsule Is Mandatory for Everything

1. **All code** — Laravel backend or Flutter/Dart interface (web+mobile per R2) — lives inside one four-layer capsule:
   `Domain → Application → Infrastructure → Presentation`
2. **The decisive purity test:** the Domain layer is moved into an empty project with no framework → does it run? sound capsule. It doesn't? structural breach, rejected at review.
3. **Capsule boundaries are non-negotiable:** Domain imports no framework · Presentation never touches Persistence · every crossing between layers goes through an injected Contract interface.
4. **A new feature = a new capsule inside the feature:** `features/<feature>/{domain,application,infrastructure,presentation}` — no loose folders like utils/helpers to park business logic in.

---

## Section 1 — The Pre-Start Consultation Protocol (mandatory — no code without documented consultation)

**Rule:** the lead starts no feature above trivial before a round of consultation with their room's agents, documented with written trace in `brain/CONTEXT.md`.

### 1.1 The Consultation Template (sent by the lead via Task to each relevant agent)

```markdown
## CONSULT-<seq> — consultation: <feature title>
Context: <two lines from the PRD + link CONTEXT.md#section>
Your three questions (answer within 10 lines max):
1. What are the technical risks in your domain for this proposed solution?
2. What is the simplest alternative meeting the same acceptance criterion?
3. What is your time estimate and the first obstacle you expect?
Wanted: specialist opinion, not social approval — dissent is welcomed and protected.
```

### 1.2 Who Is Consulted on What (the consultation map)

| Type of Work | Mandatory Consultants | Decision Owner |
|---|---|---|
| Backend feature (Endpoint/Domain) | bck-domain-engineer (modeling) · bck-api-engineer (contract) · dat-db-engineer (if touching schema) | bck-lead |
| Screen/interface component | dsn-ui-designer (tokens) · fnt-interaction-engineer (states & behavior) | fnt-lead / mob-lead |
| Feature touching money/sensitive data | + sec-threat-modeler · dat-privacy-officer | lead + escalation |
| API contract changes | + arc-review-architect | arc-lead |

### 1.3 Settling the Outcome

- **Easy consensus:** no objections → the lead approves and logs the consultation summary (3 lines) in CONTEXT.md under `## Consultations`.
- **Substantive disagreement:** the lead presents both options with consequences to brd-ceo in the RCCF — **imposing an opinion silently is forbidden**.
- **After settlement:** the contract freezes (openapi/schema-contract) and the consultation closes — later changes reopen a mini-consultation.

---

## Section 2 — The Backend Capsule (Laravel)

### The Binding Tree

```text
app/
├── Domain/<Context>/                 # pure core — zero framework (the portability test)
│   ├── Model/                        # Aggregate Roots + Entities + ValueObjects/
│   ├── Event/                        # OrderPlaced ...
│   ├── Contract/                     # OrderRepository (interface only)
│   ├── Service/                      # pure domain service if needed (calculations)
│   └── Exception/
├── Application/<Context>/UseCase/    # XHandler: coordinator — zero business rules
├── Infrastructure/<Context>/
│   ├── Persistence/                  # EloquentXRepository + Eloquent Models
│   └── Integration/                  # external service clients (payment gateway...)
└── Http/Controllers/<Context>/       # thin controllers: validate→handler→respond
```

### The Hard Rules (Ten + One · amended 2026-08-26)

| # | Rule | Checker |
|---|---|---|
| 1 | Domain has no framework import (Eloquent/Http) | CI grep |
| 2 | A single Aggregate Root per consistency block; neighbors referenced by ID | lead review |
| 3 | VOs for every rule-bearing concept (Money·Email·Quantity) | review |
| 4 | Handler receives a Command/DTO, not a Request directly | code review |
| 5 | Repository interface in Domain, implemented in Infrastructure | architecture |
| 6 | Controllers ≤ 15 lines: validate→usecase→envelope | lint/review |
| 7 | Every response Envelope v1 through a single trait | contract tests |
| 8 | Events for any state change another context cares about | review |
| 9 | Migrations reversible (documented down) | Gate-4a |
| 10 | Feature test for every UseCase handler | coverage ≥90% |
| 11 | **Code passes `ops-sandbox-executor` build/syntax gate inside an isolated container before moving to review or QA** *(owner order 2026-08-26)* | sandbox-verdict.json PASS |

---

## Section 3 — The Interface Capsule (unified Flutter/Dart: Web + Mobile)

### The binding tree for every feature

```text
lib/features/<feature>/
├── domain/            # entities + value_objects + failures + XRepository (abstract)
├── application/       # providers/notifiers: state machine for the eight states
├── infrastructure/    # dto + dio datasource (Envelope v1) + repository implementation
└── presentation/      # screens/ widgets/ — design from design-tokens exclusively
lib/core/              # api_client · router · theme · l10n — shared, never duplicated
```

### Hard interface rules

1. **The eight states** for every data screen: Default/Hover/Focus/Selected/Loading/Success/Empty/Error — missing one = delivery rejection.
2. DataSource calls the frozen contract exclusively — **zero mocks crossing boundaries** (internal units exempt).
3. Presentation imports neither dio nor dto — it receives models from application only.
4. Colors, fonts, and spacing come from Theme/tokens — **zero hard-coded hex** (checked automatically).
5. One widget = one function ≤ 150 lines; a third repetition ⇒ extract shared.

---

## Section 4 — The Professional TODO Task Protocol

### 4.1 Mandatory tree (Law 13)

```text
Phase-01 → <batch name>
├── 01-01 <task>        [owner-agent] [est: 0.5d] [deps: -]
└── 01-02 <task>        [owner-agent] [est: 1d]  [deps: 01-01]
Phase-02 → ...
```

### 4.2 The Standard Task Card (attached to the RCCF tree)

```markdown
### T-<phase>-<nn>: <verb + goal>          [owner: <agent>] [est: Xd] [P0/P1/P2]
- Depends: T-…  · Blocks: T-…
- Deliverable: <specific files by path>
- Done-when: <inspectable condition — test/command/screen>
- Evidence: commit sha + file:line + exit codes
- License-check: [allowed / rejected]      ← mandatory when the task changes dependencies (Law 15)
- Sandbox: [PASS verdict ref]              ← mandatory before review/QA handoff (Hard Rule #11)
```

### 4.3 Flow Rules

1. A task with no single owner and no inspectable Done-when = **not accepted** into the plan.
2. Priority: what others depend on first (contract→core→interface→integration).
3. In-progress ≤ two tasks per agent — parallel sprawl kills quality.
4. Any estimate overrun >50% → immediate escalation to the lead (no silence until deadline).
5. Closure: evidence in HANDOFFS + moving the card to Done — there is no "almost finished".
6. **Debt-capacity reserve (owner decision 2026-08-26):** every Phase tree reserves **≥15% of its estimated capacity** for tech-debt/refactoring tasks (`bck-refactoring-surgeon`-type). `str-roadmap-planner` allocates it at planning time; `str-agile-orchestrator` verifies it on every board sweep — a plan without the reserve returns to re-planning, and burning the reserve on features requires brd-ceo approval.

---

## Section 5 — Practical Communication Protocol During Execution

| Situation | Channel and Format |
|---|---|
| Starting a task | a line in the agent session: `START T-02-01 — per CONSULT-3 and the frozen contract` |
| Technical blocker | immediate escalation to the lead in the form: blocker ← what I tried ← I need a decision between (a/b) |
| Request from another room | direct contact forbidden (Law 2): via your lead → brd-ceo |
| Technical disagreement with a reviewer | present both options with consequences to the lead — neither grinding nor silent compliance |
| Finishing a task | sofi-handoff ticket + update card T to Done with evidence |

**Room rhythm:** session opening = reading Today cards · closing = updating status and blockers — logged automatically into hippocampus-sessions.

---

## Section 6 — Capsule Acceptance Checklist (review signs off against it before any delivery)

**Backend:** [ ] Domain portability test ✓ [ ] zero framework imports ✓ [ ] Handlers logic-free ✓ [ ] Envelope ×all routes ✓ [ ] Events for significant transitions ✓ [ ] tests ≥90% ✓ [ ] migrations down ✓ [ ] sandbox gate PASS (`ops-sandbox-executor`) ✓ [ ] License-check recorded for any dependency change ✓
**Interface:** [ ] the eight states ✓ [ ] zero hex outside tokens ✓ [ ] presentation clean of infra ✓ [ ] single Envelope mapper ✓ [ ] RTL + both modes ✓ [ ] basic a11y (focus/semantics) ✓

*Failing any item = returned to the agent with the item named — no generic rework.*

---
*Governance: AGENTS.md (16 laws) · pipeline.yaml v2 · standards/ddd-capsule.md · this protocol operationalizes them all.*
