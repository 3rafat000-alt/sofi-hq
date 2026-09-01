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

## v4.6 (2026-08-29 · SOFI bus moved to the root — opencode MCP bridge)

Owner order: the SOFI bus must live in the SOFI root, not inside projects, and agents use it inside opencode as an MCP server.

| Event | Detail |
|---|---|
| Moving the MCP server to the root | `hq/engine/mcp-server/*` + `projects/mcp-server/*` consolidated into **`mcp-server/`** (root) — services, contracts, design, docs, brain all in one home |
| Permanent old←new map | `hq/engine/mcp-server/…` → `mcp-server/…` · `projects/mcp-server/…` → `mcp-server/…` · package import `hq.engine.mcp_server` still resolves via symlink `hq/engine/mcp_server → ../../mcp-server` (Law 12 registry untouched) |
| systemd | unit regenerated by `mcp-server/install-service.sh` — WorkingDirectory/ExecStart/EnvironmentFile/logs → root `mcp-server/`; service healthy after restart |
| opencode MCP bridge | `mcp-server/mcp_bridge/server.py` registered in `opencode.json` as MCP `SOFI` (stdio) — 9 tools: sofi_org_structure · sofi_who_is · sofi_health · sofi_send · sofi_ticket · sofi_clarify · sofi_escalate · sofi_tickets · sofi_audit |
| Agent files | `<!-- SOFI-BUS-MCP-v1 -->` block appended after `<!-- MCP-FLEET-v3 -->` in all 114 `.opencode/agent/*.md` |
| Evidence paths in live code | `main.py` / `agents_mcp.py` / `leads_mcp.py` audit evidence strings updated to `mcp-server/…` (they generate new records; historical records in hq/brain never edited — Law 13) |

## v4.7 (2026-08-29 · المجلد في المحرك — governance channels · owner directive)

Owner order: "لازم يكون المجلد في المحرك engine" — the SOFI bus folder moves INTO the engine, plus Board consultation (Law 6) and room-meetings channels.

| Event | Detail |
|---|---|
| Moving the MCP server into the engine | root `mcp-server/` → **`hq/engine/mcp-server/`** — services, contracts, design, docs, brain, data all inside the engine (still under the SOFI root; not inside projects) |
| Permanent old←new map (v4.7) | `mcp-server/…` → `hq/engine/mcp-server/…` · package import `hq.engine.mcp_server` now resolves via symlink `hq/engine/mcp_server → mcp-server` (relative, inside engine) |
| systemd | unit regenerated by `hq/engine/mcp-server/install-service.sh` — WorkingDirectory/ExecStart/EnvironmentFile/ReadWritePaths/logs → `hq/engine/mcp-server/`; service healthy after restart |
| opencode MCP bridge | `opencode.json` SOFI command → `hq/engine/mcp-server/mcp_bridge/server.py` — now **13 tools** (+ sofi_consult · sofi_meeting_new · sofi_meetings · sofi_meeting_minutes) |
| Governance channels (Law 6 + اجتماع الغرف) | `POST /api/v1/consult` (consultation_request ticket) · `POST/GET /api/v1/meetings` · `POST /api/v1/meetings/{id}/minutes` (decisions → CORTEX) — new `meetings.py` + `meetings.db`; contract openapi.yaml now 13 endpoints; tests `test_governance.py` (4) — unified API-key so integration + governance run together 18/18 |
| Boardroom lead fix | bridge `sofi_who_is` now reports `brd-ceo` as boardroom lead (registry 00-boardroom has no `lead` key — AGENTS.md table) — `brd-lead` fabricated lead removed |
| Agent files | `<!-- SOFI-BUS-MCP-v2 -->` block (governance tools added) in all 114 `.opencode/agent/*.md` · annex template v1.2 · standard `hq/core/standards/room-meetings-standard.md` added |
| Evidence paths in live code | evidence strings in `hq/engine/mcp-server/*.py` → `hq/engine/mcp-server/…` (generated records; historical records in hq/brain never edited — Law 13) |

## v4.8 (2026-08-29 · لا تكرار — حذف الـ symlink نهائياً · owner directive)

Owner order: "احذف مجلد الـ link بس الاساسي لا تكرار" — the duplicated link folder is deleted; the ONE real folder becomes the Python package itself (no import shim).

| Event | Detail |
|---|---|
| Permanent old←new map (v4.8) | root `mcp-server/` → `hq/engine/mcp-server/` → **`hq/engine/mcp_server/`** (underscore = real package dir, no link) · **symlink `hq/engine/mcp_server → mcp-server` DELETED forever** — `find hq/engine -type l` = 0 |
| Why the rename (`-` → `_`) | Python imports need a valid identifier; the package is now the real folder `hq/engine/mcp_server/` (`__init__.py` existing) — imports `hq.engine.mcp_server.*` work natively WITHOUT any symlink: verified `from hq.engine.mcp_server.config import ROOMS` (15) with `find hq/engine -maxdepth 1 -type l` = 0 |
| System scripts cleaned | `start-prod.sh` · `run.sh` · `install-service.sh` — symlink-creation blocks REMOVED; paths → `hq/engine/mcp_server/`; systemd regenerated; service healthy after restart (health OK, v1.0.0) |
| Schema path fix | `ticket_bus.init_db()` now resolves `contracts/schema.sql` in-package (legacy `projects/mcp-server` fallback removed) |
| References updated | `opencode.json` · `hq/core/standards/mcp-communication-standard.md` · `room-meetings-standard.md` · `MCP_PROTOCOL_BINDING.md` · `mcp-agent-annex.md` · `.opencode/command/sofi-all.md` · all in-folder docs/scripts/evidence strings |
| Gateway lead fix | bridge `_room_lead()` now returns `gtw-dispatcher` for room 14 (registry) — `gtw-lead` fabricated lead removed (boardroom brd-ceo kept) → acquaintance test 15/15 leads |
| Acquaintance test (اختبار تعارف) | `sofi_who_is` roll-call over all official registry ids: **114/114 introduced successfully** · room match vs registry **114/114** · per-room counts exact (7·8·8·10·9·8·8·6·7·9·7·8·6·6·7) · no agent without lead · leads 15/15 · bridge tools 13/13 — record: `hq/engine/mcp_server/docs/acquaintance-test.md` |
| Tests | `test_governance.py` + `test_integration_api.py` together **18/18 passed** from the real package (no link) — full suite 31 passed + 3 known flaky (environmental, each file passes alone) |
| History untouched | `hq/brain/*` append-only (Law 13) · v4.6/v4.7 sections preserved above as historical fact |

## v4.9 (2026-09-01 · حذف جسر SOFI MCP نهائياً — O-01)

Owner order: احذف `🛰️ SOFI local hq/engine/mcp_server/mcp_bridge/server.py 00 Boardroom / brd-ceo — any` بالكامل وكل شيء له.

| Event | Detail |
|---|---|
| حذف الجسر | `hq/engine/mcp_server/mcp_bridge/` (مجلد + `server.py` + `__init__.py`) حُذف نهائياً — `rm -rf` exit 0 |
| `opencode.json` | حذف كتلة `mcp.SOFI` (8→28 خادم) — `python3 -m json.tool opencode.json` → Valid exit 0 |
| `hq/core/nexus/mcp-routing.yaml` | حذف سطر `SOFI: {room: "00"...}` — الأصلية 9→8 — المصدر 29→28 خادم — header محدّث |
| `hq/training/mcp-platform-guide.md` | حذف صف `SOFI (الجسر)` — 29→28 — تحديث كل الإشارات + header |
| `hq/engine/mcp_server/docs/opencode-bridge.md` | حُذف نهائياً (وثيقة الجسر) |
| `hq/engine/mcp_server/AGENT_GUIDE.md` | حذف قسم 0.7 (أدوات SOFI MCP) — استبدال بتنبيه الحذف + SDK مباشر |
| `hq/core/templates/mcp-agent-annex.md` | إزالة إشارة `mcp_bridge/server.py` — تحديث القناة إلى SDK فقط |
| `hq/core/standards/room-meetings-standard.md` | إزالة `mcp_bridge/server.py` من Evidence |
| Agent files | إزالة بلوك `<!-- SOFI-BUS-MCP-v2 -->` (5 أسطر + 🛰️) من **114** ملف `.opencode/agent/*.md` + `.kilo/agent` — `grep SOFI-BUS-MCP` → 0 |
| التوثيق التاريخي | أقسام v4.6/v4.7/v4.8 محفوظة كسجل تاريخي (Law 13) — لم تُحرر |
| الحالة | لا بقايا `mcp_bridge` كـ MCP فعال — الحافلة `hq/engine/mcp_server` نفسها باقية كخدمة HTTP/WS `mcp.local:8765` (main.py/ticket_bus.py) — الجسر الـ stdio فقط هو المحذوف |
