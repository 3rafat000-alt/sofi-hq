# `projects/` — Project Memories (Law 7)

> **Two completely separate memories that never mix** (Law 7): organization memory (`hq/brain/`) and
> project memory (`projects/<slug>/brain/`). Promotion from project to org requires explicit
> `brd-ceo` decision.

This directory is the **container for all active and archived projects**. Every project has its own
subdirectory with a `brain/` (PRD + decisions + handoffs + lessons) and a codebase.

---

## The active project (sakk)

> Source: `projects/sakk/brain/CONTEXT.md` — the PRD v2.0 (single source of truth for sakk).

**The sakk project (سَكّ):** a fintech/digital-wallet platform for the Saudi market.

**Stack:**
- **Backend:** Laravel 11+ · PHP 8.3+ · PostgreSQL 16+ · Redis 7+ (per Stack Lock R3)
- **Web (admin + portal):** React 19 + Vite (per Stack Lock R3 — see `apps/`)
- **Mobile:** Flutter 3.22+ · Dart 3+ (per Stack Lock R3 — see `mobile/`)

**Memory structure (per project, mirrors `hq/brain/`):**
- `CONTEXT.md` — PRD (Product Requirements Document) — single source of truth
- `DECISIONS.md` — project-level decisions (promotable to CORTEX only by `brd-ceo`)
- `HANDOFFS.md` — task handoffs within the project
- `LESSONS.md` — lessons learned

**Operational artifacts (per project, outside brain):**
- `backend/` — Laravel 11+ codebase
- `mobile/` — Flutter 3.22+ codebase
- `apps/` — React 19 + Vite codebase (admin + portal)

---

## Per-project schema (created by `sofi-project-spawn`)

```
projects/<slug>/
├── README.md                       ← project overview + onboarding (this is created)
├── brain/                          ← project memory (Law 7)
│   ├── CONTEXT.md                  ← PRD
│   ├── DECISIONS.md                ← project-level decisions
│   ├── HANDOFFS.md                 ← task handoffs
│   └── LESSONS.md                  ← lessons learned
├── backend/                        ← optional — language-specific
├── mobile/                         ← optional — Flutter/Dart
├── apps/                           ← optional — React/Vue
└── docs/                           ← optional — supplementary
```

> **Tip:** `projects/sakk/brain/CONTEXT.md` is the gold-standard example — read it before creating
> a new project.

---

## The sakk project in detail

> Source: `projects/sakk/brain/CONTEXT.md`

**Mission:** build a digital-wallet platform for the Saudi market with KYC/AML, Mada/Apple Pay
integration, and full Arabic UX.

**Core features:**
- User onboarding with KYC (national ID / Absher)
- Wallet (topup via Mada/Apple Pay, transfer P2P, bill payment)
- Merchant payments (QR + online checkout)
- Admin (KYC review, fraud monitoring, reports)
- Arabic-first UX (RTL + Law 11 voice)

**Sprints:** 6 sprints (12 weeks MVP).

**Current state (2026-09-05):**
- Backend: 16 Domain (`backend/app/Domains/*`) · 45+ migrations · 1309 tests in cache
- Web: 28 React admin pages
- Mobile: 22 Flutter features
- Pipeline: 1 ERD unified, frozen OpenAPI, DFR pending

---

## How to create a new project

1. Use the `sofi-project-spawn` skill (or run its underlying tool)
2. The skill creates the directory structure + template files (CONTEXT/DECISIONS/HANDOFFS/LESSONS)
3. Fill in `CONTEXT.md` first (PRD — single source of truth)
4. Then trigger Strategy (S1) to fill in the rest

**Tip:** for every project, always **start with the PRD** in `CONTEXT.md`. Do not write code without
CONTEXT.md being approved (Law 5 + the S1→S6 flow).

---

## The sakk cleanup (2026-08-25)

> Source: `hq/core/system-state-current.md` — the sakk-only cleanup that archived all non-sakk projects.

On 2026-08-25 (owner directive), all non-sakk projects were archived to
`/home/es3dlll/Desktop/SOFI-archive-20260825-2040/`. The cleanup established:

- **sakk is the only active project** (the single source of truth for the live engine layer)
- All archived projects can be restored via `bash <archive>/restore.sh <path>` if needed
- This is documented in CORTEX as `ADR-20260831-SAKK-DOUBLE-VERIFY`

---

## Law 7 — the binding rule (restated)

> **`AGENTS.md:42` Law 7:** "Two completely separate memories that never mix:
> - **Organization memory:** `hq/brain/` (CORTEX decisions · HIPPOCAMPUS sessions · AMYGDALA incidents).
> - **Project memory:** `projects/<name>/brain/` (DECISIONS · HANDOFFS · LESSONS · CONTEXT) — created from `hq/core/templates/`.
> Promotion only by CEO decision. **No documentation = L1 · repetition = L2.**"

**Forbidden:**
- Writing to `hq/brain/` from a project context without `brd-ceo` decision
- Writing to `projects/<slug>/brain/` from an org context (org-wide facts belong in `hq/brain/`)
- Mixing both in a single commit

---

## See also

- [`hq/brain/`](../hq/brain/README.md) — organization memory (sister)
- [`hq/core/templates/report-template.md`](../hq/core/templates/report-template.md)
- [Top-level README](../README.md)
- [`AGENTS.md`](../AGENTS.md) — Law 7
