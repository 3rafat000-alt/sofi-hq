# FILE: hq/core/standards/kpi-thresholds.md
# KPI & Alert-Threshold Catalog — owner order 2026-08-26
#
# Purpose: one binding table of numbers with green/yellow/red thresholds so
# alerting is based on defined limits, never impressions.
# Owner: obs-alerting-engineer measures · obs-lead reviews · brd-ceo reports to owner.
# Every KPI is computed from real system artifacts (memory files, gate records,
# task cards) — a number that cannot cite its source (`file:line`) is invalid (Law 4).

## 1) Process KPIs (the organization itself)

| # | KPI | Source of truth | 🟢 Green | 🟡 Yellow | 🔴 Red |
|---|-----|----------------|----------|-----------|--------|
| K1 | Intake cycle time — raw request → routed work order | gateway intake records | same session | next session | > 1 session |
| K2 | Ambiguity-loop rate — requests needing Law-16 clarification | intake records | < 20% | 20–35% | > 35% |
| K3 | Gate pass rate — artifacts passing their gate on first submission | gate_checklists records | ≥ 85% | 70–84% | < 70% |
| K4 | Rework rate — tasks rejected back by qa/security | QA verdict records | < 15% | 15–30% | > 30% |
| K5 | Evidence completeness — sampled deliveries with full file:line evidence | monthly sample of 10 deliveries | 100% | 90–99% | < 90% |
| K6 | License-check compliance — merges with recorded `License-check` field (Law 15) | task cards + merge records | **100% (hard)** | — | any miss = L2 |
| K7 | Memory logging compliance — decisions in CORTEX, sessions in HIPPOCAMPUS (Law 7) | memory files vs session log | ≥ 95% | 85–94% | < 85% |

## 2) Incident KPIs (Protocol 10 deadlines)

| # | KPI | Target (from P-10.x) | Breach = |
|---|-----|----------------------|----------|
| K8 | SEV-1 response start | immediate (same turn) | L3 for detecting lead |
| K9 | SEV-2/3 response start | ≤ 3 / ≤ 5 turns | L2 for lead |
| K10 | RCA on-time for SEV-1/2 | ≤ 20 turns (P-10.4) | L3 for lead |
| K11 | Postmortem filed after every emergency | 100% (P-10.8) | L2 |
| K12 | Emergency drill executed | every 50 turns (P-10.9) | L1 for ops-lead |
| K13 | MTTR — mean time to resolve SEV-1/2 | trending down month-over-month | yellow if rising 2 months |

## 3) Project-delivery KPIs (apply per active project, e.g. sakk)

| # | KPI | 🟢 Green | 🟡 Yellow | 🔴 Red |
|---|-----|----------|-----------|--------|
| K14 | Deployment rollback plan present before deploy | 100% (deploy-standard.md:71) | — | any miss = deploy blocked |
| K15 | Automated test coverage on changed code | ≥ 90% | 75–89% | < 75% |
| K16 | Known defects at stage close | zero at S6 close (pipeline.yaml Gate rules) | ≤ 2 minor | any critical open |
| K17 | Alert↔runbook 1:1 mapping (gate-8.md:20) | 100% | — | any unmapped alert |

## 4) Operating rules

1. obs-alerting-engineer computes K1–K17 from source artifacts during the Daily Ops Digest and Weekly Review (standards/reporting-cadence.md).
2. Any 🔴 red reading fires an alert to the owning lead the same session; two consecutive reds escalate to brd-ceo automatically.
3. Thresholds change only by owner order or brd-ceo decision logged in CORTEX — silent drift is forbidden.
4. This catalog feeds Gate-8's `slo-report.md`; Gate-8 cannot pass while any hard rule (K6/K11/K14/K16/K17) is unmet.

*References: protocols.md P-10.4/P-10.8/P-10.9/P-14.6 · gate_checklists/gate-8.md:20 · standards/deploy-standard.md:71 · standards/reporting-cadence.md · nexus/room-priority.yaml. Created 2026-08-26.*
