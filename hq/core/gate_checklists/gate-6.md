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

## Documentation

- [ ] Runbook updated — deploy steps, rollback steps, common issues
- [ ] Release notes drafted
- [ ] On-call engineer identified

## Evidence Required

- [ ] staging-report.md [verified: artifact]
- [ ] uat-log.md [verified: artifact]

## Verification

- [ ] ops-cicd-engineer: pipeline produces green staging deploy
- [ ] ops-cloud-engineer: env matches prod
- [ ] ops-release-manager: rollback rehearsal successful

## Sign-off

- [ ] ops-lead signs: "Gate 6 PASS — proceed to Production"
