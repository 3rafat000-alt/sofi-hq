#!/usr/bin/env python3
"""
Semantic Memory MCP Server — Long-term Knowledge via Vector DB
================================================================
Stores and searches persistent knowledge using the MemoryCore Semantic store.
Supports tags, metadata, and vector similarity search.
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
        "name": "store_knowledge",
        "description": "Store a piece of knowledge in semantic (long-term) memory with vector embedding",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Knowledge text/content to store"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for categorization (e.g. python, api, security)"},
                "metadata": {"type": "object", "description": "Additional metadata (e.g. source, author, version)"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "search_knowledge",
        "description": "Search semantic memory using vector similarity — finds related knowledge by meaning",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural language query to search for"},
                "n": {"type": "integer", "description": "Number of results to return (max 20)", "default": 5},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Filter by tags"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "knowledge_stats",
        "description": "Get statistics about stored knowledge entries",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


class SemanticMemoryMCP(SofiBaseMCP):
    def __init__(self):
        super().__init__("Semantic Memory MCP", "1.0.0", TOOLS)
        self.memory = MemoryCore()

    async def handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        if name == "store_knowledge":
            return self._store_knowledge(arguments)
        elif name == "search_knowledge":
            return self._search_knowledge(arguments)
        elif name == "knowledge_stats":
            return self._knowledge_stats()
        return self._text_error(f"Unknown tool: {name}")

    def _store_knowledge(self, args: Dict) -> Dict:
        text = args.get("text", "")
        if not text:
            return self._text_error("text is required")
        tags = args.get("tags", [])
        metadata = args.get("metadata", {})
        doc_id = self.memory.store_knowledge(text, tags=tags, metadata=metadata)
        count = self.memory.semantic.count()
        return self._text_result(json.dumps({
            "status": "stored",
            "id": doc_id,
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "tags": tags,
            "total_knowledge_entries": count
        }, ensure_ascii=False, indent=2))

    def _search_knowledge(self, args: Dict) -> Dict:
        query = args.get("query", "")
        n = min(args.get("n", 5), 20)
        tags = args.get("tags")
        if not query:
            return self._text_error("query is required")
        results = self.memory.search_knowledge(query, n=n, tags=tags)
        return self._text_result(json.dumps({
            "query": query,
            "count": len(results),
            "results": results
        }, ensure_ascii=False, indent=2))

    def _knowledge_stats(self) -> Dict:
        count = self.memory.semantic.count()
        return self._text_result(json.dumps({
            "total_entries": count,
            "memory_type": "semantic",
            "storage": "chromadb" if hasattr(self.memory.semantic, '_collection') and self.memory.semantic._collection else "sqlite"
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    server = SemanticMemoryMCP()
    asyncio.run(server.run())
