# MODIFIED — Modifications Table for the Active Tree

> Purpose: every file modified or created within the operation, the nature of the change, and its reason.
> Created: 2026-08-25 · Squads: Waves 3–5 · Rollback of any change: the previous copy in `../SOFI-archive-20260825-2040/` or git.

| Path | Nature of change | Reason |
|--------|---------------|-------|
| `cleanup-workspace/LOCK-REGISTRY.md` · `BLOCKED.md` | created | step 1: the lock registry and the blocked-items log |
| `cleanup-workspace/reports/*.md` (9 reports) | created | section 10: mandatory operation outputs |
| `../SOFI-archive-20260825-2040/` (outside root) | archive created + checksums.txt + restore.sh | W3: no deletion without a documented copy |
| `org_brain/brain-index.md` | rewritten as an archive introduction (same name) | W4 + keeping the constitution reference alive |
| `memory_index/memory-index.md` | rewritten as an archive introduction (same name) | W4 + zero broken references |
| `.gitignore` | removed the duplicated `projects/sakk` line and the stale `projects/caddy` one; added `cleanup-workspace/` | cleaning dead patterns + W5 |
| `caddy/Caddyfile` | rewrite: 43 lines (snippets + 404 guard + single import) | W7 |
| `caddy/sites/sakk.caddy` | created — verbatim carry of sakk's section from the archived original | W7: no functional change |
| `caddy/sites-disabled/*.caddy` (3 files) | created — disabled block texts as they were | locked decision 2 |
| `caddy/php-fpm/disabled/` | created; 5 pools moved into it | W8 |
| `caddy/php-fpm/disable-pools.sh` | created (one-time root script) | executing W8 live needs sudo |
| `caddy/scripts/status.sh` | tobacco checks → local and public sakk checks | step 7: the script reflects reality |
| `caddy/OPERATIONS.md` | comprehensive update + merging README-LIVE's core (sites/ structure · new domain map · corrected paths) | W9 |
| `caddy/php-fpm/README.md` | updated pool map (active: sakk only) | documentation consistency |
| `governance_law/structure-standard.md` | updated canonical tree + added v4.3 log entry (outside law texts) | supporting document matching reality |
| `caddy/brain/DECISIONS.md` | added evidence-documented ADR-002 | Law 7: documenting the decision |
| `caddy/brain/CONTEXT.md` | updated project structure line to the new layout | project memory consistency |

## What Was Never Touched (justified)

`AGENTS.md` · law texts in `governance_law` (except the supporting structure map) · `identity/` · `training/` · `tech_templates/` · `tooling/` · `.kilo/` · `.opencode/` · everything inside `projects/sakk/` except 9 transient `.log` files · `backups/` (root-owned) · `opencode.json`.
