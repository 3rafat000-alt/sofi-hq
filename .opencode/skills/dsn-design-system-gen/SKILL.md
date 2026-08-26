---
name: dsn-design-system-gen
description: >-
  Generate a complete design system from a project brief: three-layer tokens, color palette,
  typography, motion, and core components — validated against WCAG 2.2 and ready for any framework
  (React+Tailwind or Flutter ThemeData). Triggers — Arabic: "build a design system",
  "generate design tokens", "project color palette and fonts", "unified design system", "unified
  ThemeData", "identity tokens". English: "generate a design system", "design tokens",
  "color palette and typography system", "build a token system", "design system
  from brief". Invoked inside the Design room when a project/feature needs a unified visual
  language before screen design or after approving the visual direction.
---

# dsn-design-system-gen — Design System Generator ⬛

> **Value:** replaces visual improvisation with one documented system: every color, font, and spacing derived from three-layer tokens and tested against WCAG 2.2 before delivery — so no page invents its own colors.
> **Scientific source:** patterns extracted from `plugin87/ux-ui-agent-skills` (three-layer DTCG architecture), `Laith0003/ux-skill` (deterministic recommendation engine), and `ui-ux-pro-max-skill` (system generation from project type).

## 🎯 When to invoke (When) ⬛
- A new project/feature needs a unified visual system before designing any screen.
- A new brief arrived that must be converted into tokens + palette + typography + motion.
- Consolidating scattered systems: pages using hardcoded colors get one source of truth built for them.
- Generating a Flutter version (`ThemeData`) or React/Tailwind (`theme.css` + Tailwind config) from the same tokens.

**Do not invoke** for: reviewing/auditing an existing design (that's `dsn-design-review`), preparing a frontend delivery package (that's `dsn-design-handoff`), or choosing a free creative aesthetic direction (that's `frontend-design`).

## 📥 Required inputs (Inputs) ⬛
- **RCCF work order (Law 5)** — no execution without it.
- **The mandatory 10-field brief** (no recommendation without a brief — improvisation is the source of slop):
  1. Project type 2. Target audience 3. Primary goal 4. Tone 5. Must-haves
  6. Forbidden moves 7. Reference marks 8. Tech stack 9. Region/language (RTL?) 10. Success metric.
  - Vague phrases ("modern", "clean", "professional") **rejected as inputs** — ask for specificity.
- Existing identity if any (logo, brand colors, approved fonts).
- Target accessibility standard: **WCAG 2.2 AA minimum**.

## 🔧 Steps (Steps) ⬛
1. **Verify RCCF and brief** — any missing field of the ten → send back through your lead; never guess.
2. **Generate three-layer tokens (DTCG):**
   | Layer | Role | Example |
   |--------|-------|------|
   | Primitive | raw values never used directly | `blue.600`, `space.4` |
   | Semantic | purpose-named — used in design | `action.primary`, `text.secondary`, `surface.card` |
   | Component | scoped to a component — used in code | `button.primary-bg`, `input.border-focus` |
   - Cover: colors, typography scale, spacing, shadows, borders, breakpoints, **motion** (durations/easing), states (the eight states).
3. **Choose the typographic pair deliberately:** display font + body font + tools/data font — never Inter/Roboto by default; fix the type scale with explicit weights and sizes.
4. **Apply strict color roles:** Primary = one main positive action; Secondary = neutral outline (never colored fill with bold text over it); Destructive = one danger variable used identically everywhere (delete button and its confirmation dialog share the color — a blue "Delete" button = a bug).
5. **Define motion presets:** explicit durations and timings (not always-default 300ms) + respecting `prefers-reduced-motion`.
6. **Validate contrast numerically (not by eye):** normal text ≥ 4.5:1, large text ≥ 3:1, essential UI borders ≥ 3:1, focus ring ≥ 3:1 — in **both light and dark modes**. Any failing pair → adjust the token before continuing.
7. **Emit both frameworks' outputs** from the same source:
   - Web: `tokens.json` (DTCG) + `theme.css` (CSS variables `:root` + `[data-theme="dark"]`) + mapping for Tailwind config.
   - Flutter: unified `ThemeData` (ColorScheme + TextTheme + motion durations) covering all screens.
8. **Apply the RTL rule** if the region is Arabic: logical properties in CSS, mirrored layout and directional icons — test the mirror.
9. **Review against slop** before delivery: no automatic purple→blue gradient, no 3 identical cards as a lazy template, no emoji in UI — use a real icon set (lucide/SVG with `currentColor`).
10. Produce the evidence block (see below) via the `sofi-evidence` skill.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- **Output:** one design system under `artifacts/<ticket>/design-system/`:
  - `tokens/` (three-layer DTCG JSON) · `theme.css` or `theme_data.dart` · a README explaining color roles and usage rules.
- **Evidence (Law 4) — Designer type** via `sofi-evidence`:
  - Measured contrast table: every text/UI/border/focus pair → its computed ratio → pass/fail, **light + dark**.
  - Token and theme file paths (`file:line`).
  - One component sample (Button) in all eight states: default/hover/focus/disabled/loading/error/selected/empty-state.
  - Decision log: why this typographic pair and palette (tied to the brief — no arbitrary choice).

## 🔗 Handoff ⬛
- Deliver the system to **your room lead `dsn-lead`** only (Law 3) via the `sofi-handoff` skill.
- Frontend access goes through Contract 03 (`dsn-design-handoff`) — never directly (Law 2).
- No direct delivery to the user.

## ⛔ Constraints ⬛
- **No hardcoded value outside the tokens** — every color/spacing/duration in code references a token.
- Layers are never skipped: a component never imports Primitive directly.
- Aesthetics never outrank accessibility: any taste choice breaking WCAG → rejected without debate.
- No inventing a new identity when an approved brand identity exists — extension only.
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Record system approval (tokens version, palette, typographic pair) in project memory `projects/<name>/brain/DECISIONS.md` (Law 7).

## 📚 References ⬜
- `github.com/plugin87/ux-ui-agent-skills` — three-layer DTCG architecture + contrast gates.
- `github.com/Laith0003/ux-skill` — the 10-field brief + deterministic recommendation engine.
- Sibling skills: `dsn-design-review` (auditing), `dsn-design-handoff` (delivery), `frontend-design` (creative direction).
- **Owner (Law 9):** Design room 03 — `dsn-lead`.
