## FILE: .opencode/skills/qa-laravel-architect/SKILL.md
---
name: qa-laravel-architect
description: >-
  Laravel 11+ / DDD / Database / Security end-to-end QA architecture protocol — five mandatory phases, 22 acceptance points measured against approved documents (frozen OpenAPI, DFR design tokens, S4/S6 criteria), DB-fingered N+1/EXPLAIN/security evidence, and a unified advisory report. Triggers — "run the Laravel QA architecture review", "verify the Laravel backend against the contract", "5-phase Laravel check", "22 acceptance points Laravel", "review the Laravel architecture and security", "DDD layer conformance Laravel", "N+1 / EXPLAIN / indexes / cache review", "WCAG / security / Policy audit Laravel". Invoked by qa-lead (room 10) assigning a Laravel delivery to the Laravel QA Architect — never for general test strategy (qa-test-plan), React/Flutter (qa-react-architect / qa-flutter-architect), or gate verdicts (qa-lead / brd-cqo).
---

# qa-laravel-architect — The Laravel/DDD QA Architecture Protocol

> **Core value:** an end-to-end Laravel 11+ / DDD / Database / Security review protocol whose every acceptance point is measured against SOFI's approved documents — the report advises, the room lead decides. **No gate verdicts, no security classification (C3).**

## 🎯 When to invoke (When) ⬛
- A Laravel delivery (REST API, GraphQL, full web app, admin backend) arrives needing DDD + database + performance + security + testing verification in one coherent review.
- qa-lead needs DB-fingered N+1/EXPLAIN/index evidence + security audit (Policies/Gates/FormRequest/rate limiting) before assembling Gate-5 evidence.
- A frozen-contract + DDD-layer cross-check is required: does this backend conform to the approved OpenAPI + DDD context map + ERD + DFR design tokens?
**Do not invoke** for: general test strategy or Gate-5 decision (use `qa-test-plan`, decided by qa-lead) · React/Next.js (qa-react-architect owns that — C4) · Flutter/mobile (qa-flutter-architect owns that — C4) · Symfony/CodeIgniter/Yii/raw PHP (Stack Lock R3 — wrong stack, return to qa-lead) · security classification (sec-lead → brd-cso) · running any forbidden op (C6).

## 📥 Required inputs (Inputs) ⬛
- Formal RCCF work order from `qa-lead` (Law 5) — no execution without it.
- The delivery under review: project path, domain/bounded-context scope, backend target (API/web/queue).
- The approved references: frozen OpenAPI / schema-contract (S2) + ERD (S2) + DFR tokens (S3) + S4/S6 gate criteria — each with a locatable `file:line`.
- An approved local target (staging, local `php artisan serve`, or Telescope-enabled env) — else the report records a documented exit-0 skip (C7).

## 🔧 Steps (Steps) ⬛

### Phase 1 — Domain Discovery & Data Modeling
1. Verify the RCCF (Law 5) and locate every approved reference with `file:line` (C5). **Missing reference → stop: return to qa-lead with a gate-return note — never invent an in-report standard.**
2. Identify bounded contexts: read `app/Domain/` (DDD) or `app/Models/` (legacy) · identify Entities, Value Objects, Aggregates, Repositories.
3. Review migrations: `database/migrations/`. Check data types (bigInteger IDs · decimal for money · json for flexible) · indexes (WHERE/JOIN/ORDER BY) · foreign keys (onDelete cascade/restrict) · timestamps/softDeletes.
4. Build/verify the ERD (paper-only — never auto-generate against live production without sign-off).
5. Identify project size tier: thousands / millions / billions of records — to determine indexing + partitioning strategy.
6. Target pre-check (C7): detect artisan/DB target. Present → capture fingerprint (Laravel version · PHP version · DB driver+version · Redis version · Pest/PHPUnit version). Absent → record a documented skip (`exit 0`, `no-target`), report without runtime phases, never fake measurement.

### Phase 2 — DDD Architecture Review (paper + code, against documents)
7. Verify DDD layer separation: `app/Domain/{Entities,ValueObjects,Aggregates,Repositories,Events}` · `app/Application/{DTOs,Services,Actions}` · `app/Infrastructure/{Database,Repositories,Api,Queue}` · `app/Http/{Controllers,Requests,Resources}`. Any layer bleeding = P0 finding.
8. Repository pattern: `Domain/Repositories/<Name>RepositoryInterface` exists + `Infrastructure/Database/Repositories/Eloquent<Name>Repository` implementation + binding in a Service Provider.
9. DTOs: `Application/DTOs/` or `Spatie\LaravelData\Data` for all use-case inputs/outputs.
10. Models: `$fillable` or `$guarded` set · `$casts` for non-string types · `$hidden` for sensitive fields (passwords, tokens, PII) · relationships scoped.
11. Controllers: thin — no business logic · use FormRequest for validation · return Resources/Responses.
12. DI: Service Container used correctly · NO direct `app()` calls in business code.
13. Migrations: backward-compatible changes use `nullable()` with defaults.
14. Any design question surfacing during review → document as a **gate return** (S2/S3), never resolved inside the report (Design-First · C5).

### Phase 3 — Database & Performance Measurement (C6 + C7)
15. Detect N+1 queries: any `foreach` over a relation WITHOUT prior `with()` is a P0.
16. Count queries per request via Telescope/Debugbar/`DB::listen` — threshold: ≤ 10 queries per page/endpoint (with eager loading).
17. Heavy queries: `EXPLAIN` (or `EXPLAIN ANALYZE` on Postgres) on suspected slow queries; require `select()` (never `*`) on large tables.
18. Indexes: confirm all WHERE/JOIN/ORDER BY columns are indexed; flag compound-index opportunities.
19. Caching: `Cache::remember()` for rarely-changing data (countries, settings, product lists) with explicit TTL and tagged cache keys.
20. Queue monitoring: `failed_jobs` count, average processing time, queue depth (Horizon if present).
21. API response time targets: < 200ms for simple GETs, < 500ms for complex joins — measured with fingerprint.
22. Only the whitelisted commands run — any other need returns to qa-lead unexecuted (C6).

### Phase 4 — Security Audit & Testing Review (C6 + C7)
23. Authentication: `config/auth.php` guards correctly configured · Sanctum/Passport tokens rotated.
24. Authorization: EVERY sensitive action protected by `$this->authorize()` or Gates. Every model has a Policy. No inline `$user->id === $post->user_id` in controllers — must be in a Policy.
25. Input validation: EVERY incoming request uses a FormRequest with strict rules. No `Request::all()` direct usage.
26. XSS: Blade `{{ }}` used everywhere (NOT `{!! !!}`) — `e()` / `htmlspecialchars` equivalent. Strip HTML for user input if needed.
27. SQL injection: Eloquent/Query Builder used; if `DB::raw()` is used, it must be parameterized.
28. Sensitive data: `APP_KEY` strong · `.env` outside version control · passwords hashed with `Hash::make()` · no API keys in logs · `config:cache` in production.
29. Rate limiting: `throttle:api` on auth + sensitive routes.
30. Tests: Unit (Domain/Value Objects) + Feature (Endpoints with FakeAuth) + Database (RefreshDatabase/DatabaseTransactions) + CI/CD (GitHub Actions/GitLab CI). Coverage: happy path + unhappy path.
31. Documentation: OpenAPI/Swagger via l5-swagger or Scribe present for API deliveries.

### Phase 5 — Unified Advisory Report & Delivery
32. Score the **22 acceptance points** (table below) — each measured **against its approved document** (C5); each claim carries `file:line` + `exit code` + Laravel/PHP/DB fingerprint (C7).
33. **Advisory verdict only (C3):** per-point pass / fail-with-reason — no gate decisions, no security classification, no release sign-off.
34. Sanitize transient output (identifiers, dumps) before including any evidence — nothing leaves the working tree (C6).
35. Produce the evidence block (Law 4) and hand off to `qa-lead` (Law 3).

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: the **unified advisory report** (template below) + the 22-point score table + evidence block. Report = consultation for qa-lead's Gate-5 decision and brd-cqo.
- **Evidence (Law 4) — QA type:** use the `sofi-evidence` skill. Mandatory per claim: `file:line` · command + `exit code` · **Laravel/PHP/DB fingerprint per EXPLAIN/query/security phase (C7)** · sanitized logs/dumps. Target absence = documented skip with exit 0 (C7).

### Unified Advisory Report Template (compact — full example in `references/acceptance-and-report.md`)
```
### Laravel/DDD QA Architecture — Unified Advisory — <ticket-id> — <timestamp>
- Reviewed: <project/domain> · Scope: <bounded contexts / tables / endpoints> · Stack: <Laravel + PHP + DB + Redis versions>
- References: OpenAPI <file:line> · Schema-contract <file:line> · ERD <file:line> · DFR tokens <file:line> · S4/S6 criteria <file:line>
- Target: <artisan target or DB> · Laravel <ver> · PHP <ver> · DB <driver ver>   (per phase where applicable)
- Phases: 1 domain/ERD: <n findings> · 2 DDD: <n findings> · 3 DB/perf: <n findings> · 4 security/testing: <n findings>
- 22 acceptance points: <pass-count>/22 advisory pass — <fail-count> findings (see score table)
- Query metrics: ≤10 per request · N+1 count · missing indexes · EXPLAIN samples
- Security: Policies status · Throttling status · sensitive data status
- Gate returns: <list of deviations returned to S2/S3 — never resolved here>
- Advisory: <overall consultation for qa-lead — NOT a gate verdict>
- Evidence: <evidence block per sofi-evidence — file:line · exit codes · fingerprints · sanitized dumps>
- Escalations: <any security-classified observation → qa-lead → sec-lead → brd-cso>
```

### The 22 Acceptance Points (scored against approved documents — C5)
**Code Structure & DDD (6):**
| # | Point | Measured against |
|---|-------|------------------|
| 1 | DDD layer separation (Domain/Application/Infrastructure/Presentation) | ddd-capsule.md · projects/<slug>/brain |
| 2 | Contracts/Interfaces with constructor injection | ddd-capsule.md · Service Providers |
| 3 | Models: $fillable/$guarded + $casts + $hidden | Eloquent docs · projects/<slug>/brain |
| 4 | Controllers thin (FormRequest + Resources only) | ddd-capsule.md · Laravel docs |
| 5 | DI via Service Container (no app() in business code) | Laravel docs · projects/<slug>/brain |
| 6 | Backward-compatible migrations (nullable + defaults) | migrations · Laravel docs |

**Database & Performance (6):**
| # | Point | Measured against |
|---|-------|------------------|
| 7 | Query count ≤ 10 per request (with eager loading) | Telescope/Debugbar · DB::listen |
| 8 | Zero N+1 (with/load everywhere) | Telescope · code review |
| 9 | Indexes on all WHERE/JOIN/ORDER BY | migrations · EXPLAIN |
| 10 | Cache::remember for rarely-changing data | config/cache.php · code review |
| 11 | Heavy queries use select() (no *) | code review · EXPLAIN |
| 12 | p95 latency < 200ms simple / < 500ms complex | Telescope · Horizon |

**Security (6):**
| # | Point | Measured against |
|---|-------|------------------|
| 13 | Auth guards correct (Sanctum/Passport/JWT) | config/auth.php |
| 14 | $this->authorize() on every sensitive action | Policies · Gates |
| 15 | FormRequest on all input | app/Http/Requests |
| 16 | Eloquent/Query Builder (no unparameterized DB::raw) | code review |
| 17 | Sensitive fields in $hidden + not in logs | Models · logs |
| 18 | Rate limiting on auth/sensitive routes | Kernel · routes |

**Testing (4):**
| # | Point | Measured against |
|---|-------|------------------|
| 19 | Happy path covered | tests/ · Pest/PHPUnit |
| 20 | Unhappy path covered (validation, auth failure, invalid input) | tests/ · Pest/PHPUnit |
| 21 | Isolated test DB (sqlite in-memory or mysql_testing) | phpunit.xml · config/database.php |
| 22 | Tests run in CI/CD (GitHub Actions / GitLab CI) | .github/workflows · CI config |

## 🔗 Handoff ⬛
- Deliver the advisory report + evidence block to **`qa-lead` only** (Law 3) via the `sofi-handoff` skill; qa-lead consolidates into Gate-5 and delivers upward.
- No direct delivery to the user. No addressing another room (Law 2). Security observations escalate only through qa-lead → sec-lead → brd-cso.

## ⛔ Constraints ⬛
- **Advisory only (C3, verbatim intent):** outputs are consultation feeding qa-lead's Gate-5 decision (and brd-cqo); no gate openings/rejections, no verdicts, no security classification; no direct delivery; no other-room addressing (Laws 2-3); escalation through qa-lead (security → sec-lead → brd-cso).
- **Scope (C4, verbatim intent):** Laravel 11+ products only — REST API, GraphQL, full web app, admin backends under the non-retroactive R2 contract; no Symfony/CodeIgniter/Yii/raw PHP (Stack Lock R3 — wrong stack, return to qa-lead); no React/Next.js (qa-react-architect owns that); no Flutter/mobile (qa-flutter-architect owns that); distinct from bck-code-reviewer (per-PR review in Room 05).
- **Command whitelist (C6, verbatim):** allowed: `php artisan route:list` · `db:show` · `migrate:status` · `composer show` (read-only) · `php artisan test --coverage` · `EXPLAIN SELECT` (read-only) · Telescope status. Forbidden: any `composer require/update` · `migrate` against prod · `key:generate` · env writes · `tinker` with mutations · DB writes/drops · key access · paid APIs (INT-0003). Outputs sensitive/transient: sanitized before documentation.
- **Fingerprint (C7, verbatim):** every DB/security report carries the Laravel/PHP/DB fingerprint per EXPLAIN/query/security phase + pre-check: no target → documented skip with exit-0 (Law 4 executable on any environment).
- **License gate (Law 15):** any dependency suggestion cites `package + version + license evidence (file:line)`. Allowed: MIT · Apache-2.0 · BSD-2/3 · ISC · MPL-2.0. Vetoed: GPL/AGPL/SSPL and unknown.
- **Latest-Version-Mandatory:** before any code touching a library → Context7 MCP first; for any external repo claim → DeepWiki MCP.
- Never override any of the sixteen laws; a skill "saving time" by skipping the lead is rejected.

## 🧠 Memory ⬜
- Important decisions and findings patterns → recorded per Law 7 through the room (CORTEX for org-level records; `projects/<slug>/brain/` for project-level).

## 📚 References 📚
- `references/acceptance-and-report.md` — expanded 22-point acceptance matrix (measurement recipe per point) + full worked example of the unified report + the C6 whitelist/forbidden table.
- `hq/core/nexus/gates.yaml` (Gate-5 · DFR) · `hq/core/standards/api-envelope.md` · `hq/core/standards/ddd-capsule.md` · `hq/core/standards/pipeline-production-line.md` · `hq/core/system-state-current.md` · `hq/brain/cortex-decisions.md` (ADR-20260905-GTW-LARAVEL-DDD-ARCHITECT).
