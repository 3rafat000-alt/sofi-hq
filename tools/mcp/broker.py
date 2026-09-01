#!/usr/bin/env python3
"""
📨 Sofi Broker MCP — تفويض المهام هرمياً (533 وكيل)
"""

import sys, os, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tools.mcp.base import SofiBaseMCP

class BrokerMCP(SofiBaseMCP):
    def __init__(self):
        super().__init__("📨 sofi-broker", "7.0.0", tools=[
            {
                "name": "delegate",
                "description": "📨 تفويض مهمة للنظام الهرمي — CEO → GM → Office → Lead → Micro (533 وكيل)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_name": {"type": "string", "description": "اسم المهمة"},
                        "description": {"type": "string", "description": "وصف المهمة"},
                        "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]}
                    },
                    "required": ["task_name"]
                }
            }
        ])
    
    async def handle_tool_call(self, name: str, arguments: dict) -> dict:
        if name == "delegate":
            from tools.shared.broker_lib import BrokerLib
            broker = BrokerLib()
            task_name = arguments.get("task_name", "مهمة")
            description = arguments.get("description", "")
            priority = arguments.get("priority", "medium")
            with self._silence_stdout():
                result = await broker.dispatch(task_name, description, priority)
            return self._text_result(json.dumps(result, indent=2, ensure_ascii=False))
        return self._text_error(f"أداة غير معروفة: {name}")

asyncio.run(BrokerMCP().run())
