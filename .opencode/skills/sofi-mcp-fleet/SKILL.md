---
name: sofi-mcp-fleet
description:
  The unified training & enablement curriculum for the MCP server fleet in SOFI — status board, each of the 15 rooms' specialization, the six binding rules, LSP language servers, and decision recipes (which server for what). Triggers — "MCP fleet", "which MCP server", "MCP training", "server usage", "how do I use the servers", "which MCP for".
owner: gtw-dispatcher
type: Standard
rooms: all-15
---

# 🛰️ sofi-mcp-fleet — The MCP Fleet Curriculum

> **Doctrine:** a 100% free arsenal (INT-0003) · any new addition/enablement passes `sec-mcp-vetting` mandatorily · living reference: [`hq/core/standards/mcp-registry.md`](../../../hq/core/standards/mcp-registry.md) · maintenance log: `hq/brain/handoffs/SOFI-HQ-INT-0006.md`

---

## 📊 Current fleet (9 servers + 4 language servers)

| Icon | Server | Type | One-line function |
|---------|--------|-------|---------------|
| 📚 | Context7 | Remote | Up-to-the-minute library documentation with official examples |
| 🌌 | DeepWiki | Remote | Q&A about any GitHub repository from its code and docs |
| 🧠 | Sequential-Thinking | Local | Structured step-by-step thinking for complex problems |
| 🎭 | Chrome-DevTools | Local | A real Chrome browser: navigation, screenshots, DOM, network |
| 🕸️ | Playwright | Local | Professional browser automation and long E2E test suites |
| 🪁 | Kitesurf | Cloud | Free cloud browser without an account — the default live inspection tool |
| 🎯 | Dart-Flutter | Local | Flutter/Dart cockpit: hot reload, runtime errors, tooling |
| 🕷️ | Crawl4AI | Local container | Site scraping → structured Markdown/JSON — the open Firecrawl alternative (port 11235) |
| 🐙 | GitHub | Local | Repository management: issues, PRs, files — with the owner's connected token |
| 🗂️ | Filesystem-Scoped | Local | File read/write — **scoped to the SOFI folder exclusively** |

**🔤 LSP language servers (enabled strongly):** Dart/Flutter · TypeScript/JS · Python · PHP/Laravel — deeper code understanding and precise symbol navigation.

> **Complementary relationship:** 🪁 Kitesurf for interactive live visual inspection · 🕷️ Crawl4AI for bulk programmatic scraping converted into structured knowledge.

---

## 🏛️ Room specialization — who uses what?

| Room | Code | Primary servers | Specialization note |
|--------|------|-------------------|----------------|
| Boardroom | brd (00) | 🧠 · 🌌 · 📚 | Thinking before decisive decisions + source verification |
| Strategy | str (01) | 🧠 · 🌌 · 📚 | Classification and framing built on verification, not assumption |
| Research | res (02) | 🪁 · 🌌 · 📚 | Live visual competitor inspection + res-web-scrape skill for local scraping |
| Design | dsn (03) | 🪁 · 🎭 | Auditing designs on live screens (dsn-design-review) |
| Architecture | arc (04) | 🧠 · 🌌 · 📚 | Studying architecture patterns from proven repositories before an ADR |
| Backend | bck (05) | 📚 · 🧠 | Laravel/PHP documentation before any line of code + PHP LSP |
| Frontend | fnt (06) | 🎯 · 📚 · 🕸️ | Building + testing interfaces on unified Flutter (R2 decision) |
| Mobile | mob (07) | 🎯 · 📚 | Instant hot reload after every change — per the server's own instructions |
| Data | dat (08) | 📚 · 🧠 | Schemas and migrations done deliberately without improvisation |
| Security | sec (09) | 🌌 · 🪁 · 🛡️ | Owner of the sec-mcp-vetting gate and the owner's veto |
| Quality | qa (10) | 🕸️ · 🪁 · 🎭 | Organized E2E + visual evidence for deliveries (Law 4) |
| Operations | ops (11) | 🕸️ · 🎭 | Health checks and screenshot-documented deployment |
| Observability | obs (12) | 🎭 · 🪁 | Visual monitoring of live boards and indicators |
| Knowledge | knw (13) | 🌌 · 📚 | Delivering knowledge with sourced references |
| Gateway | gtw (14) | Full supervision 🛡️ | Fleet routing + the vetting gate for any addition |

---

## 📏 The six binding rules (every agent in every room)

1. **Before any code against a library** → 📚 Context7 first. Your general memory may be stale; live documentation is the judge.
2. **Any claim about an external repository or tool** → 🌌 DeepWiki to verify before asserting. *(The documented HiveFence lesson: external intelligence "invented" non-existent tools and we believed it!)*
3. **Visual delivery evidence** → 🪁 Kitesurf by default (live screenshots = Law 4).
4. **A complex branching problem** → 🧠 Sequential-Thinking before any decision or diagnosis.
5. **A new MCP server?** → self-enablement absolutely forbidden — the `sec-mcp-vetting` gate is mandatory (violation = L2+).
6. **Everything is free** — any server demanding a paid key is auto-rejected and replaced with a local alternative (INT-0003 policy).

---

## 🧭 Quick decision recipes

| Situation | Correct server |
|--------|----------------|
| "How do I write X in Flutter/Laravel/React?" | 📚 Context7 |
| "What is this open-source project's structure? Does this tool even exist?" | 🌌 DeepWiki |
| "Inspect this site/interface and give me image proof" | 🪁 Kitesurf (or 🎭 locally) |
| "Run a long, organized browser test suite" | 🕸️ Playwright |
| "Apply my change to a Flutter app and see the result instantly" | 🎯 Dart-Flutter (hot reload) |
| "A tangled problem I don't know where to start with" | 🧠 Sequential-Thinking, then diagnose |

## ⚖️ Constitutional linkage
- **Law 4 (Evidence):** browser screenshots and server outputs are approved evidence — attach them in every delivery.
- **Law 3 (Delivery):** server results are working tools — delivery stays hierarchical through your room lead.
- **Law 9 (Responsibility):** you own what they fetch — verify before passing any result upward.
