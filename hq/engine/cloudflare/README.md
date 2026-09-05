# `hq/engine/cloudflare/` — Cloudflare Configuration

> The Cloudflare config for the live engine. Cloudflare is the **DNS + edge proxy** layer
> in front of Caddy (which is the canonical reverse proxy). Per `deploy-standard.md`, public
> sites (sakk + zanjour-portal) are behind Cloudflare's orange cloud.

Owned by `ops-domain-warden` (11-devops).

---

## Files

| File | Purpose |
|------|---------|
| `CONFIG-OF-RECORD.md` | The canonical Cloudflare config (zone + DNS records + page rules + workers + rate limits + WAF) |

---

## The config (per `CONFIG-OF-RECORD.md`)

- **Zones:** `sakk.zanjour.com` (sakk) + `zanjour.com` (portal) + `sakk.local` (dev — no Cloudflare)
- **DNS records:** managed via Cloudflare API (per `ops-domain-warden`)
- **Page rules:** cache static assets, bypass cache for `/api/*` + `/admin/*`
- **Rate limits:** 100 r/s for public API + 10 r/s for admin endpoints
- **WAF:** enabled for OWASP Top 10 + custom rules per `sec-threat-modeler`
- **Workers:** none currently (reserved for future use)
- **SSL/TLS:** Full (strict) — Cloudflare → Caddy (Let's Encrypt) → PHP-FPM

---

## The flow (per `deploy-standard.md`)

```
Owner → Cloudflare (orange cloud) → Caddy (Let's Encrypt) → PHP-FPM (Laravel) → sakk app
                       ↓
                  Cloudflare Workers (none currently)
                       ↓
                  Cloudflare WAF + Rate Limit
                       ↓
                  Cloudflare Analytics + Logs
```

The Cloudflare layer adds:
- **DDoS protection** (always-on)
- **WAF** (managed rules + custom OWASP rules)
- **Rate limiting** (per zone + per URL pattern)
- **Bot management** (challenge/captcha for suspicious traffic)
- **Caching** (static assets only — never `/api/*` or `/admin/*`)
- **Analytics** (request volume, error rate, performance)

---

## The TLS model

- **Origin → Cloudflare:** Full (strict) TLS 1.2+ (Cloudflare validates the cert)
- **Cloudflare → visitor:** TLS 1.0+ (configurable)
- **Caddy (origin) → Let's Encrypt:** ACME challenge via Cloudflare DNS-01 (token in env)
- **PHP-FPM:** no TLS (localhost only)

The origin cert is renewed automatically by Caddy via the `tls { dns cloudflare }` directive
in `hq/engine/sites/*.caddy`.

---

## How to update the config

1. Update `CONFIG-OF-RECORD.md` first (the canonical doc)
2. Apply the change via Cloudflare API (per `ops-domain-warden` script)
3. Run `bash hq/engine/scripts/validate.sh` to verify the change
4. Run `bash hq/engine/scripts/status.sh` to verify the origin is still up
5. Update `OPERATIONS.md` if the change affects operations
6. Commit atomically — pre-commit enforces all 4 guards
7. Record ADR in CORTEX if the change is constitutional

**Forbidden:** making Cloudflare changes without updating `CONFIG-OF-RECORD.md` first. The file
is the **single source of truth** for the Cloudflare config.

---

## The CONDITION-FOLLOW-UP (DEC-R3.4)

> `hq/engine/cloudflare/CONFIG-OF-RECORD.md` is **never** truncated in delivery handoffs. It is
> part of the operational canon.

---

## See also

- [`../README.md`](../README.md) — `hq/engine/` parent
- [`../Caddyfile`](../Caddyfile) — canon
- [`../sites/README.md`](../sites/README.md) — per-domain Caddy sites
- [`../scripts/README.md`](../scripts/README.md) — operational scripts
- [`../../core/standards/deploy-standard.md`](../../core/standards/deploy-standard.md) — binding standard
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 8 (Security)
