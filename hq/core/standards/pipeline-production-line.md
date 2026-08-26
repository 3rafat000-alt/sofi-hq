# SOFI — The Six-Stage Contracted Production Line Constitution (pipeline-production-line.md)

> **Authority:** this constitution is the binding organizational translation of `hq/core/nexus/pipeline.yaml`.
> On detailed conflict, the machine source (`pipeline.yaml`) is the literal reference and this file is the reference for interpretation and application.
> Read in harmony with `AGENTS.md` (the 11 laws) and `constitution-master.md`; it overrides neither.

---

## | 1) Purpose & Authority

- **Purpose:** unify the path of any executive work across **six contracted stages**; a stage may not begin before the previous gate is crossed with inspectable evidence (Law 4).
- **The governing v2 principle — Upfront Comprehensive Design:** writing **any line of code** before the design documents (data, contracts, interfaces) are fully approved through the Design Freeze Review (DFR) gate is forbidden, and any interface code before the backend is complete, running, and security-checked is forbidden. The project is written and understood 100% on paper first, then executed literally against what was approved.
- **Authority:** issued under **OWNER-DIRECTIVE-2026-0823-R2** (the owner's direct amendment of program v1), executed under ticket **SOFI-HQ-INT-0002**.
- **Scope of application:** every project under `projects/*` and all internal HQ work, on all three tracks alike (Law 1), unless a brd-ceo exception is documented in organization memory (Law 7).
- **Non-retroactivity:** projects existing at R2 issuance finish on their current stack and contracts; v2 applies to new projects and new stages except by explicit owner order.

---

## | 2) The Six-Stage Map (official room codes from `registry.yaml`)

```
S1 Idea, Strategy & Research            S2 Data & Contract Design (paper)
   (00·01·14·02)              ──▶        (04·08 + 05 engineering for design)
                                                     │
                                                     ▼
S6 Shield & Production ◀── S5 Both Interfaces in Parallel + Live Wiring ◀── S3 Experience & Visual System + DFR
   (09–13)                (06·07 merged Flutter/Dart team)     (03 + 09·10 review)
                                                     │
                                                     ▼
                                        S4 Live Backend Execution (08·05)
```

| Stage | Name | Rooms | Owning Lead |
|---------|-------|-------|----------------|
| S1 | Idea, Strategy & Research | 00 · 01 · 14 · 02 | str-lead |
| S2 | Data & Contract Design (paper only) | 04 · 08 · 05(design) | arc-lead (+dat-lead, bck-lead) |
| S3 | Experience & Visual System + Design Freeze Review (DFR) | 03 (+09 · 10 review) | dsn-lead |
| S4 | Live Backend Execution | 08 · 05 | bck-lead |
| S5 | Both Interfaces in Parallel + Live Wiring | 06 · 07 (merged Flutter/Dart team) | fnt-lead + mob-lead |
| S6 | Shield & Production | 09 security · 10 quality · 11 operations · 12 observability · 13 knowledge | qa-lead |

> **Gate-to-stage linkage (INT-GTW-024):** stages S1–S6 and gates Gate-0–8 are one vision from two angles — official machine map: `hq/core/nexus/gates.yaml#stage_map` (S1→G0,G1 · S2→Gate-3 on paper · S3→Gate-2+DFR signature · S4→Gate-4a · S5→Gate-4b · S6→Gate-5–8). The **DFR** design-freeze gate's machine block: `gates.yaml#dfr`.

**Fixed rules in the map:**

- **S1 issues the PRD:** S1's mandatory output is a Product Requirements Document (PRD) anchored in `projects/<name>/brain/CONTEXT.md` — no later stage without an anchored context.
- **S2 is paper only:** Data Design (ERD + schema-contract) and API Design (frozen OpenAPI + documented business logic) on paper exclusively — **building live databases or writing code is forbidden**. No move to interface design before both data and contract documents are approved.
- **The Design Freeze Review (DFR) is now the heart of the line:** security room (09) and quality room (10) review **every** design (data + API + interfaces), and their signatures are the crossing condition. Zero lines of code anywhere in the project before DFR signature.
- **S4 executes the design, it does not improvise it:** activating live databases from the approved Data Design and writing code 100% against the frozen contract — S4 closes only once the backend runs end-to-end and passes its security scan.
- **S5 is constrained parallelism strictly after backend completion:** rooms 06 and 07 operate as **one merged interface team** on the unified **Flutter/Dart** stack (web and mobile from the same design system and official skills), wired live to a completed, running backend — no verbal assumptions and no direct bridge between them (Law 2).
- **S6 is a shield with no optional step:** no delivery to the user before the shield signs in full: security + quality + operations + observability + knowledge.

---

## | 3) Stage Contracts Table

| Stage | Owning Lead | Input artifact | Output artifact |
|---------|---------------|------------------|------------------|
| S1 | str-lead | raw user request | intake-report + RCCF approved by brd-ceo + PRD anchored in CONTEXT.md |
| S2 | arc-lead (+dat/bck) | RCCF + PRD | adr + ERD + schema-contract + business-logic-doc + frozen openapi-spec |
| S3 | dsn-lead (+DFR: sec/qa) | openapi-spec + schema-contract | ux-flows + design-tokens + hi-fi-mockups (web+mobile) + dfr-signoff |
| S4 | bck-lead | every approved S2+S3 output | live-schema (applied migrations) + api-code + backend-security-scan |
| S5 | fnt-lead + mob-lead | api-code + design-tokens + hi-fi-mockups | web-app + mobile-app + live-integration-evidence |
| S6 | qa-lead | web-app + mobile-app + integration-evidence | security-signoff + qa-verdict + deploy-runbook + telemetry + knowledge-log |

**Gate-crossing criteria (inspectable — attached as Law 4 evidence):**

- **S1 gate:** (1) an intake-report issued by gtw-intake-reformer including the fast|standard|fateful track classification. (2) An RCCF work order exists and is approved by brd-ceo before any execution (Law 5). (3) A PRD covering the full MVP scope backed by market/competitor research dossier, anchored in `projects/<name>/brain/CONTEXT.md`.
- **S2 gate:** (1) an ADR documented for every architectural decision. (2) ERD + schema-contract signed by arc-lead and dat-lead — **with no live database or applied migration whatsoever**. (3) openapi-spec approved, frozen, and matching the `api_envelope_v1` envelope. (4) Business logic documented in full on paper. (5) Zero lines of code — verified via git log. (6) Interface design does not start before this signature.
- **Design Freeze Review (DFR) gate (heart of S3):** (1) ux-flows mirroring data and contract logic precisely without improvisation. (2) A central unified design-system actually exported (colors/fonts/shared components). (3) hi-fi mockups for web and mobile together under one digital identity. (4) Review signatures from sec-lead and qa-lead on the complete designs (data + API + interfaces). (5) Zero lines of code before signature.
- **S4 gate:** (1) Live databases activated literally per the approved schema-contract — migrations reversible with an existing rollback plan. (2) api-code implements the frozen openapi-spec at 100% — green contract tests against the spec. (3) Backend running end-to-end and security-scanned clean. (4) **Decisive condition:** rooms 06/07 have not written a single line of interface code before crossing this gate.
- **S5 gate:** (1) Web and mobile apps built as one unified Flutter/Dart stack on the approved design system exclusively. (2) Both consume the openapi-spec contract exclusively. (3) Evidence of direct live wiring to the completed backend. (4) Zero mocks crossing service boundaries between the two interfaces and 05 (Law 2 below).
- **S6 gate:** (1) security-signoff from sec-lead with zero unresolved critical findings. (2) qa-verdict = pass with the full regression suite green — zero known defects. (3) deploy-runbook includes a rollback plan and post-deployment health checks on servers and stores. (4) Live telemetry dashboards and a knowledge-log updated by knw-lead in CORTEX (Law 7).

**Artifact glossary (one definition binding all rooms):**

| Artifact | Definition | Format Owner |
|--------------|---------|-------------|
| intake-report | initial understanding/classification report for the request with the proposed track | gtw-intake-reformer |
| RCCF | the formal work order: intent, scope, criteria, gate, expected evidence | brd-ceo |
| PRD | product requirements document: MVP scope, functional and non-functional requirements, success measure | str-lead |
| adr | architectural decision record: context, options, decision, consequences | arc-lead |
| ERD | visual structural diagram of the database: tables, relations, distribution | dat-lead |
| schema-contract | the data structure contract approved before any live migration | dat-lead |
| business-logic-doc | full documentation of business logic on paper before any code | bck-lead |
| openapi-spec | the frozen OpenAPI specification — the sole contract between layers | bck-lead |
| ux-flows | user flows reflecting the approved contract and data logic | dsn-lead |
| design-tokens | machine-consumable tokens of the unified central design system | dsn-lead |
| hi-fi-mockups | final high-fidelity interfaces for web and mobile under one identity | dsn-lead |
| dfr-signoff | security and quality review signature on all designs before any code | sec-lead + qa-lead |
| backend-security-scan | clean security scan report on a running backend before opening S5 | sec-lead |
| live-integration-evidence | evidence of live wiring between both interfaces and the completed backend | fnt-lead + mob-lead |
| qa-verdict | documented quality verdict with evidence: pass/fail + coverage scope | qa-lead |
| deploy-runbook | release booklet: steps, health checks, rollback plan | ops-lead |

---

## | 4) The Three Tracks (preserved as-is — Law 1)

| Track | Eligibility | Approval | Constraint |
|--------|---------|----------|-------|
| 🟢 Fast | trivial **reversible** tasks (read/check/single-file fix/docs research) | self-approved by the single room lead | absolutely forbidden: money, security, production, schema — promoted immediately |
| 🟡 Standard | a feature or medium change spanning one to two rooms | brd-ceo approves the RCCF and closes gates S1→S6 fully | no skipping gates or leads |
| 🔴 Fateful | money/security/architecture/production/schema/irreversible | brd-ceo + advisory board (Law 6) with **absolute security veto by brd-cso** | full flow, no shortcuts |

- The Fast track shortens the **number of stages** (one room lead executes a mini-cycle) but never removes: evidence (Law 4), memory logging (Law 7), or sovereign intake.
- Doubt in classification always escalates upward: ambiguity = the higher track.

---

## | 5) The Six Production Line Laws

1. **`design_before_code`** *(new in v2)* — writing any line of code in any layer before full approval of the design documents (ERD + schema-contract + openapi-spec + business-logic-doc + design-system + mockups) and the DFR signatures from security and quality is forbidden. Any code appearing before DFR = mandatory deletion and reopening S2.
2. **`backend_complete_before_ui`** *(new in v2)* — interface rooms (06·07) are forbidden from writing any visual code before the backend is fully complete, running end-to-end, and passing its security scan (crossing gate S4).
3. **`openapi_first`** — no API code is written before an approved, frozen OpenAPI spec exists. The spec is designed in S2 (on paper) and implemented literally in S4; amending it after freezing officially reopens S2 through DFR.
4. **`mocks_cross_boundary_forbidden`** — any mock crossing service boundaries between the interfaces (06·07) and the backend (05) is forbidden: cross-boundary testing happens against a real contract or a server matching the frozen spec. **Explicit exception:** internal test doubles within the same layer (unit tests for components of the same room) are exempt and unaffected by the ban.
5. **`api_envelope_v1`** — all API responses are bound by the `api-envelope.md` wrapper mandatorily, not optionally; any response outside the envelope = S6 gate failure even if functionally working.
6. **`isolated_json_handoff`** — inter-room handoff happens via self-contained isolated JSON only, with no verbal context or implicit links. This rule **is added to the Law 4 evidence as a complement, not a replacement**: file:line, exit code, and logs evidence remain mandatory on every delivery.

Violating any of the six laws = rejection at the relevant gate and rework returned to the owning stage (L2); repetition escalates per the violation-level table in `AGENTS.md`.

---

## | 6) Knowledge Injection Map (`hq/core/standards/knowledge-cx-uiux.md`)

| Knowledge Branch | Mandatory Consumer | Companion Skill / Injection Point |
|--------------|--------------------|-------------------------------|
| 3.1 Strategy · 3.4 Metrics | room 01 (S1) | str-gate0-classify — framing and a measurable success scale |
| 2.1 Research · 3.5 VoC · 3.4 Metrics | room 02 (S1) | res-journey-map — research dossier closing the S1 entry and PRD |
| 2.2 Information Architecture · 2.3 Flows · 2.6 Psychological Laws | room 03 (S3) + room 05 (S2 contract-error design) | injected when building flows and error states on paper |
| 1.1–1.5 atoms→interaction · 1.6 Eight States · 1.7 Accessibility | room 03 (S3) | dsn-design-handoff — tokens and screens before crossing DFR |
| 1.1–1.7 complete (web UI) · 2.3 Flows | room 06 Flutter Web (S5) | fnt-component-build then fnt-ux-lint before review |
| 1.1–1.7 complete (mobile UI) · 2.3 Flows | room 07 Flutter (S5) | mob-feature-build + flutter-ui-ux + mob-flutter-kb |
| 2.5 Testing · pre-handoff interface checklist | quality room 10 (DFR + S6) | qa-test-plan — DFR examines designs and S6 examines the eight states and a11y |
| 3.3 Service · 3.2 Omnichannel · 3.6 Culture/EX | knowledge room 13 (S6) | knw-brain-write — documenting institutional lessons |
| Error messages and response tone (branch 2.3) | room 05 (S4 envelope text execution) | injecting api_envelope_v1 error copy in the user's language |

- Injection is mandatory, not advisory: no room crosses its gate without proving consumption of its assigned knowledge branches above.
- Room 13 is custodian of the complete reference; any change to `knowledge-cx-uiux.md` routes through it to brd-ceo.

---

## | 7) Immediate Escalation Rule on Higher Risk

- Detecting higher risk at **any stage** (money/security/production/schema/irreversible) = immediate track promotion: fast → standard → fateful.
- **Never downgrade**, however small the remaining work or however much is done — the new classification re-enters through intake and resumes from the latest uncrossed gate.
- Executing a fateful task on a lower track (even by mistake) = immediate freeze + escalation to brd-ceo (L3).
- The broken-loop countermeasure applies within every stage: 3 consecutive failures of one category = dump logs + escalate, with no fourth attempt.

---

## | 8) References

| Reference | Path | Role |
|--------|--------|-------|
| Machine source of the line | `hq/core/nexus/pipeline.yaml` | the literal truth of stages, gates, and tracks |
| API envelope | `hq/core/standards/api-envelope.md` | definition of the binding `api_envelope_v1` |
| DDD standards | `hq/core/standards/ddd-capsule.md` | governing the backend core in S4 |
| Stack standards | `hq/core/standards/stacks-tech.md` | the unified Flutter/Dart interface stack (S5) |
| Official room registry | `hq/core/nexus/registry.yaml` | source of room codes 00–14 and their leads |
| CX/UX/UI knowledge reference | `hq/core/standards/knowledge-cx-uiux.md` | source of the injection map (Section 6) |
| **UI/UX executive law** | `hq/core/standards/uiux-standard.md` | binding on rooms 03·06·07·10 — screen order, eight states, a11y, anti-slop, mockups |

> *Last updated: 2026-08-23 (R3: attaching UIUX-STANDARD as the executive law for interfaces) — version v2 "Upfront Comprehensive Design" under OWNER-DIRECTIVE-2026-0823-R2 / SOFI-HQ-INT-0002 (direct owner amendment of v1). Any change requires brd-ceo approval and updating the machine source together.*
