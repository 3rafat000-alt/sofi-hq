# Gate 4: Build Checklist

**Owners:** bck-lead (Aws Al-Ghazzi) · fnt-lead (Adnan Al-Daqqaq) · mob-lead (Khattab Al-Bunni)
**Deliverable:** Working Software
> **v2 Split (INT-GTW-024):** Gate-4a = S4 live backend only (closes before any interface) · Gate-4b = S5 unified interfaces. The "Legacy Web" section below applies to existing projects exclusively — new work is Flutter/Dart through Gate-4b.

## Backend — Gate-4a / S4 (bck-lead)

- [ ] All endpoints match the **frozen openapi-spec from S2** — 422-JSON rule enforced
- [ ] Live databases activated strictly per approved schema-contract — migrations reversible, rollback tested
- [ ] Domain services complete — business logic, money math (buy ≥ sell, precision)
- [ ] Queue jobs idempotent — retry/backoff/DLQ configured
- [ ] Integration connections live — webhook handlers per documented shape
- [ ] Coverage ≥ 90% (unit + integration)
- [ ] **Backend running end-to-end + security-scanned clean — precondition for opening S5**

## Legacy Web (fnt-lead) — existing projects only

- [ ] Blade/Vue views cover all states — empty, loading, error, success, edge
- [ ] Responsive — 320px to 1200+px, no horizontal scroll
- [ ] WCAG 2.2 AA enforced — keyboard nav, ARIA, contrast
- [ ] Micro-interactions complete — with reduced-motion alternative
- [ ] Bundle budgets met — code-split, lazy load
- [ ] Core Web Vitals pass — TTI < 2s

## Unified Interfaces — Gate-4b / S5 (fnt-lead + mob-lead · merged team)

- [ ] Flutter/Dart unified for web and mobile, sourced exclusively from the approved design system
- [ ] Consumes the frozen openapi-spec exclusively — live direct wiring backed by evidence
- [ ] Flutter clean architecture — feature-first with GetIt DI
- [ ] All states covered via Bloc/Cubit
- [ ] Platform channels typed — ApiException pattern
- [ ] Perf profile: no leaks, shrink-wrap verified
- [ ] Zero transient mocks crossing service boundaries

## Cross-Cutting

- [ ] No secrets in code — sec-secrets-warden scan pass (mechanical hook retired 2026-07-16)
- [ ] Code review passed (code-reviewer) — clean context V2
- [ ] All team leads sign: "Build complete"

## Evidence Required

- [ ] code on main tree [verified: artifact]
- [ ] test-report.md [verified: artifact]

## Verification

- [ ] CI pipeline: lint → test → build → scan all green
- [ ] Gatekeeper: endpoint count matches spec, no scope creep
- [ ] TTI measurement: Lighthouse / k6

## Sign-off

- [ ] bck-lead signs Gate-4a close (S4); then fnt-lead + mob-lead co-sign Gate-4b close: "Gate 4 PASS — proceed to Quality"
