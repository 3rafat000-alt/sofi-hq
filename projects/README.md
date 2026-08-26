# Projects — Sole Home for Live Project Work

**Owner decision, 2026-07-24: superseded the 2026-07-16 "projects live outside the tree" policy below.** All product/project work the team builds now lives **inside this directory**, nothing elsewhere in the SOFI root.

## Rules

- **Direct on the main tree** (`AGENTS.md`, Law 10) — no worktrees, no isolated copies, no forgotten long-lived branches. A temporary branch for a hard technical reason must be merged and deleted before the task closes.
- Each project gets its own subdirectory here.
- `shamel` CLI is retired (no `shamel new`/`import`/`projects --verify`) — project setup is manual/agent-driven, not tool-generated.

## Project memory (Law 7) — separate from SOFI's own memory

Every project gets its own `brain/` folder, fully separate from the organization's `org_brain/`:

```
projects/<name>/
├── brain/
│   ├── CONTEXT.md      # live context — identity, rooms involved, current pipeline stage
│   ├── DECISIONS.md    # this project's own ADR chain
│   ├── HANDOFFS.md     # this project's handoff tickets (TKT-NNN)
│   └── LESSONS.md      # this project's own lessons (LES-NNN·sig)
└── <the project's native structure>   # Laravel/Flutter/… — SOFI imposes nothing here
```

**Setup:** when the first RCCF for a new project opens, its assigned lead copies `org_brain/brain_templates/{CONTEXT,DECISIONS,HANDOFFS,LESSONS}.md` into `projects/<name>/brain/`, replacing the `PRJ-XXXX` placeholder with the real project name.

**No mixing:** project decisions/lessons/handoffs are never written directly into `org_brain/cortex-decisions.md` or `org_brain/org_lessons/LESSONS.md`. They only get promoted to SOFI's own memory — with explicit `brd-ceo` approval — when a lesson repeats ≥3× across different projects, or a decision affects SOFI itself rather than just the one project. Full rules: `org_brain/brain-index.md` § "ذاكرة المشاريع".

## Governance

Projects are governed by the binding laws in `AGENTS.md` (pipeline lanes, hierarchy, evidence, RCCF) — enforcement is hierarchical (lead/CEO review), not mechanical.
