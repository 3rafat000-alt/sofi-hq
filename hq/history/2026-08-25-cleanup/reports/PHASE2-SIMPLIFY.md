# PHASE2-SIMPLIFY — The Second Simplification Wave & Leads Update Report

> Purpose: documenting the owner's second request («delete, shrink, and order the structure; remove what is unnecessary; simplify the system to be flexible and smooth; and update every room lead on how work operates»).
> Date: 2026-08-25 · this folder moved from the tree root into the archive to keep the root clean.

## What Was Executed

| Action | Detail | Evidence |
|---------|---------|--------|
| moving both operations' reports out of the root | `cleanup-workspace/` now lives here inside the archive | the root now carries only the constitutional structure (12 items exactly) |
| archiving closed audit snapshots | sakk/docs/audits/{w3r1-shots,w4-shots,w5r2-lighthouse} (~1.9MB) with a pointer README left in place | archive fingerprints: 69 matching files |
| archiving remaining transient | training/internet_knowledge/_harvest.log | zero transients in the managed layer |
| **the reference state document** | new: `governance_law/system-state-current.md` — the single updated source for how the system works, explaining any old path | 4 sections: The Map · The Variable · The Constant · Decoding Old Paths |
| **updating 15 room leads** | a «read first» notice under each lead's heading in source `.opencode/agent/` pointing to the state document | grep: 15/15 |
| **updating 15 room charters** | same notice at the top of each charter in governance_law/room_charters | grep: 15/15 |
| regenerating the agent mirror | `node tooling/port-agents.mjs` → OK: 106/106 (count preserved; non-leads exited byte-identical) | script output |
| updating the public identity document | identity/public-readme.md: stale hq/ structure map ← current reality; skills counter 87/99 ← 106; archived-memory status documented | diffs in git |

## Simplification Proposals Deliberately Rejected (and their defense)

| Proposal | Reason for rejection |
|----------|-----------|
| deleting node_modules of both tools (126MB) | live dependencies of the operating tools themselves (`@kilocode/plugin`) — deleting breaks the very table we work on |
| merging memory_index into org_brain | binding law texts command reading the former path literally; two folders of one file each run at zero cost; merging breaks a working flow for cosmetic gain |
| wiping artifacts inside sakk (vendor/dist/node_modules) | dist is what the site serves live right now and vendor runs it — wiping = taking down production (outside «what is unnecessary») |

## State After the Wave

- sakk.local → 200 in ~0.7ms · sakk.zanjour.com → 200 in ~0.9s
- Root: AGENTS.md · governance_law · identity · org_brain · memory_index · projects · caddy · training · tech_templates · tooling · backups(root) + hidden config files
- Tree size: 706MB (excluding .git) — 99% of it sakk and live tools
- git: a safety commit by the owner `d6c1511` appeared mid-wave (a snapshot before the SAKK-DDD program); post-commit diffs = exactly this wave's changes (47 modified + the new state document); no commit recorded by the executor

## Rollback

`bash /home/es3dlll/Desktop/SOFI-archive-20260825-2040/restore.sh <path>` — covers both waves' archives (69 fingerprints).
