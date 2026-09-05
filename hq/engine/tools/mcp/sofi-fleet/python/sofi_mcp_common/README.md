# sofi-mcp-common

Shared infrastructure for all SOFI-Fleet MCP servers.

## What it provides

- `SofiMCPServer` — base class for JSON-RPC 2.0 stdio MCP servers
- `Tool` / `ToolResult` — tool definitions
- `Envelope` — standard response shape (`{success, message, data, error, meta}`)
- `APIKeyMiddleware` — Bearer-token authentication
- `TokenBucket` — rate limiter
- `setup_logging` — structured JSON logging
- `verify_dependencies_license` — Law 15 license gate (rejects GPL/AGPL/SSPL)

## Install

```bash
pip install -e .
```

## Usage

```python
from sofi_mcp_common import SofiMCPServer, Tool, ToolResult

class MyServer(SofiMCPServer):
    def __init__(self):
        super().__init__("my-server", "1.0.0")

    def register_tools(self) -> list:
        return [
            Tool(
                name="hello",
                description="Say hello",
                input_schema={"type": "object", "properties": {"name": {"type": "string"}}},
                handler=self._hello,
            )
        ]

    async def _hello(self, args):
        name = args.get("name", "world")
        return ToolResult(content=[{"type": "text", "text": f"Hello, {name}!"}])

if __name__ == "__main__":
    import asyncio
    asyncio.run(MyServer().run())
```

## License

MIT — Part of SOFI-Fleet v1.0
