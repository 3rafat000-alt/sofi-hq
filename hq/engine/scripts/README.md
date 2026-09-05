# `hq/engine/scripts/` — Operational Scripts

> The 6 operational scripts that manage the live Caddy + PHP-FPM + n8n + MCP server stack. These
> are the **only** scripts that touch `/etc/caddy/Caddyfile` or the runtime services.

All scripts are owned by room 11 (DevOps) — `ops-lead` is the lead. Per `OPERATIONS.md`, the
operational flow is `bootstrap-live` (one-time) → `validate` (read-only check) → `deploy` (reload).

---

## Files

| File | Privilege | Purpose | Owner |
|------|-----------|---------|-------|
| `bootstrap-live.sh:6` | **sudo** (one-time) | EUID guard + remove legacy symlink + import canon Caddyfile to `/etc/caddy/Caddyfile` | `ops-lead` |
| `validate.sh:1` | read-only (no sudo) | Validate canon + live Caddyfile + PHP-FPM pools — exit 1 on error | `ops-cicd-engineer` |
| `deploy.sh:7` | no sudo + sudo fallback | Reload Caddy via admin API (preferred) + sudo fallback | `ops-release-manager` |
| `diff-live.sh` | read-only (no sudo) | Diff canon Caddyfile against live `/etc/caddy/Caddyfile` | `ops-cicd-engineer` |
| `check-env-guard.sh` | read-only (no sudo) | Minimal environment / EUID check (prevents accidental root) | `ops-lead` |
| `status.sh` | read-only (no sudo) | Health check for all layers (Caddy + PHP-FPM + MCP + n8n) | `obs-monitoring-engineer` |

---

## The 6 scripts in detail

### `bootstrap-live.sh` — one-time setup (sudo)

**Purpose:** imports the canon Caddyfile to `/etc/caddy/Caddyfile`. This is the **only** script
that writes to `/etc/caddy/Caddyfile`. EUID guard prevents accidental execution as non-root.

**Run:** once per server, when the canon Caddyfile changes. Per Axis 6 (least privilege) +
Axis 2 (Law 13 symlink removal).

```bash
sudo bash hq/engine/scripts/bootstrap-live.sh
```

### `validate.sh` — read-only check (no sudo)

**Purpose:** validates the canon Caddyfile syntax + the live Caddyfile syntax + all PHP-FPM pools.
Used in pre-deploy and pre-commit pipelines.

```bash
bash hq/engine/scripts/validate.sh
# Expected: ✓ Caddyfile canon sound · ✓ live Caddyfile sound · ✓ sakk.conf syntax sound
```

### `deploy.sh` — reload via admin API (no sudo)

**Purpose:** reloads Caddy via the admin API (no sudo). Falls back to `sudo systemctl reload caddy`
only if the admin API is unreachable.

```bash
bash hq/engine/scripts/deploy.sh
```

### `diff-live.sh` — diff canon vs live (no sudo)

**Purpose:** shows the diff between the canon Caddyfile and the live `/etc/caddy/Caddyfile`. Useful
for debugging "why is X not working in production?"

```bash
bash hq/engine/scripts/diff-live.sh
```

### `check-env-guard.sh` — minimal env check (no sudo)

**Purpose:** EUID check + basic environment validation. Prevents accidental execution as root or
in a misconfigured shell.

```bash
bash hq/engine/scripts/check-env-guard.sh
```

### `status.sh` — health check (no sudo)

**Purpose:** quick health check for all layers (Caddy + PHP-FPM + MCP + n8n). Used in
`obs-monitoring-engineer` alerts and `ops-sandbox-executor` validation.

```bash
bash hq/engine/scripts/status.sh
# Expected: ✓ Caddy up · ✓ PHP-FPM up · ✓ MCP up · ✓ n8n up
```

---

## The privilege model (Axis 6 — least privilege)

> Source: `ADR-20260831-9AXIS-FIX` (Axis 6).

- **One script** uses sudo: `bootstrap-live.sh` (one-time, EUID-guarded)
- **Five scripts** are read-only or admin-API (no sudo) — usable by anyone with shell access
- **Caddy reload** uses admin API (no sudo) — preferred over `systemctl reload`
- **PHP-FPM** is managed by `ops-migration-runner` and `ops-cicd-engineer` via systemd
- **MCP server** is managed by `gtw-dispatcher` via `mcp_server/scripts/`

This is the **least-privilege** model: scripts do the minimum needed and never write to the live
config without explicit operator action.

---

## The CONDITION-FOLLOW-UP (DEC-R3.4)

> These runtime artifacts are **NEVER** truncated in delivery handoffs:
> - `hq/engine/mcp_server/data/tickets.db`
> - `hq/engine/logs/*.log`
> - `hq/engine/n8n/workflows/*.json`
> - `hq/engine/sites/*.caddy`

This is enforced at the P-02.5 layer (handoff receipt). The scripts themselves are gitignored or
have explicit `pathspec` exclusion in commit.

---

## See also

- [`../README.md`](../README.md) — `hq/engine/` parent
- [`../Caddyfile`](../Caddyfile) — canon
- [`../OPERATIONS.md`](../OPERATIONS.md) — operational runbook
- [`../standards/deploy-standard.md`](../../core/standards/deploy-standard.md) — binding standard
- [`../../core/tooling/README.md`](../../core/tooling/README.md) — guards
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md)
