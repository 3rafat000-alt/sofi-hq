---
name: dsn-design-intelligence
description: Searchable design intelligence — 161 color palettes, 57 font pairings, 99 UX rules, and 161 product patterns across 10 technologies (Flutter included) to generate a complete design system from a single line describing the product. Mandatory in room 03 when building the Design System in S3 and before the design-freeze gate (DFR), and for every color/font/layout decision. Triggers — "design system generation", "color palette", "typography pairing", "UI style", "project colors", "visual identity", "generate the theme".
---

# dsn-design-intelligence — Design Intelligence Engine (ui-ux-pro-max)

## Source & license
**nextlevelbuilder/ui-ux-pro-max-skill** — MIT · free · 100k+ stars · verified 2026-08-23.
Local Python search rules (BM25 + regex) — **no network and no keys** after installation.

## Installation (one time)
```bash
npx ui-ux-pro-max-cli init --ai universal   # installs into ./.agents/skills/
# Prerequisite: python3 present on the machine ✓
```

## Usage across the v2 pipeline
| Stage | Invocation |
|---|---|
| S3 system build | `--domain style --stack flutter` → palettes and fonts compatible with Flutter |
| S3 mockups | `--domain ux` → layout rules and the eight states |
| DFR check | attach search outputs to the dfr-signoff evidence as justification for each choice |

## Binding SOFI rules
1. Its outputs are **a filter, not the final verdict** — final approval belongs to dsn-lead, then DFR (Security + Quality).
2. Every color/font enters design-tokens and is never written directly into screens (tokens-only).
3. Flutter support takes priority (R2 decision: web and mobile share one unified stack) — React/Vue remain legacy secondary options.
4. Any suggestion contradicting KNOWLEDGE-CX-UIUX.md is rejected and the reason documented.

## Provenance
nextlevelbuilder · MIT · a SOFI wrapper over the original without modifying it.
