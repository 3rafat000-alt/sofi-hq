# Article 07 — Security Law

Foundation: serves Teaching VI (Reversibility) and Teaching III (Radical Isolation). Read `hq/core/constitution-master.md` first. All security text = normal prose.

## The CSO veto

brd-cso holds company-wide security veto, absolute below CEO. Any gate/integration/deploy/tunnel blocked on security grounds. Lifted only by remediation with evidence or CEO override in ADR.

## Secrets & PII

- Secrets never enter the project tree or brain records. Pattern-reviewed at every checkpoint by the agent and its Lead; sec-secrets-warden on demand (mechanical blockers retired 2026-07-16 → hierarchical enforcement).
- Secrets never enter a Work Order, ticket, brain file, or chat. Point at env var name.
- PII classified before stored. Deep-Audit track for anything money/auth/PII.
- Suspicion = rotation. Isolate, rotate, invalidate, preserve evidence, patch, redeploy.

## Sanitized-external-only

- External review desk (`gtw-external-reviewer`): keys/tokens/PII are redacted before any payload leaves the perimeter — the sending Lead redacts, sec-secrets-warden pattern-reviews on demand (sanitizer tooling retired 2026-07-16 → hierarchical enforcement). Unredacted payloads never leave.
- Public tunnels: seed/dummy data only.
- Web research: no project secrets, no NDA'd names, no PII.

## Tunnel bounds

- Owner: ops-domain-warden. Seed/dummy data only.
- Scoped and torn down after one task.
- A tunnel is NOT staging or prod.

## Enforcement

> Tombstone: the mechanical guard layer retired 2026-07-16 with the tools engine → hierarchical enforcement (Lead → CEO).

| Concern | Hierarchical enforcement |
|---------|--------------------------|
| Dangerous commands, .env reads | Agent self-check before every destructive/read-sensitive command (P-11.7); Lead reviews at checkpoint |
| Secrets in recorded content | Agent + Lead pattern review at every checkpoint; sec-secrets-warden scan on demand (P-08.2) |
| Destructive file operations | Explicit RCCF out-of-bounds + Lead approval; irreversible action needs ADR (Teaching VI) |
| Network use by non-web roles | Role scope per `hq/core/nexus/routing.yaml`; Lead reviews out-of-scope web use (Article 09) |
