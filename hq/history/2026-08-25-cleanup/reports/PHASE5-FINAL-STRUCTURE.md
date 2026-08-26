# PHASE5-FINAL-STRUCTURE — Final Cleanup & Precision Structuring

> Date: 2026-08-25 · by owner order («clean the system entirely of duplication and random elements»)

## Delivered
| Action | Detail | Evidence |
|---------|---------|--------|
| removing the three root bridges | governance_law/org_brain/training links removed after migrating 188 files to the new paths (hq/core · hq/brain · hq/training) | closing sweep: zero old references outside protected history records |
| consolidating «caddy» to one home | the root caddy/ folder became a single link → hq/engine (the live /etc chain works through it); full removal by one documented root command recorded in system-state | caddy validate via the link ✓ |
| a home for operation reports | cleanup-workspace moved from the archive into `hq/history/2026-08-25-cleanup/` with a README index | the folder complete with its 11 reports |
| renewing AGENTS.md | the same binding content verbatim in cleaner presentation with today's paths (by explicit owner permission) | comparison of items: 13 laws+levels+rooms+boot+v2 line |
| renewing opencode.json | logical ordering into sections; removed a disabled server (Crawl4AI) | config_validation: success |
| renewing both presentation layers | new .opencode/README and .kilo/README explaining «what is generated and what is its source» + removing empty worktrees | the files |
| fixing the migration tool | port-agents.mjs pointed at the removed bridge — fixed to hq/core/nexus | OK: 106/106 |

## Closing Checks
validate exit0 · sakk local and public 200×3 consecutive (transient tunnel-network flakiness already documented in the cloudflared log) · jw.local → 404 guard · porter 106/106 · AGENTS free of old paths · the only remaining references = the protected historical legacy table in structure-standard.md

## The Single Remaining Root Step (optional)
`sudo bash hq/engine/scripts/bootstrap-live.sh && rm caddy` — makes /etc point directly at hq/engine and removes the last link.
