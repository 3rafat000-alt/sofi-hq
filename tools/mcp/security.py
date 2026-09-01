#!/usr/bin/env python3
"""
🔒 Sofi Security MCP — فحص أمني للكود
"""

import sys, os, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tools.mcp.base import SofiBaseMCP

class SecurityMCP(SofiBaseMCP):
    def __init__(self):
        super().__init__("🔒 sofi-security", "7.0.0", tools=[
            {
                "name": "scan_security",
                "description": "🔒 فحص أمني للكود — يكتشف eval, exec, os.system, subprocess وغيرها",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "مسار المشروع (اختياري)"}
                    }
                }
            }
        ])
    
    async def handle_tool_call(self, name: str, arguments: dict) -> dict:
        if name == "scan_security":
            from tools.testing.sofi_security_scanner import SecurityScanner
            scanner = SecurityScanner()
            with self._silence_stdout():
                results = scanner.scan_project()
            return self._text_result(json.dumps(results, indent=2, ensure_ascii=False))
        return self._text_error(f"أداة غير معروفة: {name}")

asyncio.run(SecurityMCP().run())
