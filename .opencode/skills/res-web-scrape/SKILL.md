---
name: res-web-scrape
description: A 100% free local competitor-scraping pipeline — the Tavily/Firecrawl replacement with no keys at all: discovery (local search/SearXNG) → deep scraping (Crawl4AI) → condensing (PageMap-style) → competitive analysis matrix → delivery to the Data room. Mandatory in room 02 for market and competitor research in S1, and in room 01 when evaluating a product opportunity. Triggers — "competitor analysis", "market research pipeline", "web scraping free", "crawl competitors", "research the market", "scrape a site", "competitive feasibility study".
---

# res-web-scrape — The Local Market-Intelligence Pipeline

> **Official SOFI policy (SOFI-HQ-INT-0003):** cloud Tavily/Firecrawl/Exa/Serper are prohibited — replaced by this fully self-hosted free chain.

## The four-stage chain

### 1) Discovery
```bash
# Option A: built-in search (websearch/webfetch tools) — zero installation
# Option B: self-hosted SearXNG (docker run -p 8080:8080 searxng/searxng) when large volume is needed
```
Output: a JSON list of 3–5 direct competitor domains (no tracking parameters).

### 2) Deep Scrape
**The instant option (zero installation) — Jina Reader:** prepend `https://r.jina.ai/` to the page URL and get clean Markdown content back, free with no key and no account.
```bash
curl -sL "https://r.jina.ai/https://<site>/pricing" > artifacts/scrape/<domain>-pricing.md
# verified live: HTTP 200 twice (INT-0006 annex 6 · 2026-08-23)
```
**The deep option (for large volume) — Crawl4AI — 🟢 installed and ready (2026-08-24):**
```bash
# The ready environment (no new install — v0.9.2 in an isolated venv + Chromium 151):
/home/es3dlll/.crawl4ai-venv/bin/crwl crawl https://competitor.com/pricing -o md-fit -O artifacts/scrape/competitor-pricing.md -bc
# or via the API: AsyncWebCrawler from crawl4ai (see MCP-REGISTRY §Crawl4AI)
```
Scrape the `/pricing`, `/features`, and `/about` pages of each competitor → clean Markdown.
Rules: ignore header/footer/ads · save every page to `artifacts/scrape/<domain>-<page>.md`.

**⚠️ Bot-blocking sites (verified experimentally 2026-08-24):** nngroup.com · baymard.com · martinfowler.com return empty content to automated scraping — use 🪁 Kitesurf manually with screenshots as evidence instead.

### 3) Condense
Convert every Markdown into an economical page map (PageMap pattern): headings, prices, features as key lines only — target ≤10% of original size (P-12.3).

### 4) Synthesize — Analysis & Delivery
Produce `projects/<prj>/<project>/brain/CONTEXT.md (competitive matrix)`:
| Competitor | Features | Pricing | Gaps | Lessons |
Then **sofi-handoff** to room 08 (dat) to generate a first-pass ERD from the functional gaps.

## Mandatory evidence (Law 4)
- A source link for every fact + the literal extracted line from it (LLM summarization forbidden as evidence P-03.3)
- Paths of the saved scrape files
- Page count + scrape duration (exit codes)

## Limits & prohibitions
- No scraping behind login and no unethical robots.txt bypassing — public sites only
- Default maximum volume: 30 pages/analysis — more requires an expanded RCCF work order
- Crawl4AI is installed and ready in an isolated venv outside the repository (~/.crawl4ai-venv) — invoke it by its absolute path

## Provenance
Original SOFI authorship (2026-08-23) over open tools: Crawl4AI Apache-2.0 · SearXNG AGPL · PageMap patterns AGPL.
