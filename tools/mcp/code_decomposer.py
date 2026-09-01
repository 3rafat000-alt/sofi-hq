#!/usr/bin/env python3
"""
📊 Sofi Code Decomposer MCP — تحليل بنية المشروع
"""

import sys, os, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tools.mcp.base import SofiBaseMCP

class CodeDecomposerMCP(SofiBaseMCP):
    def __init__(self):
        super().__init__("📊 sofi-code-decomposer", "7.0.0", tools=[
            {
                "name": "decompose_code",
                "description": "📊 تحليل بنية المشروع — عد الكلاسات، الدوال، الأسطر، والتعقيد",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "مسار المشروع (افتراضي: الحالي)"}
                    }
                }
            }
        ])
    
    async def handle_tool_call(self, name: str, arguments: dict) -> dict:
        if name == "decompose_code":
            from tools.shared.sofi_code_decomposer import CodeDecomposer
            path = arguments.get("path", ".")
            decomposer = CodeDecomposer(root=path)
            with self._silence_stdout():
                summary = decomposer.project_summary()
            return self._text_result(json.dumps(summary, indent=2, ensure_ascii=False))
        return self._text_error(f"أداة غير معروفة: {name}")

asyncio.run(CodeDecomposerMCP().run())
