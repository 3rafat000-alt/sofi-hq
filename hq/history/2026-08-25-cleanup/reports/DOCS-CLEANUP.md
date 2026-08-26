# DOCS-CLEANUP — The Fate of Every Document in the Documentary Cleanup

> Purpose: classifying every document within cleanup scope (governance_law · caddy · projects/sakk/docs): stayed/updated/merged/archived.
> Created: 2026-08-25 · Team: Wave 5b · Method: live reference checks + modification dates + automated orphan-link detection.

## The caddy layer

| Document | Fate | Detail |
|---------|--------|---------|
| `caddy/OPERATIONS.md` | **updated** | restructured to the new sites/ layout, current domain map, corrected paths, and new rollback lines |
| `caddy/README-LIVE.md` | **merged then archived** | reflected the 2026-08-09 reality (single source in /etc · ended tobacco/owais sites). Its valid core (tunnel principle · distribution · troubleshooting) merged into OPERATIONS.md, then removed |
| `caddy/php-fpm/README.md` | **updated** | pool map: active = sakk only; disabled documented with reasons |
| `caddy/cloudflare/CONFIG-OF-RECORD.md` | **stayed** | recent and live — documents the tunnel (secrets outside the repository deliberately) |
| `caddy/brain/*.md` | **updated** | new ADR-002 + updated structure line (project memory is outside memory-cleanup scope — Law 7 pattern) |
| `caddy/site/README.md` | **archived and replaced** | by the newer-instructions `sites/` folder per the 2026-08-25 plan |

## The governance_law layer (binding laws untouched — supporting documents only)

| Document | Fate | Detail |
|---------|--------|---------|
| all laws, standards, charters, gates, and nexus files (60 files) | **stayed** | a coherent, updated living system (M10) — nothing stale or duplicated inside |
| `standards/nextjs-standards-legacy.md` | **stayed** | «suspended for new projects» per R2 but remains an approved retrospective reference for existing projects |
| `structure-standard.md` | **updated** | canonical tree matched to the new reality + change log v4.3 (outside law texts) |

## The projects/sakk/docs layer (source code untouched)

| Item | Fate | Detail |
|--------|--------|---------|
| `rebrand-plan/D01–D10 + RCCF + README + docx/pdf/assets/_core/_followup` | **stayed** | the active rebranding package (August 2025) |
| `api/openapi-v2.yaml` | **stayed** | the frozen contract — protected core |
| `admin/ architecture/ backend/ brand/ design/ guides/ mobile/ strategy/ tickets/ web/ memory/ skills/ audits/ cleanup/` | **stayed** | recent and tied to the living project; internal link check: **zero orphan links** |
| `rebrand-plan/*.log` (9 files) | **archived and removed** | transient conversion logs |

## The Documented Exception (memory references archived inside binding texts)

References to `org_brain/*` in law, protocol, contract, and `.kilo/.opencode` agent texts are **procedural writing targets** in binding texts whose editing is outside this operation's scope. Locked decision 1 emptied the memories while keeping `org_brain/brain-index.md` as an introduction documenting the archive and how to restore or recreate — so these references remain valid as future instructions rather than dead links. Recorded here for transparency, not as failure.
