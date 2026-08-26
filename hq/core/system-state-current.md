# System State Current — the reference operating state (post-purge & simplification)

> **This document is the sole up-to-date source for how the system works now** — any legal text or charter citing an old path is interpreted through it.
> Date: 2026-08-25 · Authority: two consecutive owner directives (the purge plan, then the simplification wave) · Full archive: `/home/es3dlll/Desktop/SOFI-archive-20260825-2040/`

## 1) The final root map (the hq pivot — owner directive 2026-08-25)

```
SOFI/
├── AGENTS.md              The constitution — as-is, untouched
├── opencode.json · .gitignore · .git
├── identity/              System identity (sofi-system-identity · public-readme)
├── memory_index/          A single primer memory-index.md — memory fully archived
├── hq/                    General HQ ("headquarters"):
│   ├── core/              All governance: mother constitution · protocols · contracts · charters
│   │   │                  · gates · nexus · standards + tech_templates + tooling
│   ├── brain/             Organization memory (archived — primer brain-index.md)
│   ├── engine/            Live publishing layer (formerly caddy/): Caddyfile · sites/
│   │                      · sites-disabled/ · php-fpm/ · scripts/ · cloudflare/ · brain/
│   └── hq/training/          Training guides (rooms-guide · file-discipline · internet_knowledge)
├── projects/sakk/         The only active project — its memories in projects/sakk/brain/ are intact
└── .opencode/             Source of the 109 agents and the skills (operating layer)
```

**The one remaining bridge (until the next root bootstrap):**
- `caddy → hq/engine` symlink on the root because `/etc/caddy/Caddyfile` (the root file) imports `SOFI/caddy/Caddyfile` literally. Final removal: `sudo bash hq/engine/scripts/bootstrap-live.sh` then `rm caddy`.

## 2) What changed and how things work from now on

| Axis | New binding state |
|--------|------------------------|
| **Organization memories** | Content of `hq/brain/` and `memory_index/` archived with sha256 fingerprints; a single primer file remains in each explaining retrieval. Recording a new decision = recreate the target file under the same name (the same pattern as after the M10 reset) or first restore the old one via `restore.sh` |
| **Project memories** | `projects/<slug>/brain/` untouched and remains the fixed working pattern (CONTEXT · DECISIONS · HANDOFFS · LESSONS) |
| **Publishing layer** | `hq/engine/Caddyfile` (reached live through the caddy/ link) is a short primary (snippets + 404 guard + one import) · every domain = a file `hq/engine/sites/<domain>.caddy` · adding a domain = create the file → `bash hq/engine/scripts/validate.sh` → `bash hq/engine/scripts/deploy.sh` · disabled sites live in `hq/engine/sites-disabled/`, retired fpm pools in `hq/engine/php-fpm/disabled/` |
| **Active domain** | sakk only (`sakk.local` + `sakk.zanjour.com`); every other host answers the 404 guard |
| **Reports of the two operations** | Moved to `<archive>/cleanup-workspace/reports/` — full detail in `FINAL-REPORT.md` and `PHASE2-SIMPLIFY.md` there |
| **Rolling anything back** | `bash /home/es3dlll/Desktop/SOFI-archive-20260825-2040/restore.sh <original-path>` |

## 3) What did not change at all (keep working on it as usual)

The constitution AGENTS.md and its laws (16 as of 2026-08-26 — Laws 14–16 added by owner order) · protocols, contracts, gates, and the nexus · the 15 rooms and their 109 agents (source `.opencode/agent/`, generation via `node hq/core/tooling/port-agents.mjs`) · the `.opencode/skills/` skills · the S1–S6 production line and the design-before-code rule · evidence discipline (file:line · exit code) · Law 10 (working directly on the main tree, no worktrees).

> **Amendment 2026-08-26 — six operational gaps closed (owner order):** +3 agents (`str-agile-orchestrator` flow/WIP tracking in 01 · `ops-sandbox-executor` container build gate in 11 · `sec-license-auditor` license/IP merge gate in 09) · Laws 14–16 (double-rejection arbitration · license gate · smart clarification loop ≥20%) · shift-left rules in charters 01+04 · Hard Rule #11 + mandatory `License-check` task-card field in `tech_templates/ddd-capsule-protocol.md`. Full record: `hq/history/2026-08-26-operational-gaps/`.

> **Amendment 2026-08-26 (2) — priority & cadence package (owner order):** room priority tiers and work-order map `nexus/room-priority.yaml` (T0 spine → T1 paper → T2 code → T3 shield → T4 memory, with escalation priority) · reporting rhythm `standards/reporting-cadence.md` (Daily Ops Digest / Weekly Performance Review / Monthly Organizational Report) · KPI & alert-threshold catalog `standards/kpi-thresholds.md` (K1–K17, hard rules K6/K11/K14/K16/K17 block Gate-8) · consolidated incident runbooks `runbooks/incident-response.md` (R1–R4 implementing Protocol 10; satisfies gate-8 1:1 alert↔runbook) · privacy shift-left rule wired into charter 03 (`dat-privacy-officer` signs the DFR). No agent-count change — still 15 rooms · 109 agents. Origin: owner's gap-analysis of an external rebuild prompt (verdict: analyze-and-adopt, never rebuild — system law prevails).

> **Amendment 2026-08-26 (3) — core-five rooms package (owner order, enhanced variant):** +2 agents in room 04 — `arc-security-architect` (secure-architecture design at S2/S3: authn/authz flows, encryption strategy, Zero-Trust segmentation) and `arc-performance-architect` (performance-by-design: caching strategy, load paths, SLO budgets) — registry now **15 rooms · 111 agents** · scope extensions instead of duplicate agents (verified against existing rosters): `dsn-motion-designer` also owns interaction-behavior design (charter 03) · `mob-state-engineer` owns state architecture for the whole merged S5 Flutter/Dart team (charter 07) · builder-test-authorship rules wired into charters 05+07 (tests authored by the building engineer, verified by room 10 — no test-engineer duplication) · 4 consultation rows added to `domain/communication-matrix.md` (research-data flow, endpoint security design, performance-budget handoff, mobile design fit). Rejected as stale: "React vs Vue conflict" (already resolved by R2/DEC-0013 — stacks-tech.md §React is legacy-only). Origin: external Qwen analysis of rooms 03–07, verified item-by-item then adopted in enhanced form.

> **Amendment 2026-08-26 (4) — visual research & feeding system (owner order, literal variant):** Protocol 18 added to `protocols.md` (P-18.1 research-before-design · P-18.2 mandatory pattern documentation in `projects/<slug>/brain/visual-patterns/` · P-18.3 no verbatim copying = L3 · P-18.4 design-system integration via `dsn-design-system-gen` + uiux-standard update · P-18.5 refresh every 40 turns) · +3 agents — `res-visual-pattern-scout` in room 02 (Karam Al-Sayed), `dsn-competitive-ui-analyst` + `dsn-arabic-ux-specialist` in room 03 (Rania Al-Maarri · Layla Al-Homsi; RTL signature gates DFR) — registry now **15 rooms · 114 agents** · +3 skills with ownership deeds and room-manifest entries (`mobbin-scraper` 02 · `design-system-extractor` + `rtl-mirror-validator` 03) · binding platform list appended to `standards/uiux-standard.md §Visual Inspiration Sources`. Owner chose literal adoption after duplication warnings were documented (overlaps noted vs res-web-scout/res-competitor-analyst/res-web-scrape/design-system skills).


## 5) DDD layers (approved and active — 2026-08-25)

Governing blueprint: `hq/core/design/system-ddd-blueprint.md` · contract map: `hq/core/domain/context-map.yaml`

| Layer | Its home |
|--------|-------|
| Domain | `hq/core/domain/`: shared-kernel · rooms/15 (charter+contracts+capabilities+agents as capsules) |
| Application | The intake gateway, RCCF, the gates, and the ticket bus (nexus + protocols) — matures gradually under `hq/core/application/` |
| Infrastructure | `hq/engine` + `tooling` + `training` + the memory stores and the archive |
| Presentation | `.opencode/agent` (the legal spec source — Article 00) + the generated mirror `.kilo/agent` |

**Capsule rule:** every agent = `domain/rooms/<room>/agents/<name>/{agent.md→link to source, senses.yaml, memory.md, capabilities.yaml}` — its capabilities by name ⊆ its own room's manifests, and the checker fails on any leakage.
**Skill ownership:** the room manifests are the binding registry (`SKILLS-ASSIGNMENT.md` documents the assignment deeds of the 106); the skills index serves invocation and description.

## 4) The rule for decoding old paths

Any path appearing in old texts (hq/core · hq/brain · projects/caddy · caddy/site · prompts · .playwright-mcp · tobacco-center · shamestate · sofi-shop): consult the legacy map in `structure-standard.md` and its v4.3 table there; if you cannot find it, it is in the archive above — never recreate it without a ticket.
