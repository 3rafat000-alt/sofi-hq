# 🛰️ MCP-REGISTRY — SOFI Server Fleet Registry

> **Governing doctrine:** a 100% free arsenal with no paid keys (INT-0003) · every new addition/activation must pass the `sec-mcp-vetting` check · fleet ownership: Gateway room (14).
> **Last updated:** 2026-08-23 · INT-0006 maintenance (documentation: `hq/brain/handoffs/SOFI-HQ-INT-0006.md`) · unified professional naming (Annex 4)

---

## 📊 Quick Status Board

| # | Icon | Name | Type | Status |
|---|---------|-------|-------|--------|
| 1 | 📚 | Context7 | remote ☁️ | 🟢 operational |
| 2 | 🌌 | DeepWiki | remote ☁️ | 🟢 operational |
| 3 | 🧠 | Sequential-Thinking | local 💻 | 🟢 operational |
| 4 | 🎭 | Chrome-DevTools | local 💻 | 🟢 operational |
| 5 | 🕸️ | Playwright | local 💻 | 🟢 operational |
| 6 | 🪁 | Kitesurf | local→cloud ☁️ | 🟢 operational |
| 7 | 🎯 | Dart-Flutter | local 💻 | 🟢 operational |
| 10 | 🕷️ | Crawl4AI | local source install (pip venv) | 🟢 operational — successful live scrape · via `crwl`/API (no MCP server in the source build) |
| 8 | 🐙 | GitHub | local 💻 | 🟢 operational |
| 9 | 🗂️ | Filesystem-Scoped | local 💻 | 🟢 operational — scoped to the SOFI folder exclusively |

> **Tool fleet = 10 · active MCP servers = 9** (INT-GTW-024 for count unification): the 🕷️ Crawl4AI entry is deliberately disabled until a new decision (the open Firecrawl alternative · INT-0006-M7) · the GitHub server runs via global config `~/.config/opencode/opencode.json`, not project config.

---

## 🧠 Section One — Knowledge & Research *(rooms 02 Research · 13 Knowledge)*

### 📚 Context7 — the Live Documentation Library
- **What it does:** fetches up-to-the-minute documentation for any library/framework with official code examples.
- **When to use it:** before writing code against any library — your general memory may be stale.
- **Priority:** the first source of documentation, ahead of web search.

### 🌌 DeepWiki — the Open-Repository Brain
- **What it does:** answers questions about any GitHub repository, grounded in its code and docs.
- **When to use it:** understanding an open-source project's structure, studying competitors, extracting architectural patterns, **verifying that any tool actually exists before believing its name** (the HiveFence lesson).
- **Note:** the official address after service migration: `mcp.deepwiki.com/mcp` (documented in INT-0006).

### 🧠 Sequential-Thinking — the Stepwise Thinking Board
- **What it does:** an organized step-by-step thinking space, reviewable and branchable, for complex problems.
- **When to use it:** architectural analyses, diagnosing intertwined failures, pivotal decisions before presenting them to the board.

## 🎭 Section Two — Automated Browser *(rooms 03 Design · 06 Frontend · 10 Quality · 02 Research)*

### 🎭 Chrome-DevTools — the Local Browser Lab
- **What it does:** drives a real Chrome: navigation, clicking, screenshots, DOM reading, network and performance tracing.

### 🕸️ Playwright — Comprehensive Professional Automation
- **What it does:** the same browser capabilities + multi-browser support and long test scenarios.
- **Practical difference:** structured E2E tests → Playwright · quick visual inspection → Chrome-DevTools.

### 🪁 Kitesurf — the Cloud Browser (fleet jewel ✨)
- **What it does:** a real cloud browser on Cloudflare infrastructure — **no account, no key, no cost**, consuming none of your machine's resources.
- **When to use it:** the default live inspection of any site/interface, screenshot evidence for deliveries (Law 4).
- **History:** activated by direct owner order + a signed security-vetting card (INT-0005).

## 🎯 Section Three — Development Tools *(rooms 05 Backend · 07 Mobile)*

### 🎯 Dart-Flutter — the Smart Flutter/Dart Cockpit
- **What it does:** connects agents to live Flutter apps: hot reload/restart, runtime error analysis, package and emulator management.
- **Actual architecture:** the official `dart_mcp_server v1.1.1` runs on top of the owner's preinstalled SDK (Flutter 3.44.1 · Dart 3.12.1) at its official home `~/snap/flutter/common/flutter`.
- **Caveat:** the built-in `dart mcp` command does not exist in this version — the guaranteed path is the absolute path in settings.

### 🕷️ Crawl4AI — the Website-to-Knowledge Factory (the open Firecrawl alternative) — 🟢 **running live**
- **What it does:** scrapes any website and returns **clean Markdown or structured JSON** ready for AI — exactly Firecrawl's idea and work, but **open-source Apache-2.0 running locally with no key or account** (literally compliant with the INT-0003 doctrine).
- **Actual structure (owner decision: drop Docker, install from source):** an isolated Python environment at `~/.crawl4ai-venv` on **v0.9.2 from official PyPI** · used via the `crwl` CLI tool and the `AsyncWebCrawler` API · official Chromium 151 browser at `/root/.cache/ms-playwright`.
- **Explicit note:** the pip build ships no MCP/SSE server (exclusive to the Docker image) — hence the opencode.json entry is deliberately disabled until a new owner decision (options: a private MCP bridge or returning to Docker).
- **History:** explicit owner request (2026-08-23) · DeepWiki verification against the official repository · the owner's network drops large downloads, so a curl-resume downloader was used for heavy files plus a self-healing loop for small packaging (19 cycles) — successful live test: example.com returned 200 within two seconds.
- **Relation to Kitesurf:** they operate side by side — 🪁 for interactive visual live inspection, 🕷️ for massive programmatic scraping and turning it into structured knowledge.

## 🔤 Section Four — LSP Language Servers *(all technical rooms)*

> **Status:** 🟢 fully enabled (`"lsp"` explicit in settings) — previously completely disabled due to missing servers; all were installed (INT-0006 Annex 4).

| Language | Server | Covers |
|------|--------|------|
| 🎯 Dart/Flutter | `dart language-server` (from the owner SDK) | .dart — mobile and frontend rooms |
| 🟨 TypeScript/JS | typescript-language-server | .ts .tsx .js .jsx |
| 🐍 Python | pyright-langserver | .py — scripts and tooling |
| 🐘 PHP/Laravel | intelephense | .php — backend room |

## ⚪ Section Five — Settled by Owner Order (2026-08-23)

The two previously suspended servers were **activated with documented security vetting** (INT-0006 Annex 5):
- 🐙 **GitHub:** the token was extracted from the owner's own Git credentials (his own account) · live verification HTTP 200 + server handshake v0.6.2 ✅
- 🗂️ **Filesystem-Scoped:** its scope was tightened to `/home/es3dlll/Desktop/SOFI` exclusively — it sees nothing outside.

> ⚠️ Security note for the registry: the GitHub token has broad scopes (repo+workflow+delete_repo) — acceptable on a single-user personal machine; a reduced-scope token is recommended if the team grows.

---

## 👥 Team Enablement Guide — who uses what?

| Room | Primary Servers | Existing Driving Skill |
|--------|------------------|---------------------------|
| 02 Research | 🌌 DeepWiki · 📚 Context7 · 🪁 Kitesurf · 🕷️ Crawl4AI | `res-web-scrape` · visual competitor checks + structured scraping |
| 01 Strategy | 🧠 Sequential-Thinking · 🌌 DeepWiki · 📚 Context7 · 🕷️ Crawl4AI | classification built on verification + market scraping |
| 03 Design | 🪁 Kitesurf · 🎭 Chrome-DevTools | `dsn-design-review` (live visual audit) |
| 05 Backend | 📚 Context7 · 🧠 Sequential-Thinking | Laravel/PHP documentation before any code |
| 06 Frontend | 🎯 Dart-Flutter · 📚 Context7 · 🕸️ Playwright | `fnt-component-build` · `fnt-ux-lint` |
| 07 Mobile | 🎯 Dart-Flutter · 📚 Context7 | `mob-feature-build` · `dart-fix-runtime-errors` |
| 09 Security | 🌌 DeepWiki · 🪁 Kitesurf | `sec-mcp-vetting` · `sec-threat-model` |
| 10 Quality | 🕸️ Playwright · 🪁 Kitesurf · 🎭 Chrome-DevTools | `qa-agent-browser` · `qa-test-plan` |

### 📏 Binding Usage Rules
1. **Before any code against a library** → 📚 Context7 first (no improvising from memory).
2. **Any claim about an external repository** → verify with 🌌 DeepWiki (HiveFence lesson: invented names do exist!).
3. **Any visual delivery evidence** → 🪁 Kitesurf by default (live screenshots = Law 4).
4. **A complex branching problem** → 🧠 Sequential-Thinking before deciding.
5. **A new server?** → self-activation is forbidden — the `sec-mcp-vetting` gate is mandatory.
6. **Everything free** — any server demanding a paid key is auto-rejected (INT-0003).

---

## 📜 Fleet Change Log
| Date | Event | Reference |
|---------|-------|--------|
| earlier | birth of the free arsenal + replacement policy | INT-0003 · CORTEX.md |
| 2026-08-23 | 🪁 Kitesurf joins by owner order + security vetting | INT-0005 |
| 2026-08-23 | 🛠️ DeepWiki fixed (address migration) + 🎯 Dart-Flutter (owner SDK + dart_mcp_server 1.1.1) | INT-0006 |
| 2026-08-23 | 📋 unified organization & documentation + sofi-mcp-fleet training curriculum + 106 agents injected | INT-0006 annexes 2–3 |
| 2026-08-23 | ✨ unified professional naming (Title-Case) + 🔤 LSP fully powered (4 languages) | INT-0006 annex 4 |
| 2026-08-23 | 🐙🐙 GitHub activated (connected owner token + live handshake) and Filesystem-Scoped (scoped to SOFI folder) — **fleet 9/9 🟢** | INT-0006 annex 5 |
| 2026-08-23 | 🕷️ birth of Crawl4AI — open Firecrawl alternative by owner order: official Docker + resumable downloader + SSE wired to the fleet (fleet → 10) | INT-0006 annex 7 |
