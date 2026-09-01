#!/usr/bin/env python3
"""
🔨 Sofi Tool Forge MCP — بناء أدوات PY بواسطة Lead Agents
"""

import sys, os, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tools.mcp.base import SofiBaseMCP

class ToolForgeMCP(SofiBaseMCP):
    def __init__(self):
        super().__init__("🔨 sofi-tool-forge", "7.0.0", tools=[
            {
                "name": "build_tool",
                "description": "🔨 بناء أداة PY جديدة — 20 Lead Agent يمكنهم بناء أدوات بفحص أمني",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "اسم الأداة"},
                        "code": {"type": "string", "description": "كود Python الكامل"},
                        "agent": {"type": "string", "description": "اسم الوكيل الباني (architect, builder, tester, ...)"},
                        "description": {"type": "string", "description": "وصف الأداة"}
                    },
                    "required": ["name", "code", "agent"]
                }
            },
            {
                "name": "catalogue",
                "description": "🔧 عرض كتالوج الأدوات لكل مكتب ووكيل",
                "inputSchema": {"type": "object", "properties": {}}
            }
        ])
    
    async def handle_tool_call(self, name: str, arguments: dict) -> dict:
        if name == "build_tool":
            from tools.shared.tool_forge_lib import ToolForge
            forge = ToolForge()
            with self._silence_stdout():
                result = forge.forge_tool(
                    name=arguments.get("name", "unnamed"),
                    code=arguments.get("code", ""),
                    agent=arguments.get("agent", "shared"),
                    description=arguments.get("description", "")
                )
            return self._text_result(json.dumps(result, indent=2, ensure_ascii=False))
        elif name == "catalogue":
            from tools.shared.tool_forge_lib import ToolForge
            forge = ToolForge()
            with self._silence_stdout():
                cat = forge.catalogue()
            return self._text_result(json.dumps(cat, indent=2, ensure_ascii=False))
        return self._text_error(f"أداة غير معروفة: {name}")

asyncio.run(ToolForgeMCP().run())
