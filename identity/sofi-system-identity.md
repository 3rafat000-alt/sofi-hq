# SOFI AI

> Unified AI Software Enterprise Framework
> The current generation of SOFI (successor to SOFI v1–v6). One entry point, one registry, one brain.

## Identity

- **Name:** SOFI AI — the team/brand name of this unified AI software enterprise
- **Root:** `~/Desktop/SOFI/`
- **Genesis:** 2026-07-10 — clean break from Lorka lineage

## Layer Map

| Layer | Path | Purpose |
|-------|------|---------|
| Governance | `hq/core/` | Constitution, Nexus, rooms, gates |
| Edge/Proxy | `projects/caddy/` | unified control center for domains and sites (paper — no live configuration yet) |
| Memory | `hq/brain/` | Org knowledge, templates, memdb |
| Projects | `projects/` | Isolated product repos |
- **Runtime substrate:** `hq/` — governance (core), memory (brain) · live domains and sites → `projects/caddy/`
| Integration (opencode) | `.opencode/` | Agents, skills (opencode native) |
| Archive | — | Founding generations destroyed with git history (owner decision 2026-07-16) |

## Key Principles

- Single source per concern (P1)
- Code is truth — every number generated (P2)
- No claim without automated enforcement (P3)
- ~~Git day-zero for every project~~ (P4 — retired 2026-07-16; git removed by owner decision)
- Builder never self-grades (P5)
- Flat topology inside opencode (P6)

## Pipeline (MANDATORY — no exceptions)

```
User raw input
    ↓ [mandatory — cannot be skipped]
gtw-intake-reformer → brd-ceo (+ board via Task) → room leads (via Task) → agents
    ↓ [mandatory]
room lead → brd-ceo → user
```

**Violating the flow = a constitutional violation. The system refuses to respond.**

## Entry

Boot = read the docs in order (see `AGENTS.md` boot sequence).
The `shamel` CLI (doctor/selftest/lint) was retired 2026-07-16 by owner decision — tools engine removed.

## Runtime Support

| Runtime | Config | Agents | Skills | MCP |
|---------|--------|--------|--------|-----|
| **opencode** | `opencode.json` | `.opencode/agent/` (106) | `.opencode/skills/` (99 — INDEX.md is the live reference) | `opencode.json → mcp` |
