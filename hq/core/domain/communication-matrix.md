# Communication & Return Matrix — SOFI HQ

> **Purpose:** ONE reference answering "who talks to whom, who returns work to whom, who escalates to whom" — consolidated verbatim from existing binding sources; introduces zero new rules.
> **Sources:** AGENTS.md Laws 1–16 · constitution-master.md (Teachings · Room Isolation · Precedence) · room charters · agents' senses.yaml · ddd-capsule-protocol §5 · context-map.yaml.
> **Created:** 2026-08-26 (owner-requested consolidation) · record: `hq/history/2026-08-26-operational-gaps/`.

---

## 1. Intake chain (how work enters)

| Step | From → To | Rule |
|---|---|---|
| 1 | Owner → `gtw-intake-reformer` | Law 1 — no request bypasses intake; ambiguity >20% halts (Law 16) |
| 2 | Intake → `brd-ceo` (via classification) | reformulated intent + track (fast/standard/critical) |
| 3 | CEO → room Lead(s) via Task | work order (RCCF, Law 5); chief-of-staff formats orders |
| 4 | Lead → own specialists via Task | each agent's `senses.yaml.listens` defines its tickets |

## 2. Delivery chain (how work exits)

`specialist → own room Lead → brd-ceo → owner` (Law 3). Direct delivery to owner or another room = L3. Cross-room handoff = isolated JSON only (`sofi-handoff` ticket + evidence block per Law 4).

## 3. Cross-room requests (consultation paths)

`specialist A → A's Lead → B's Lead → specialist B` (Room Isolation Law; leads forward verbatim). Standing consultation gates already wired:

| Gate | Consulted party | Trigger |
|---|---|---|
| DFR design freeze | 09-security + 10-quality | every S3 design before any code |
| Roadmap risk sign-off | `sec-threat-modeler` | roadmap approval (room 01 charter) |
| Contract testability | `qa-test-architect` | API contract freeze (room 04 charter) |
| Sandbox build gate | `ops-sandbox-executor` | every code task before review/QA (Hard Rule #11) |
| License gate | `sec-license-auditor` | any dependency change (Law 15) |
| External review desk | `gtw-external-reviewer` | fateful decision points (Teaching VII) |
| Board consultation | brd-* advisors | critical-track decisions (Law 6) |
| Excellence ritual | `str-agile-orchestrator`+`knw-reflector`+`arc-review-architect` → `brd-cto` | monthly process-health review |
| Research data flow | `dsn-ux-architect` → dsn-lead → res-lead → `res-ux-researcher` / `res-journey-architect` | design needs user/journey evidence (added 2026-08-26) |
| Endpoint security design | `arc-security-architect` ↔ sec-lead → `sec-threat-modeler` / `sec-authn-engineer` | secure-architecture design ↔ threat model & implementation (added 2026-08-26) |
| Performance budget handoff | `arc-performance-architect` → obs-lead → `obs-monitoring-engineer`; → dat-lead → `dat-cache-engineer` | SLO budgets to measurement; cache mechanics to implementation (added 2026-08-26) |
| Mobile design fit | `mob-flutter-engineer` → mob-lead → dsn-lead → `dsn-ux-architect` | mobile-suitability verification of designs (added 2026-08-26) |

## 4. Return / rejection paths (work going back)

| Rejection source | Returns to | Via |
|---|---|---|
| `ops-sandbox-executor` FAIL | owning builder agent | error-log.json through both leads (self-repair loop) |
| Quality rejection (room 10) | building room's lead → builder | RCCF return naming the failed item |
| **2nd consecutive same-reason rejection** | **FREEZE** | Law 14 → `brd-arbiter`, binding verdict ≤24h |
| License VETO | builder agent | package+version+evidence so an alternative is picked immediately |
| Design-audit mismatch (`qa-design-auditor`) | `dsn-lead` → designers | item named, no generic rework |
| Regression break (`qa-regression-warden`) | last-changing builder | failing test evidence |
| Standards drift finding (`arc-review-architect`) | owning lead | correction decision through CEO when cross-room |

## 5. Escalation ladder

```
agent → room Lead → brd-ceo → owner
conflicts: gtw-conflict-resolver → brd-arbiter (Law 14 window)
security incidents: obs-alerting → incident chain (obs-incident-commander ↔ sec-incident-responder) → brd-cso veto if needed
3 consecutive technical failures of one category: stop + dump logs + escalate (Anti-Loop, Law 6)
emergencies: HALT · RESTART · ESCALATE · FREEZE (AGENTS.md commands)
```

## 6. Hard prohibitions

- No direct owner-chat for any non-intake agent (`forbidden-inputs` in every senses.yaml).
- No specialist-to-specialist across rooms (L3).
- No work order without intake; no delivery without evidence; no merge without sandbox PASS + license check.

---
*This matrix is descriptive consolidation, not new law — where wording differs, the underlying binding source governs.*
