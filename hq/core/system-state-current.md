# System State Current — the reference operating state (post-purge & simplification)

> **This document is the sole up-to-date source for how the system works now** — any legal text or charter citing an old path is interpreted through it.
> Date: 2026-08-25 · Authority: two consecutive owner directives (the purge plan, then the simplification wave) · Full archive: `/home/es3dlll/Desktop/SOFI-archive-20260825-2040/`

> **⚡ Binding state 2026-09-05 (R3.1 + Phase B):** the system runs **14 rooms · 109 agents · 111 skills**. The Data room (08) was merged into Architecture (04) — its agents now live as `arc-*` and extra capsules were archived to `hq/core/archive/r3.1-reconciliation/`. Historical amendment notes below (§2) quoting older counts (15 rooms · 114 agents · 109 skills) are **kept as history** (Law 13 continuity) — the derived counts above are the binding reality; they are guarded by `hq/core/tooling/registry_guard.py` + `count_sync.py`.

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
└── .opencode/             Source of the 109 agents and 111 skills (operating layer · gate-0 guarded by hq/core/tooling/registry_guard.py + count_sync.py)
```

**The one remaining bridge — REMOVED 2026-08-31 (9-axis fix Axis 2: hq/core/tooling/evidence_guard.py + hq/engine/scripts/bootstrap-live.sh):**
- `caddy → hq/engine` symlink **deleted** — verified `ls -l /home/es3dlll/Desktop/SOFI/caddy` = not found (exit 0). Canon lives at `hq/engine/Caddyfile` and is imported directly by `/etc/caddy/Caddyfile` via `sudo bash hq/engine/scripts/bootstrap-live.sh` (single privileged write). All later deploys use `bash hq/engine/scripts/deploy.sh` via Caddy admin API **without sudo** (least-privilege, Axis 6). Legacy symlink path kept in `hq/core/structure-standard.md` legacy map only as historical record — never recreate.
- Evidence: hq/engine/scripts/bootstrap-live.sh:12 (least-privilege guard + symlink removal check) · hq/engine/scripts/validate.sh:1 (read-only, unprivileged) · hq/engine/scripts/deploy.sh:7 (admin-API first, sudo fallback).

## 2) What changed and how things work from now on

| Axis | New binding state |
|--------|------------------------|
| **Organization memories** | Content of `hq/brain/` and `memory_index/` archived with sha256 fingerprints; a single primer file remains in each explaining retrieval. Recording a new decision = recreate the target file under the same name (the same pattern as after the M10 reset) or first restore the old one via `restore.sh` |
| **Project memories** | `projects/<slug>/brain/` untouched and remains the fixed working pattern (CONTEXT · DECISIONS · HANDOFFS · LESSONS) |
| **Publishing layer** | `hq/engine/Caddyfile` (canon, imported directly by `/etc/caddy/Caddyfile`) is a short primary (snippets + 404 guard + one import) · every domain = a file `hq/engine/sites/<domain>.caddy` · adding a domain = create file → `bash hq/engine/scripts/validate.sh` (read-only, no sudo) → `bash hq/engine/scripts/deploy.sh` (admin-API reload, sudo only as fallback) · disabled sites: `hq/engine/sites-disabled/` · retired fpm pools: `hq/engine/php-fpm/disabled/` · Isolated alternative: `ops-sandbox-executor` can validate inside container (no host sudo) |
| **Active domain** | sakk only (`sakk.local` + `sakk.zanjour.com`); every other host answers the 404 guard |
| **Reports of the two operations** | Moved to `<archive>/cleanup-workspace/reports/` — full detail in `FINAL-REPORT.md` and `PHASE2-SIMPLIFY.md` there |
| **Rolling anything back** | `bash /home/es3dlll/Desktop/SOFI-archive-20260825-2040/restore.sh <original-path>` |

## 3) What did not change at all (keep working on it as usual)

The constitution AGENTS.md and its laws (16 as of 2026-08-26 — Laws 14–16 added by owner order) · protocols, contracts, gates, and the nexus · the 14 rooms and their **109 agents** (source `.opencode/agent/`, generation via `node hq/core/tooling/port-agents.mjs` + guarded by `hq/core/tooling/registry_guard.py`) · the 111 skills on disk (guarded by `hq/core/tooling/count_sync.py` — WARN-active until the INDEX stamp is reconciled) · the S1–S6 production line and the design-before-code rule · evidence discipline (`file:line` · exit code · `hq/core/tooling/evidence_guard.py` Law 4) · Law 10 (working directly on the main tree, no worktrees).

> **Amendment 2026-08-26 — six operational gaps closed (owner order):** +3 agents (`str-agile-orchestrator` flow/WIP tracking in 01 · `ops-sandbox-executor` container build gate in 11 · `sec-license-auditor` license/IP merge gate in 09) · Laws 14–16 (double-rejection arbitration · license gate · smart clarification loop ≥20%) · shift-left rules in charters 01+04 · Hard Rule #11 + mandatory `License-check` task-card field in `tech_templates/ddd-capsule-protocol.md`. Full record: `hq/history/2026-08-26-operational-gaps/`.

> **Amendment 2026-08-26 (2) — priority & cadence package (owner order):** room priority tiers and work-order map `nexus/room-priority.yaml` (T0 spine → T1 paper → T2 code → T3 shield → T4 memory, with escalation priority) · reporting rhythm `standards/reporting-cadence.md` (Daily Ops Digest / Weekly Performance Review / Monthly Organizational Report) · KPI & alert-threshold catalog `standards/kpi-thresholds.md` (K1–K17, hard rules K6/K11/K14/K16/K17 block Gate-8) · consolidated incident runbooks `runbooks/incident-response.md` (R1–R4 implementing Protocol 10; satisfies gate-8 1:1 alert↔runbook) · privacy shift-left rule wired into charter 03 (`dat-privacy-officer` signs the DFR). No agent-count change — still 15 rooms · 109 agents. Origin: owner's gap-analysis of an external rebuild prompt (verdict: analyze-and-adopt, never rebuild — system law prevails).

> **Amendment 2026-08-26 (3) — core-five rooms package (owner order, enhanced variant):** +2 agents in room 04 — `arc-security-architect` (secure-architecture design at S2/S3: authn/authz flows, encryption strategy, Zero-Trust segmentation) and `arc-performance-architect` (performance-by-design: caching strategy, load paths, SLO budgets) — registry now **15 rooms · 111 agents** · scope extensions instead of duplicate agents (verified against existing rosters): `dsn-motion-designer` also owns interaction-behavior design (charter 03) · `mob-state-engineer` owns state architecture for the whole merged S5 Flutter/Dart team (charter 07) · builder-test-authorship rules wired into charters 05+07 (tests authored by the building engineer, verified by room 10 — no test-engineer duplication) · 4 consultation rows added to `domain/communication-matrix.md` (research-data flow, endpoint security design, performance-budget handoff, mobile design fit). Rejected as stale: "React vs Vue conflict" (already resolved by R2/DEC-0013 — stacks-tech.md §React is legacy-only). Origin: external Qwen analysis of rooms 03–07, verified item-by-item then adopted in enhanced form.

> **Amendment 2026-08-26 (4) — visual research & feeding system (owner order, literal variant):** Protocol 18 added to `protocols.md` (P-18.1 research-before-design · P-18.2 mandatory pattern documentation in `projects/<slug>/brain/visual-patterns/` · P-18.3 no verbatim copying = L3 · P-18.4 design-system integration via `dsn-design-system-gen` + uiux-standard update · P-18.5 refresh every 40 turns) · +3 agents — `res-visual-pattern-scout` in room 02 (Karam Al-Sayed), `dsn-competitive-ui-analyst` + `dsn-arabic-ux-specialist` in room 03 (Rania Al-Maarri · Layla Al-Homsi; RTL signature gates DFR) — registry now **15 rooms · 114 agents** · +3 skills with ownership deeds and room-manifest entries (`mobbin-scraper` 02 · `design-system-extractor` + `rtl-mirror-validator` 03) · binding platform list appended to `standards/uiux-standard.md §Visual Inspiration Sources`. Owner chose literal adoption after duplication warnings were documented (overlaps noted vs res-web-scout/res-competitor-analyst/res-web-scrape/design-system skills).

> **Verdict 2026-08-26 (5) — external "15-room comprehensive audit" REJECTED & archived (owner order):** a Qwen-sourced audit proposing +35 agents/skills/protocols was verified item-by-item against live state and rejected: already-implemented overlaps (architects · visual system · KPIs · escalation behavior), items the owner had explicitly rejected hours earlier (test/state duplicates), stale conflicts (React/Vue — resolved by R2), and off-stack speculative hires (Kubernetes/IaC/vector-DB/streaming/AR-VR vs locked Laravel+Flutter+Caddy stack). Full record: `hq/history/2026-08-26-rooms-audit-verdict.md`. Zero changes applied; genuine micro-gaps parked as backlog.

> **Amendment 2026-08-26 (6) — unified DoD & execution-rules reference (owner order, enhanced-consolidation):** `standards/room-dod-and-execution-rules.md` created as a DERIVATIVE reference (explicitly subordinate — auto-void on any conflict with constitution/protocols/KPIs/gates/charters). Contents: unified per-room Definition-of-Done matrix (Gateway → Knowledge, aligned with gates 0–8 + charters + K15 ≥90%) + three binding micro-rules: dependency-aware parallelism (str-agile-orchestrator WIP enforcement), specific-rejection rule (rejections must cite file:line + violated criterion + fix direction; vague rejection = L1 for the rejecting Lead), and Law-14 double-rejection freeze restated. Origin: external Qwen "execution constitution" draft adopted after correcting five factual errors (stale counts 17 protocols/106 skills · hallucinated tool "OrangePro" removed · coverage 80%→aligned K15 90% · self-claimed Level-4 constitutional precedence stripped).

> **Amendment 2026-08-31 (7) — 9-axis radical fix (owner order — fateful, full evidence):** closes the six operational gaps + three architectural gaps identified by the 9-axis audit (2026-08-31). **Axis 1 (Law 12):** Gate-0 now machine-guarded by `hq/core/tooling/registry_guard.py:1` + `hq/core/tooling/count_sync.py:1` + `node hq/core/tooling/port-agents.mjs:6` (15 rooms · 114 agents · capsules 1:1 vs `.opencode/agent`). **Axis 2 (Law 13):** legacy symlink `caddy → hq/engine` deleted (verified `ls -l caddy` = not found) — canon at `hq/engine/Caddyfile` directly imported by `/etc/caddy/Caddyfile` via `hq/engine/scripts/bootstrap-live.sh:6`. **Axis 3+4 (Law 1/16):** P-01.10 timeout 24h + anti-paralysis (max 2 rounds) added to `hq/core/protocols.md:28` and `hq/core/domain/rooms/14-gateway/charter.md:85` + `.opencode/agent/gtw-intake-reformer.md:252`; Fast Track fully delegated to Room Lead with weekly post-audit by `gtw-dispatcher` (P-01.8). **Axis 5+7 (Law 4/13 + P-08.1):** `hq/core/tooling/evidence_guard.py:1` (0 broken on hq/core) + `hq/core/tooling/hooks/pre-commit:1` (gitleaks git --staged --pre-commit) + `hq/core/tooling/hooks/install.sh:1` + `gitleaks.toml:1` — pre-commit blocks secrets/file:line drift/registry drift. **Axis 8 (P-06.7):** `hq/core/tooling/memory_summarizer.py:1` ritual via `knw-reflector` (hippocampus >800 / amygdala >600 → keep last 5 full + summarize older) + charter `hq/core/domain/rooms/13-knowledge/charter.md:86`. **Axis 9 (Law 4/13):** `hq/core/gate_checklists/gate-6.md:26` (law13 + evidence on hq/core) + charter `hq/core/domain/rooms/13-knowledge/charter.md:91` + `.opencode/skills/INDEX.md:4` (106/106 → 109/109). All on main tree only (Law 10) — evidence: registry_guard exit 0 · count_sync exit 0 · evidence_guard hq/core exit 0 · gitleaks no leaks exit 0 · validate.sh exit 0 · pre-commit PASS exit 0. Full record: `hq/brain/cortex-decisions.md:ADR-20260831-9AXIS-FIX` + `hq/brain/hippocampus-sessions.md:SES-20260831-9AXIS-FIX`.


## 5) DDD layers (approved and active — 2026-08-25)

Governing blueprint: `hq/core/design/system-ddd-blueprint.md` · contract map: `hq/core/domain/context-map.yaml`

| Layer | Its home |
|--------|-------|
| Domain | `hq/core/domain/`: shared-kernel · rooms/14 (charter+contracts+capabilities+agents as capsules) |
| Application | The intake gateway, RCCF, the gates, and the ticket bus (nexus + protocols) — matures gradually under `hq/core/application/` |
| Infrastructure | `hq/engine` + `tooling` + `training` + the memory stores and the archive |
| Presentation | `.opencode/agent` (the legal spec source — Article 00) + the generated mirror `.kilo/agent` |

**Capsule rule:** every agent = `domain/rooms/<room>/agents/<name>/{agent.md→link to source, senses.yaml, memory.md, capabilities.yaml}` — its capabilities by name ⊆ its own room's manifests, and the checker fails on any leakage.
**Skill ownership:** the room manifests are the binding registry (`SKILLS-ASSIGNMENT.md` documents the assignment deeds of the 109); the skills index (`.opencode/skills/INDEX.md` 109/109) serves invocation and description. Gate-0 machine guards: `hq/core/tooling/registry_guard.py` + `hq/core/tooling/count_sync.py` + `hq/core/tooling/evidence_guard.py`.

## 4) The rule for decoding old paths

Any path appearing in old texts (hq/core · hq/brain · projects/caddy · caddy/site · prompts · .playwright-mcp · tobacco-center · shamestate · sofi-shop): consult the legacy map in `structure-standard.md` and its v4.3 table there; if you cannot find it, it is in the archive above — never recreate it without a ticket.
