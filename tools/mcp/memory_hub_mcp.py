#!/usr/bin/env python3
"""
🧠 Sofi Memory Hub MCP — التسجيل الإلزامي لكل الـ 534 وكيلاً
===============================================================
كل وكيل يسجل كل حدث في 5 أنظمة ذاكرة دفعة واحدة:
  📋 Audit Log → 📝 Episodic → 🧠 Semantic → ⚡ Working → 🔄 Procedural

الأدوات:
  log          : تسجيل حدث في جميع الذكريات (لأي وكيل)
  search       : بحث في جميع الذكريات
  get_stats    : إحصائيات التسجيل
  get_history  : سجل وكيل معين
  get_recent   : آخر الأحداث
  search_audit : بحث في سجل التدقيق
"""

import sys, os, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tools.mcp.base import SofiBaseMCP
from tools.shared.agent_memory import AgentMemory


class MemoryHubMCP(SofiBaseMCP):
    """🧠 Memory Hub MCP Server — كل وكيل يسجل هنا"""
    
    def __init__(self):
        self.memory = AgentMemory()
        
        super().__init__("🧠 sofi-memory-hub", "7.0.0", tools=[
            {
                "name": "log",
                "description": "🧠 تسجيل حدث في جميع الذكريات — لـ أي وكيل من الـ 534",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "agent": {"type": "string", "description": "اسم الوكيل (مثال: Stitch-UI, Builder-3)"},
                        "office": {
                            "type": "string",
                            "enum": ["creative", "engineering", "quality", "ai_data", "council", "sofi", "sniffer"],
                            "description": "المكتب"
                        },
                        "action": {"type": "string", "description": "الإجراء (task.complete, task.fail, consult, etc.)"},
                        "summary": {"type": "string", "description": "ملخص بالعربية"},
                        "details": {"type": "object", "description": "تفاصيل كاملة (JSON)"},
                        "lesson": {"type": "string", "description": "درس مستفاد (اختياري)"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "وسوم للتصنيف"}
                    },
                    "required": ["agent", "office", "action", "summary"]
                }
            },
            {
                "name": "search",
                "description": "🔍 بحث في جميع الذكريات (دلالية + عرضية + إجرائية)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "نص البحث"},
                        "n": {"type": "number", "description": "عدد النتائج (افتراضي: 5)"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "وسوم للفلترة"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_stats",
                "description": "📊 إحصائيات التسجيل في الذاكرة",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_history",
                "description": "📖 سجل وكيل معين",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "agent": {"type": "string", "description": "اسم الوكيل"},
                        "n": {"type": "number", "description": "عدد النتائج (افتراضي: 20)"}
                    },
                    "required": ["agent"]
                }
            },
            {
                "name": "get_recent",
                "description": "📋 آخر الأحداث في سجل التدقيق",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "n": {"type": "number", "description": "عدد النتائج (افتراضي: 20)"}
                    }
                }
            },
            {
                "name": "search_audit",
                "description": "🔎 بحث في سجل التدقيق JSONL",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "نص البحث"},
                        "n": {"type": "number", "description": "عدد النتائج (افتراضي: 20)"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_office_history",
                "description": "🏢 سجل مكتب معين",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "office": {
                            "type": "string",
                            "enum": ["creative", "engineering", "quality", "ai_data", "council", "sofi", "sniffer"]
                        },
                        "n": {"type": "number", "description": "عدد النتائج"}
                    },
                    "required": ["office"]
                }
            }
        ])
    
    async def handle_tool_call(self, name: str, arguments: dict) -> dict:
        if name == "log":
            result = self.memory.log(
                agent=arguments.get("agent", "unknown"),
                office=arguments.get("office", "unknown"),
                action=arguments.get("action", "unknown"),
                summary=arguments.get("summary", ""),
                details=arguments.get("details", {}),
                lesson=arguments.get("lesson", ""),
                tags=arguments.get("tags", [])
            )
            return self._text_result(json.dumps({
                "success": result.get("success"),
                "episodic_id": result.get("episodic"),
                "semantic_id": result.get("semantic"),
                "audit": result.get("audit"),
                "total_logs": self.memory.get_stats().get("total_logs", 0)
            }, indent=2, ensure_ascii=False))
        
        elif name == "search":
            query = arguments.get("query", "")
            n = arguments.get("n", 5)
            tags = arguments.get("tags")
            results = self.memory.search(query, n=n, tags=tags)
            return self._text_result(json.dumps(results, indent=2, ensure_ascii=False, default=str))
        
        elif name == "get_stats":
            stats = self.memory.get_stats()
            return self._text_result(json.dumps(stats, indent=2, ensure_ascii=False))
        
        elif name == "get_history":
            agent = arguments.get("agent", "")
            n = arguments.get("n", 20)
            history = self.memory.get_agent_history(agent, n=n)
            return self._text_result(json.dumps([{
                "id": e.get("id"),
                "type": e.get("event_type"),
                "summary": e.get("summary", "")[:100],
                "lesson": e.get("lesson", ""),
                "created": e.get("created_at", "")
            } for e in history], indent=2, ensure_ascii=False))
        
        elif name == "get_recent":
            n = arguments.get("n", 20)
            entries = self.memory.get_recent_audit(n=n)
            return self._text_result(json.dumps(entries, indent=2, ensure_ascii=False, default=str))
        
        elif name == "search_audit":
            query = arguments.get("query", "")
            n = arguments.get("n", 20)
            results = self.memory.search_audit(query, n=n)
            return self._text_result(json.dumps(results, indent=2, ensure_ascii=False, default=str))
        
        elif name == "get_office_history":
            office = arguments.get("office", "")
            n = arguments.get("n", 20)
            history = self.memory.get_office_history(office, n=n)
            return self._text_result(json.dumps([{
                "agent": json.loads(e.get("data", "{}")).get("details", {}).get("agent", e.get("agent", "")),
                "summary": e.get("summary", "")[:100],
                "lesson": e.get("lesson", ""),
                "created": e.get("created_at", "")
            } for e in history], indent=2, ensure_ascii=False))
        
        return self._text_error(f"أداة غير معروفة: {name}")


if __name__ == "__main__":
    asyncio.run(MemoryHubMCP().run())
