# Security Gate — Approval of the Removals List (step 5)

> The last freely reversible threshold before the first actual deletion. Everything below is fully archived in:
> `/home/es3dlll/Desktop/SOFI-archive-20260825-2040` (fingerprints: checksums.txt · restore: restore.sh).

## The Abbreviated List Presented for Approval (path + reason)
1. `org_brain/**` except `brain-index.md` — emptying organization memory via archiving (locked decision 1).
2. `memory_index/memory-index.md` current content — same logic; the file remains as an introduction under the same name.
3. `.playwright-mcp/**` — transient browser-test session leftovers.
4. `prompts/` and `caddy/docs/` — two completely empty folders (zero files).
5. `caddy/site/README.md` — replaced by the new `sites/` folder per W7.
6. the five non-sakk PHP-FPM pools — disabled by moving into `php-fpm/disabled/`.
7. non-sakk Caddy host blocks — disabled by verbatim move into `sites-disabled/` (locked decision 2).
8. nine transient `.log` files inside `projects/sakk/docs/rebrand-plan/`.

## Approval Line
**Approved** — on 2026-08-25 at 20:42, delegated by the owner through direct execution of the plan file
(`.kilo/plans/1787677024434-sofi-cleanup-caddy-docs-plan.md`) which stipulates handover to the executing agent «without any further questions»,
and per the «don't ask — assume and document» rule documented in project memory. Every item is instantly reversible via `restore.sh`.
