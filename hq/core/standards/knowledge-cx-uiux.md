# SOFI — Condensed Knowledge Reference: CX · UX · UI (Trinity Knowledge Reference)
**Binding on every room working on interfaces or customer experience. Injected into skills (`SKILL.md`) and rooms before any design decision — no improvisation outside this reference. Source: established professional practices, updated only by CEO decision.**

> Purpose: a single three-branch knowledge tree (UI ← UX ← CX) governing everything built for the end user in any project under `projects/<name>/`. The governing rule: **CX defines "why", UX defines "how it flows", UI defines "what it is seen with"** — every feature is built from CX down to UI, never the reverse.

> **Injection mechanism:** every room skill working on an interface/experience cites this file in its references section and adheres to its tree during design, review, and testing. Any conflict between project code and this reference = a violation against the reference unless a documented CEO decision exists.

---

## | Tree 1 — UI (User Interface): from Atom to System

### 1.1 Atoms — the smallest visual unit; never designed individually outside the system
| Atom | Binding Rule |
|-------|----------------|
| Shapes & corners | one unified radius per element family (card 12–16px, field 8–12px, pill or 8px button) — no random radius mixing |
| Shadows / elevation | a fixed elevation ladder (0 surface, 1 card, 2 dropdown, 3 modal) — shadow is hierarchical semantics, not decoration |
| Icons | exactly one family (Heroicons), one stroke weight, size from scale tokens — mixing two families is forbidden |
| Borders | one thickness (1px); the border is for semantic separation, not ornament — a card with shadow needs no border |
| Spacing | one doubling ladder (4/8/12/16/24/32/48) — every gap is a number from the ladder, never a free number |

### 1.2 Components — composing atoms into known functions
- **Input:**
  - Text fields: label always above the field + placeholder as example, not instructions + a specific textual error message below the field ("Enter an email containing @"), not "error".
  - Buttons: only one primary per screen (the most important action) + secondary + text-button for tertiary actions — clear hierarchy, never three equal buttons.
  - Selection: checkbox for multiple options, radio for a single choice (all options visible), switch for instant toggle state, dropdown when options exceed 7.
- **Navigation:**
  - Top navbar (web): identity + primary navigation + primary action (cart/sign-up).
  - Bottom-nav (mobile): 3–5 items maximum, most important first or centered, active indicator clearly visible.
  - Drawer: long secondary lists (settings, rare links) — must not hide primary navigation.
  - Breadcrumbs: mandatory in sequences deeper than two levels — the last item is the current location and is not clickable.
- **Display:**
  - Cards: the whole unit is clickable, not part of it — one uniform touch area.
  - Modals: for one decision that cannot wait (delete, payment confirmation) — modal-on-top-of-modal is forbidden.
  - Loaders: spinner for under a second; skeleton for longer and for structured content — matching the shape of the incoming content.

### 1.3 Layout — Web vs Mobile
| Environment | Tools | Binding Rule |
|--------|---------|-----------------|
| Web (React/Tailwind) | Grid for overall structure, Flex for inner rows, responsive breakpoints (mobile-first: sm→md→lg→xl) | no fixed pixel widths; max-width containers + flexible ratios; the small screen is designed first |
| Mobile (Flutter) | vertical Column / horizontal Row / Stack overlay / SizedBox for spacing and sizing / LayoutBuilder + MediaQuery for adaptive behavior | spacing via SizedBox/EdgeInsets from tokens — no scattered magic numbers; Expanded/Flexible to prevent overflow |
| Both | 8pt grid | every alignment and gap is a multiple of 8 (or 4 in tight cases) across both platforms — cross-platform visual consistency |

### 1.4 Design Systems
- **Semantic color tokens:** naming by function, not by color — `primary` / `secondary` / `success` / `warning` / `danger` / `surface` / `background` / `text-primary` / `text-muted`. Using a raw color name (`blue-500`) inside component code is **forbidden**.
- **Typography scale:** a fixed ladder (12/14/16/20/24/32/48) with semantic names (caption/body-sm/body-lg/h3/h2/h1). Minimum body text 16px web and 14sp mobile; line-height ≥ 1.5 for continuous text.
- **Light/dark themes:** same semantics with two value sets — no component with hard-coded colors outside the theme.
  - Tailwind: semantic vars in config (`bg-surface`, `text-primary`) + a unified `dark:` class strategy.
  - Flutter: `ThemeData` + `ColorScheme.fromSeed` — reading from `Theme.of(context)` exclusively.
- **Single source of truth:** tokens are managed in one place (`packages/ui` for monorepo projects) and consumed by web and mobile alike — no scattered copies falling out of sync.

### 1.5 Interaction
- **Element states:** default ← hover (web only) ← pressed/focus ← disabled (grayed + forbidden cursor + visible reason). Flutter: InkWell/Ripple is mandatory on every clickable element.
- **Motion:** screen transitions 200–300ms with a natural easing curve; Hero (Flutter) / Framer Motion (React) for elements traveling between states; motion > 500ms or exaggerated bounce is forbidden — motion explains relationships, it does not distract.
- **Feedback:** snackbar (Flutter) / toast (React) for every successful or rejected action — no action without visual echo within 100ms; critical errors use modal, not a dismissable toast.

### 1.6 The Eight Interface States — mandatory for every screen before passing quality
| # | State | Mandatory Handling |
|---|--------|--------------------|
| 1 | Ideal | full content after successful loading |
| 2 | Loading | skeleton mirroring the screen structure (no spinner floating in emptiness) |
| 3 | Empty | illustrative graphic + "what you will find here" message + first-action button |
| 4 | Error | human-readable cause + Retry button repeating the same request |
| 5 | Partial | some data arrived: show what arrived + placeholder for the rest |
| 6 | Offline | persistent alert bar + queueing the action until connectivity returns |
| 7 | Permission/Denied | explain "why we need the permission" before requesting it + a manual fallback path |
| 8 | Loading-more (pagination) | skeleton rows at the bottom of the list, not flashing the entire list |

### 1.7 Accessibility (a11y) — mandatory, not a luxury
- Text/background contrast ≥ 4.5:1 for body text and ≥ 3:1 for headings and icons.
- Every interactive element has a meaningful label (semantic HTML / Semantics in Flutter) — a screen reader understands it without visual context.
- Interaction never depends on color alone (error = text + icon + color together).
- Font size respects system scaling; touch does not require precision (targets ≥ 48dp).

---

## | Tree 2 — UX (User Experience): from Research to Testing

### 2.1 Research — no design without research
- **Personas:** 2–4 personas maximum; each persona = one main goal + one pain point + usage context (device/time/environment) — no decorative demographics without decision function.
- **Journeys:** the user's path of steps toward achieving the goal + an emotion curve pinpointing frustration moments — every trough in the curve is a repair opportunity.
- **Quantitative:** usage analytics, completion rates, closed surveys — answers "how much? and where?".
- **Qualitative:** interviews, usability testing, direct observation — answers "why?".
- **Rule:** a pivotal design decision without two forms of evidence (quantitative + qualitative) = rejection at the quality gate.

### 2.2 Information Architecture (IA)
sitemap (map of screens/pages and their relations) ← card-sorting with real users to group sections the way they understand them ← labeling in the user's language, not the team's ("Buy now", not "Complete purchase transaction"; "My orders", not "CRM records").

### 2.3 Flows & Error Prevention
- A flow = a diagram from entry point to goal with no dead ends; every step has a clear output and a safe way back.
- **Prevent errors before correcting them (priority order):**
  1. Prevention: disable the submit button until required fields are complete.
  2. Warn before irreversible actions: confirm before delete/payment.
  3. Easy correction: instant validation on field blur, not after submission, with a suggested fix.
  4. Tolerance: undo where possible instead of nagging confirmation.

### 2.4 Wireframes → Prototype
lo-fi (paper/Balsamiq — structure and sequence only, no colors or cosmetic detail) → hi-fi (colors from tokens and real content) → a clickable interactive prototype tested **before writing any line of code** — fixing a wireframe error costs minutes; in code it costs days.

### 2.5 Testing
| Stage | Tool | What It Measures |
|---------|--------|-----------|
| alpha | the team internally | breakage of core flows before any external user |
| beta | a limited group of real users | real usability + qualitative feedback |
| A-B | two competing variants of exactly **one** decision | which option achieves the goal better (button/heading/sequence) |
| heatmaps | click and scroll maps | drop-off points, distraction, ignored elements |

### 2.6 Psychological Laws — binding with practical application per law
| Law | Statement | Mandatory Practical Application |
|---------|------|--------------------------|
| Hick | more options increase decision time | split long forms into short steps (stepper); 5–7 options maximum per menu; tuck rare settings under "advanced" |
| Fitts | large nearby targets are easier to hit | a huge confirmation button at the bottom of the screen within thumb reach; tap area ≥ 48×48dp; dangerous buttons far from frequent ones |
| Jakob | users expect your product to resemble what they know | familiar patterns (cart top corner, hamburger menu, search up top) — innovate in value, not in navigation basics |
| Serial Position | people remember first and last best | the most important item first and last in navigation/bottom-nav; the middle for secondary items; in long lists put the important items at the edges, not the center |

---

## | Tree 3 — CX (Customer Experience): from Strategy to Culture

### 3.1 Strategy
- **Promise:** one binding sentence the organization commits to before the customer — every department serves this promise or undermines it.
- **The full journey:** a map of the customer journey across all departments (marketing ← sale ← service ← after-sales), not a single screen — CX looks at the whole journey, and its weakest link defines the impression.
- **Segmentation:** divide customers by value (VIP / regular / at-risk of churn) and tailor treatment per segment — VIP gets reply priority, faster recovery, tangible perks; the at-risk segment receives a retention offer before leaving, not after.

### 3.2 Omnichannel — One Channel, One Memory
Digital (web/mobile/social/email) + physical (branch/store) + **unified**: the customer moves between channels without losing context.
- **The binding example:** the cart starts on web and continues on mobile automatically; the support conversation resumes where it stopped regardless of channel change; the reservation appears at the branch employee's terminal.
- **Forbidden:** a siloed channel system with separate memories — that is multiple clashing experiences, not one customer.

### 3.3 Service
- **Self-service first:** an FAQ organized in customers' terms + a chatbot for recurring questions — 80% of inquiries should never reach a human, and a bot that doesn't know the answer hands off to humans immediately, without loops.
- **Human helpdesk:** a clear bot→human escalation without re-explaining the problem; the agent sees the customer's full context before the first reply.
- **Binding SLA:** first-response time and resolution time written per segment (example: VIP response ≤ 5 minutes and resolution ≤ 4 hours; regular response ≤ 24 hours) — measured on a live dashboard and enforced, not a marketing slogan.

### 3.4 Metrics — in Binding Computational Forms
| Metric | Formula | Reading & Action |
|--------|--------|-------------------|
| NPS | `(promoters − detractors) ÷ total × 100` | overall loyalty; > 0 acceptable, > 50 excellent; ask detractors "why?" monthly |
| CSAT | `(satisfied ÷ surveyed) × 100` | satisfaction at a specific moment (after a purchase/service interaction) |
| CES | average score of "how much effort did you exert to complete your request?" (1–7) | the lower, the easier the flow — a rise is an alarm for a convoluted flow |
| Churn | `(customers who left ÷ start-of-period customers) × 100` | leakage; monitored monthly per segment, a jump = immediate root-cause investigation |

### 3.5 VoC (Voice of the Customer) — Two Mandatory Loops
- **Inner loop (immediate):** rescue the angry customer now — explicit apology + resolution within their segment's SLA, before any analysis or blame; instant rescue turns the angry into the most loyal advocates.
- **Outer loop (systemic):** aggregate complaint causes monthly ← fix the system that generated the anger (policy/feature/flow), not endless firefighting; any complaint recurring twice = a mandatory fix item.
- Capture channels: post-service surveys, store reviews, social media, categorized support calls — aggregated into one repository.

### 3.6 Institutional Culture & EX
Employee experience (EX) creates customer experience (CX): a deprived employee = deprived customers.
- Empower front-line staff to make rescue decisions within clear limits (example: discount/refund up to a known ceiling) without bureaucratic escalation.
- Measure team satisfaction as a leading CX indicator reviewed quarterly.
- Celebrate customer-rescue stories internally — rewarded behavior repeats.

---

## | Pre-Handoff Checklist for Any Interface Delivery
1. The screen covers all eight interface states (§1.6) — no screen ships in a single state.
2. All colors, spacings, and fonts come from tokens — zero magic numbers.
3. One primary per screen, and every clickable element has ripple/hover + feedback within 100ms.
4. Error prevention applied: disabled button until fields are complete, confirmation before irreversible actions, instant validation.
5. The four psychological laws respected in flows and navigation (§2.6).
6. Basic a11y complete: contrast, labels, never color alone.
7. The CX metrics for the screen/feature defined (what will we measure? CSAT or CES or completion?) — a feature without a metric is half a feature.

---

## | Final Mapping Table — Knowledge Branch ↔ Room ↔ Skill

| Knowledge Branch | Owning Room | Executing Skill |
|---------------|----------------|------------------|
| UX research (personas/journeys/quant+qual) | res-lead (02) | `res-journey-map` |
| UX review and audit of an existing design (heuristics/a11y) | dsn-lead (03) | `dsn-design-review` |
| UI systems (tokens/themes/scale/components) | dsn-lead (03) | `dsn-design-system-gen` |
| UI web components from an approved spec | fnt-lead (06) | `fnt-component-build` |
| UI mobile components + mobile states | mob-lead (07) | `mob-feature-build` |
| UX/CX testing (alpha/beta/A-B) + quality gate | qa-lead (10) | `qa-test-plan` |
| CX metrics/VoC/omnichannel (live monitoring) | obs-lead (12) | `obs-incident-response` (on SLA/metric breach) |

**Governance rule:** any new interface feature crosses this chain in order: UX research (res) → UI design system (dsn) → build (fnt/mob) → QA testing (qa). Skipping a stage = rejection at the quality gate (Law 8). Any change to this reference = a CEO decision documented in `hq/brain/cortex-decisions.md`.

**Skill injection rule:** every skill in the table above refers to sections of this reference by number (`§1.x` / `§2.x` / `§3.x`) during execution and review, and rejects any output violating it with `file:line` evidence.

- Unified icon system: Heroicons (@heroicons/react) exclusively — outline by default, solid for active, mini for dense
**Date added:** 2026-08-23 — OWNER-DIRECTIVE

---

## | Tree 4 — The Six Governing UX Laws (injected from lawsofux.com · Self-Development Initiative 2026-08-24)

> **Status:** mandatory as the ruling reference in design reviews (the Design Freeze Review gate (DFR)) and construction — full source: `hq/training/internet_knowledge/ux-*.md` (6 files).

| Law | Binding Summary | Model Application in Our Stores/Platforms |
|---------|------------------|--------------------------------------|
| **Fitts** Fitts's Law | touch targets large, well-spaced, and in easy-reach zones | "Add to cart" button ≥48px at the bottom of the mobile screen; critical buttons not adjacent to destructive ones |
| **Jakob** Jakob's Law | users transfer expectations from familiar products | checkout flow matching global patterns (cart ← address ← shipping ← payment) — innovate in value, not ordering |
| **Miller** Miller's Law | chunk content into small digestible pieces | a one-address form in short steps, not 12 fields in one row; filter groups ≤7 |
| **Peak-End** Peak-End Rule | design the peak and ending moments — negatives are remembered more | the payment success message = a celebratory ending moment + clear confirmation; any payment error shown gently with an alternative exit |
| **Aesthetic-Usability** aesthetic-usability effect | beauty raises tolerance for flaws and hides them from testing | double-edged: beautiful ≠ working — functional testing (qa) does not accept beauty as an argument; nor do we use beauty to hide a discovered defect |
| **Serial-Position** serial-position effect | first and last are remembered — the middle forgotten | the top 3 categories lead the nav bar and the key CTA closes it; product lists: most prominent first/last, not middle |

**Linkage rule with commerce research:** these laws explain the documented Baymard findings (`(research source from the _intake era — archived by owner order M1)`): ~70% cart abandonment = mass violation of Peak-End (bad endings) + Jakob (unfamiliar patterns).

**Date added:** 2026-08-24 — Self-Development Initiative by owner order (INT-EVOL P1).
