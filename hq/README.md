# `hq/` — The Headquarters

> The **headquarters** of SOFI HQ. This directory is the **constitution + runtime** of the
> organization. Every byte here is governed by `AGENTS.md:1` and audited by the 4 constitutional
> guards. You are inside the HQ.

The `hq/` directory is the **operational core** of SOFI HQ. It contains the constitution
(`core/`), the memory (`brain/`), the engine (`engine/`), and the training guides. The 17 rooms
are defined in `core/nexus/registry.yaml` and materialized as capsules in `core/domain/rooms/`.

---

## Layout

```
hq/
├── README.md                       ← you are here
├── core/                           ← the constitution material (see hq/core/README.md)
│   ├── protocols.md                ← 17 protocols (P-01..P-20)
│   ├── contracts.md                ← 10 cross-room contracts
│   ├── nexus/                      ← 17 rooms · 121 agents (Law 12)
│   ├── domain/                     ← DDD context-map + 17 rooms
│   ├── standards/                  ← 22 binding standards
│   ├── gate_checklists/            ← G0..G8 + DFR
│   ├── design/                     ← Mermaid diagrams
│   ├── tooling/                    ← 4 guards + pre-commit
│   ├── archive/                    ← historical (Law 13.5)
│   └── ...
├── brain/                          ← organization memory (CORTEX + HIPPOCAMPUS + AMYGDALA)
│   ├── README.md
│   ├── cortex-decisions.md         ← ADR log
│   ├── hippocampus-sessions.md     ← session log
│   ├── amygdala-incidents.md       ← incident log
│   └── evidence/                   ← snapshot files
├── engine/                         ← live publishing layer (Caddy + PHP-FPM + n8n + MCP)
│   ├── README.md
│   ├── Caddyfile
│   ├── sites/
│   ├── php-fpm/
│   ├── scripts/
│   ├── n8n/
│   ├── mcp_server/
│   ├── brain/
│   └── cloudflare/
└── training/                       ← file-discipline + rooms-guide
```

---

## The 3 pillars of HQ

| Pillar | Directory | Purpose | Owner |
|--------|-----------|---------|-------|
| **Constitution** | `core/` | The law of the organization (16 laws + 17 protocols + 10 contracts + 22 standards + 17 rooms) | `brd-ceo` |
| **Memory** | `brain/` | The institutional memory (CORTEX + HIPPOCAMPUS + AMYGDALA) | `knw-lead` |
| **Engine** | `engine/` | The runtime that serves the live project (Caddy + PHP-FPM + n8n + MCP) | `ops-lead` |

---

## How to navigate HQ

**First-time visitors:**
1. Read `core/README.md` — start with the constitution
2. Read `core/SOFI-QUICK-REFERENCE.md` — 1-page map
3. Read `core/system-state-current.md` — binding state
4. Read `brain/README.md` — CORTEX decisions + sessions
5. Read `engine/README.md` — live publishing layer

**Editors:**
- Every edit must be `file:line`-cited (Law 4)
- Every new file must have `## FILE: <path>` header (Law 13.3)
- Every change must pass the 4 guards (Law 12)
- Any change to `core/protocols.md` / `core/contracts.md` / `AGENTS.md` requires `brd-ceo` approval

---

## The 17 rooms (where they live)

> Source: `core/nexus/registry.yaml:1` + `core/domain/rooms/<room>/charter.md`.

| # | Room | Directory | Tier |
|---|------|-----------|------|
| 00 | Boardroom | `core/domain/rooms/00-boardroom/` | T0 |
| 14 | Gateway | `core/domain/rooms/14-gateway/` | T0 |
| 01 | Strategy | `core/domain/rooms/01-strategy/` | T1 |
| 02 | Research | `core/domain/rooms/02-research/` | T1 |
| 04 | Architecture | `core/domain/rooms/04-architecture/` | T1 |
| 03 | Design | `core/domain/rooms/03-design/` | T1 |
| 08 | Localization | `core/domain/rooms/08-localization/` | T1 |
| 16 | Innovation | `core/domain/rooms/16-innovation/` | T1 |
| 05 | Backend | `core/domain/rooms/05-backend/` | T2 |
| 06 | Frontend | `core/domain/rooms/06-frontend/` | T2 |
| 07 | Mobile | `core/domain/rooms/07-mobile/` | T2 |
| 09 | Security | `core/domain/rooms/09-security/` | T3 |
| 10 | Quality | `core/domain/rooms/10-quality/` | T3 |
| 11 | DevOps | `core/domain/rooms/11-devops/` | T3 |
| 12 | Observability | `core/domain/rooms/12-observability/` | T3 |
| 15 | WarRoom | `core/domain/rooms/15-warroom/` | T3 |
| 13 | Knowledge | `core/domain/rooms/13-knowledge/` | T4 |

---

## The 4 constitutional guards (where they live)

> Source: `core/tooling/README.md`.

Every commit is checked by 4 machine guards:

| Guard | File | Law | What it checks |
|-------|------|-----|----------------|
| `registry_guard` | `core/tooling/registry_guard.py:1` | 12 | `.opencode/agent/*` ↔ `registry.yaml` 1:1 |
| `count_sync` | `core/tooling/count_sync.py:1` | 12/13 | derived vs declared vs textual vs disk |
| `evidence_guard` | `core/tooling/evidence_guard.py:1` | 4 | every `file:line` resolves |
| `gitleaks` | `gitleaks.toml:1` | 8 | no secrets in code |

Run them with: `bash core/tooling/hooks/pre-commit` (from `hq/` root) or simply `git commit`
after `bash core/tooling/hooks/install.sh`.

---

## See also

- [`core/README.md`](./core/README.md) — constitution material
- [`brain/README.md`](./brain/README.md) — organization memory
- [`engine/README.md`](./engine/README.md) — live publishing layer
- [`training/README.md`](./training/README.md) — file-discipline
- [Top-level README](../README.md)
- [`AGENTS.md`](../AGENTS.md) — supreme law
