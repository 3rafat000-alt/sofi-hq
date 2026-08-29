# FILE: hq/core/standards/identity-handbook.md

# SAKK Identity Handbook — One Page (v1 · 2026-08-26)

> **Signed:** dsn-lead (design adoption) · brd-cqo (quality ratification) · issued by gtw-intake-reformer under owner directive.
> **Governing standard:** `visual-identity-standard.md` · **Violations:** `hq/core/tooling/design_lint.py` catches them automatically.
> **The one sentence:** cream is the stage, burgundy is the voice, gold is the crown, ink is the pen — and nothing else exists.

---

## 1 · The Tricolor (constitutional — owner tokens)

| Role | Name | Hex | Where it may appear | Weight |
|---|---|---|---|---|
| **Stage** | كريمي Cream | `#f7f3ee` canvas · `#fdfcfa` cards | Page background, cards, panels | ~60% |
| **Voice** | عنبي دمشقي Burgundy | `#6e1b2d` (hover `#4a1320`) | CTA buttons, key accents, brand mark, product card | ~10% |
| **Crown** | ذهبي Gold | `#c49b55` (labels `#a9853c`, soft `#fbf7ee`) | Numbers, section labels, highlights, the gold card | ~10% |
| **Pen** | حبري Ink | `#2a1a1f` · `#6e5f63` · `#a99fa2` | Text and icons ONLY — never a background | text |
| **Soft tints** | wine-50 `#fbf6f8` · gold-50 `#fbf7ee` · marble-200 `#efece6` | section tints | sparingly |

**FORBIDDEN FOREVER:** `#1f0810` and near-black wine backgrounds · shadows · gradients · glow/blur · colored borders (neutral `border-ink/10` hairlines only) · raw hex outside token files.

---

## 2 · Logo

- **Mark:** «ص» white on `wine-600` square — the seal. Square corners (stamps are not rounded).
- **Wordmark:** «محفظة صك» ink, extrabold + `SAKK WALLET` mono caps `tracking-[0.28em]` beneath.
- **Clear space:** one mark-height on all sides. **Min size:** 32px mark.
- **Never:** recolor · rotate · stretch · outline · shadow · place the ink wordmark on burgundy (use white there).

## 3 · Typography

- **Arabic:** IBM Plex Sans Arabic · **Latin:** Inter. Arabic is drawn first; Latin mirrors it.
- **Scale (max 5 sizes per page):** Display `7xl/extrabold` (hero) · H2 `5xl/extrabold` · H3 `xl/extrabold` · Body `sm–base` · Label `xs/bold tracking-[0.3em]` gold-600.
- **Line-height:** titles 1.05–1.12 · body ≥1.6. Tracking-tight on display sizes only.

## 4 · Space & Radius

- **Sections:** `py-20 md:py-28` · **Container:** `max-w-6xl px-5` · **Card padding:** `p-6/p-7` · **Stacks:** `gap-5`.
- **Radius system:** cards `rounded-2xl` · panels `rounded-3xl` · buttons/badges/inputs `rounded-full` · footer top `rounded-t-[2.5rem]`.
- **Borders:** `border-ink/10` hairline only — structure, never color.

## 5 · Rhythm — tricolor distribution

- Page flow: cream canvas → one burgundy block → gold band → cream cards → burgundy close.
- Weight rule: **60** cream/white · **30** content cards · **10** burgundy+gold accents.
- One burgundy moment per screen-height. Gold as large background only in its `50/100` tints — solid `#c49b55` reserved for the product card and small crowns.

## 6 · Do / Don't

| DO | DON'T |
|---|---|
| Solid fills · hairline separators · gold numbers · pill buttons · generous whitespace · reveal-fade only · hover = color inversion | shadow · gradient · glow/blur · colored border · sharp card corners · scale-hover · raw hex · fabricated claims · two heroes on one screen |

---

*This page is law for every SAKK surface (site · admin · portals · mobile). Changes require dsn-lead + brd-cqo re-signature under brd-ceo approval.*
