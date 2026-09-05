# `hq/core/standards/` — The 22 Binding Standards

> Every standard in this directory is a **rule of construction** for code, design, ops, or
> documentation in SOFI HQ. They are referenced by `AGENTS.md`, the 17 protocols, and the 9 gates.
> A standard has the same force as a protocol — if you violate one, you violate the constitution.

---

## The 22 standards

| File | Domain | One-line summary |
|------|--------|-------------------|
| `api-envelope.md` | API | Unified API response wrapper — every API uses it |
| `ddd-capsule.md` | Architecture | DDD layer rules + DO/DON'T table for bounded contexts |
| `deploy-standard.md` | Ops | Caddy + PHP-FPM + Cloudflare + Laravel + Flutter/React&Next |
| `devops-standard.md` | Ops | DevOps conventions (CI/CD · secrets · rollback) |
| `identity-handbook.md` | Org | Identity + access + role definitions |
| `installer-standard.md` | Setup | Environment setup rules |
| `knowledge-cx-uiux.md` | Knowledge | UX + knowledge engineering |
| `kpi-thresholds.md` | Quality | **K1–K17** — hard rules K6/K11/K14/K16/K17 block Gate-8 |
| `latest-tech-2026.md` | Tech | Tech currency — what's in / out as of 2026 |
| `latest-version-mandatory.md` | Code | **Context7 + DeepWiki before any code** — no improvising |
| `living-docs.md` | Docs | **Doc freshness** — max 1 commit lag (Audit-ALL) |
| `mcp-communication-standard.md` | MCP | MCP bus rules (transport + payload) |
| `mcp-registry.md` | MCP | MCP server registry (all 27 local) |
| `nextjs-standards-legacy.md` | Legacy | **Legacy** — Next.js (R2 contract) — no new Next.js |
| `pipeline-production-line.md` | Pipeline | **S1→S6 in detail** — stages, leads, gates, outputs |
| `qa-assessment-matrix.md` | Quality | **20/28/22 points** + shared Perf/Security/A11y criteria |
| `reporting-cadence.md` | Ops | **on-merge · on-incident-close · on-session-end** (Rec #16) |
| `room-dod-and-execution-rules.md` | Quality | Per-room Definition-of-Done + 3 binding micro-rules |
| `room-meetings-standard.md` | Org | Meeting cadence + quorum + minutes |
| `stacks-tech.md` | Tech | **R2 legacy** stacks (React / Vue / Flutter / Laravel) |
| `uiux-standard.md` | Design | UI/UX + Protocol 18 (visual feeding + RTL + a11y) |
| `visual-identity-standard.md` | Design | Visual identity (colors · typography · spacing · logos) |

---

## How standards are referenced

- `AGENTS.md` lists no specific standard — it delegates to `protocols.md` which references them
- `protocols.md` references standards inline (e.g. P-18 → `uiux-standard.md` §Visual Inspiration)
- `gates.yaml` + `gate_checklists/*.md` reference `kpi-thresholds.md` for the binding thresholds
- The 4 constitutional guards check standards implicitly via `file:line` citations

---

## The KPI thresholds (K1–K17)

> Source: `kpi-thresholds.md` — the binding numeric/qualitative rules for quality.

**Hard rules (block Gate-8 if violated):**
- **K6** — Test coverage ≥ 85% on critical paths
- **K11** — Zero P0 bugs at release
- **K14** — No task may be rejected twice for the same reason (Law 14 freeze)
- **K16** — Ambiguity score ≤ 20% for any request (Law 16)
- **K17** — Every `file:line` must resolve to a real file (Law 4)

Other K1–K17 are advisory and feed into Gate-5's verdict.

---

## The visual identity (colors · typography)

> Source: `visual-identity-standard.md`.

- **Primary:** #6e1b2d (Sofi bordeaux)
- **Secondary:** #00E676 (online green) / #008047 (sakk green) / #7a1f2b (admin bordeaux — legacy)
- **Typography:** sans-serif, 1.5 line-height for body, 18sp minimum for a11y
- **Contrast:** ≥ 4.5:1 (WCAG 2.1 AA)
- **RTL:** explicit `dir="rtl"` on Arabic UI

---

## How to add a new standard

1. Create the `.md` file with the standard format (one-line summary + scope + rules + examples)
2. Reference it from at least one `protocols.md` section
3. Add a row to the table above
4. Commit atomically — pre-commit enforces all 4 guards
5. Record ADR in CORTEX if the new standard changes constitutional behavior

---

## The 3 binding micro-rules (`room-dod-and-execution-rules.md`)

> A **derivative reference** explicitly subordinate to the constitution. Auto-void on any conflict
> with `AGENTS.md` / `protocols.md` / `gates.yaml` / `kpi-thresholds.md`.

1. **Dependency-aware parallelism:** `str-agile-orchestrator` enforces WIP limits
2. **Specific-rejection rule:** rejections must cite `file:line` + violated criterion + fix direction (vague = L1 for the rejecting Lead)
3. **Law-14 double-rejection freeze** (restated) — see Law 14 in `AGENTS.md`

---

## See also

- [`hq/core/README.md`](../README.md) — parent
- [`hq/core/protocols.md`](../protocols.md) — 17 protocols
- [`hq/core/gate_checklists/`](../gate_checklists/) — per-gate criteria
- [`hq/core/nexus/registry.yaml`](../nexus/registry.yaml) — registry
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md)
