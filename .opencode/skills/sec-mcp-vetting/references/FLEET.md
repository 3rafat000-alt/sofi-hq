# MCP FLEET Registry — Fleet Vetting Record (INT-GTW-029)

> Operational sources: `opencode.json` (project) + `~/.config/opencode/opencode.json` (global).
> Every addition/change passes through the sec-mcp-vetting gate and is recorded here immediately.

| # | Server | Status | Source | Security note |
|---|---|---|---|---|
| 1 | Context7 | 🟢 ACTIVE | Project | Library documentation — networked reads from trusted sources |
| 2 | DeepWiki | 🟢 ACTIVE | Project | Repository verification — read-only |
| 3 | Sequential-Thinking | 🟢 ACTIVE | Project | Local, no external I/O |
| 4 | Chrome-DevTools | 🟢 ACTIVE | Project | Local browser — mind session data |
| 5 | Playwright | 🟢 ACTIVE | Project | Browser automation — same caution applies |
| 6 | Kitesurf | 🟢 ACTIVE | Project | Live visual guides |
| 7 | Dart-Flutter | 🟢 ACTIVE | Project (absolute path) | Dart/DTD tooling |
| 8 | GitHub | 🟢 ACTIVE | Global setup (token {env:GITHUB_TOKEN}) | Token permissions reviewed periodically |
| 9 | Filesystem-Scoped | 🟢 ACTIVE | Project | Scoped to the SOFI root exclusively |
| 10 | Crawl4AI | ⚪ GATED | Deliberately not enabled (INT-0006-M7) | Firecrawl alternative when needed |

**REJECTED:** none so far. **Rule:** any new server = full vetting before enablement, then a row here.
