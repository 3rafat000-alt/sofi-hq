---
name: dsn-web-design-guidelines
description: Vercel's global web design standards — a strict checklist covering typography, visual hierarchy, spacing, interactions, and accessibility before any screen is approved. Invoked in room 03 when building mockups and before crossing the DFR gate, and in rooms 06/07 when building Flutter web screens. Triggers — "web design guidelines", "UI checklist", "before design approval", "audit the screen".
---

# dsn-web-design-guidelines — Vercel Design Standards

## Source
The `web-design-guidelines` skill from **vercel-labs/agent-skills** (free, open source) — github.com/vercel-labs/agent-skills.

## Usage
1. When generating any mockup in S3: scan the design against the checklist before presenting it to dsn-lead.
2. At the design-freeze gate (DFR): attach the checklist result to the dfr-signoff evidence package (Law 4).
3. When building Flutter Web/Mobile screens in S5: the same checklist applies to ThemeData and layout.

## Install when needed
```bash
npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines
```

## SOFI rule
These standards complement knowledge-cx-uiux.md without replacing it — conflicts resolve toward the stricter requirement (Law 8).

## Provenance
vercel-labs · free · verified 2026-08-23.
