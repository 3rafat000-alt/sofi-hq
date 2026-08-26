---
name: knw-knowledge-harvest
description: "knw-knowledge-harvest — harvesting external knowledge and organizing it into the Knowledge room"
mode: subagent
---
#  knw-knowledge-harvest — The Periodic Knowledge Harvest Ritual

```yaml
name: knw-knowledge-harvest
version: 1.0
room: 13-knowledge (owner) · 02-research as the scraping executor
authority: OWNER-DIRECTIVE 2026-08-24 — SOFI self-development initiative (item P2-10)
cadence: quarterly (January/April/July/October) + on owner request or when an impactful new technology appears
tools: 🕷️ Crawl4AI (crwl CLI) for automated scraping · 🪁 Kitesurf for bot-blocking sites
triggers_ar: ["knowledge harvest", "scrape elite sources", "refresh external knowledge"]
triggers_en: ["knowledge harvest", "scrape elite sources", "refresh external knowledge"]
```

## 🎯 Purpose
Keep SOFI's external knowledge **periodically fresh** instead of relying on stale training memory — by re-scraping elite sources every quarter and updating the injection documents in `hq/core/`.

## ⬛ Elite Sources List (the official list — reviewed quarterly)

| Category | Source | Status |
|-------|--------|--------|
| UX laws | lawsofux.com (+ individual pages) | ✅ automated scraping works |
| DDD | learn.microsoft.com DDD-microservices · khalilstemmler.com | ✅ works |
| React | react.dev/learn | ✅ works |
| Flutter | docs.flutter.dev/app-architecture (+ local KB base `mob-flutter-kb`) | ✅ works |
| Next.js (legacy only — R2) | nextjs.org/docs | ✅ works |
| Agency team design | anthropic.com/engineering (effective-agents + multi-agent articles) | ✅ works |
| Commercial CX | nngroup.com · baymard.com | ⚠️ **both block bots** ← manual harvest via 🪁 Kitesurf only |
| Architecture patterns | martinfowler.com | ⚠️ blocks bots ← 🪁 |

## 🔄 Execution Protocol
1. **Prepare the season folder:** `hq/training/internet_knowledge/harvest-YYYY-QN/` (never pollute the original folder).
2. **Automated scrape:** for each non-blocking source:
   `~/.crawl4ai-venv/bin/crwl crawl <URL> -o md-fit -O <outfile> -bc` (200s timeout, log to `_harvest.log`)
3. **Bot-blocking sites:** a manual 🪁 Kitesurf session with screenshots as evidence (Law 4) — see the 2026-08-23 session pattern in `projects/_intake/evidence-*`.
4. **Synthesis:** update `_SYNTHESIS-GAP-ANALYSIS.md` with new findings → propose amendments to the injection documents (`knowledge-cx-uiux.md` · `ddd-capsule.md` · engineer prompts).
5. **Approval:** any change to `hq/core/*` passes through brd-ceo before application (no self-amendment of the constitution).
6. **Documentation:** log an ADR into CORTEX with the evidence (files + sizes + dates).

## 📜 Institutional Precedent (First Harvest — 2026-08-24)
21 files ~150KB: the six UX laws + the DDD trio + React/Flutter/Next + Anthropic ×2.
**Hard-won lessons:** (a) bot-blocking sites are detected early by their tiny size (450b = refusal), so attempts aren't burned. (b) `-o md-fit` reduces noise. (c) Intermittent connectivity does not hinder crwl because pages are usually lightweight — unlike heavy library downloads.
