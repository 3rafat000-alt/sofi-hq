# Gate 6: Staging Checklist

**Owner:** ops-lead (Kamil Al-Samman)
**Deliverable:** Staged Release

## Environment

- [ ] staging ≈ prod parity — same architecture, same config shape
- [ ] Staging database seeded — realistic test data
- [ ] All env vars set — verified against prod template
- [ ] Secrets loaded — vault, not .env

## Deployment

- [ ] Migration ran against staging — no errors
- [ ] Rollback tested — proven return path
- [ ] Smoke tests green — health endpoint, login, core flow
- [ ] Zero-downtime deploy configured (blue/green or rolling)

## Observability

- [ ] Monitoring configured — Prometheus/Grafana dashboards
- [ ] Logging configured — structured, searchable
- [ ] Alert rules created — dry-tested
- [ ] Sentry/Datadog connected — error tracking active

## Documentation (Axis 9 fix 2026-08-31 — knw-doc-writer link hygiene · Law 4/13)

- [ ] Runbook updated — deploy steps, rollback steps, common issues
- [ ] Release notes drafted
- [ ] On-call engineer identified
- [ ] **Internal documentation index freshness (knw-doc-writer):**
  - [ ] `python3 hq/core/tooling/law13_path_guard.py` passes — every internal path has a real home (Law 13) — evidence: exit code + scanned count attached
  - [ ] `python3 hq/core/tooling/evidence_guard.py hq/ --strict` passes — zero broken `file:line` citations in hq/ docs (Law 4) — evidence: scanned/broken counts attached
  - [ ] `.opencode/skills/INDEX.md` + `hq/core/domain/SKILLS-ASSIGNMENT.md` updated if any skill added/removed (count_sync PASS 109/109)
  - Failure = Gate-6 blocked until index/links fixed (mirrors Gate-0 registry guard but for docs)

## Evidence Required

- [ ] staging-report.md [verified: artifact]
- [ ] uat-log.md [verified: artifact]

## Verification

- [ ] ops-cicd-engineer: pipeline produces green staging deploy
- [ ] ops-cloud-engineer: env matches prod
- [ ] ops-release-manager: rollback rehearsal successful

## Sign-off

- [ ] ops-lead signs: "Gate 6 PASS — proceed to Production"
