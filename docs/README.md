# `docs/` — Non-Binding Supplementary Documents

> **Non-binding** documentation. The constitutional documents live in `hq/core/` and `AGENTS.md`.
> This directory is the **public-facing** documentation that mirrors and explains parts of the
> constitution in a more accessible way.

Anything in this directory may be **less rigorous** than the constitution. If you find a
discrepancy, the constitution (`AGENTS.md` + `hq/core/`) wins. This directory is informational
only.

---

## Files

| File | Purpose | Source mirror |
|------|---------|----------------|
| `sakk-wallet/` | Sakk-specific supplementary documentation (analysis, decisions, qa-reports, feeding logs, guides) | mirrors `projects/sakk/brain/` |
| `superpowers/` | External superpowers plans (e.g. `2026-08-27-sakk-flutter-web.md`) | ad-hoc |
| `*.md` (root) | Other non-binding docs | ad-hoc |

---

## The visual diagrams mirror (per `README.md:24`)

The 9 Mermaid diagrams live canonically in `hq/core/design/diagrams/`. A public mirror is
maintained at `docs/diagrams/` (currently 18 files: 9 SVG + 9 PNG). The mirror is for presentations
and the public website; the canon is for constitutional work.

---

## The sakk-wallet subdirectory

> Source: `docs/sakk-wallet/`

This subdirectory contains supplementary sakk documentation:
- `analysis/design-rules.md` — design rules and constraints
- `decisions-log.md` — chronological log of sakk decisions
- `evidence/feeding-log.md` — visual feeding log
- `guide/template-usage-guide.md` — template usage guide
- `qa-report.md` — QA report

These are **ad-hoc** documents that complement (not replace) the formal `projects/sakk/brain/`
memory. They are written for human readers, not for the constitutional guards.

---

## The superpowers subdirectory

> Source: `docs/superpowers/`

This subdirectory contains ad-hoc plans from external superpowers tools (e.g. Obra's
superpowers). The `2026-08-27-sakk-flutter-web.md` is an example of a Flutter web implementation
plan that was adopted (or rejected) per the S1→S6 flow.

**Update policy:** when a superpowers plan is adopted, link to it from CORTEX with the
`ADR-YYYYMMDD-NAME` reference. When rejected, archive with a `REJECTED` marker.

---

## What lives here vs. the constitution

| Type | Location | Binding? |
|------|----------|----------|
| Constitution | `AGENTS.md` (root) | YES — supreme |
| Operational law | `hq/core/protocols.md` + `hq/core/contracts.md` | YES — by constitution |
| Standards | `hq/core/standards/` | YES — by protocol |
| Contracts (room-by-room) | `hq/core/domain/context-map.yaml` | YES — by Law 2 |
| Public-facing docs | `docs/` (this directory) | **No — informational only** |
| Brand identity | `identity/` | YES for usage, NO for detail |

---

## How to add to this directory

**Allowed without ceremony:**
- Ad-hoc analysis, design notes, guides
- Mermaid diagram mirrors
- External superpowers plans
- One-off QA reports

**Requires ADR in CORTEX:**
- Any document that changes organizational structure or behavior
- Any document that supersedes or contradicts constitutional material
- Any public-facing statement that affects stakeholder trust

---

## See also

- [`../README.md`](../README.md) — top-level
- [`../hq/core/design/diagrams/`](../hq/core/design/diagrams/) — diagram canon
- [`../identity/`](../identity/) — system identity
- [`AGENTS.md`](../AGENTS.md) — supreme law
