# SOFI Skills Index

> **⚖️ Binding ownership registry (2026-08-25):** every skill's ownership is defined in `hq/core/domain/rooms/<room>/capabilities/skills.yaml` and the full assignment record in `hq/core/domain/SKILLS-ASSIGNMENT.md` — this index is the invocation and description reference; ownership lives there.

> The register of every approved skill. Built/updated via `skill-forge`. Every skill enforces the sixteen laws (Laws 14-16 added 2026-08-26). Add a row when approving any skill (§6 of skill-forge).
> Audit 2026-09-05 (Phase B — gtw-dispatcher · GATE-OPEN ADR-20260905-GTW-FLUTTER-QA-ARCHITECT + Board conditions): **actual total 111 skills — disk match 111/111** (14 rooms · 109 agents · 16 laws). Prior audits: 2026-08-31 (9-axis fix) = 109/109 · 2026-08-24 = 106/106 (+3 operational gaps: str-agile-orchestrator · ops-sandbox-executor · sec-license-auditor companion). Counted on disk before writing, no guesses: `ls -d .opencode/skills/*/` = 111 · `ls .opencode/skills/*/SKILL.md | wc -l` = 111. verific: `hq/core/tooling/count_sync.py` = PASS (exit 0) · `hq/core/tooling/registry_guard.py` = PASS (exit 0).

## 🏭 Foundation (serving all rooms)

| Skill | Owner | Type | When to invoke |
|---------|--------|-------|-------------|
| [skill-forge](skill-forge/SKILL.md) | knw-lead | Meta | build/update/validate any SOFI skill |
| [sofi-evidence](sofi-evidence/SKILL.md) | knw-lead | Standard | evidence block (Law 4) before any delivery/gate |
| [sofi-handoff](sofi-handoff/SKILL.md) | knw-lead | Standard | RCCF ticket for hierarchical delivery (Law 3) |
| [sofi-project-spawn](sofi-project-spawn/SKILL.md) | ops-lead | Automation | birthing new projects: isolated tree + template copies + project memory init (L7) |
| [sofi-mcp-fleet](sofi-mcp-fleet/SKILL.md) | gtw-dispatcher | Training | MCP fleet curriculum: status board + 15 rooms' specialization + six binding rules (INT-0006-M3) |
| [sofi-boot](sofi-boot/SKILL.md) | gtw-dispatcher | Standard | the eight-step boot ritual for every session — constitution, memory, gates, then standing at the gate |
| [agent-reach](agent-reach/SKILL.md) | res-lead | Internet | 👁️ read & search 15+ platforms (Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, V2EX, Xueqiu, LinkedIn, RSS, web) — multi-backend routing, zero API fees (Panniantong/Agent-Reach 78K⭐) |

## 🌐 Internet capability (multi-platform)

| Skill | Owner | When to invoke |
|---------|--------|-------------|
| [agent-reach](agent-reach/SKILL.md) | res-lead | research/look-up: web URLs, GitHub, YouTube, Reddit, Twitter, Bilibili, XiaoHongShu, V2EX, Xueqiu, Xiaoyuzhou podcasts, RSS feeds, Exa semantic search |

## 🏛️ Room playbooks (one per room)

| Code | Skill | Owner | When to invoke |
|-----|---------|--------|-------------|
| 00 | [brd-decision-gate](brd-decision-gate/SKILL.md) | brd-ceo | fateful decisions: Board consultation + CEO decision + gate |
| 01 | [str-gate0-classify](str-gate0-classify/SKILL.md) | str-lead | Gate 0: classification + fast-track eligibility + priorities |
| 02 | [res-journey-map](res-journey-map/SKILL.md) | res-lead | research dossier + journey map + personas (Gate-1) |
| 03 | [dsn-design-handoff](dsn-design-handoff/SKILL.md) | dsn-lead | UI spec + tokens + a11y → frontend (Contract 03) |
| 03 | [dsn-design-system-gen](dsn-design-system-gen/SKILL.md) | dsn-lead | design system generation: 3-layer tokens + WCAG 2.2 + React/Flutter |
| 02 | [mobbin-scraper](mobbin-scraper/SKILL.md) | res-lead | visual platform pattern extraction (Mobbin/PageFlows/Land-book) per Protocol 18 |
| 03 | [design-system-extractor](design-system-extractor/SKILL.md) | dsn-lead | competitor design-token extraction + comparison vs SOFI system per Protocol 18 |
| 03 | [rtl-mirror-validator](rtl-mirror-validator/SKILL.md) | dsn-lead | RTL/Arabic layout validation checklist — signature gates DFR (Protocol 18) |
| 03 | [dsn-design-review](dsn-design-review/SKILL.md) | dsn-lead | design review: Nielsen + axes + P0/P1/P2 findings |
| 04 | [arc-adr](arc-adr/SKILL.md) | arc-lead | architecture decision: ADR + system design + migration |
| 05 | [bck-feature-build](bck-feature-build/SKILL.md) | bck-lead | backend feature build + tests + code evidence |
| 06 | [fnt-component-build](fnt-component-build/SKILL.md) | fnt-lead | component build + a11y + perf + screenshot |
| 06 | [fnt-ux-lint](fnt-ux-lint/SKILL.md) | fnt-lead | deterministic anti-slop + a11y checker before merge (CI-safe) |
| 07 | [mob-feature-build](mob-feature-build/SKILL.md) | mob-lead | mobile feature (Flutter/native) + state + perf |
| 07 | [mob-flutter-kb](mob-flutter-kb/SKILL.md) | mob-lead | local official Flutter/Dart knowledge gateway (docs + 757 videos) with citations |
| 08 | [dat-schema-migration](dat-schema-migration/SKILL.md) | dat-lead | schema/migration + PII check + rollback |
| 09 | [sec-threat-model](sec-threat-model/SKILL.md) | sec-lead | threat model + scan + pentest + security veto |
| 09 | [sec-mcp-vetting](sec-mcp-vetting/SKILL.md) | sec-lead | vetting gate for any MCP server before enablement ([FLEET.md](sec-mcp-vetting/references/FLEET.md)) |
| 10 | [qa-test-plan](qa-test-plan/SKILL.md) | qa-lead | quality gate (Gate 5): plan + execution + coverage |
| 10 | [qa-flutter-architect](qa-flutter-architect/SKILL.md) | qa-lead | Flutter QA architecture: 5-phase contract-conformance review + device-fingerprint perf/a11y evidence — advisory only, no gate verdicts (qa-lead · brd-cqo · C3) |
| 10 | [qa-react-architect](qa-react-architect/SKILL.md) | qa-lead | React/DDD QA architecture: 5-phase contract-conformance review + Web Vitals/Lighthouse/Bundle evidence — advisory only, no gate verdicts (qa-lead · brd-cqo · C3) |
| 11 | [ops-deploy-runbook](ops-deploy-runbook/SKILL.md) | ops-lead | deploy + migration + health check + rollback |
| 12 | [obs-incident-response](obs-incident-response/SKILL.md) | obs-lead | detection + alerting + incident response → AMYGDALA |
| 13 | [knw-brain-write](knw-brain-write/SKILL.md) | knw-lead | brain writing (Law 7): CORTEX/HIPPOCAMPUS/AMYGDALA |
| 14 | [gtw-intake-route](gtw-intake-route/SKILL.md) | gtw-dispatcher | intake: reformulation + routing + gate check |

---

## 📱 External pack — official Flutter/Dart (Mobile room 07)

From `github.com/flutter/agent-plugins` (the official Flutter team) — 22 free keyless Agent Skills supporting the [mob-feature-build](mob-feature-build/SKILL.md) playbook. Details + reinstallation in [FLEET.md](sec-mcp-vetting/references/FLEET.md).

- **Flutter (10):** add-integration-test · add-widget-preview · add-widget-test · apply-architecture-best-practices · build-responsive-layout · fix-layout-issues · implement-json-serialization · setup-declarative-routing · setup-localization · use-http-package
- **Dart (12):** add-unit-test · build-cli-app · collect-coverage · fix-runtime-errors · generate-test-mocks · migrate-to-checks-package · resolve-package-conflicts · run-static-analysis · setup-ffi-assets · use-ffigen · use-pattern-matching · use-primary-constructors

## 🔌 MCP layer (free local keyless servers)

Real configuration: the `mcp` section in `opencode.json` (source of truth) — **enabled:** context7 · sequential-thinking · playwright · chrome-devtools · dart-flutter · deepwiki — **ready disabled:** github (needs a free access token) · filesystem-scoped (duplicates native opencode tools). Full map + expansion in [FLEET.md](sec-mcp-vetting/references/FLEET.md). **Replacement policy (INT-0003): no server with a paid key or subscription — the self-hosted alternative always** (Tavily→SearXNG+Crawl4AI · Firecrawl→Crawl4AI · Exa/Serper→local search/SearXNG · Browserbase→local Playwright). Any new server passes the [sec-mcp-vetting](sec-mcp-vetting/SKILL.md) gate before enablement.

## 🌐 External pack — from agentskillsforall.com (approved 2026-07-17)

Two trusted sources, security-screened by the `skills` CLI (a risk report per skill). Installation with `--copy` = real files on the tree (Law 10), registered in `skills-lock.json`. **19 Tier-1 skills** (priorities: UI/UX · Flutter · Blade · HTML/CSS + mobile/QA/ops).

### From `anthropics/skills` (official Anthropic — all Low Risk)

| Skill | Rooms | Beneficiary agents |
|---------|------|--------------------|
| [frontend-design](frontend-design/SKILL.md) ⭐ | 03/06 | dsn-ui-designer · dsn-lead · fnt-lead — distinctive visual direction/typography/UI (292k installs) |
| [theme-factory](theme-factory/SKILL.md) | 03/06 | dsn-design-system · fnt-css-artisan — 10 color/font themes + generation (HTML/CSS) |
| [web-artifacts-builder](web-artifacts-builder/SKILL.md) | 06 | fnt-react-engineer · fnt-lead — React+Tailwind+shadcn/ui |
| [canvas-design](canvas-design/SKILL.md) | 03 | dsn-brand-designer · dsn-ui-designer — .png/.pdf visual art |
| [brand-guidelines](brand-guidelines/SKILL.md) | 03 | dsn-brand-designer — identity/colors/typography |
| [webapp-testing](webapp-testing/SKILL.md) | 10/06 | qa-manual-explorer · qa-automation-engineer — Playwright UI testing + screenshots |
| [skill-creator](skill-creator/SKILL.md) | 13 | knw-lead — building/improving/measuring skills (feeds [skill-forge](skill-forge/SKILL.md)) |
| [mcp-builder](mcp-builder/SKILL.md) | 04/09 | arc-integration-architect · sec — building MCP servers (feeds [sec-mcp-vetting](sec-mcp-vetting/SKILL.md)) |

### From `LambdaTest/agent-skills` (TestMu — test automation)

| Skill | Room | Agents | Risk |
|---------|------|---------|--------|
| [flutter-testing-skill](flutter-testing-skill/SKILL.md) ⭐ | 07 | mob-flutter-engineer — widget/integration/golden | Low |
| [laravel-dusk-skill](laravel-dusk-skill/SKILL.md) ⭐ | 05 | bck-blade-engineer — Blade/Laravel browser testing | Low |
| [phpunit-skill](phpunit-skill/SKILL.md) | 05 | bck-domain/api/code-reviewer — PHP/Laravel unit | Low |
| [playwright-skill](playwright-skill/SKILL.md) | 10/06 | qa-automation-engineer · fnt — multilingual E2E (16 sections) | Med |
| [cypress-skill](cypress-skill/SKILL.md) | 10/06 | qa-automation-engineer — E2E/component JS/TS | Low |
| [smartui-skill](smartui-skill/SKILL.md) | 10/03 | qa-design-auditor · dsn-a11y-specialist — visual regression | Med |
| [detox-skill](detox-skill/SKILL.md) | 07 | mob (React Native) | Low |
| [espresso-skill](espresso-skill/SKILL.md) | 07 | mob-platform-engineer (Android) | Low |
| [xcuitest-skill](xcuitest-skill/SKILL.md) | 07 | mob-platform-engineer (iOS) | Low |
| [appium-skill](appium-skill/SKILL.md) ⚠️ | 07 | mob — Android/iOS. **blocked until sec-lead review** | **Critical/Med** |
| [cicd-pipeline-skill](cicd-pipeline-skill/SKILL.md) | 11 | ops-cicd-engineer — GH Actions/Jenkins/GitLab/Azure | Low |

**⚠️ Security (Law 9):** the scanner rated `appium-skill` **Critical Risk** (0 actual alerts, but it runs device automation) — unused before passing [sec-threat-model](sec-threat-model/SKILL.md). `playwright`/`smartui` = Med. Mirror copies created by the CLI in `.agents/skills/` + `.pi/skills/` were deleted 2026-07-17 (cleanup; the sole copy is `.opencode/skills/`).

### Tier-2 — also installed (2026-07-17, 23 skills on the stack)

- **anthropics docs/content (7):** [docx](docx/SKILL.md) · [pdf](pdf/SKILL.md)⚠️High · [pptx](pptx/SKILL.md) · [xlsx](xlsx/SKILL.md) → 13-knw-doc-writer + 08-dat (xlsx/analytics) · [doc-coauthoring](doc-coauthoring/SKILL.md) → 13-knw · [internal-comms](internal-comms/SKILL.md) → 03-dsn-content-strategist · [algorithmic-art](algorithmic-art/SKILL.md)⚠️Med → 03-dsn-motion-designer
- **LambdaTest on-stack testing (10):** selenium · webdriverio · jest · vitest · mocha → 06-fnt + 10-qa · pytest · unittest → 08-dat + 10-qa · behat (PHP BDD) → 05-bck · cucumber → 10-qa · test-framework-migration → 10-qa-test-architect + bck-refactoring-surgeon
- **api-skill group ×6:** api-designer · api-analyzer · api-documentation → 05-bck-api-engineer + 04-arc-api-architect · api-compliance-checker → 09-sec-compliance-auditor + 08-dat-privacy-officer (GDPR/PCI) · api-ai-augmented → 04-arc-integration + mcp · api-fetcher-specific-domains → 05-bck

**⚠️ Additional security:** `pdf` = High Risk, `algorithmic-art` = Med (both execute scripts) — use cautiously within the owning room.

**Deliberately rejected (outside SOFI's stack):** Java (junit-5/testng/gauge/serenity/geb/selenide) · .NET (nunit/mstest/xunit/specflow/reqnroll) · Ruby (rspec/capybara) · codeception/puppeteer/protractor/nightwatchjs/testcafe/jasmine/karma/behave/lettuce/robot-framework/nemojs/testunit · `hyperexecute` (LambdaTest cloud only; SOFI is self-hosted) · slack-gif-creator · template-skill.

## Index rules

- Every new skill → a row here **and** an approval decision in `hq/brain/cortex-decisions.md` (Law 7).
- Naming: room skill `<prefix>-<kebab>`, shared `sofi-<kebab>`.
- No duplication: search here before building a new skill (skill-forge §step 6).
- Every external skill names beneficiary agents → must be reflected in each such agent's file (skills section) — verified mechanically via grep.
- Next expansion (optional, via skill-forge when needed): individual-agent skills inside each room (e.g., `sec-pentest`, `fnt-a11y-audit`, `bck-queue`) — derived from the room playbook.

*Last updated: 2026-07-17.*

## 🆕 Arsenal batch 2026-08-23 (SOFI-HQ-INT-0003)

| Skill | Room | Type | Role |
|---------|--------|-------|-------|
| [systematic-debugging](systematic-debugging/SKILL.md) | all engineering | behavioral (obra/superpowers·MIT) | four-phase debugging methodology — ally of the anti-loop rule |
| [brainstorming](brainstorming/SKILL.md) | 01·02·03 | behavioral (obra/superpowers·MIT) | mandatory ideation before S1/S3 for unprecedented features |
| [writing-plans](writing-plans/SKILL.md) | 01·04 | behavioral (obra/superpowers·MIT) | multi-step plans inside RCCF (L5) |
| [dsn-design-intelligence](dsn-design-intelligence/SKILL.md) | 03 | ui-ux-pro-max wrapper (MIT) | design system generation — S3/DFR — Flutter priority (R2) |
| [dsn-web-design-guidelines](dsn-web-design-guidelines/SKILL.md) | 03·06·07 | vercel-labs wrapper | web standards before screen approval |
| [qa-agent-browser](qa-agent-browser/SKILL.md) | 10·02 | vercel-labs wrapper | live-evidence browser atop Playwright MCP |
| [res-web-scrape](res-web-scrape/SKILL.md) | 02·01 | original SOFI authorship | free local competitor scraping pipeline (Tavily/Firecrawl alternative) |
| [sofi-agent-eval](sofi-agent-eval/SKILL.md) | 13·00 | original SOFI authorship (P0 self-development initiative) | periodic agent quality evaluation — weighted five-dimension rubric + monthly/quarterly mechanism |
| [knw-knowledge-harvest](knw-knowledge-harvest/SKILL.md) | 13 (executor: 02) | original SOFI authorship (P2) | quarterly knowledge harvest ritual from elite sources via Crawl4AI/Kitesurf |

## 🆕 Kilo provisioning batch 2026-08-24 (second operating-channel bridge)

| Skill | Room | Type | Role |
|---------|--------|-------|-------|
| sofi-boot | approved — Foundation table |

*Last updated: 2026-08-24 (evening) — INT-GTW-016 audit: linked 38 external skills + corrected total 96→99 by actual disk sweep.*

## 📦 Linked External (audit 2026-08-24 — closing the linking gap)

| Family | Skills (38) |
|---------|---------------|
| API (6) | [api-ai-augmented](api-ai-augmented/SKILL.md) · [api-analyzer](api-analyzer/SKILL.md) · [api-compliance-checker](api-compliance-checker/SKILL.md) · [api-designer](api-designer/SKILL.md) · [api-documentation](api-documentation/SKILL.md) · [api-fetcher-specific-domains](api-fetcher-specific-domains/SKILL.md) |
| Dart (12) | [dart-add-unit-test](dart-add-unit-test/SKILL.md) · [dart-build-cli-app](dart-build-cli-app/SKILL.md) · [dart-collect-coverage](dart-collect-coverage/SKILL.md) · [dart-fix-runtime-errors](dart-fix-runtime-errors/SKILL.md) · [dart-generate-test-mocks](dart-generate-test-mocks/SKILL.md) · [dart-migrate-to-checks-package](dart-migrate-to-checks-package/SKILL.md) · [dart-resolve-package-conflicts](dart-resolve-package-conflicts/SKILL.md) · [dart-run-static-analysis](dart-run-static-analysis/SKILL.md) · [dart-setup-ffi-assets](dart-setup-ffi-assets/SKILL.md) · [dart-use-ffigen](dart-use-ffigen/SKILL.md) · [dart-use-pattern-matching](dart-use-pattern-matching/SKILL.md) · [dart-use-primary-constructors](dart-use-primary-constructors/SKILL.md) |
| Flutter (10) | [flutter-add-integration-test](flutter-add-integration-test/SKILL.md) · [flutter-add-widget-preview](flutter-add-widget-preview/SKILL.md) · [flutter-add-widget-test](flutter-add-widget-test/SKILL.md) · [flutter-apply-architecture-best-practices](flutter-apply-architecture-best-practices/SKILL.md) · [flutter-build-responsive-layout](flutter-build-responsive-layout/SKILL.md) · [flutter-fix-layout-issues](flutter-fix-layout-issues/SKILL.md) · [flutter-implement-json-serialization](flutter-implement-json-serialization/SKILL.md) · [flutter-setup-declarative-routing](flutter-setup-declarative-routing/SKILL.md) · [flutter-setup-localization](flutter-setup-localization/SKILL.md) · [flutter-use-http-package](flutter-use-http-package/SKILL.md) |
| Test frameworks (10) | [behat-skill](behat-skill/SKILL.md) · [cucumber-skill](cucumber-skill/SKILL.md) · [jest-skill](jest-skill/SKILL.md) · [mocha-skill](mocha-skill/SKILL.md) · [pytest-skill](pytest-skill/SKILL.md) · [selenium-skill](selenium-skill/SKILL.md) · [test-framework-migration-skill](test-framework-migration-skill/SKILL.md) · [unittest-skill](unittest-skill/SKILL.md) · [vitest-skill](vitest-skill/SKILL.md) · [webdriverio-skill](webdriverio-skill/SKILL.md) |
> ✅ **Owner decision executed (INT-GTW-023 · 2026-08-24):** 28 dead links pointed to `shared/testmu-cloud-reference.md` and `puppeteer-skill/reference/cloud-integration.md` — files never shipped by the vendor — deleted by his decision: 18 fully deleted lines + 9 surgical trims from rows mixing live and dead links + 2 spots with bare paths. Zero residue (grep verified). Working vendor files untouched otherwise.

## 🎨 Absorbed from .agents (INT-GTW-027 · 2026-08-24)

The seven design and creative production skills — moved from `.agents/skills/` into their canonical home then the source folder deleted entirely:

| Skill | Role |
|---|---|
| [banner-design](banner-design/SKILL.md) | platform banner and ad design |
| [brand](brand/SKILL.md) | brand voice, identity, messaging |
| [design](design/SKILL.md) | comprehensive design: logos, CIP, decks, icons |
| [design-system](design-system/SKILL.md) | three-layer tokens and component specs |
| [slides](slides/SKILL.md) | strategic HTML decks with Chart.js |
| [ui-styling](ui-styling/SKILL.md) | shadcn/Tailwind interface styling |
| [ui-ux-pro-max](ui-ux-pro-max/SKILL.md) | searchable UI/UX intelligence (79 patterns) |

## ⚠️ Invocation disambiguation (INT-GTW-029)

| Intent | Correct skill |
|---|---|
| generate a complete design system from a product description (room 03) | dsn-design-intelligence |
| build/document an existing design system step by step | design-system · dsn-design-system-gen |
| general creative design (logo/CIP/deck) outside room 03 | design · slides · banner-design |
