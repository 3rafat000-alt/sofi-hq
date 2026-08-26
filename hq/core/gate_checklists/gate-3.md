# Gate 3: Architecture Checklist

**Owner:** arc-lead (Luay Al-Hakim)
**Deliverable:** Architecture Package (frozen)

## Validation

- [ ] Component diagram complete (system-architect)
- [ ] Data schema finalized on paper — rollback plan per migration, **zero live databases** (data-architect)
- [ ] OpenAPI contract authored and frozen on paper (api-architect)
- [ ] Third-party integrations mapped — field-by-field from authoritative source (integration-architect)
- [ ] Infrastructure plan: network segmentation, scaling strategy, DR posture (infra-architect)
- [ ] STRIDE threat model complete (sec-threat-modeler)
- [ ] 4-pillar spec review passed (review-architect)
- [ ] Performance budget defined — TTI < 2s, bundle sizes, API response times
- [ ] Caching strategy documented — what, where, TTL, invalidation
- [ ] Error handling strategy — error codes, fallbacks, user messaging
- [ ] Security architecture reviewed — auth, encryption, secrets (sec-authn-engineer)

## Evidence Required

- [ ] Component diagram [verified: artifact]
- [ ] Traceability matrix (screen → endpoint)
- [ ] ER diagram with migration plan
- [ ] OpenAPI spec (openapi.yaml)
- [ ] STRIDE threat model document
- [ ] 4-pillar spec review report

## Verification

- [ ] Gatekeeper runs spec review in clean context (never self-grade)
- [ ] Every planned migration proven reversible with rollback script
- [ ] No secret in code — secrets-warden scans pass
- [ ] **Git audit: zero lines of code anywhere in the entire project** — traceability to interfaces is deferred to the Design-Freeze Review gate (DFR) in S3 (v2 · INT-GTW-024)

## Sign-off

- [ ] Architecture Package signed by arc-lead: "Gate 3 PASS — paper-only bundle; next = S3 design + DFR"
- [ ] arc-lead confirms CTO review (brd-cto)
