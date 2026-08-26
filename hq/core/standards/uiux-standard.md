# SOFI — The Binding Law of Interface Design & User Experience (UI/UX STANDARD)
**OWNER-DIRECTIVE-WEB-2026-0823 · binding on every room touching a user interface (03·06·07·10·14)**
> This is an **executive law**, not theoretical knowledge: the knowledge lives in `knowledge-cx-uiux.md`, and ruling lives here. Any violation = the violation level noted beside each clause. A conflict between project convention and this law = the law prevails, except by documented owner decision.

---

## | §0 The Eternal Design Order for Any Screen (Design Order — violation = L2)
```
UX flows (from the frozen contract exclusively) → system tokens (tokens-only) → screen spec
(the full matrix §2) → Hi-Fi mockup (§9) → DFR signature → only then: code
```
No screen enters execution before its quartet is complete: spec + tokens + mockup + signature. **Code speaks last.**

## | §1 Strict Web Rules (Web Rules — violation = L1, repetition = L2)
| # | Rule |
|---|---------|
| W1 | **Native RTL:** `dir="rtl"` from the root; no LTR page wrapped inside an Arabic one; directional icons mirror logically |
| W2 | **Mobile-first:** design the narrow column first, then expand — no desktop later squeezed down |
| W3 | **One system breakpoint ladder:** `sm 360 · md 900 · lg 1200 · xl 1440` — no value outside the ladder |
| W4 | **Content container:** max width 1200px centered; 8pt grid (multiples of 4/8 exclusively) |
| W5 | **A single primary button per screen** — all other actions secondary or ghost (mandatory hierarchy) |
| W6 | **Breadcrumbs** mandatory for any sequence deeper than two levels; the last item is not clickable |
| W7 | **Dual navigation:** always-fixed top bar + bottom bar for mobile (< md) on client surfaces; dashboards use sidebar ≥ md and drawer below it |
| W8 | No fixed pixel widths for flexible content — ratios, columns, and grids only |

## | §2 Definition of "Complete Screen" (Screen DoD — missing any item = DFR rejection)
Every screen has a written spec containing the **eleven fields**:
1. Purpose and the task-success sentence ("when does this screen succeed?")
2. Entry points (incoming links/buttons) and their exits
3. Layout regions in RTL visual order (header/main/footer/panels)
4. Responsive behavior at every break in the W3 ladder
5. Components consumed from the design system **by their token names exclusively**
6. **The eight states:** loading (skeleton matching structure) · empty (with cause + exit action) · error (human message + retry) · success · offline · partial · permission-denied · optimistic-pending
7. Ready microcopy per state — human Arabic, not technical (Law 11)
8. Contract bindings: consumed endpoints + expected error envelope per call
9. Accessibility notes (a11y): focus order, aria for live states, text alternative for every functional image
10. Motion: what moves and why (§7 tokens only)
11. Acceptance evidence: 3 repeatable manual checks (Testable criterion from INVEST)

## | §3 The Accessibility Floor — WCAG 2.2 AA (violation = L2, veto held by dsn-a11y-specialist)
| # | Rule |
|---|---------|
| A1 | Text contrast ≥ 4.5:1 and large text/icons ≥ 3:1 — measured, not estimated |
| A2 | `focus-visible` ring always visible (outline in a contrasting color, 2px) — never `outline:none` |
| A3 | Touch target ≥ 48dp/px on every touch device (aligned with KNOWLEDGE-CX-UIUX §2.6 · INT-GTW-024) |
| A4 | Arabic: line-height ≥ 1.6 for continuous text, body ≥ 16px web, no excessive letter tracking |
| A5 | Color alone means nothing — every state carries an icon or accompanying text (color blindness) |
| A6 | DOM reading order = RTL visual order; skip-link to main content |

## | §4 Anti-Slop — Explicit Prohibitions (violation = immediate rejection in review)
- ❌ Tailwind default blue/purple or any `from-X to-Y` gradient without an approved identity decision (owner veto on gradients stands until lifted)
- ❌ A single default font (Inter/Poppins/Roboto) as identity — identity comes from the approved typography table
- ❌ A row of three identical cards with no functional differentiation · a central eyebrow-badge above H1 · a suffocating uniform padding rhythm
- ❌ Decorative `backdrop-blur`, blanket `rounded-2xl` without a radius ladder, generic skeletons not matching structure
- ❌ Filler copy: "start your journey", "easily and smoothly", "powered by AI" — copy names a specific action or is not written
- ✅ The governing test: can this delivery **defend itself?** (intent + calculated choice + specificity) — "nothing at stake" = rejected

## | §5 Performance as a Design Requirement (Budgets — breach = redesign, not code tuning)
LCP ≤ 2.5s · CLS ≤ 0.1 (dimensions reserved for every image/skeleton) · INP ≤ 200ms · WebP images with declared dimensions · subset fonts with `font-display: swap` · only the primary font preloaded.

## | §6 Functional Motion (Motion Tokens — violation = L1)
| Token | Value | Usage |
|---|---|---|
| motion-fast | 150ms ease-out | hover/focus/press |
| motion-standard | 250ms ease-out | opening/closing panels and content transitions |
| motion-loop | 1.4s linear ∞ | skeleton shimmer only |
- Forbidden: decorative loops, parallax, motion on reading text. **`prefers-reduced-motion` stops everything except instant state changes.**

## | §7 Arabic Content (Microcopy — Law 11 applied inside the interface)
- Buttons start with a verb: "Add to cart", not "Cart". Errors come from the envelope's `errors[]` exclusively — no codes to the user
- Prices: Latin digits + "SAR" (financial reading), and dates are Hijri-numeral or Gregorian depending on project context by documented decision
- Empty states: cause + way out ("No orders yet — browse stores") — blind emptiness forbidden
- tone: warm professionalism without exaggeration; neither excessive sentiment nor bureaucratic dryness

## | §8 Hi-Fi Mockups — The Official Medium
- **Approved medium:** one self-contained HTML/CSS page per critical screen under `projects/<name>/docs/design/mockups/`
- Built **with §2 tokens from the design system exclusively** (CSS variables matching the table) — a single hard-coded value = rework
- No business JavaScript and no API consumption — the mockup is a **design document**, not application code (does not touch design_before_code)
- Every mockup carries a header: screen name + spec number + system version + date
- Critical screens = every screen holding money or an irreversible decision (checkout/admin) + the first screen per role

## | §9 Design Freeze Review (DFR) — This Law's Additional Checklist
1. [ ] Every screen has a spec with eleven fields (§2)
2. [ ] The eight-state matrix covered textually and mockup-wise for critical screens
3. [ ] §4 anti-slop scan documented with a result per screen
4. [ ] §3 a11y check signed by dsn-a11y-specialist
5. [ ] §8 mockups present and token-conformant (automated check: grep hex values outside variables)
6. [ ] §5 budgets computed theoretically on the heaviest screen
**Missing any item = no signature. Signature without evidence = L2 on its holder.**

---
*Source of authority: owner decision WEB-2026-0823. Periodic review: every 90 days or upon issuance of an industry standard changing a quantitative clause.*
