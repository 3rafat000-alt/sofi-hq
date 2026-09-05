# `hq/brain/evidence/` — Audit + Snapshot Files

> Per-task audit + snapshot files. **Immutable historical artifacts** — never edited, only
> added to. Used for surgical reviews, sign-offs, and major decisions that need a permanent
> paper trail beyond the ADR log in CORTEX.

Owned by `knw-historian` (13-knowledge) + `brd-cso` (security, for security audits).

---

## What's in here

| Pattern | Example | Purpose |
|---------|---------|---------|
| `surgical-review-*.md` | `surgical-review-full-2026-09-01.md` | The sakk double-pass review (R3.1 acceptance) |
| `surgical-review-*.md` | `surgical-review-visual-2026-08-31.md` | The 9 Mermaid diagrams review (4/4 APPROVED) |
| `roadmap-planner-WAVE-PLAN-UPDATE-001.md` | — | A roadmap wave plan (per roadmap-planner output) |
| `feeding-log.md` | — | Visual feeding log (per `mobbin-scraper` + Protocol 18) |
| `sofi-platform-n8n-test-plan-20260830.md` | — | The n8n test plan (per `n8n/workflows/`) |
| `test-execution-20260830/` | — | Test execution results (per `qa-automation-engineer`) |
| `visual-diagrams-test-report.md` | — | The visual diagrams test report (per `qa-design-auditor`) |
| `admin-2026-09-01/` | — | sakk admin audit (per `dsn-lead` + `fnt-lead`) |
| `backend-2026-09-01/` | — | sakk backend audit (per `bck-lead` + `sec-lead`) |
| `flutter-2026-09-01/` | — | sakk flutter audit (per `mob-lead` + `qa-flutter-architect`) |
| `2-2026-09-01/` | — | Second surgical review (per `brd-ceo` + Board) |
| `*` | various | Any other evidence file |

---

## The audit format

```markdown
# <Audit Name> — <date>
- **Owner:** <room> (lead: <agent>)
- **Scope:** <what was audited>
- **Reviewers:** <names>
- **Verdict:** APPROVED / APPROVED with conditions / REJECTED
- **Evidence:** file:line per finding

## Findings
### Finding 1
- file:line
- description
- suggested fix
- owner
- due date
```

---

## The 4/4 surgical review pattern

Major constitutional changes (e.g. R3.1 reconciliation, Audit-ALL-Phase3) go through a **4/4
surgical review**:

1. **dsn-lead** — design review (4/4) — UX + design system + DFR
2. **knw-lead** — knowledge review (4/4) — docs + memory + skills
3. **sec-lead** — security review (4/4) — STRIDE + DFR + License + Secrets
4. **qa-lead** — quality review (4/4) — K1–K17 + test plan + Gate-5

All 4 must approve before the change is committed. The evidence file is the audit trail.

---

## The CONDITION-FOLLOW-UP (DEC-R3.4)

> Files in `hq/brain/evidence/` are **never** truncated in delivery handoffs. They are
> immutable historical artifacts.

**Why:** they are the audit trail for fateful decisions. Truncating them breaks the constitutional
evidence chain (Law 4 + Law 7).

---

## How to add to this directory

1. Create the evidence file with the standard audit format above
2. Add a row to the table (or to the "various" catch-all)
3. Commit atomically — pre-commit enforces all 4 guards
4. If the evidence supports an ADR, reference the file from CORTEX

**Forbidden:** modifying existing evidence files. They are **immutable** — any correction is a
new file with a `correction-` prefix or a versioned name (e.g. `surgical-review-v2-*.md`).

---

## See also

- [`../README.md`](../README.md) — `hq/brain/` parent
- [`../cortex-decisions.md`](../cortex-decisions.md) — ADR log (CORTEX)
- [`../hippocampus-sessions.md`](../hippocampus-sessions.md) — session log
- [`../amygdala-incidents.md`](../amygdala-incidents.md) — incident log
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 4 + 7
