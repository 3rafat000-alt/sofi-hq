# FILE: hq/core/standards/visual-identity-standard.md

# Visual Identity Standard — SAKK Design Doctrine (v1 · 2026-08-26)

> **Origin:** Owner directive — "وجه الفريق واعمل بالقانون": identity must be derived from Law, System, Structure, Organization. Every principle below cites its governing source. Nothing is decorative taste; everything is law applied to pixels.
> **Owners of this standard:** dsn-lead (execution) · res-lead (verification) · str-lead (strategy) · fnt-lead + mob-lead (implementation) · brd-cqo (final sign-off via DFR).
> **Live proof-of-concept:** `projects/sakk/apps/site-prototype/` (flat tricolor MVP, built and verified 2026-08-26).

---

## PART 1 — Identity Drawn from Law, System, Structure, Organization

How designers, researchers, thinkers, and builders derive visual identity from governance — each row: governance source → design principle → live evidence.

| # | Governance Source | Design Principle | Live Evidence (2026-08-26 build) |
|---|---|---|---|
| 1.1 | **Law 13 — Zero-Randomness** | Zero random values: every color/size/radius comes from the token registry. Raw hex or px in components = defect. | Official palette tokens only (`#6e1b2d` · `#c49b55` · `#f7f3ee` · `#2a1a1f`); vendored preset aligned to owner's `:root` |
| 1.2 | **Teaching IV — Token Economy** | Economy of elements: no decoration without function. If it doesn't carry meaning, it doesn't render. | Owner bans codified: 0 shadows · 0 gradients · 0 glow · 0 colored borders (measured 0/0/0/0 in DOM audit) |
| 1.3 | **Law 3 — Hierarchical Handoff** | Visual hierarchy mirrors command hierarchy: one primary action per view, descending weight, never two competing heroes. | Hero order: badge → H1 → one-line sub → primary CTA → trust line |
| 1.4 | **Law 4 — Evidence Required** | Every design claim carries evidence: reference, measurement, or code citation. Marketing claims without code evidence are forbidden. | Content-truth audit: gold/135-currencies/50M-users claims purged (154 fabricated sites logged); features map 1:1 to backend domains |
| 1.5 | **Law 2 — Room Isolation** | Component encapsulation: identity lives in tokens + shared components; pages compose, never redefine. | `@sakk/ui` preset is single source; pages consume classes only |
| 1.6 | **Law 16 — Clarification Threshold** | Clarity principle: one idea per section; if a section needs a paragraph to explain, it is over-threshold and gets split. | 9 sections, each with single SectionHead idea |
| 1.7 | **DFR Gate (S3)** | Identity changes pass security + quality signature before code — same as features. | This standard itself = the S3 artifact for identity |
| 1.8 | **S1–S6 Pipeline** | Identity lifecycle mirrors production line: strategy (meaning) → tokens (contract) → system (components) → build → QA → ship. | Tricolor rollout executed in this exact order |
| 1.9 | **Owner Palette (constitutional tokens)** | The tricolor is law, not preference: **عنبي دمشقي** `#6e1b2d` = voice · **كريمي** `#f7f3ee/#fdfcfa` = stage · **ذهبي** `#c49b55` = crown · **حبري** `#2a1a1f` = text/depth only | Distribution rhythm v5: cream → burgundy block → gold band → burgundy+gold card → cream → burgundy footer |
| 1.10 | **Law 10 — Main Tree** | Identity evolves on the live system via prototype branch → approval → swap; no parallel brands. | site-prototype → owner approval → port to apps/site → Caddy swap |
| 1.11 | **Rounding Directive (owner, 2026-08-26)** | Soft geometry: cards `rounded-2xl` · panels `rounded-3xl` · actions/badges `rounded-full`. Sharp corners are a defect. | 17 rounded surfaces measured in live DOM |
| 1.12 | **Law 6 — Anti-Loop** | Iteration discipline: each review round produces named changes; a third round on the same unresolved note escalates to owner, not blind retries. | v2→v3→v4→v5 rounds each closed with measured deltas |

**The Inspiration Method (how the rooms actually derive identity):**
1. **Read the Law before the moodboard** — every visual decision starts from a numbered source above, not from "I feel".
2. **Extract structure, not decoration** — the S-curve of the pipeline, the room grid, the ticket flow: layout rhythms are borrowed from how the organization itself flows.
3. **Damascus grammar** — عنبي دمشقي is the city's historical burgundy; cream is its limestone; gold is its craftwork. Identity = place, encoded as tokens.
4. **Constraint breeds style** — the banned list (glow/gradient/shadow) is not limitation; it is the brand's signature austerity.

---

## PART 2 — Skills Matrix per Role

Minimum verified skill set for a complete visual identity capability. Verification = sofi-agent-eval rubric (constitution 30% · evidence 25% · accuracy 20% · craft 15% · communication 10%) on real deliveries.

### 2.1 المصممون — Designers (room 03: dsn-ui, dsn-design-system, dsn-brand, dsn-motion, dsn-ux-architect)
| Skill | Standard of proof |
|---|---|
| Token-driven design | Zero raw values in handoffs; every spec cites a token name |
| Tricolor distribution | Can compose any page using only the v5 rhythm (cream/burgundy/gold blocks) within the 60-30-10 weight rule |
| Typography system | Arabic-first scale (IBM Plex Sans Arabic) with Latin mirror (Inter); 5 sizes maximum per page |
| RTL-native layout | Designs are drawn RTL-first; LTR is the translation, never the reverse |
| Flat discipline | Produces richness via composition (space/weight/color-blocks) with the banned list active |
| Component spec writing | Hands builders states + tokens + measurements, not pictures alone |

### 2.2 الباحثون — Researchers (room 02: res-ux, res-competitor, res-fact-checker)
| Skill | Standard of proof |
|---|---|
| Content-truth verification | Every claim traced to code/backend evidence (the 154-fabrication audit method) |
| Competitive visual audit | Structured teardown: palette, rhythm, hierarchy of 3 references — cited, not vibes |
| Journey evidence | Section order justified by user-journey data, not order-of-writing |
| Claim register | Maintains the honest-copy register: allowed claims + their code citations |

### 2.3 المفكرون — Thinkers/Strategists (room 01: str-product, str-business + arc-review)
| Skill | Standard of proof |
|---|---|
| Identity strategy | One-page doctrine: what the brand says, refuses, and how tricolor maps to meaning |
| Information architecture | Section inventory with hierarchy levels before any screen exists |
| Design-to-code contracts | Writes token contracts (names, values, usage rules) that builders sign |
| Review arbitration | Applies Law 14 to design disputes; names the failing item, never generic rework |

### 2.4 البنّاؤون — Builders (rooms 05/06/07: fnt-react, mob-flutter, fnt-css)
| Skill | Standard of proof |
|---|---|
| Token-only implementation | 0 raw hex/shadows/gradients in diff (automated grep must return 0) |
| Component reuse | New page = ≥80% shared components; new component requires lead approval |
| Responsive discipline | Every section verified at 390px + 1440px with screenshots attached |
| Motion restraint | Reveal/fade only; no scale/glow/parallax without DFR exception |
| Iteration speed | HMR-round capable: owner note → live delta in minutes (prototype loop) |

---

## PART 3 — Radical Development Proposals (prioritized)

| # | Proposal | Impact | Effort | Decision gate |
|---|---|---|---|---|
| 3.1 | **Build the real `@sakk/ui` package** (the ghost made flesh): tokens.ts + Button/Card/SectionShell/Badge components — single source consumed by site, admin, portal, mobile | Kills duplication forever; identity changes in one file | M | Owner + arc-lead |
| 3.2 | **Design-lint guard** (`tooling/design_lint.py`): CI grep banning raw hex/shadow-/gradient classes outside token files — the Law-13 guard for visuals | Makes the banned list self-enforcing | S | fnt-lead |
| 3.3 | **Visual regression snapshots**: Playwright screenshot diff on every deploy (desktop+mobile) | Catches identity drift before the owner does | M | qa-lead |
| 3.4 | **Identity handbook** (one page): logo rules, tricolor ratios, spacing scale, do/don't — signed by dsn-lead + brd-cqo | Onboards any future agent/human in minutes | S | dsn-lead |
| 3.5 | **Content-truth completion**: purge/rewrite the 154 remaining fabricated sites (blog long-form, gold guide, legal, about) — each rewritten ONLY from verified backend features | Zero-fraud guarantee across all pages | L | Owner decision: delete vs rewrite vs unpublish |
| 3.6 | **Quarterly identity eval**: sofi-agent-eval rubric applied to design deliveries + owner satisfaction score | Identity stays law-aligned over time | S | brd-cqo |

**Sequencing:** 3.4 + 3.2 (this week, small) → 3.1 (next sprint, the big rock) → 3.3 + 3.6 (with deploy pipeline) → 3.5 (parallel content track, owner-gated).

---

## Adoption Directives (issued to room leads via their chain)

- **dsn-lead:** Adopt Part 1 table as design-review checklist item #1; produce the Identity Handbook (3.4) within the week.
- **res-lead:** Stand up the Claim Register (2.2) from today's 154-audit; no marketing text enters i18n without a code citation.
- **str-lead:** Ratify the doctrine one-pager (2.3) and bring 3.1 to the owner as the next sprint's big rock.
- **fnt-lead + mob-lead:** Enforce token-only diffs (2.4) via 3.2 lint; prototype loop (`site-prototype`) becomes the standard iteration workflow for identity work.
- **brd-cqo:** Add Part-1 rows to the DFR checklist; no identity merge without this standard cited.

---

*Signed into standards by gtw-intake-reformer under owner directive · 2026-08-26 · Any modification requires brd-ceo approval per Law 12 discipline.*
