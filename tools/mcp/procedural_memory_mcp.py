#!/usr/bin/env python3
"""
Procedural Memory MCP Server — Workflows & Procedures
=======================================================
Stores, retrieves, and executes multi-step procedures.
Agents use this to remember how to perform complex tasks,
with version tracking and execution history.
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
        "name": "store_procedure",
        "description": "Store a multi-step procedure with version tracking (auto-increments on update)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Unique procedure name (e.g. deploy_api, run_tests)"},
                "steps": {"type": "array", "description": "Ordered list of steps. Each step: {'description': '...', 'action': '...', 'args': {...}}"},
                "description": {"type": "string", "description": "Human-readable description of what this procedure does"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for categorization"},
                "inputs": {"type": "object", "description": "Expected input parameters schema"},
                "outputs": {"type": "object", "description": "Expected output schema"}
            },
            "required": ["name", "steps"]
        }
    },
    {
        "name": "get_procedure",
        "description": "Retrieve a procedure by name with full step details and version info",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Procedure name to retrieve"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "search_procedures",
        "description": "Search for procedures by name, description, or step content",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query (matches name, description, and steps)"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Filter by tags"},
                "n": {"type": "integer", "description": "Max results (default 10)", "default": 10}
            },
            "required": ["query"]
        }
    },
    {
        "name": "list_procedures",
        "description": "List all stored procedures with name, description, tags, and version",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "execution_history",
        "description": "View execution history for a procedure (success/failure, duration, context)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "procedure_name": {"type": "string", "description": "Procedure name"},
                "n": {"type": "integer", "description": "Number of recent executions (default 10)", "default": 10}
            },
            "required": ["procedure_name"]
        }
    }
]


class ProceduralMemoryMCP(SofiBaseMCP):
    def __init__(self):
        super().__init__("Procedural Memory MCP", "1.0.0", TOOLS)
        self.memory = MemoryCore()

    async def handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        if name == "store_procedure":
            return self._store_procedure(arguments)
        elif name == "get_procedure":
            return self._get_procedure(arguments)
        elif name == "search_procedures":
            return self._search_procedures(arguments)
        elif name == "list_procedures":
            return self._list_procedures()
        elif name == "execution_history":
            return self._execution_history(arguments)
        return self._text_error(f"Unknown tool: {name}")

    def _store_procedure(self, args: Dict) -> Dict:
        name = args.get("name", "")
        steps = args.get("steps", [])
        description = args.get("description", "")
        tags = args.get("tags", [])
        inputs = args.get("inputs", {})
        outputs = args.get("outputs", {})
        if not name or not steps:
            return self._text_error("name and steps are required")
        version = self.memory.store_procedure(
            name, steps,
            description=description,
            tags=tags
        )
        return self._text_result(json.dumps({
            "status": "stored",
            "name": name,
            "version": version,
            "step_count": len(steps),
            "tags": tags
        }, ensure_ascii=False, indent=2))

    def _get_procedure(self, args: Dict) -> Dict:
        name = args.get("name", "")
        if not name:
            return self._text_error("name is required")
        proc = self.memory.get_procedure(name)
        if not proc:
            return self._text_error(f"Procedure '{name}' not found")
        return self._text_result(json.dumps(proc, ensure_ascii=False, indent=2))

    def _search_procedures(self, args: Dict) -> Dict:
        query = args.get("query", "")
        tags = args.get("tags")
        n = args.get("n", 10)
        if not query:
            return self._text_error("query is required")
        results = self.memory.search_procedures(query, tags=tags)
        return self._text_result(json.dumps({
            "query": query,
            "count": len(results),
            "results": results
        }, ensure_ascii=False, indent=2))

    def _list_procedures(self) -> Dict:
        procs = self.memory.procedural.list_all()
        return self._text_result(json.dumps({
            "count": len(procs),
            "procedures": procs
        }, ensure_ascii=False, indent=2))

    def _execution_history(self, args: Dict) -> Dict:
        name = args.get("procedure_name", "")
        n = args.get("n", 10)
        if not name:
            return self._text_error("procedure_name is required")
        history = self.memory.procedural.get_execution_history(name, n=n)
        return self._text_result(json.dumps({
            "procedure": name,
            "count": len(history),
            "executions": history
        }, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    server = ProceduralMemoryMCP()
    asyncio.run(server.run())
