# FILE: hq/core/standards/reporting-cadence.md
# Reporting Cadence Standard — owner order 2026-08-26
#
# Purpose: fixed rhythm of institutional reports so the owner sees the health of
# the organization regularly instead of discovering problems late.
# Delivery law: every owner-facing report is written by brd-ceo in clear simple
# Arabic (Law 11) — internal drafts stay technical.

## 1) The three reports

| Report | Producer (drafts) | Reviewer | Delivered | Anchored to |
|--------|-------------------|----------|-----------|-------------|
| Daily Ops Digest | gtw-dispatcher + obs-monitoring-engineer | obs-lead -> brd-ceo | Owner | First session of each working day |
| Weekly Performance Review | str-agile-orchestrator | str-lead + qa-lead -> brd-ceo | Owner | Last session of each week (Friday close) |
| Monthly Organizational Report | knw-historian + obs-insights-analyst | brd-ceo (+ Board consulted per Law 6) | Owner | Last session of each calendar month |

Since agents run on demand rather than wall-clock, "first/last session" means
the first/last SOFI session of that period; if a period had no session, the
report merges into the next one and says so explicitly.

## 2) Fixed contents (same skeleton every time — comparability over prose)

### Daily Ops Digest (≤ half page)
1. Rooms status: which rooms did work yesterday, which are idle/blocked
2. Open tickets and their lane (fast / standard / fateful)
3. Incidents: anything filed to AMYGDALA since last digest (or "none")
4. Bottlenecks: any stage frozen by a blocked T1 artifact (nexus/room-priority.yaml)
5. One line: "system healthy / needs attention" verdict

### Weekly Performance Review (≤ 2 pages)
1. Flow & WIP: tasks completed vs carried over (str-agile-orchestrator tracking)
2. QA verdicts: pass/fail counts, rework loops, any Law-14 freeze risk
3. KPI snapshot vs thresholds (standards/kpi-thresholds.md — yellow/red items highlighted)
4. Technical debt top-5 with proposed owners
5. Next-week plan (max 5 items, prioritized by room-priority tiers)

### Monthly Organizational Report (≤ 4 pages)
1. Month trend: KPI movement across the weeks, patterns and anomalies
2. Incidents recap: count by SEV level, MTTR, postmortem status (P-10.8)
3. Drills & audits: emergency-drill compliance (P-10.9), isolation audit (P-14.6)
4. Organizational review: room load balance, registry integrity (Law 12), skill gaps
5. Decisions log: CORTEX entries of the month (Law 7)
6. Next-month priorities (tiered per nexus/room-priority.yaml)

## 3) Rules

- Missing a report = L1 for the producing lead; missing twice consecutively = L2 (mirrors Law 7 discipline).
- Every number in a report cites its source artifact (`file:line`) — no uncited claims (Law 4).
- Reports are stored under `hq/brain/org_reports/<yyyy>/<mm>/` and indexed by knw-historian.
- The owner's reading time is respected: limits above are maximums; red/yellow findings come first.

*References: nexus/room-priority.yaml (priorities) · standards/kpi-thresholds.md (numbers) · protocols.md P-10.8/P-14.6 · AGENTS.md Laws 4/7/11. Created 2026-08-26.*
