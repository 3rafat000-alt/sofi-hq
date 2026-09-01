#!/usr/bin/env python3
"""
⚡ Sofi Redis MCP Server — التخزين المؤقت والطوابير
======================================================
JSON-RPC 2.0 stdio MCP server for Redis operations
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.mcp.base import SofiBaseMCP
import json
from typing import Dict


TOOLS = [
    {
        "name": "redis_get",
        "description": "قراءة مفتاح — Get value by key from Redis",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Redis key"}
            },
            "required": ["key"]
        }
    },
    {
        "name": "redis_set",
        "description": "كتابة مفتاح — Set key-value in Redis with optional TTL",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Redis key"},
                "value": {"type": "string", "description": "Value to store"},
                "ttl": {"type": "integer", "description": "TTL in seconds (0 = no expiry)", "default": 0}
            },
            "required": ["key", "value"]
        }
    },
    {
        "name": "redis_delete",
        "description": "حذف مفتاح — Delete key from Redis",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Redis key"}
            },
            "required": ["key"]
        }
    },
    {
        "name": "redis_keys",
        "description": "البحث عن مفاتيح — List keys matching pattern",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Glob pattern (e.g. sofi:*)",
                    "default": "*"
                }
            }
        }
    },
    {
        "name": "redis_ping",
        "description": "اختبار الاتصال — Test Redis connection",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


REDIS_AVAILABLE = False
REDIS_CLIENT = None


def _get_client():
    global REDIS_CLIENT, REDIS_AVAILABLE
    if REDIS_CLIENT is not None:
        return REDIS_CLIENT
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
    try:
        import redis as redis_mod
        REDIS_CLIENT = redis_mod.from_url(redis_url, socket_connect_timeout=3)
        REDIS_CLIENT.ping()
        REDIS_AVAILABLE = True
        return REDIS_CLIENT
    except Exception:
        REDIS_AVAILABLE = False
        return None


class RedisMCPServer(SofiBaseMCP):
    _local_store: Dict[str, str] = {}

    def __init__(self):
        super().__init__("⚡ Redis MCP", "1.0.0", TOOLS)

    async def handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        client = _get_client()
        if name == "redis_ping":
            if REDIS_AVAILABLE:
                return self._text_result("✅ Redis متصل ويعمل")
            return self._text_result("⚠️ Redis غير متاح — استخدام التخزين المحلي كبديل")

        if REDIS_AVAILABLE:
            return await self._handle_redis(client, name, arguments)
        else:
            return self._handle_local(name, arguments)

    async def _handle_redis(self, client, name: str, args: Dict) -> Dict:
        try:
            if name == "redis_get":
                val = client.get(args.get("key", ""))
                return self._text_result(val.decode() if val else "(nil)")
            elif name == "redis_set":
                key = args.get("key", "")
                value = args.get("value", "")
                ttl = args.get("ttl", 0)
                if ttl > 0:
                    client.setex(key, ttl, value)
                else:
                    client.set(key, value)
                return self._text_result(f"✅ {key} = {value}" + (f" (TTL: {ttl}s)" if ttl else ""))
            elif name == "redis_delete":
                r = client.delete(args.get("key", ""))
                return self._text_result(f"✅ Deleted {r} key(s)")
            elif name == "redis_keys":
                keys = client.keys(args.get("pattern", "*"))
                return self._text_result(json.dumps([k.decode() for k in keys], ensure_ascii=False, indent=2))
        except Exception as e:
            return self._text_error(f"Redis error: {e}")
        return self._text_error(f"Unknown tool: {name}")

    def _handle_local(self, name: str, args: Dict) -> Dict:
        if name == "redis_get":
            val = self._local_store.get(args.get("key", ""))
            return self._text_result(val if val else "(nil)")
        elif name == "redis_set":
            self._local_store[args.get("key", "")] = args.get("value", "")
            return self._text_result(f"✅ (local) {args.get('key')} = {args.get('value')}")
        elif name == "redis_delete":
            self._local_store.pop(args.get("key", ""), None)
            return self._text_result("✅ (local) deleted")
        elif name == "redis_keys":
            pattern = args.get("pattern", "*")
            if pattern == "*":
                keys = list(self._local_store.keys())
            else:
                import fnmatch
                keys = [k for k in self._local_store if fnmatch.fnmatch(k, pattern)]
            return self._text_result(json.dumps(keys, ensure_ascii=False, indent=2))
        return self._text_error(f"Unknown tool: {name}")


if __name__ == "__main__":
    server = RedisMCPServer()
    asyncio.run(server.run())
