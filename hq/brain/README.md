# `hq/brain/` — Organization Memory (Law 7)

> **Two memories that never mix:** organization memory (this directory) and project memory
> (`projects/<slug>/brain/`). Promotion from project to org requires explicit `brd-ceo` decision.

The `hq/brain/` directory is the **institutional memory** of SOFI HQ. Every fateful decision is
recorded here, every session logs its outcome, and every P0 incident leaves a forensic trail.

---

## The 3 memory files (the constitutional triad)

| File | Records | Format | Curation |
|------|---------|--------|----------|
| `cortex-decisions.md` | **CORTEX** — Architecture Decision Records (ADRs) | `## ADR-YYYYMMDD-NAME — title` + context + decision + consequences + evidence refs | `knw-doc-writer` |
| `hippocampus-sessions.md` | **HIPPOCAMPUS** — session log (one per session) | `## SES-YYYYMMDD-…` + classification + what + evidence + status | `knw-historian` |
| `amygdala-incidents.md` | **AMYGDALA** — incident log (WarRoom P0 + SEV-1) | timeline + forensic + rollback + postmortem + re-eval | `knw-memory-curator` |

**Auto-summarize (P-06.7):** `hq/core/tooling/memory_summarizer.py:1` runs every 10 turns via
`knw-reflector` — when `hippocampus >800` or `amygdala >600`, keep last 5 full + summarize older.

---

## CORTEX — the ADR log

> Source: `cortex-decisions.md` — every fateful decision is recorded here. **Read this first**
> when joining an existing project or before making any new fateful decision.

**Key ADRs to read:**
- `ADR-20260831-9AXIS-FIX` — the constitutional machinery (4 guards + 16/114/109)
- `ADR-20260831-VISUAL-DIAGRAMS` — 9 Mermaid diagrams
- `ADR-20260831-SAKK-DOUBLE-VERIFY` — sakk double-pass
- `DEC-R3.4-PHASEB-ACCEPT-20260905` — Phase B acceptance
- `ADR-20260905-GTW-FLUTTER-QA-ARCHITECT` — qa-flutter-architect (Rayan Al-Qadi)
- `ADR-20260905-GTW-REACT-DDD-ARCHITECT` — qa-react-architect (Samer Al-Khalil)
- `ADR-20260905-GTW-LARAVEL-DDD-ARCHITECT` — qa-laravel-architect (Yousuf Al-Amiri)
- `ADR-20260905-AUDIT-ALL` — Audit-ALL (Level 1+2 + WarRoom 15)
- `ADR-20260905-AUDIT-ALL-Phase2` — Localization 08 + Innovation 16
- `ADR-20260905-AUDIT-ALL-Phase3` — Redistribute 04 (ml→inn · privacy→loc) + 3 skills + zero pending
- `DEC-R6-20260905-ARCHIVE-LEGACY-AGENTS` — R6 closure (legacy tree archived)
- `ADR-20260905-GTW-DELEGATE-EXEC` — owner-explicit override (Law 10 + 11 invocation)

---

## HIPPOCAMPUS — the session log

> Source: `hippocampus-sessions.md` — one entry per session, with classification (Fast/Standard/Fateful),
> evidence, and status.

Current sessions include: 9-axis fix, R3.1 reconciliation, Phase A/B, all 3 qa-* additions, Audit-ALL
+ Phase2 + Phase3, and the recent WarRoom / loc / inn creations.

---

## AMYGDALA — the incident log

> Source: `amygdala-incidents.md` — every P0 incident (WarRoom activation or SEV-1).

Currently empty (no P0 incidents since inception — the organization is in good standing). If
incidents occur, they are logged here within 24h, including:
- Timeline (detection → triage → containment → recovery → postmortem)
- Forensic evidence (file:line per finding, hashes)
- Rollback actions (who did what when)
- Postmortem (root cause + actions + re-evaluated gate)

---

## `evidence/` — per-task audit + snapshot files

> Source: `hq/brain/evidence/` — snapshot files for major reviews (e.g. `surgical-review-*`).

These are **immutable historical artifacts** — never edited, only added to. They include surgical
review reports, audit reports, and any major review with file:line evidence.

---

## How to add to CORTEX / HIPPOCAMPUS / AMYGDALA

**Add an ADR (CORTEX):**
```markdown
## ADR-YYYYMMDD-NAME — title
- **date:** YYYY-MM-DD
- **owner decision:** <what the owner said>
- **classification:** FATEFUL/STANDARD/FAST
- **verdict:** APPROVE/REJECT/CONDITIONS
- **what was done:** <one-line>
- **guards state:** PASS/FAIL · zero pending
- **evidence refs:** file:line
```

**Add a session log (HIPPOCAMPUS):**
```markdown
## SES-YYYYMMDD-… — title
- **session:** date + context
- **classification:** FATEFUL/STANDARD/FAST
- **what:** <one-line>
- **guards state:** PASS/FAIL
- **status:** in-flight / closed
```

**Add an incident (AMYGDALA):** only WarRoom commander or `sec-incident-responder` may add.
Must include timeline + forensic + postmortem + re-evaluated gate.

---

## Law 7 — the binding rule

> **`AGENTS.md:42` Law 7 — Memory Binding:** "Two completely separate memories that never mix:
> - **Organization memory:** `hq/brain/` (CORTEX decisions · HIPPOCAMPUS sessions · AMYGDALA incidents).
> - **Project memory:** `projects/<name>/brain/` (DECISIONS · HANDOFFS · LESSONS · CONTEXT) — created from `hq/core/templates/`.
> Promotion only by CEO decision. **No documentation = L1 · repetition = L2.**"

**Forbidden:**
- Reading from `projects/<slug>/brain/` to write to `hq/brain/` (without `brd-ceo` decision)
- Writing `hq/brain/` content to `projects/<slug>/brain/`
- Mixing the two in a single commit (each goes in its own commit)

---

## See also

- [`hq/core/README.md`](../core/README.md) — parent
- [`projects/sakk/brain/`](../../projects/sakk/brain/) — example project memory
- [Top-level README](../../README.md)
- [`AGENTS.md`](../../AGENTS.md) — Law 7
