#!/usr/bin/env python3
"""
💬 Sofi Consult MCP — تشاور بين الوكلاء
"""

import sys, os, json, asyncio, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tools.mcp.base import SofiBaseMCP

class ConsultMCP(SofiBaseMCP):
    def __init__(self):
        super().__init__("💬 sofi-consult", "7.0.0", tools=[
            {
                "name": "consult",
                "description": "💬 تشاور بين الوكلاء — نقاش، تصويت، توصيات، توافق",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string", "description": "موضوع التشاور"},
                        "participants": {
                            "type": "array", "items": {"type": "string"},
                            "description": "المشاركون (افتراضي: all)"
                        }
                    },
                    "required": ["topic"]
                }
            }
        ])
    
    async def handle_tool_call(self, name: str, arguments: dict) -> dict:
        if name == "consult":
            from tools.mcp_broker.consultation_engine import ConsultationEngine, VoteChoice
            engine = ConsultationEngine()
            topic = arguments.get("topic", "تشاور عام")
            participants = arguments.get("participants", ["architect", "security", "ux", "performance", "ethics"])
            
            with self._silence_stdout():
                session = await engine.start_consultation(topic, "user", participants)
                for p in participants:
                    vote = random.choice([VoteChoice.APPROVE, VoteChoice.APPROVE, VoteChoice.APPROVE, VoteChoice.NEEDS_MORE_INFO])
                    await engine.submit_opinion(session.id, p, p, vote, f"تحليل {topic}", 0.75)
                await engine.finalize(session.id)
            
            return self._text_result(json.dumps({
                "topic": session.topic,
                "consensus": session.consensus_score,
                "decision": session.status.value,
                "recommendation": session.final_recommendation,
                "opinions": {aid: {"vote": o.vote.value, "confidence": o.confidence} for aid, o in session.opinions.items()}
            }, indent=2, ensure_ascii=False))
        return self._text_error(f"أداة غير معروفة: {name}")

asyncio.run(ConsultMCP().run())
