# Structure Standard — the canonical structuring standard (v4.5 · the hq pivot + DDD layers)

> **Verdict:** this tree is the only set of true homes. Every file has exactly one humble home — Law 13.
> Last updated: 2026-08-25 · Authority: OWNER-DIRECTIVE M8 + INT-GTW-026 + the documented purge plan

## The canonical tree

```text
SOFI/
├── AGENTS.md · opencode.json        🔒 The constitution and tool configuration
├── identity/                        Public identity (public-readme · system-identity)
├── memory_index/                    Memory pointer (a single primer — the archive lives in hq/brain)
├── hq/                              General HQ ("headquarters"):
│   ├── core/
│   │   ├── domain/                  ★ The DDD domain: rooms/15 (charter·contracts·capabilities·agents capsules)
│   │   │                            shared-kernel · context-map.yaml · SKILLS-ASSIGNMENT.md
│   │   ├── nexus/                   Official registries: registry(106)·gates·routing·personas·pipeline·bus
│   │   ├── standards/ tech_templates/ tooling/ templates/
│   │   ├── design/system-ddd-blueprint.md · structure-standard.md · system-state-current.md
│   │   └── constitution-master · protocols · contracts · constitution_articles/
│   ├── brain/                       Organization memory (archived — primer brain-index.md)
│   ├── engine/                      Live publishing layer: Caddyfile · sites/ · sites-disabled/ · php-fpm/ · scripts/
│   ├── training/                    file-discipline · rooms-guide · internet_knowledge/
│   └── history/                     Timestamped reports of the major operations
├── projects/<slug>/                 Projects — currently sakk (fixed brain convention)
├── caddy → hq/engine                A single symlink: bridge to the live root file /etc/caddy until the next bootstrap
├── .opencode/                       Presentation: agent/106 spec source (Article 00) · skills/106+INDEX
└── .kilo/                           Generated mirror (.kilo/agent via port-agents.mjs) + tool state
```


## Old←New legacy map (a permanent reference for historical records)

| Old (before M8) | New |
|---|---|
| hq/core/* | governance_law/* |
| hq/core/CONSTITUTION.md | constitution-master.md |
| hq/core/PROTOCOLS.md | protocols.md |
| hq/core/CONTRACTS.md | contracts.md |
| hq/core/STRUCTURE.md | this file |
| hq/core/constitution/ | constitution_articles/ |
| hq/core/rooms/X/CHARTER.md | room_charters/X.md |
| hq/core/gates/checklists/ | gate_checklists/ |
| hq/core/nexus/ | nexus/ |
| STACKS·PIPELINE·API-ENVELOPE·DDD·UIUX·KNOWLEDGE-CX·INSTALLER·DEPLOY·DEVOPS·NEXTJS·MCP-REGISTRY | standards/* |
| hq/core/templates/ | 99_templates/ |
| hq/brain/CORTEX·HIPPOCAMPUS·THALAMUS·AMYGDALA·PREFRONTAL·BASAL-GANGLIA·TOOLS·BRAIN·OWNERS "00–08 by their bare names (brain-index…owners-matrix)" |
| hq/training/ | training/ |
| SOFI.md · README.md | identity/ |
| MEMORY.md | memory_index/memory-index.md |
| projects/ · templates/auth-rbac-stack · tools/ | projects · tech_templates · tooling |

> **Historical reading rule:** CORTEX/HIPPOCAMPUS/AMYGDALA entries and HANDOFFS records cite old paths as testimony of their time — they are never edited; interpret them through this table.

## The reserved zone (technical identifiers)

The names of the 106 agents, the 106 skill folders, the five project slugs, and AGENTS.md/opencode.json — operational identifiers that are never renumbered and never localized.

## v3.1 updates (M8-b · INT-GTW-027)

| Event | Detail |
|---|---|
| Absorbing `.agents/` | Its seven skills (banner-design · brand · design · design-system · slides · ui-styling · ui-ux-pro-max) moved into `.opencode/skills/` — the folder was deleted; the total is now **106** |
| Numbering inside the brain | templates→20_brain_templates · HANDOFFS→30_handoffs · org→40_org_lessons · auto-memory→50_auto_memory_archive · state→90_state_runtime |
| Training numbering | internet-knowledge→03_internet_knowledge |
| Deleting `19_scaffolds/` | Dead hq structures (6 READMEs + an old intake wizard) — zero live references |


## v4 (M8-c · INT-GTW-028): removal of ordinal numbering

Owner decision: the ordinal numeric prefixes (01_ · 10_ · 99_) were removed from every folder and file — the explicit English name suffices, and ordering is governed by this standard's map rather than by prefixes.
**Preserved exception:** room numbers (00-boardroom), article numbers (00-operating-system), and gate numbers (gate-0) are **semantic identifiers** inside contract and law texts — they are not ordinals and remain untouched.
The legacy map above was updated to point directly at the final bare names; stage record: M8 numeric → M8-b absorption & cleanup → M8-c abstraction.

## v4.5 (2026-08-25 · the hq pivot + DDD)

| Event | Detail |
|---|---|
| Reviving the pivoted hq/ structure | By owner order: core·brain·engine·training under hq/, followed by bridge removal and migration of every reference (188 files) — one bridge remained: the caddy symlink to the live root file |
| DDD layers | domain/ (15 contexts with their 106 capsules + shared-kernel + context-map.yaml) per design/system-ddd-blueprint.md — skill ownership sits in the room manifests |


## v4.3 (2026-08-25 · the documented purge plan)

| Event | Detail |
|---|---|
| Emptying memories via archival | The content of `org_brain/` and `memory_index/` moved out to `../SOFI-archive-20260825-2040/` — a single primer file remained in each under the same former name (`brain-index.md` · `memory-index.md`) so the constitution's references would not break |
| caddy "sakk only" | The primary became short (snippets + 404 guard + one import), sites in `sites/`, disabled ones relocated to `sites-disabled/`, retired fpm pools in `php-fpm/disabled/` |
| Merging deployment documentation | `caddy/README-LIVE.md` merged into `caddy/OPERATIONS.md` and removed (it mirrored the reality of 2026-08-09) |
| Removing empty and transient items | `prompts/` and `caddy/docs/` (both completely empty) and `.playwright-mcp/` plus the transient rebrand-plan conversion logs |
| Operation archive | `SOFI-archive-20260825-2040/` sibling to the root: sha256 fingerprints + `restore.sh` — reports in `cleanup-workspace/reports/` |
