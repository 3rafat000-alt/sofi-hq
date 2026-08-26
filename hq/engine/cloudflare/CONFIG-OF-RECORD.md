# Cloudflare — Config of Record
> Last synced: 2026-08-24 · Domain: zanjour.com · **never place tokens here** (the tunnel token lives exclusively in `/etc/cloudflared/token` on the server)

## 1) TLS Pattern

| Setting | Value | Reason |
|---|---|---|
| SSL/TLS Mode | **Flexible → upgrading to Full recommended** | the current Caddyfile serves HTTP:80 — TLS terminates at CF (documented in the file header). Once HTTPS is enabled on the origin: switch to Full(strict) and enable ACME in Caddy |
| Always Use HTTPS | ON | mandatory for production |
| Min TLS | 1.2 | |

## 2) Tunnel (cloudflared)

- Runtime: systemd service `cloudflared` — active ✓ · Authentication: token-based (`/etc/cloudflared/token`)
- Direction: internet ← CF Edge ← tunnel ← `http://localhost:80` (Caddy catch-all) ← internal routing by Host header
- Diagnostic commands:
```bash
systemctl status cloudflared
journalctl -u cloudflared -n 20 --no-pager
cloudflared tunnel info   # if a local account certificate exists
```

## 3) DNS Table (reference record — actual edits happen in the CF dashboard)

| Name | Type | Content | Proxy | Purpose |
|---|---|---|---|---|
| tobacco.zanjour.com | A/CNAME | (via tunnel CNAME <TUNNEL-ID>.cfargotunnel.com) | 🟠 Proxied | store + POS + API |
| *.zanjour.com | CNAME | same tunnel | 🟠 Proxied | wildcard for future sites — Caddy answers 404 for anything undefined |

> Matching Caddy rule: `http://*.zanjour.com` answers 404 for any undefined subdomain — no incidental disclosure.

## 4) Cache and Rules

- Cache Level: Standard · Browser TTL: respect origin headers
- Cache bypass (Cache Rule) for paths: `/api/*` · `/pos/*` (dynamic)
- Rocket Loader: OFF (sakk SPA is CSP-sensitive)

## 5) Standard Change Checklist

1. Record it here first (decision + date + approver).
2. Apply from the CF dashboard.
3. Verify: `curl -sI https://<host>` — CF headers plus the expected status.
4. Update this file's state whenever any row above changes.
