#!/usr/bin/env python3
"""
🔍 Sofi Research MCP — بحث عميق متعدد المصادر
"""

import sys, os, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tools.mcp.base import SofiBaseMCP

class ResearchMCP(SofiBaseMCP):
    def __init__(self):
        super().__init__("🔍 sofi-research", "7.0.0", tools=[
            {
                "name": "research",
                "description": "🔍 بحث عميق متعدد المصادر — يحلل، يوصي، يقيس الثقة",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "استعلام البحث"},
                        "depth": {
                            "type": "string", "enum": ["quick", "standard", "deep", "exhaustive"],
                            "description": "عمق البحث"
                        }
                    },
                    "required": ["query"]
                }
            }
        ])
    
    async def handle_tool_call(self, name: str, arguments: dict) -> dict:
        if name == "research":
            from tools.mcp_broker.research_engine import ResearchEngine
            engine = ResearchEngine()
            query = arguments.get("query", "general")
            depth = arguments.get("depth", "standard")
            with self._silence_stdout():
                report = await engine.research(query, depth, "user")
            return self._text_result(json.dumps({
                "query": report.query,
                "sources": len(report.sources),
                "recommendations": report.recommendations,
                "confidence": report.confidence,
                "gaps": report.gaps
            }, indent=2, ensure_ascii=False))
        return self._text_error(f"أداة غير معروفة: {name}")

asyncio.run(ResearchMCP().run())
