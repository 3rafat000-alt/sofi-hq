# `docs/diagrams/` — Public Mirror of the 9 Mermaid Diagrams

> The **public mirror** of the 9 Mermaid diagrams that live canonically in
> `hq/core/design/diagrams/`. This directory is for presentations, the public website, and
> external sharing — it is non-binding (the canon is `hq/core/design/diagrams/`).

The diagrams are generated via Mermaid CLI ^10.9.0 (MIT) from the `.mmd` source files in
`hq/core/design/diagrams/`. SVG = web · PNG = slides.

---

## Files

| File | Source mirror | Purpose |
|------|----------------|---------|
| `*.svg` (9 files) | `hq/core/design/diagrams/*.mmd` | Vector graphics for the web |
| `*.png` (9 files) | `hq/core/design/diagrams/*.mmd` | Raster graphics for slides (≤ 200KB each) |

Total: **18 files** (9 SVG + 9 PNG).

---

## The 9 diagrams

| # | SVG/PNG | Source | Purpose |
|---|---------|--------|---------|
| 1 | `d1-use-case.svg/.png` | `nexus/registry.yaml:6` | 17 rooms + their relationships |
| 2 | `d2-pipeline-s1-s6.svg/.png` | `nexus/pipeline.yaml:8` | Production line stages + lead + gate + output |
| 3 | `d3-gateway-routing.svg/.png` | `README.md:80` + `charter.md:86` (14-gateway) | Intake → 3-lane → route + 24h timeout |
| 4 | `d4-layered-architecture.svg/.png` | `system-ddd-blueprint.md:42` | 4 DDD layers + their dependencies |
| 5 | `d5-context-map.svg/.png` | `context-map.yaml:11` | 14 contexts + provides/requires/talks-to |
| 6 | `d6-gate-state-machine.svg/.png` | `gates.yaml:1` | G0→G8 + DFR + 4 owner approval points |
| 7 | `d7-ticket-bus-sequence.svg/.png` | `AGENTS.md:40` (Law 3) | agent→lead→ceo→user + JSON ticket |
| 8 | `d8-deployment-caddy.svg/.png` | `hq/engine/Caddyfile` | Canon Caddyfile + sites import + PHP-FPM |
| 9 | `d9-memory-isolation.svg/.png` | `AGENTS.md:44` (Law 7) | org `hq/brain/` ↔ project `projects/<slug>/brain/` |

---

## Regenerating the mirror

```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Regenerate one diagram
npx -p @mermaid-js/mermaid-cli mmdc -i ../hq/core/design/diagrams/d1-use-case.mmd -o d1-use-case.svg
npx -p @mermaid-js/mermaid-cli mmdc -i ../hq/core/design/diagrams/d1-use-case.mmd -o d1-use-case.png

# Regenerate all 9
for d in d1-use-case d2-pipeline-s1-s6 d3-gateway-routing d4-layered-architecture d5-context-map d6-gate-state-machine d7-ticket-bus-sequence d8-deployment-caddy d9-memory-isolation; do
  npx -p @mermaid-js/mermaid-cli mmdc -i ../hq/core/design/diagrams/$d.mmd -o $d.svg
  npx -p @mermaid-js/mermaid-cli mmdc -i ../hq/core/design/diagrams/$d.mmd -o $d.png
done
```

---

## The accessibility spec (per `ADR-20260831-VISUAL-DIAGRAMS`)

- **Mermaid CLI:** ^10.9.0 (MIT)
- **SVG format:** `role="img"` + `aria-label` + `<title>` + `<desc>` + `alt` in markdown
- **Contrast:** ≥ 4.5:1 (WCAG 2.1 AA)
- **Typography:** 18sp minimum (a11y)
- **RTL:** explicit `prefers-reduced-motion` 200ms
- **Identity:** #6e1b2d (Sofi bordeaux)
- **PNG size:** ≤ 200KB per file

---

## The audit

> Source: `hq/brain/evidence/surgical-review-visual-2026-08-31.md:1` — 4/4 APPROVED surgical review.

The 9 diagrams were created and reviewed before the canonic version (`hq/core/design/diagrams/`)
was committed. The audit includes:
- `dsn-lead` (4/4) — design review
- `knw-lead` (4/4) — knowledge review
- `sec-lead` (4/4) — security review
- `qa-lead` (4/4) — quality review

---

## See also

- [`../README.md`](../README.md) — `docs/` parent
- [`../../hq/core/design/diagrams/`](../../hq/core/design/diagrams/) — diagram canon
- [`../../hq/core/design/README.md`](../../hq/core/design/README.md) — design README
- [Top-level README](../../README.md)
- [`AGENTS.md`](../../AGENTS.md) — Law 4
