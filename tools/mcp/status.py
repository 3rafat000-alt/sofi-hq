#!/usr/bin/env python3
"""
📋 Sofi Status MCP — حالة النظام الكاملة
"""

import sys, os, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tools.mcp.base import SofiBaseMCP

class StatusMCP(SofiBaseMCP):
    def __init__(self):
        super().__init__("📋 sofi-status", "7.0.0", tools=[
            {
                "name": "system_status",
                "description": "📋 حالة النظام الكاملة — الوكلاء، الأدوات، المهارات، خوادم MCP",
                "inputSchema": {"type": "object", "properties": {}}
            }
        ])
        # تحميل سجل المهارات مع البيانات المخزنة
        self._registry_path = os.path.join(os.path.dirname(__file__), "../../agents/sofi_skill_registry.json")
    
    async def handle_tool_call(self, name: str, arguments: dict) -> dict:
        if name == "system_status":
            from tools.mcp_broker.skill_registry import SkillRegistry
            from tools.shared.tool_forge_lib import ToolForge
            sr = SkillRegistry()
            sr.load(self._registry_path)
            tf = ToolForge()
            status = {
                "system": "Sofi AI Enterprise v7.0.0",
                "agents": {"total": 533, "leads": 20, "micro": 500, "offices": 4, "council": 5},
                "tools": {"forge_total": tf.get_stats()["total_tools"]},
                "skills": sr.get_stats()
            }
            return self._text_result(json.dumps(status, indent=2, ensure_ascii=False))
        return self._text_error(f"أداة غير معروفة: {name}")

asyncio.run(StatusMCP().run())
