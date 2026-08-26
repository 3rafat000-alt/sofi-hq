# File Discipline — Team Training
**For every agent in every room. Read it once, apply it always. The governing reference: [[STRUCTURE]].**

> The problem we address: swarms creating files randomly — screenshots at the root, forgotten temp files, clashing names, uncommitted work drifting apart. The result: chaos that slows everyone down. These seven rules end it.

## The Seven Rules

1. **Before creating a file, ask: what is its type?** The type determines the folder per [[STRUCTURE]] §2. No "temporarily at the root". If you cannot find a place, ask your lead — never invent.

2. **Temp files live outside the tree.** Any script/intermediate output/working file → `$OPENCODE_JOB_DIR/tmp` (cleaned automatically). Temp files inside the main tree are forbidden.

3. **Visual assets → `tech_templates/` (template assets).** Screenshots, drawings, diagrams, graph exports. **Zero images at the root or scattered among documents.** Name them clearly: `<subject>-YYYY-MM-DD.png`.

4. **Evidence goes to its designated place.** The delivery evidence block via `sofi-evidence`; work-order artifacts → `hq/brain/org_lessons/artifacts/WO-.../`; never scatter evidence at the root.

5. **No blind deletion, no `git add -A`.** (LES-013) Selective staging by path. Old/finished material → `hq/brain/auto_memory_archive/` (local archive)`YYYY-MM-DD/`, **never deleted** (lesson CS-4: a security report was unintentionally deleted). Permanent deletion only for recurring litter (playwright/cache) and by lead decision.

6. **One correct name from the first attempt.** kebab-case, room prefix, official identifier ([[STRUCTURE]] §5). No `_v2_final_new`. One file per subject — no scattered copies.

7. **Never leave uncommitted work drifting.** (Law 10) Work directly on the main tree, committed selectively at task closure. No forgotten branches, no worktrees, no modified files left for days.

## Chain of Responsibility
- **Agent:** applies the seven to every file they touch.
- **Lead:** rejects any delivery containing a misplaced file (a mandatory clause in every delivery review) — just as they reject a delivery without evidence.
- **CEO:** inspects root cleanliness at the close of every session.

## Quick Self-Check (before delivery)
```
□ zero new files at the root (except intake docs)?
□ every image in tech_templates/ (template assets) with a clear name?
□ every temp file in $OPENCODE_JOB_DIR/tmp?
□ naming kebab + prefix + official identifier?
□ old material in archive/, not deleted?
□ work committed selectively, nothing drifting?
```

*Governing reference: [[STRUCTURE]]. Last updated 2026-07-17.*
