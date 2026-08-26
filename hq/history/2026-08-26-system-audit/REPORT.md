# System-Wide Investigation Report — 50-Agent Swarm Audit

> **Date:** 2026-08-26 · **Executor:** 50 read-only investigation agents, single parallel wave, zero writes to the system.
> **Scope:** entire SOFI tree (governance hq/, presentation layers, live deployment engine) + the sakk product (backend/admin/portal/mobile).
> **Coverage limits (honest):** sandbox denied `systemctl`, `ss`, `stat`, `sudo` for several probes; root-owned surfaces (`backups/`, crontab spool) unverifiable from this session — flagged where relevant.

---

## A) Architecture Overview

**Governance system (hq/):** hub layout `hq/{core,brain,engine,training,history}` · core hosts a strict DDD domain layer: shared-kernel + 15 bounded rooms (charter, contracts, capabilities manifests, 106 agent capsules of 4 files each) + context-map.yaml contracts + nexus registries. Presentation layers: `.opencode/agent` (canonical specs per Article 00) + `.kilo/agent` generated mirror; skills owned via room manifests (Σ=106). Deployment engine: Caddy GitOps (single-import chain), sakk-only active sites + guard 404, PHP-FPM sakk pool via unix socket, Cloudflare tunnel ingress.

**Product sakk:** Laravel 12.62 DDD-style backend (~326 routes across 11 domains, Sanctum, Redis queues), React 19 SPA admin (38 lazy chunks) + partner portal, Flutter mobile (Riverpod, secure storage). SQLite dev/test behind MySQL prod target. Frozen-contract discipline claimed via openapi-v2.

---

## B) Findings by Severity

### CRITICAL (act immediately)
| # | Finding | Evidence |
|---|---------|----------|
| C1 | **Live prod secrets world-readable**: `.env.production` mode 644 with real DB password, mail password, CCPayment secrets ×2, Stripe webhook secret (=issuing secret, single point of compromise); APP_KEY reused dev+prod | sakk/backend/.env.production:6,41,94 · .env:68,78,90–92 |
| C2 | **Finance FK chain CASCADE**: users→wallets→transactions (+aml_flags) all ON DELETE CASCADE — one user delete erases full money/compliance history | database/migrations/03_finance/squashed.sql:37-38,207-212 |
| C3 | **Ledger bound to MySQL-only table**: EloquentLedgerRepository → `ledger_entries` exists only in self-skipping v2-01 (sqlite skips, owner-frozen); DI-wired into live Deposit/Withdraw/Transfer actions → runtime failure on sqlite envs | DomainServiceProvider.php:47-48 · v2-01 |
| C4 | **Crash-looping systemd units**: jawaher-htdocs (missing WorkingDirectory + ExecStart=/usr/bin/php nonexistent) restarting every 3s; whatsapp.service points into purged tobacco-center tree, restarting every 5s; sofi-demo-reset.timer failing every 30min | systemctl units + journal evidence |
| C5 | **PayPal webhook fail-open + no retry**: signature path returns success if PAYPAL_WEBHOOK_ID unset; PAYMENT.CAPTURE.COMPLETED processed synchronously, exceptions swallowed → silent lost credits; idempotency claim runs BEFORE signature check (replay poisoning) | PayPalWebhookController.php:108-116,154-165 · web.php:42 |

### HIGH
| # | Finding | Evidence |
|---|---------|----------|
| H1 | Unidentified public listeners: 0.0.0.0:5500 (user uid) and :8080 (**root**) on all interfaces; MySQL-X `[::]:33060` exposed; UFW state unverified | /proc/net/tcp analysis |
| H2 | Web-reachable diagnostic `public/redis_test.php` leaks Redis status + connection info, unauthenticated | sakk/backend/public/redis_test.php |
| H3 | Auth gaps: verify-email self-verifies w/o token proof; changePin/verifyPin/disablePin/2fa-disable unthrottled (4-digit PIN online-brute-forceable); forgot-PIN user enumeration; device_mismatch flag stored but never enforced | AuthController.php:499-509,578-639 · AuthFlowController.php:164-176,246-248 |
| H4 | Contract fiction: openapi-v2 serves `/api/v2` vs backend 100% `v1/*`; ~275 live endpoints undocumented; holds/compliance/statement routes missing entirely — contract is DRAFT-NOT-FROZEN | openapi-v2.yaml:68-71 vs routes census 326 |
| H5 | SPA auth tokens (admin + partner) in localStorage, XSS-exfiltratable; no 401 interceptor/refresh (admin); portal 2FA flow dead-ends partners entirely | admin/api/client.js:2-12 · portal/AuthContext.jsx:37 |
| H6 | iOS not release-ready: zero entitlements files (FCM push dead), signing unconfigured; Google Maps API key committed unrestricted (needs bundle-id+SHA-1 restriction); Android release falls back to DEBUG key silently when keystore absent | ios entitlements absence · build.gradle.kts:71-75 · Info.plist:7-8 |
| H7 | Nightly encrypted backup **UNVERIFIABLE**: no visible artifacts, no cron/timer evidence reachable, zero restore-runbook for `.enc` anywhere | G36+H41 joint verdict |
| H8 | Doc-reality breaks created mid-flight by concurrent restructuring: root `memory_index/` removed while constitutional Article 05/09 + agents still cite it literally; `caddy→hq/engine` bridge gone while system-state/structure-standard still declare it; archive reports moved out of documented location | A1/A6 findings |
| H9 | Money-cast mismatch: columns migrated to DECIMAL(24,8) but ~30 model casts still `decimal:2` → silent sub-cent rounding on reads | VirtualCard/Wallet/Merchant/Agent models |
| H10 | `usd_only_cleanup` migration DELETEs non-USD wallets (money!) with intentional noop down(); committed as repeatable migration | 2026_08_17_000004:18-21 |
| H11 | Zero CI pipelines + zero mobile tests + money paths event-tested only (no Stripe charge/deposit/withdrawal test) — S6 shield law unmet | J50 census: 10 test files total |
| H12 | opcache.validate_timestamps contradicts doctrine: FPM override ini sets 1 (60s staleness) while README/Law documents Off; CLI/FPM see different values | /etc/php/8.5/fpm/conf.d/99-sakk-override.ini:18 |

### MEDIUM (selected, full lists in team sections above)
- Caddy perimeter: no HSTS at origin (edge must enforce); CSP only on sakk fallback/assets (not admin/portal SPAs, api, storage); block_sensitive misses `.git/`, `.sql`, `.bak`, keystores; security_headers absent on `/api/*`,`/webhooks/*`; **block_sensitive is DEAD for `/storage/*` (handle priority)** — latent upload exposure once files land; duplicate `/storage/*` block; `/portal*` 404-vs-assets intent conflict.
- Debug surface: env-gated money-mutating test endpoints (ccpayment deposit/withdraw, 3DS factory hardcoding user_id=122) — one APP_ENV slip = exposure; public unthrottled ccpayment/info pre-signature.
- Queue ops: no Horizon/worker provisioning anywhere despite redis driver; tokens:prune-expired scheduled line commented out; SendLoginAlertJob swallows throwables.
- Schema: users.email non-unique/non-indexed in base sqlite schema; wallets missing UNIQUE(user_id,currency); password_reset_codes created twice; CHECK constraints MySQL-only (sqlite dev never enforces balance≥0).
- Frontend: portal single-chunk monolith (351KB JS, zero splitting); no brotli/gzip precompression either app; React runtime duplicated in both bundles; IBM Plex fonts shipped twice (~223KB×2); admin Dashboard.jsx 67KB monolith; can() trusts `['*']` blindly; api_secret permanently re-revealable.
- Governance: phantom `gtw-lead` (7 gateway capsules report to nonexistent lead; dispatcher lacks dispatch/escalate senses); context-map v1 has ~7 dangling require-names; room contracts all empty placeholders; skills INDEX↔ledger ownership conflicts (mcp-builder, smartui-skill); SKILLS-ASSIGNMENT row-inflation 111 vs 106 unique; AGENTS.md cites nonexistent "Rule 6" in protocols.md.
- Hygiene: `__pycache__` committed to git; `.playwright-mcp/` resurrected post-purge; root stray `guide-top.png`; tracked-files-fight-their-own-gitignore (.opencode pkg trio); root-level `.env` gitignore gap; naming law violations (5 snake_case dirs incl. constitution_articles/gate_checklists/room_charters, ~17 SCREAMING docs); stale systemd-doc drift (CONFIG-OF-RECORD says token-mode, reality config-file mode; engine brain CONTEXT/HANDOFFS describe inverted/dead topology); N+1 hotspots (WalletController:128 paginate-without-with + TransactionResource unguarded card access top the list); riverpod 2.x vs 3.x; hive unmaintained + triple storage layers; simple-qrcode dormant lineage.
- Mobile arch: KYC/PIN gates enforced in UI/banner not router guards; deep links bypass PIN lock; mixed Riverpod idioms + 100+ setState in network paths.

---

## C) Hidden Discoveries

1. **No SSH daemon exists on this machine at all** — only xrdp-sesman present. Remote shell posture is xrdp-only (owner may intend this; it was invisible until probed).
2. The infamous "~48 unresolved class bindings" LSP errors in DomainServiceProvider are **stale-index false positives** — all 35 bindings resolve; fix = `composer dump-autoload` + LSP restart, zero code changes.
3. Phantom PSR-4 mapping `App\Domains\Qr\` in composer.json points to a nonexistent directory (ghost domain from a removed feature).
4. `.opencode/skills/{docx,pptx,xlsx}` vendor the same office toolkit three times (~2.07MB recoverable); design/slides/banner skills carry 6 accidental identical reference docs.
5. A dead symlink `/run/php/php-fpm.sock` → nonexistent target will confusingly fail anything using the default socket name.
6. Root-owned `config.yml.bak` sits inside the user's 0700 `~/.cloudflared/`; tunnel credentials.json is group-readable 0664.
7. The external archive violates its own spec: subdirs 775 + plan file 664 instead of 700/600 — and it contains the archived forbidden worktree as evidence.
8. cloudflared does per-hostname ingress itself (sakk/tobacco/owais → *.local + internal catch-all 404) — meaning the famous "Caddy catch-all" is NOT what unknown-subdomain visitors actually hit; CONFIG-OF-RECORD's whole model is stale.
9. `audit_log` hash-chained table (v2-04, MySQL-only) is created but its model binding is commented out — two parallel audit trails, the new one unreferenced.
10. Backend has zero `dd/dump/var_dump` leftovers and zero injection-capable raw SQL (56 raw hits, all parameterized/literals) — genuine hygiene bright spot.
11. Portal login hard-fails for any 2FA-enabled partner (flow simply doesn't exist client-side).
12. The i18n sweep left exactly 4 sanctioned literals (ر.س currency spec ×3 copies, message_ar wire samples) — verified independently.

---

## D) Recommendations (priority order)

**P0 — today (security/finance):**
1. Rotate everything in C1 (APP_KEY per-env, DB/mail passwords, CCPayment secrets, split Stripe webhook vs issuing secret); chmod 600 both env files + admin/.env; add root `.env*` gitignore rule; git-history sweep for leaks.
2. Identify & kill/rebind listeners 5500/8080; bind mysqlx to loopback; confirm UFW default-deny inbound (one sudo session).
3. Convert finance FKs CASCADE→RESTRICT (or SET NULL) via gated migration before G2/G3; archive usd_only_cleanup as one-off script.
4. Fix PayPal webhook: fail-closed on missing webhook-id, move idempotency AFTER signature, queue + reconcile command.
5. Delete public/redis_test.php; decide fate of the two crash-looping units (disable --now or repoint to /usr/bin/php8.5 + real paths).

**P1 — this week:**
6. Close auth gaps: token-proof email verification, throttle sensitive authenticated groups, enforce device_mismatch, generic enumeration messages.
7. Align money casts to DECIMAL(24,8) (guarded narrowing already exists in v2-03 pattern).
8. Provision queue workers (supervisor unit) or document Horizon decision; uncomment tokens prune.
9. Reconcile governance drift from the parallel restructure: restore-or-retire `memory_index` references (amend Articles 05/09 or recreate pointer), update system-state/structure-standard to post-bridge reality, close TKT-DRAFT-002, correct engine brain rows, fix bootstrap-live.sh comment baked into /etc header.
10. CI pipeline (GitHub Actions or local runner): phpunit suites + vitest on push; first money-path feature test (Stripe deposit happy-path + failure).
11. SPA auth: move to httpOnly-cookie-first, add 401 interceptor + refresh; implement portal 2FA verify flow; show-once for api_secret.

**P2 — next sprint:**
12. Contract reality: regenerate openapi from v1 routes (or version-bump plan), freeze with diff-check in CI; adopt ApiEnvelope in remaining controllers (KycController::getStatus).
13. Caddy hardening pass: extend block_sensitive regex, apply security_headers globally (server-level), import csp_sakk on SPA handles, dedupe /storage blocks, resolve /portal* intent, add HSTS at Cloudflare edge.
14. iOS release prep: entitlements (aps-environment, associated-domains), signing team, Maps-key restriction by bundle-id+SHA-1; Android CI guard against debug-signed releases.
15. Performance: vite-plugin-compression + portal route-splitting + shared chunk strategy; fix top N+1s (::with('card','recipient'), whenLoaded()); dedupe fonts via shared path.
16. Governance polish: create gtw-lead capsule or retarget 7 gateway senses to gtw-dispatcher-as-lead; mature provides/requires for top-5 traffic pairs; fix Rule-6 cross-ref; rename snake_case dirs in a mapped migration (Law 13 continuity table); untrack __pycache__/tracked-ignored trio; dedupe design-reference clones.
17. Backup truth: owner runs one root session (`crontab -l`, `ls -la backups`) — then write the missing decrypt/restore runbook and do one restore drill; tighten archive dirs to 700/600.

---

*Method note: findings carry their evidence inline (file:line). Sandbox-denied probes were reported as such rather than guessed. Nothing in the system was modified by this swarm.*
