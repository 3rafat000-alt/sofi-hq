# DELETED — Removals Table from the Active Tree

> Purpose: every item that left the active tree, its reason, and its archive location. Archive: `../SOFI-archive-20260825-2040/` (full sha256 fingerprints in its `checksums.txt`).
> Created: 2026-08-25 · Team: Wave 3 · Rollback for any row: `bash ../SOFI-archive-20260825-2040/restore.sh <original-path>`

## Archived Files & Contents

| Original path | Action | Reason | Archive location |
|---------------|---------|-------|------------------|
| `org_brain/**` (33 items: cortex-decisions · hippocampus-sessions · amygdala-incidents · owners-matrix.yaml · brain_templates/ · handoffs/ · org_lessons/ · state_runtime/ …) | removal via archiving | Locked decision 1: emptying organization memory from the tree with full preservation | `org_brain/**` |
| `memory_index/memory-index.md` (previous content) | archive then rewrite the file as an introduction under the same name | same memory logic + zero broken references | `memory_index/memory-index.md` |
| `.playwright-mcp/` (8 browser log/snapshot files) | archive and remove | transient test-session leftovers (W1) | `.playwright-mcp/` |
| `caddy/Caddyfile` (old unified 405-line version) | archive then replace with the short main file | W7: extensible structure | `caddy/Caddyfile` |
| `caddy/site/README.md` | archive and remove folder | replaced by `sites/` per the 2026-08-25 plan | `caddy/site/README.md` |
| `caddy/php-fpm/pool.d/{jw,owais,sofi,sofi-demo,www}.conf` | archive then move to `caddy/php-fpm/disabled/` | W8: sakk only active | `caddy/php-fpm/pool.d/` |
| `projects/sakk/docs/rebrand-plan/cv-D*.log` ×8 + `conv-run.log` | archive and remove | transient conversion logs (automatic surplus W1) | `projects/sakk/docs/rebrand-plan/*.log` |
| `caddy/README-LIVE.md` | archive and remove after merging valid remains into `OPERATIONS.md` | W9: stale document (2026-08-09 reality), duplicated | `caddy/README-LIVE.md` |

## Direct Removals Without Archiving (no content at all)

| Path | Reason | Rollback |
|--------|-------|---------|
| `prompts/` | completely empty folder (0 files — verified by check) | `mkdir prompts` |
| `caddy/docs/` | completely empty folder (0 files — verified by check) | `mkdir caddy/docs` |

## Internal Moves (left their position without leaving the tree)

| From | To | Reason |
|----|-----|-------|
| Caddy blocks: jw/wa×2 · tobacco×5 · wildcard | `caddy/sites-disabled/{jw-owais-wa-410,wildcard-zanjour,tobacco}.caddy` | Locked decision 2: disable by moving, not deleting |
| the five `php-fpm/pool.d/*` | `caddy/php-fpm/disabled/` | W8 |

**Total archived:** 48 files = 48 sha256 fingerprints (match confirmed) · random restore sample: 10/10 success with fingerprint equality.
