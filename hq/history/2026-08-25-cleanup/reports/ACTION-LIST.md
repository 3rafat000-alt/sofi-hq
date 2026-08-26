# ACTION-LIST — The Approved Actions List

> Purpose: converting the inventory into final executive decisions: what leaves, what is modified, what stays — with a reason per line.
> Created: 2026-08-25 · Team: Classification (before wave 2) · Sources: INVENTORY.md + live reference checks.

## A Governing Rule Derived from the Reference Check

The references of the constitution, standards, and generated agents were checked live; `training/`, `tech_templates/`, and `tooling/` turned out to be referenced by live binding files (`AGENTS.md`, `governance_law/standards/*`, `.kilo/agent/*`), so they are treated as «tool folders whose need was proven» and stay — executing the clause «tool folders whose need was proven» in spec W6.

## A) Removed from the Active Tree (after full archiving)

| Path | Action | Reason | Rollback |
|--------|---------|-------|---------|
| `org_brain/**` (all content except `brain-index.md`) | removal via archiving | Locked decision 1: emptying organization memory from the tree while preserving it | `restore.sh <path>` |
| `memory_index/memory-index.md` (current content) | archive then rewrite as an introduction | Locked decision 1: same memory logic, same name for zero broken references | `restore.sh` |
| `.playwright-mcp/**` | archive and remove | transient browser-test session leftovers (W1: automatic surplus classification) | `restore.sh` |
| `prompts/` | direct removal | completely empty folder (0 files) — nothing to archive | recreate the empty folder |
| `caddy/docs/` | direct removal | completely empty folder (0 files) | recreate the empty folder |
| `caddy/site/README.md` | archive and replace folder with `sites/` | spec W7 names the sites folder `sites/`; the stale 2026-08-24 note updated by merge | `restore.sh` |
| `caddy/php-fpm/pool.d/jw.conf` | move to `php-fpm/disabled/` | side project outside «sakk only» scope | move the file back |
| `caddy/php-fpm/pool.d/owais.conf` | move to `php-fpm/disabled/` | side project outside scope | move back |
| `caddy/php-fpm/pool.d/sofi.conf` | move to `php-fpm/disabled/` | served tobacco-center whose path no longer exists at all | move back |
| `caddy/php-fpm/pool.d/sofi-demo.conf` | move to `php-fpm/disabled/` | tobacco demo trial on a dead path | move back |
| `caddy/php-fpm/pool.d/www.conf` | move to `php-fpm/disabled/` | unused default serving no site (documented in php-fpm/README) | move back |
| Caddy blocks: jw/wa×2 · tobacco×4 · wildcard · localhost | move their text verbatim into `sites-disabled/` | Locked decision 2: disable by moving, not deleting — sakk only active | move file to `sites/` or append |
| `projects/sakk/docs/rebrand-plan/*.log` (9 files) | archive and remove | transient conversion logs (cv-*.log, conv-run.log) — automatic surplus | `restore.sh` |

## B) To Be Modified

| Path | Nature of change | Reason |
|--------|---------------|-------|
| `caddy/Caddyfile` | rewrite: shared snippets + catch-all 404 guard + a single `sites/*.caddy` import | W7: short main extensible by line/file |
| `caddy/sites/sakk.caddy` (new) | carry sakk's config verbatim with no functional change | W7 literally |
| `org_brain/brain-index.md` | rewrite as the sole introductory file (archive location, history, restore) | W4 + keeping the constitution's reference to `org_brain/brain-index.md` alive |
| `memory_index/memory-index.md` | rewrite as an archive introduction under the same name | W4 + zero broken references (constitution references stay valid) |
| `.gitignore` | delete the stale duplicated `projects/caddy` and `projects/sakk` lines (without slash), add `cleanup-workspace/` | cleaning dead duplicated patterns + preventing tracking of operation reports |
| `caddy/scripts/status.sh` | replace tobacco checks with local and public sakk checks | script must reflect the new reality (step 7) |
| `caddy/OPERATIONS.md` | comprehensive update for the `sites/` structure and reduced pools | W9: every surviving document reflects actual state |
| `caddy/README-LIVE.md` | check content duplication with OPERATIONS then merge or update | W9: prevent duplication |
| `caddy/php-fpm/README.md` | update pool map (sakk only active) | documentation consistent with reality |
| `governance_law/structure-standard.md` | update the tree-root map only (outside law texts) | supporting document that must match reality after restructuring |
| `caddy/brain/CONTEXT.md` + `DECISIONS.md` | record the deployment restructuring decision with its date | Law 7: every decision documented |

## C) Stays As-Is (justified)

| Item | Reason for staying |
|--------|------------|
| `AGENTS.md` · `opencode.json` · `.gitignore` (modified only) | constitutional core and live tooling |
| `governance_law/` entire | binding laws and living standards (light documentary cleanup only outside law texts) |
| `identity/` | official system identity |
| `training/` · `tech_templates/` · `tooling/` | live binding references from constitution, standards, generated agents (see rule above) |
| `.kilo/` · `.opencode/` | live agent tooling and agent source |
| `projects/sakk/` (source code, brain, core docs, openapi) | explicitly protected from the operation |
| `caddy/cloudflare/` | live tunnel documentation (its secrets outside the repository in ~/.cloudflared) |
| `caddy/scripts/{validate,deploy,diff-live,bootstrap-live}.sh` | work as-is after restructuring (validate will cover sakk.conf alone automatically) |
| `caddy/brain/` | deployment layer memory (Law 7 pattern) — updated, never emptied |
| `backups/` | root-owned — untouched (locked decision 5) |

## Special Cases Documented but Not Handled

- **613 prior deletions in git** (the shamestate tree removed from disk before this operation without migration): outside our scope, no commit in this operation, mentioned in the final report.
- **`jawaher-htdocs.service`** in a restart loop (system service outside the repository): out of scope, recorded as a warning.
