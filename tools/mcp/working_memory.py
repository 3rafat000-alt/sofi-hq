#!/usr/bin/env python3
"""
Working Memory MCP Server — Short-term Session Context with TTL
================================================================
Provides session-based key-value storage with TTL expiry.
Backed by MemoryCore singleton for shared state across all agents.
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.mcp.base import SofiBaseMCP
from tools.shared.memory_core import MemoryCore
import json
from typing import Dict


TOOLS = [
    {
        "name": "store_context",
        "description": "Store a context item in working memory with TTL",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Context key (namespace:key)"},
                "value": {"type": "string", "description": "Value to store (JSON string or text)"},
                "ttl": {"type": "integer", "description": "Time-to-live in seconds", "default": 3600}
            },
            "required": ["key", "value"]
        }
    },
    {
        "name": "recall_context",
        "description": "Retrieve context from working memory by key or namespace",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Context key to retrieve"},
                "namespace": {"type": "string", "description": "Filter by namespace prefix"}
            }
        }
    },
    {
        "name": "forget_context",
        "description": "Remove context from working memory by key or namespace",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Context key to forget"},
                "namespace": {"type": "string", "description": "Forget all keys in namespace"}
            }
        }
    },
    {
        "name": "list_context",
        "description": "List all items in working memory, optionally filtered by namespace",
        "inputSchema": {
            "type": "object",
            "properties": {
                "namespace": {"type": "string", "description": "Filter by namespace prefix"}
            }
        }
    },
    {
        "name": "memory_stats",
        "description": "Get working memory usage statistics",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


class WorkingMemoryServer(SofiBaseMCP):
    def __init__(self):
        super().__init__("Working Memory MCP", "1.0.0", TOOLS)
        self.memory = MemoryCore()

    async def handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        if name == "store_context":
            return self._store_context(arguments)
        elif name == "recall_context":
            return self._recall_context(arguments)
        elif name == "forget_context":
            return self._forget_context(arguments)
        elif name == "list_context":
            return self._list_context(arguments)
        elif name == "memory_stats":
            return self._memory_stats()
        return self._text_error(f"Unknown tool: {name}")

    def _store_context(self, args: Dict) -> Dict:
        key = args.get("key", "")
        value = args.get("value", "")
        ttl = args.get("ttl", 3600)
        if not key:
            return self._text_error("key is required")
        self.memory.set_context(key, value, ttl=ttl)
        return self._text_result(json.dumps({
            "status": "stored",
            "key": key,
            "ttl": ttl,
            "ttl_seconds": ttl
        }, ensure_ascii=False, indent=2))

    def _recall_context(self, args: Dict) -> Dict:
        key = args.get("key", "")
        namespace = args.get("namespace", "")
        if key:
            value = self.memory.get_context(key)
            if value is None:
                return self._text_error(f"Key not found: {key}")
            return self._text_result(json.dumps({
                "key": key,
                "value": value
            }, ensure_ascii=False, indent=2))
        if namespace:
            keys = [k for k in self.memory.working.keys() if k.startswith(namespace + ":") or k.startswith(namespace + "/")]
            items = {}
            for k in keys:
                v = self.memory.get_context(k)
                if v is not None:
                    items[k] = v
            return self._text_result(json.dumps({
                "namespace": namespace,
                "count": len(items),
                "items": items
            }, ensure_ascii=False, indent=2))
        return self._text_error("Specify key or namespace")

    def _forget_context(self, args: Dict) -> Dict:
        key = args.get("key", "")
        namespace = args.get("namespace", "")
        if key:
            self.memory.clear_context(key)
            return self._text_result(json.dumps({"status": "forgotten", "key": key}))
        if namespace:
            keys = [k for k in self.memory.working.keys() if k.startswith(namespace + ":") or k.startswith(namespace + "/")]
            for k in keys:
                self.memory.clear_context(k)
            return self._text_result(json.dumps({"status": "forgotten", "namespace": namespace, "count": len(keys)}))
        return self._text_error("Specify key or namespace")

    def _list_context(self, args: Dict) -> Dict:
        namespace = args.get("namespace", "")
        if namespace:
            keys = [k for k in self.memory.working.keys() if k.startswith(namespace + ":") or k.startswith(namespace + "/")]
        else:
            keys = self.memory.working.keys()
        items = {}
        for k in keys:
            v = self.memory.get_context(k)
            if v is not None:
                items[k] = {
                    "value_truncated": (str(v)[:100] + "...") if len(str(v)) > 100 else v
                }
        return self._text_result(json.dumps({
            "count": len(items),
            "items": items
        }, ensure_ascii=False, indent=2))

    def _memory_stats(self) -> Dict:
        stats = self.memory.stats()
        return self._text_result(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    server = WorkingMemoryServer()
    asyncio.run(server.run())
