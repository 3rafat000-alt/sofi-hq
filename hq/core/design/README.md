# `hq/core/design/` — System Design

> The **system architecture blueprint** + 9 visual Mermaid diagrams. This is the visual
> representation of the constitution — every diagram cites its source `file:line` in the
> constitution.

Owned by `dsn-lead` (03-design) + `arc-lead` (04-architecture).

---

## Files

| File | Purpose | Mirror |
|------|---------|--------|
| `system-ddd-blueprint.md` | The 4-layer DDD blueprint (text + ASCII) | `standards/ddd-capsule.md` |
| `diagrams/` | 9 Mermaid diagrams (source + SVG + PNG) | `docs/diagrams/` (public) |

---

## The DDD blueprint (4 layers)

> Source: `system-ddd-blueprint.md` + `standards/ddd-capsule.md` + `tech_templates/ddd-capsule-protocol.md`.

```
┌────────────────────────────────────────────────────────────┐
│  Presentation Layer  (UI / Controllers / HTTP / API views)  │  ← fnt + mob
├────────────────────────────────────────────────────────────┤
│  Application Layer    (Use cases / Services / Actions)      │  ← bck
├────────────────────────────────────────────────────────────┤
│  Domain Layer         (Entities / VOs / Aggregates)         │  ← arc (bdd only)
├────────────────────────────────────────────────────────────┤
│  Infrastructure Layer (DB / APIs / Queue / Cache)            │  ← bck + ops
└────────────────────────────────────────────────────────────┘
```

The 4 layers are **strictly separated** — `domain/` cannot import from `infrastructure/` or
`presentation/`. The `application/` layer orchestrates the domain. The `infrastructure/` layer
implements the domain's repository contracts.

---

## The 9 visual diagrams (`diagrams/`)

> Source: `diagrams/*.mmd` (Mermaid source) + `*.svg` (vector) + `*.png` (raster) + mirror at
> `docs/diagrams/`.

| # | Diagram | Source | Purpose |
|---|---------|--------|---------|
| D1 | Use-Case | `nexus/registry.yaml:6` | The 17 rooms + their relationships |
| D2 | Pipeline S1→S6 | `nexus/pipeline.yaml:8` | The production line stages + lead + gate + output |
| D3 | Gateway Routing | `README.md:80` + `charter.md:86` (14-gateway) | The intake → 3-lane → route flow + 24h timeout |
| D4 | Layered Architecture | `system-ddd-blueprint.md:42` | The 4 DDD layers + their dependencies |
| D5 | Context-Map | `domain/context-map.yaml:11` | The 14 contexts + their provides/requires/talks-to |
| D6 | Gate State Machine | `nexus/gates.yaml:1` | G0→G8 + DFR + 4 owner approval points |
| D7 | Ticket-Bus Sequence | `AGENTS.md:40` (Law 3) | agent→lead→ceo→user + JSON ticket |
| D8 | Deployment Caddy | `hq/engine/Caddyfile` | The canon Caddyfile + sites import + PHP-FPM |
| D9 | Memory Isolation | `AGENTS.md:44` (Law 7) | org `hq/brain/` ↔ project `projects/<slug>/brain/` |

### Diagram format

- **Source:** Mermaid CLI ^10.9.0 (MIT)
- **Rendered:** SVG (web) + PNG (slides) — both ≤ 200KB
- **Accessibility:** SVG with `role="img"` + `aria-label` + `<title>` + `<desc>` + `alt` in markdown
- **Contrast:** ≥ 4.5:1 (WCAG 2.1 AA)
- **Typography:** 18sp minimum (a11y)
- **RTL:** explicit `prefers-reduced-motion` 200ms
- **Identity:** #6e1b2d (Sofi bordeaux)

### Regenerating diagrams

```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Regenerate one
npx -p @mermaid-js/mermaid-cli mmdc -i diagrams/d1-use-case.mmd -o diagrams/d1-use-case.svg

# Regenerate all (script at scripts/regen-diagrams.sh — to be created)
```

---

## How to add a new diagram

1. Create the Mermaid source at `diagrams/d<N>-<name>.mmd`
2. Generate SVG + PNG
3. Mirror to `docs/diagrams/`
4. Add a row to the table above
5. Commit atomically — pre-commit enforces all 4 guards
6. Update `hq/brain/evidence/` with the new diagram's audit

**Forbidden:** making up new diagrams without citing constitutional source `file:line`.

---

## The audit (per ADR-20260831-VISUAL-DIAGRAMS)

> Source: `hq/brain/evidence/surgical-review-visual-2026-08-31.md:1`.

The 9 diagrams were created in a 4/4 APPROVED surgical review (4 of 4 reviewers approved):
- `dsn-lead` — design review (4/4) · `knw-lead` — knowledge review (4/4)
- `sec-lead` — security review (4/4) · `qa-lead` — quality review (4/4)

DFR-equivalent sign-off. No code was written before this signature.

---

## See also

- [`../README.md`](../README.md) — `hq/core/` parent
- [`../standards/ddd-capsule.md`](../standards/ddd-capsule.md) — DDD capsule standard
- [`../tech_templates/ddd-capsule-protocol.md`](../tech_templates/ddd-capsule-protocol.md) — DDD protocol
- [`../../../docs/diagrams/`](../../../docs/diagrams/) — public mirror
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 13
