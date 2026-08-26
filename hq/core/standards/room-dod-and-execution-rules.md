# FILE: hq/core/standards/room-dod-and-execution-rules.md
# Consolidated Operational Reference — Room DoD & Execution Rules

> **Document type:** Derivative Reference ONLY — no precedence over
> `constitution-master.md`, `protocols.md`, `kpi-thresholds.md`,
> `gate_checklists/`, or any room charter.
> **Purpose:** one-stop access to completion criteria currently scattered across
> gates and charters, plus three binding operational micro-rules.
> **Authority:** owner order 2026-08-26 (enhanced-consolidation variant).
>
> **Constitutional subordination:** this document is derived exclusively from
> AGENTS.md (Laws 1·4·14·15·16), protocols.md (1–18), kpi-thresholds.md (K1–K17),
> gate_checklists/, and domain/rooms/*/charter.md. On ANY conflict, this document
> is automatically void at that point and the source documents apply.

**Ground facts (aligned):** 15 rooms · 114 agents · 109 skills · 18 protocols · test coverage ≥ 90% (K15).

---

## Section 1 — Unified Definition of Done (DoD)

A room may not deliver until every criterion below is TRUE. The receiving Lead rejects any handoff that fails them.

| Room | Mandatory DoD before delivery |
|---|---|
| **14-Gateway** | ☐ Ambiguity ≤ 20% (or clarification card sent) · ☐ Lane classified 🟢/🟡/🔴 with evidence · ☐ RCCF work order formatted |
| **01-Strategy** | ☐ PRD at `projects/<slug>/brain/CONTEXT.md` · ☐ MVP scope bounded (in/out) · ☐ Risk assessment documented (`str-risk-analyst`) |
| **02-Research** | ☐ Every fact carries its cited source(s) · ☐ Visual patterns documented per Protocol 18 (3–5 examples) · ☐ `res-fact-checker` sign-off |
| **04-Architecture** | ☐ OpenAPI contract frozen & versioned · ☐ ADR chain complete for non-trivial decisions · ☐ Reviews documented by `arc-security-architect` + `arc-performance-architect` · ☐ DDD capsule rules applied |
| **08-Data** | ☐ ERD approved by `arc-data-architect` · ☐ All migrations reversible (rollback tested) · ☐ `dat-privacy-officer` sign-off on sensitive data handling · ☐ Index strategy per query pattern |
| **03-Design** | ☐ All 8 interface states designed (ideal · loading · empty · error · partial · offline · denied · loading-more) · ☐ RTL validated by `dsn-arabic-ux-specialist` · ☐ Design tokens only (raw hex forbidden) |
| **🛑 DFR Gate** | ☐ Signatures: security (09) + quality (10) recorded in `gate_checklists/` · ☐ **NO CODE before this gate passes** |
| **05-Backend** | ☐ API responds OK for contract endpoints in sandbox build · ☐ Coverage on changed code ≥ 90% (K15) · ☐ `License-check: allowed` filled per Law 15 · ☐ Secrets scan clean (`sec-secrets-warden`) |
| **07-Mobile / 06-Frontend** | ☐ Build success (Flutter iOS+Android+Web) · ☐ Connected to **live** API — mocks forbidden in final delivery · ☐ Test coverage ≥ 90% (K15) |
| **10-Quality** | ☐ E2E critical paths 100% pass · ☐ Pixel-match confirmed (`qa-design-auditor`) · ☐ Zero open critical defects · ☐ Release verdict recorded |
| **11-DevOps** | ☐ Rollback plan documented AND tested · ☐ Deploy succeeded with passing health check |
| **12-Observability** | ☐ All KPIs (K1–K17) 🟢 or 🟡 · ☐ Alert ↔ Runbook 1:1 mapping complete (K17) |
| **13-Knowledge** | ☐ Decision logged (CORTEX) · ☐ Lesson extracted (LESSONS) · ☐ Memory isolation verified (no cross-project contamination) |

---

## Section 2 — Binding Operational Micro-Rules

### Rule 1 — Dependency-Aware Parallelism
*Derived from: Law 1 (Proportional Flow) + `str-agile-orchestrator` mandate.*

Rooms inside the same phase (e.g., 04 · 08 · 03 in P3) run in parallel **only while their
contracts are independent**. If Architecture needs Data's ERD to freeze its API contract,
Architecture waits. `str-agile-orchestrator` tracks these dependencies and blocks premature
starts (WIP limits) until required inputs exist.

### Rule 2 — Specific Rejection Rule
*Derived from: handoff protocol (Protocol chain) + Law 4 (Evidence).*

A rejecting room MUST NOT use vague language ("quality is low", "rework"). Every rejection
carries exactly three elements:
1. **Precise location:** `file:line` or ticket/component name.
2. **Violated criterion:** the exact DoD row or protocol clause breached.
3. **Actionable fix direction** — concrete enough to act on.

Vague or unspecified rejection = **L1 violation for the rejecting Lead**.

### Rule 3 — Double-Rejection Freeze
*Restates Law 14 verbatim for quick access.*

Same artifact rejected twice consecutively for the same specified reason → immediate freeze;
no third blind attempt; automatic escalation to `brd-arbiter` (room 00) for a binding verdict
within 24 hours.

---

*Source of authority: owner order 2026-08-26 · derived consolidation, subordinate to all source
documents above · review cadence: alongside quarterly charter reviews.*
