#!/usr/bin/env python3
"""
🌐 Sofi Network MCP — شبكة الوكلاء الطوبولوجية
"""

import sys, os, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tools.mcp.base import SofiBaseMCP

class NetworkMCP(SofiBaseMCP):
    def __init__(self):
        super().__init__("🌐 sofi-network", "7.0.0", tools=[
            {
                "name": "network_stats",
                "description": "🌐 إحصائيات شبكة الوكلاء — العقد، الاتصالات، التوزيع حسب المكتب والمستوى",
                "inputSchema": {"type": "object", "properties": {}}
            }
        ])
    
    async def handle_tool_call(self, name: str, arguments: dict) -> dict:
        if name == "network_stats":
            from tools.mcp_broker.agent_network import AgentNetwork
            network = AgentNetwork()
            offices = ["engineering", "creative", "quality", "ai_data"]
            for office in offices:
                for i in range(5):
                    network.register_node(f"{office}-lead-{i}", f"Lead {i+1}", "Lead", office, 3, ["general"])
            stats = network.get_network_stats()
            return self._text_result(json.dumps(stats, indent=2, ensure_ascii=False))
        return self._text_error(f"أداة غير معروفة: {name}")

asyncio.run(NetworkMCP().run())
