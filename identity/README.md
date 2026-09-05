# `identity/` — System Identity

> The **public-facing identity** of SOFI HQ. This directory is the only place where the
> organization speaks to the outside world as a brand — not as a constitution.

The identity is curated by `brd-cso` (security) and `knw-lead` (knowledge). It is referenced
from README (top-level), from public-facing documents, and from any external communication.

---

## Files

| File | Purpose | Audience | Update trigger |
|------|---------|----------|----------------|
| `sofi-system-identity.md` | **The system identity** — name, mission, principles, public persona | external (public) | major organizational change |
| `public-readme.md` | The public-facing README (mirrors the internal one but without constitutional detail) | external (public) | major organizational change |
| `brand-palettes/` | Visual identity palettes (colors, fonts, spacing) | design + ops | brand changes |

---

## The brand: SOFI

**SOFI** = **S**ystematic **O**rganization for **F**uture **I**ntelligence.

**The 5 brand principles (per `sofi-system-identity.md`):**
1. **Evidence over opinion** — every claim has a `file:line` proof
2. **Constitution over convention** — 16 laws + 17 protocols + 22 standards
3. **Hierarchy over chaos** — agent → lead → CEO → user (Law 3)
4. **Specialization over generalization** — 17 rooms · 121 agents · 116 skills
5. **Continuity over chaos** — CORTEX + HIPPOCAMPUS + AMYGDALA (Law 7)

---

## The visual identity (per `brand-palettes/`)

> Source: `hq/core/standards/visual-identity-standard.md` (the binding standard).

- **Primary:** #6e1b2d (Sofi bordeaux)
- **Online green:** #00E676
- **Sakk green:** #008047
- **Admin bordeaux:** #7a1f2b (legacy)
- **Typography:** sans-serif, 1.5 line-height, 18sp minimum
- **Contrast:** ≥ 4.5:1 (WCAG 2.1 AA)
- **RTL:** explicit `dir="rtl"`

---

## The public readme

> Source: `public-readme.md` — the public-facing companion to the internal `README.md` (root).

The public readme is **deduplicated** — it does not contain the full constitutional detail
(those are internal). It contains:
- What is SOFI HQ (in 3 paragraphs)
- The 17 rooms (one-liner each)
- The 16 laws (titles only)
- The 116 skills (counts)
- The license + contributing
- The 27 MCP servers (one-liner)

**Update policy:** every time the internal `README.md` (root) changes for a public-facing reason
(major room/skill count change, new public artifact, etc.), update `public-readme.md` accordingly.
This is a `dsn-lead` + `brd-cso` joint responsibility.

---

## How to update the identity

1. Update `sofi-system-identity.md` (the canonical identity)
2. If public-facing, update `public-readme.md` to mirror
3. If visual, update `brand-palettes/`
4. Bump `hq/core/standards/visual-identity-standard.md` if standard
5. Record ADR in CORTEX if it's a constitutional change
6. Commit atomically — pre-commit enforces all 4 guards

**Forbidden:** making up a new identity without `brd-cso` review (security) and `knw-lead` review
(consistency). The identity is constitutional in spirit (Law 11) and binding in communication.

---

## Law 11 — the binding rule (restated)

> **`AGENTS.md:59` Law 11 — Owner Communication Standard:** "The owner speaks Arabic only and is
> non-technical on abstract terms. Every direct communication (delivery · report · question ·
> decision option) uses clear simple Arabic, explaining *why it matters to him*, not just *what
> happened*. Applies to CEO delivery (L3) and fast-track delivery (L1). Internal agent-to-agent
> work remains technical. **Violation = L1, then L2 on repetition.**"

The identity directory enforces Law 11 by:
- Providing the brand-palettes standard
- Documenting the voice & tone (Arabic simple)
- Curating the public-facing communication

---

## See also

- [`../README.md`](../README.md) — top-level
- [`../hq/core/standards/visual-identity-standard.md`](../hq/core/standards/visual-identity-standard.md) — binding standard
- [`sofi-system-identity.md`](./sofi-system-identity.md) — the canonical identity
- [`AGENTS.md`](../AGENTS.md) — Law 11
