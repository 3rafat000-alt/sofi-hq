# sakk — The Active Project

> **Status (2026-09-05):** **DORMANT** — the live project files were archived on 2026-08-25 during
> the sakk-only cleanup. The `sakk/brain/` (PRD + decisions + handoffs + lessons) and the codebases
> (`backend/` + `mobile/` + `apps/`) live in the archive. This directory is a placeholder
> ready to be re-spawned.

> **Mission:** a digital-wallet platform for the Saudi market with KYC/AML, Mada/Apple Pay
> integration, and full Arabic UX (RTL + Law 11 voice).

> **Stack (per Stack Lock R3):**
> - **Backend:** Laravel 11+ · PHP 8.3+ · PostgreSQL 16+ · Redis 7+ · Pest 3+
> - **Web (admin + portal):** React 19 + Vite
> - **Mobile:** Flutter 3.22+ · Dart 3+ · Riverpod

---

## The sakk-only cleanup (2026-08-25)

> Source: `hq/core/system-state-current.md` + `ADR-20260831-SAKK-DOUBLE-VERIFY`.

On 2026-08-25 (owner directive), all non-sakk projects and the sakk active codebase were archived
to `/home/es3dlll/Desktop/SOFI-archive-20260825-2040/` for cleanup. This is documented in
CORTEX. The sakk project remained the **only active project** with its `brain/` intact.

> The sakk `brain/` (PRD + decisions + handoffs + lessons) was preserved in the archive along with
> the codebases. The on-disk `sakk/` directory is **a placeholder** ready to be re-spawned via
> `sofi-project-spawn` or by restoring from the archive.

---

## How to restore sakk (when needed)

```bash
# Option A: full restore from archive
bash /home/es3dlll/Desktop/SOFI-archive-20260825-2040/restore.sh projects/sakk

# Option B: re-spawn fresh from this placeholder
# (uses the same template — copy CONTEXT/DECISIONS/HANDOFFS/LESSONS from archive)
"sofi-project-spawn sakk"

# Option C: just re-read the PRD
# (the PRD was the only thing preserved in the live tree on 2026-09-05)
```

---

## The sakk PRD (what the project is)

> Source: `projects/sakk/brain/CONTEXT.md` (in archive) — the PRD v2.0.

**Vision:** a digital-wallet platform for the Saudi market that combines the ease of modern
fintech apps with full Arabic UX, KYC/AML compliance, and integration with Mada + Apple Pay.

**Core features:**
- User onboarding with KYC (national ID / Absher)
- Wallet (topup via Mada/Apple Pay, transfer P2P, bill payment)
- Merchant payments (QR + online checkout)
- Admin (KYC review · fraud monitoring · reports)
- Arabic-first UX (RTL + Law 11 voice)

**Sprints:** 6 sprints (12 weeks MVP).

**Compliance:** PCI-DSS aware (Mada integration), AML/KYC, GDPR for EU users, PII protection via
`loc-privacy-officer` (Phase 3).

**Stakeholders:** Owner (sponsor) · `str-lead` (product) · `bck-lead` (backend) · `fnt-lead` (web) ·
`mob-lead` (mobile) · `qa-lead` + `brd-cqo` (quality) · `sec-lead` (security) · `obs-lead` (observability).

---

## The sakk memory structure (when re-spawned)

```
sakk/
├── README.md                       ← this file
├── brain/
│   ├── CONTEXT.md                  ← PRD v2.0
│   ├── DECISIONS.md                ← project-level decisions
│   ├── HANDOFFS.md                 ← task handoffs within sakk
│   └── LESSONS.md                  ← lessons learned
├── backend/                        ← Laravel 11+ codebase
│   ├── app/
│   │   ├── Domains/                ← 16 DDD domains
│   │   ├── Http/
│   │   └── Providers/
│   ├── database/migrations/         ← 45+ migrations
│   ├── routes/
│   └── tests/                      ← Pest 3+ (1309 tests in cache)
├── mobile/                         ← Flutter 3.22+ codebase
│   ├── lib/
│   │   └── features/               ← 22 features
│   └── test/
├── apps/                           ← React 19 + Vite
│   ├── admin/                      ← 28 admin pages
│   └── portal/                     ← user-facing portal
└── docs/                           ← supplementary
```

---

## The sakk agents involved (per `hq/core/nexus/registry.yaml`)

| Room | Lead | Sakk focus |
|------|------|------------|
| 01 Strategy | `str-lead` | PRD + sakk roadmap |
| 02 Research | `res-lead` | Saudi fintech research + competitor analysis |
| 04 Architecture | `arc-lead` | ERD + frozen OpenAPI + sakk-specific ADRs |
| 03 Design | `dsn-lead` | UX + Arabic-first design + DFR |
| 08 Localization | `loc-translation-manager` | Arabic copy + RTL + PII |
| 05 Backend | `bck-lead` | Laravel 11+ implementation |
| 06 Frontend | `fnt-lead` | React 19 + Vite admin + portal |
| 07 Mobile | `mob-lead` | Flutter 3.22+ |
| 09 Security | `sec-lead` | PCI-DSS + Mada + KYC security |
| 10 Quality | `qa-lead` (Lama) + qa-react-architect (Samer) + qa-laravel-architect (Yousuf) + qa-flutter-architect (Rayan) | 4 reviewers per delivery |
| 11 DevOps | `ops-lead` | Caddy + PHP-FPM + Mada + Apple Pay |
| 12 Observability | `obs-lead` | SLOs (KYC success rate, payment success rate) |
| 13 Knowledge | `knw-lead` | sakk brain ↔ CORTEX promotion |
| 15 WarRoom | `war-incident-commander` (Firas) | on-call (24/7) |

---

## The sakk live URL (when re-spawned)

- **Local:** `sakk.local` (per `hq/engine/sites/sakk.caddy`)
- **Public:** `sakk.zanjour.com` (per same Caddyfile)
- **Admin:** `admin.sakk.zanjour.com`

---

## See also

- [`../README.md`](../README.md) — projects/ parent
- [`../../hq/brain/README.md`](../../hq/brain/README.md) — organization memory (sister)
- [`../../hq/core/standards/deploy-standard.md`](../../hq/core/standards/deploy-standard.md) — deploy
- [`../../hq/engine/sites/sakk.caddy`](../../hq/engine/sites/sakk.caddy) — sakk Caddy site
- [`AGENTS.md`](../../AGENTS.md) — Law 7
