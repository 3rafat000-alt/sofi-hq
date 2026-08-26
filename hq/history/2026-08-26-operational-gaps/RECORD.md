# Operational Gaps Closure — 2026-08-26 (owner order)

> Owner directive closing the six operational gaps identified in the SOFI HQ structural review (15 rooms · DDD · governance). Executed by `gtw-intake-reformer` session on the main tree (Law 10) with evidence per Law 4.

## 1. What was decided

| # | Gap | Decision |
|---|-----|----------|
| 1 | No flow/agile tracking | New agent **`str-agile-orchestrator`** in room 01-strategy — board-state tracking, cross-room blocker alerts, hard WIP ≤ 2 enforcement. Chosen over a new "delivery room" to keep the 15-room invariant of Law 12 intact. |
| 2 | No pre-QA build gate | New agent **`ops-sandbox-executor`** in room 11-devops — runs syntax/build/analyze checks (`php -l`, `flutter analyze`, …) inside ephemeral isolated containers; PASS → QA, FAIL → back to builder with precise error log. Chosen over room 10 placement: container/tooling ownership is infrastructure work; QA consumes its verdict. |
| 3 | No user-clarification protocol | Merged into **`gtw-intake-reformer`** as the Smart Clarification Loop (**Law 16**): ambiguity score > 20% halts processing and emits 1–3 specific questions until resolved. No fourth agent needed — the intake gateway already owns intent understanding. |
| 4 | No license/IP gate | New agent **`sec-license-auditor`** in room 09-security — dependency manifests checked before every merge; ALLOWED (MIT/Apache/BSD/ISC/MPL-2.0) vs VETO (GPL/AGPL/SSPL/unknown); codified as **Law 15**. Chosen over room 04: compliance/legal risk belongs with security's auditors next to `sec-compliance-auditor`. |
| 5 | Shift-left security & quality | Charter rules added: room 01 — no roadmap approval without `sec-threat-modeler` risk sign-off; room 04 — no API contract freeze without `qa-test-architect` testability review. Training checklist gains both shift-left questions as pre-build steps. |
| 6 | No strict rejection escalation | **Law 14 — Double-Rejection Protocol:** two consecutive same-reason QA rejections freeze the task; automatic escalation to `brd-arbiter` with a binding decision within 24 hours. |

## 2. Laws added to AGENTS.md

- **Law 14 — Double-Rejection Protocol**
- **Law 15 — License & IP Gate** (mandatory task-card field `License-check: [allowed/rejected]`)
- **Law 16 — Smart Clarification Loop** (20% ambiguity threshold at the gateway)

## 3. Files touched (evidence index)

| File | Change |
|------|--------|
| `hq/core/nexus/registry.yaml` | +3 agents (01·09·11), header count 106→109 |
| `hq/core/nexus/personas.yaml` | +3 persona entries (Munir Al-Sabuni · Tariq Al-Najjar · Nadim Al-Kaylani) |
| `hq/core/nexus/routing.yaml` | +3 routing entries (workhorse/mechanical tiers) |
| `.opencode/agent/{str-agile-orchestrator,ops-sandbox-executor,sec-license-auditor}.md` | new source definitions (template v2.1 conformant, nine sections + annexes) |
| `.opencode/agent/gtw-intake-reformer.md` | append-only annex LAW-16 (clarification loop) |
| `.kilo/agent/*` | regenerated mirror via `node hq/core/tooling/port-agents.mjs` → OK 109/109 |
| `hq/core/domain/rooms/{01-strategy,09-security,11-devops}/agents/<new>/` | capsules: agent.md symlink → source + capabilities.yaml + memory.md + senses.yaml |
| `hq/core/domain/rooms/01-strategy/charter.md` | roster 8 + agile-orchestrator duty + shift-left security rule |
| `hq/core/domain/rooms/04-architecture/charter.md` | shift-left quality rule (testability sign-off) |
| `hq/core/domain/rooms/09-security/charter.md` | roster 9 + license-auditor duty |
| `hq/core/domain/rooms/11-devops/charter.md` | roster 8 + sandbox-executor duty |
| `hq/core/domain/rooms/14-gateway/charter.md` | Room Law §Smart Clarification Loop (Law 16) |
| `hq/core/tech_templates/ddd-capsule-protocol.md` | Hard Rule #11 (sandbox gate) · task card `License-check` + `Sandbox` fields · acceptance checklist items · footer 13→16 laws |
| `hq/training/ddd-full-cycle-playbook.md` | Final Checklist: two shift-left pre-build questions + sandbox/license closure items |
| `hq/training/rooms-guide.md` | rows for the 3 agents + section counts (str 8 · sec 9 · ops 8) |
| `AGENTS.md` | heading 13→16 Binding Laws · Laws 14–16 bodies · Law 12 count 109 · last-updated footer |
| `hq/core/constitution-master.md` | preamble: one hundred and six → one hundred and nine agents |
| `hq/core/system-state-current.md` | counts + amendment note (2026-08-26) |

## 4. Verification commands (exit codes)

```
node hq/core/tooling/port-agents.mjs   → exit 0 · "OK: 109/109 agents -> .kilo/agent"
ls .opencode/agent | wc -l             → 109
ls .kilo/agent | wc -l                 → 109
```

## 5. Non-goals / deferred

- No new skills created (agents bind existing skills only — skill total stays 106).
- No changes to `projects/sakk/**` — this is HQ governance only.
- WIP limit tooling (board automation inside projects) remains a project-level concern; the rule and its enforcer exist now.

---

## Addendum — Engineering-Excellence decision (2026-08-26, later same day)

The external "VP of Engineering Excellence" proposal (5 new agents + Law 17) was evaluated against the live tree and **rejected as written** (duplicate coverage ~85% · merge-veto conflicts with brd-cso/brd-cqo gates · room-less agent violates Law 2). Owner chose the smart-upgrade option:

1. **`brd-cto` mandate upgrade** — append-only annex `ENG-EXCELLENCE` in `.opencode/agent/brd-cto.md`: owns engineering-process health across rooms 04–12 via a monthly binding ritual reading str-agile-orchestrator flow reports + knw-reflector lessons + arc-review-architect findings; explicitly holds NO parallel merge veto.
2. **Debt-capacity reserve** — Flow Rule #6 in `hq/core/tech_templates/ddd-capsule-protocol.md`: every Phase tree reserves ≥15% capacity for tech-debt tasks; allocated by `str-roadmap-planner`, enforced by `str-agile-orchestrator`, audited by brd-cto.
3. Charter rule added to `hq/core/domain/rooms/01-strategy/charter.md`; duty annexes appended to both strategy agents' definitions; `.kilo` mirror regenerated OK 109/109.

Net cost: **0 new agents · 0 new laws** — the VP layer's real value captured inside existing seats.

## Addendum 2 — Communication & Return Matrix (2026-08-26, same day)

Owner-requested consolidation answering the recurring external critique ("paths vague"): `hq/core/domain/communication-matrix.md` now consolidates intake chain · delivery chain · cross-room consultation gates · rejection/return paths (incl. Law-14 freeze and sandbox/license returns) · escalation ladder · hard prohibitions — derived verbatim from existing binding sources, zero new rules. Linked from AGENTS.md quick-reference table. Spot-verification confirmed agent files already answer the claimed-vague questions (brd-ceo senses · bck-code-reviewer collaboration block · res-fact-checker senses · sec-incident-responder senses).
