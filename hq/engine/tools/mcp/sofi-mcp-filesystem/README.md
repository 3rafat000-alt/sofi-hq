# SOFI Filesystem MCP

Native Python FastAPI implementation of the SOFI Filesystem MCP server.
Part of **Operation Fleet Renewal** (2026-09-04).

## Stack
- **Language:** Python 3.12+
- **Framework:** FastAPI 0.115+
- **Validation:** Pydantic v2
- **Server:** Uvicorn (uvloop + httptools)
- **License:** MIT (Law 15 compliant)

## Quick Start

```bash
# 1. Security Gate (mandatory)
make security-gate

# 2. Build
make build-fs

# 3. Test (≥ 90% coverage)
make test-fs

# 4. Run
make up
```

## API

All endpoints under `/api/v1/` require `Authorization: Bearer <SOFI_API_KEY>`.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Public health check |
| POST | `/api/v1/mcp` | JSON-RPC 2.0 MCP endpoint |

### JSON-RPC Methods

- `initialize` — MCP handshake
- `tools/list` — List available tools
- `tools/call` — Call a tool

### Tools

- `read_file(path: str)` — Read UTF-8 file
- `write_file(path: str, content: str, create_parents: bool = False)` — Write file
- `list_directory(path: str)` — List dir (non-recursive)
- `search_files(root: str, pattern: str, max_results: int = 100)` — Glob search

## Standard Envelope v1

Every response:
```json
{
  "success": true|false,
  "message": "...",
  "data": {...}|null,
  "error": null|{"code": "...", "message": "..."},
  "meta": {
    "request_id": "uuid",
    "timestamp": "ISO 8601",
    "service": "sofi-fs-mcp"
  }
}
```

## Security

- API Key Bearer authentication (all routes except `/health`, `/docs`, `/openapi.json`)
- Path traversal protection (only allowed roots accessible)
- File size limits (configurable via `SOFI_MAX_FILE_SIZE_MB`)
- All exceptions return Standard Envelope (no raw stack traces)

## Testing

```bash
pytest --cov=app --cov-fail-under=90
```

Coverage target: **≥ 90%** (Law K15).


```bash
```

Container runs as non-root user (`sofi`, UID 1000).
Caddy reverse proxy handles external access.

## Author

SOFI Team · 2026-09-04 · Operation Fleet Renewal
License: MIT
