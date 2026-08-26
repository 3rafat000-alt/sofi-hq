# Gate 2: Design Checklist

**Owner:** dsn-lead (Sulaf Al-Rashid)
**Deliverable:** Prototype Spec (frozen)

## Validation

- [ ] Every journey stage has a corresponding screen
- [ ] All states covered per screen: empty, loading, success, error, edge cases
- [ ] WCAG 2.2 AA validated — contrast, keyboard, screen reader
- [ ] Design tokens documented — color palette, spacing scale, type scale
- [ ] Motion/interaction specs for every micro-interaction
- [ ] UX copy keyed — one voice, no placeholder text, error messages explain WHAT and HOW
- [ ] Responsive considerations — 320px to 1200+px
- [ ] Accessibility considerations — focus order, aria labels, reduced-motion alternative
- [ ] Brand consistency check — colors, typography, spacing match design system

## Evidence Required

- [ ] Screen-by-screen spec with state tables
- [ ] Design token key-value pairs
- [ ] UX copy JSON with keys per screen/component
- [ ] WCAG 2.2 AA compliance matrix

## Verification

- [ ] Gatekeeper verifies: every CJM stage → screen, no orphan screens
- [ ] a11y-specialist confirms WCAG AA readiness
- [ ] Brand-designer confirms taste metrics pass

## Sign-off

- [ ] Prototype Spec signed by dsn-lead: "Gate 2 PASS"
- [ ] Spec frozen — no visual/UX changes without re-entering Gate 2

## DFR prerequisite (INT-GTW-024 · v2)

- [ ] **Design-Freeze Review gate (DFR)** — signature of sec-lead + qa-lead on every design — mandatory exit condition before any line of code (`nexus/gates.yaml#dfr`)
- [ ] ux-flows mirror the frozen S2 schema-contract and openapi-spec verbatim
- [ ] hi-fi mockups cover web and mobile from a single visual identity
