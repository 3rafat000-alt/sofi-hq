# Gate 0: Inception Checklist

**Owner:** str-lead (Nazih Al-Muhaini)
**Deliverable:** Project Blueprint (signed artifact)

## Validation

- [ ] Problem statement written — what, why, who?
- [ ] Target user identified — persona, context, scale
- [ ] Jobs To Be Done clear — functional, emotional, social
- [ ] Scope bounded — explicit In/Out lists
- [ ] Success metrics defined — measurable, time-bound
- [ ] Risk register started — top 5 risks + mitigations
- [ ] Fast-Track vs Deep-Audit classification proposed (criteria: `hq/core/nexus/gates.yaml#tracks`; authorization exclusively brd-ceo — PROTOCOLS P-01.8)
- [ ] TAM/SAM/SOM estimated (by market-analyst)
- [ ] Key stakeholders identified
- [ ] Out-of-bounds documented (what this project is NOT)

## Evidence Required

- [ ] Problem statement with source tags [verified: research]
- [ ] Scope boundary signed by product-strategist
- [ ] Risk register with severity ratings (1-5)

## Verification

- [ ] Gatekeeper verifies: every claim grounded, scope bounded
- [ ] Does any requirement trace to a Journey Map? (if no, ensure one is created in Gate 1)
- [ ] Is Fast-Track/Deep-Audit classification justified?
- [ ] **Registry invariant guard (Law 12) — mandatory Gate-0 machine check:**
  - [ ] `python3 hq/core/tooling/registry_guard.py --strict` passes: `.opencode/agent` 1:1 vs `hq/core/nexus/registry.yaml` (15 rooms · 114 agents) + `hq/core/domain/rooms/*/agents/*` capsules exist
  - [ ] `python3 hq/core/tooling/count_sync.py` passes: 114 agents · 109 skills · 16 laws · 15 rooms (exit 0)
  - [ ] `python3 hq/core/tooling/evidence_guard.py --staged --strict` passes: zero broken `file:line` citations (Law 4)
  - Evidence: gate-0 run log with exit codes attached to RCCF (P-03.1)
  - Failure = Gate-0 blocked (L2) — fix registry/agent/capsule drift first, then `node hq/core/tooling/port-agents.mjs` to re-sync `.kilo/agent`

## Sign-off

- [ ] Project Blueprint pinned into `projects/<PRJ>/brain/CONTEXT.md` 
- [ ] str-lead signs: "Gate 0 PASS — proceed to Discovery"
