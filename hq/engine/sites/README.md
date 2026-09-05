# `hq/engine/sites/` — Per-Domain Caddy Sites

> One `.caddy` file per public hostname. These are **included** by the canon `Caddyfile` (root
> of `hq/engine/`) via the `import sites/*.caddy` directive. Each file declares a virtual host
> with its reverse-proxy + headers + rate-limit + logging rules.

Owned by room 11 (DevOps) — `ops-domain-warden` is the lead for DNS/TLS/edge config.

---

## Files

| File | Endpoint(s) | Backend | TLS | Rate-limit | Owner |
|------|-------------|---------|-----|------------|-------|
| `sakk.caddy` | `sakk.local` + `sakk.zanjour.com` | Laravel 11+ PHP-FPM | Let's Encrypt (Cloudflare proxy) | 100r/s | `ops-domain-warden` |
| `zanjour-portal.caddy` | portal zanjour | Laravel 11+ PHP-FPM | Let's Encrypt | 100r/s | `ops-domain-warden` |
| `mcp.caddy` | MCP server endpoint | Python MCP server | Let's Encrypt (internal) | 1000r/s | `gtw-dispatcher` |
| `n8n.caddy` | orchestrator endpoint | n8n | Let's Encrypt (internal) | 50r/s | `ops-cicd-engineer` |

---

## The Caddyfile structure

```caddyfile
# example: sakk.caddy
{sakk.local, sakk.zanjour.com} {
    encode zstd gzip
    reverse_proxy localhost:9001 {           # PHP-FPM pool port
        transport http {
            dial_timeout 5s
        }
    }
    rate_limit 100r/s
    log {
        output file /var/log/caddy/sakk.log {
            roll_size 100mb
            roll_keep 10
        }
    }
    tls {
        dns cloudflare {env.CLOUDFLARE_API_TOKEN}
    }
}
```

---

## The TLS / DNS model (per `deploy-standard.md`)

- **Public sites** (sakk, zanjour-portal): behind Cloudflare proxy (orange cloud) — TLS termination
  at Cloudflare + Let's Encrypt at the edge
- **Internal sites** (mcp, n8n): direct Let's Encrypt (no Cloudflare) — internal access only
- **Local dev sites** (sakk.local): self-signed Caddy internal CA

DNS records managed by `ops-domain-warden` via Cloudflare API.

---

## The reverse-proxy targets

| Site | Backend port | Process |
|------|--------------|---------|
| sakk | 9001 | `php-fpm` (Laravel) |
| zanjour-portal | 9002 | `php-fpm` (Laravel) |
| mcp | 8080 | `python mcp_server/main.py` |
| n8n | 5678 | `n8n` |

Each backend is run via systemd (managed by `ops-release-manager`). Restart on failure is configured.

---

## The CONDITION-FOLLOW-UP (DEC-R3.4)

> `hq/engine/sites/*.caddy` are **never truncated** in delivery handoffs. They are part of the
> canon (via `import sites/*.caddy` in the root Caddyfile). They live in git and are versioned.

---

## How to add a new site

1. Create the `.caddy` file in this directory (follow the structure above)
2. Add the DNS record (via `ops-domain-warden` + Cloudflare API)
3. Run `bash hq/engine/scripts/validate.sh` — must exit 0
4. Run `bash hq/engine/scripts/deploy.sh` to reload Caddy
5. Run `bash hq/engine/scripts/status.sh` — site must be up
6. Commit atomically — pre-commit enforces all 4 guards
7. Update `OPERATIONS.md` with the new site

**Forbidden:** writing to `/etc/caddy/Caddyfile` directly. The only way to update the live config
is via `bootstrap-live.sh` (one-time import) or `deploy.sh` (reload). All changes go through
the canon files in git.

---

## See also

- [`../README.md`](../README.md) — `hq/engine/` parent
- [`../Caddyfile`](../Caddyfile) — canon
- [`../scripts/README.md`](../scripts/README.md) — operational scripts
- [`../OPERATIONS.md`](../OPERATIONS.md) — per-room runbook
- [`../../core/standards/deploy-standard.md`](../../core/standards/deploy-standard.md) — binding standard
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 10 (Direct-on-Project)
