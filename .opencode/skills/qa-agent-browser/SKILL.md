---
name: qa-agent-browser
description: Run an automated browser through a ready-made Vercel skill — navigation, clicks, form filling, and screenshots producing live evidence. Invoked in room 10 (Quality) to execute manual E2E cases and S5 gate evidence (live integration), and in room 02 for visual verification of competitor websites. Triggers — "open the browser", "test the screen", "live evidence", "agent browser", "browser automation skill".
---

# qa-agent-browser — Agent Browser (Vercel)

## Source
The `agent-browser` skill from **vercel-labs/agent-skills** (free) — github.com/vercel-labs/agent-skills.

## Interplay with the Playwright server
- **Playwright MCP** (enabled in opencode.json): the actual execution — navigation, screenshots, interaction.
- This skill: the usage methodology and the standard check cases run before every session.

## Binding SOFI rules
1. Every browser session produces **evidence**: screenshot path + steps + outcome (P-03.4).
2. S5 evidence (live integration) = screenshot + a visibly captured Envelope v1 response on the network.
3. No browser session outside the scope of the current RCCF work order (P-11.2).

## Provenance
vercel-labs · free · verified 2026-08-23.
