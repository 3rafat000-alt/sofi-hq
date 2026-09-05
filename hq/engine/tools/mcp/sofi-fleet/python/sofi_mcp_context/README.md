# sofi-mcp-context

**Local library context provider — Context7 alternative.**

100% local, zero cloud calls, MIT-licensed. Part of SOFI-Fleet v1.0.

## Replaces

- **Context7** (`mcp.context7.com/mcp`) — cloud SaaS
- Same API surface, but all data lives on your disk

## Tools

| Tool | Description |
|------|-------------|
| `resolve_library_id` | Identify a library by name (fuzzy match) |
| `get_library_docs` | Get docs for a library, optionally filtered by topic |
| `get_code_snippets` | Extract code snippets for a topic |
| `list_known_libraries` | List all libraries in the local cache |
| `update_library` | Ingest a new library from a source directory |

## Built-in Libraries (curated)

- **react** (18.x, 19.x) — hooks, components
- **fastapi** (0.100+, 0.141) — routing, pydantic
- **pydantic** (2.x) — models, validators
- **laravel** (10.x, 11.x) — routes, eloquent
- **flutter** (3.16+, 3.22+, 3.24) — widgets, state

## Add Your Own Library

```bash
# Tell the agent: "update_library laravel from /path/to/laravel/src"
```

Or via JSON-RPC:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "update_library",
    "arguments": {
      "libraryName": "my-lib",
      "sourceDir": "/home/user/my-lib/src",
      "description": "My custom library"
    }
  }
}
```

The library is persisted to `~/.sofi-fleet/context-cache/user_libraries.json`.

## Architecture

- **No LLM** for parsing — uses regex to extract function/class names
- **tree-sitter** (optional) for richer AST extraction
- **Ollama** (optional) for AI summaries — `httpx` to `localhost:11434`
- **JSON-RPC 2.0** stdio (MCP standard)
- **Rate-limited** via sofi-mcp-common.TokenBucket (200 burst, 20 rps)
- **API key** auth via sofi-mcp-common.APIKeyMiddleware

## Performance

- Latency: < 5ms (in-process, no network)
- Throughput: 1000+ RPS
- Memory: ~30 MB
- Startup: < 100ms

## Install

```bash
cd /home/es3dlll/Desktop/SOFI/hq/engine/tools/mcp/sofi-fleet/python
pip install -e ./sofi_mcp_common
pip install -e ./sofi_mcp_context
```

## Run

```bash
sofi-mcp-context
# or
python -m sofi_mcp_context.server
```

## License

MIT — Part of SOFI-Fleet v1.0
