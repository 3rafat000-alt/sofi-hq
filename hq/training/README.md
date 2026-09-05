# `hq/training/` — Training Guides

> Training guides for new agents + developers joining SOFI HQ. These are the **onboarding
> materials** — practical, step-by-step, no jargon (Law 11 friendly).

Owned by `knw-doc-writer` (13-knowledge) + `gtw-dispatcher` (14-gateway).

---

## Files

| File | Purpose |
|------|---------|
| `rooms-guide.md` | Per-room guide — what each room does, how to work with it |
| `file-discipline.md` | File naming + organization + Law 13.3 (every file `## FILE: <path>`) |
| `ddd-full-cycle-playbook.md` | The full DDD cycle — discovery → design → build → deploy → run |
| `kilo-agent-manager-guide.html` | (legacy) Kilo agent manager guide — pre-Audit-ALL harness documentation |

---

## The rooms-guide (`rooms-guide.md`)

> Source: the canonical guide to all 17 rooms — what each does, who's the lead, how to work
> with them.

For every room, the guide includes:
- **Purpose** (1 line)
- **Provides** (what the room produces for the org)
- **Requires** (what the room needs)
- **Talks to** (legitimate neighbors)
- **Forbidden** (what the room never does)
- **SOP** (standard operating procedure)
- **How to interact with this room** (for other agents)
- **Key agents** (the room's roster)

> Tip: read this before your first interaction with a room. The guide is the **practical**
> companion to `hq/core/domain/rooms/<room>/charter.md`.

---

## The file-discipline (`file-discipline.md`)

> Source: the file naming + organization discipline. Per Law 13.3, every file starts with a
> `## FILE: <path>` header.

Rules:
- **kebab-case** for directories and files (e.g. `qa-flutter-architect/`)
- **`## FILE: <path>` header** on every file (the path is the first line of the file's purpose)
- **kebab-case names** for agents, skills, and rooms (e.g. `qa-laravel-architect`)
- **snake_case** is allowed for technical identifiers (e.g. `cascade_cascade` is a SQL keyword)
- **No spaces** in file or directory names (use `-`)
- **No uppercase** except in the brand name (SOFI) and acronyms (API, MCP, RCCF)
- **No periods** in file names (except in extensions like `.md`)
- **old ← new maps** (Law 13.5) for any rename — see `archive/README.md`

---

## The ddd-full-cycle-playbook (`ddd-full-cycle-playbook.md`)

> The full DDD cycle playbook — discovery → design → build → deploy → run.

Phases:
1. **Discovery (S1)** — Strategy + Research (rooms 01 + 02) — PRD + research dossier
2. **Design (S2 + S3)** — Architecture + Design (rooms 04 + 03) — ERD + OpenAPI + DFR
3. **Build (S4 + S5)** — Backend + Frontend + Mobile (rooms 05 + 06 + 07) — code
4. **Deploy (S6)** — DevOps (room 11) — Caddy + PHP-FPM
5. **Run (S6)** — Observability + Quality (rooms 12 + 10) — monitoring + testing
6. **Reflect** — Knowledge (room 13) — CORTEX + HIPPOCAMPUS + AMYGDALA

The playbook is the **practical walkthrough** of the S1→S6 pipeline.

---

## The kilo-agent-manager-guide.html (legacy)

Pre-Audit-ALL documentation for the Kilo harness. Kept for historical reference. The active
harness documentation is now in `opencode.json` + `hq/core/tooling/README.md`.

---

## How to add a training guide

1. Create the `.md` file with the standard format (purpose + structure + examples)
2. Add a row to the table above
3. Reference from at least one `charter.md` or `AGENTS.md` section
4. Commit atomically — pre-commit enforces all 4 guards
5. Update the onboarding checklist (`brd-chief-of-staff` responsibility)

**Forbidden:** adding training guides that are not **practical + step-by-step + no jargon**. The
training is for new agents + developers who don't know SOFI HQ yet.

---

## See also

- [`../README.md`](../README.md) — `hq/core/` parent
- [`../../AGENTS.md`](../../../AGENTS.md) — supreme law
- [`../constitution_articles/00-operating-system.md`](../constitution_articles/00-operating-system.md) — the meta-article
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 11
