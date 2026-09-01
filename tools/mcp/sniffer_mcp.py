#!/usr/bin/env python3
"""
👁️ Sofi Sniffer MCP — وكيل التنصت والرصد والتوجيه
=====================================================
يستمع لكل اتصالات MCP بين الـ 533 وكيلاً، يلتقط التقارير،
يسجلها في سجل التدقيق، ويُمررها تلقائياً للوكيل التالي.

التدفق الكامل:
  🎨 مصمم → يرفع تقرير → 👁️ Sniffer يلتقطه → يوجهه للبناء 🏗️
  🏗️ باني → يرفع كود → 👁️ Sniffer يلتقطه → يوجهه للجودة ⚔️
  ⚔️ جودة → ترفع تقرير → 👁️ Sniffer يلتقطه → يوجهه للذكاء 🤖
  🤖 ذكاء → يرفع إصدار → 👁️ Sniffer يلتقطه → يوجهه للتقرير النهائي

الاستخدام:
  feed_message: تغذية Sniffer برسالة MCP
  get_captured: استرجاع الرسائل الملتقطة
  get_handoffs: استرجاع حزم التسليم
  get_pipeline: عرض حالة خط الإنتاج
  get_stats: إحصائيات التنصت
  search_logs: البحث في سجل التدقيق
"""

import sys, os, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tools.mcp.base import SofiBaseMCP
from tools.shared.sniffer_lib import SnifferEngine, SnifferAuditLog, SnifferFactory


class SnifferMCP(SofiBaseMCP):
    """👁️ Sniffer MCP Server — يراقب كل شيء"""
    
    def __init__(self):
        self.engine, self.audit = SnifferFactory.create_with_audit()
        
        super().__init__("👁️ sofi-sniffer", "7.0.0", tools=[
            {
                "name": "feed_message",
                "description": "👁️ تغذية Sniffer برسالة MCP — يلتقطها، يحللها، يوجهها للوكيل التالي",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "event_type": {
                            "type": "string",
                            "enum": [
                                "task.delegate", "task.accept", "task.progress",
                                "task.complete", "task.fail",
                                "consult.request", "consult.response",
                                "design.handoff", "code.handoff", "quality.handoff",
                                "cross.office"
                            ],
                            "description": "نوع حدث MCP"
                        },
                        "source_agent": {
                            "type": "string",
                            "description": "الوكيل المصدر (مثال: Stitch-UI, Builder-Core, Tester-QA)"
                        },
                        "source_office": {
                            "type": "string",
                            "enum": ["creative", "engineering", "quality", "ai_data", "council", "sofi"],
                            "description": "المكتب المصدر"
                        },
                        "content": {
                            "type": "object",
                            "description": "محتوى الرسالة — التقرير، التصميم، الكود، إلخ"
                        },
                        "target": {
                            "type": "string",
                            "description": "الوكيل المستهدف (اختياري)"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "critical"],
                            "description": "الأولوية"
                        }
                    },
                    "required": ["event_type", "source_agent", "source_office", "content"]
                }
            },
            {
                "name": "get_captured",
                "description": "📋 استرجاع الرسائل الملتقطة — مع فلترة حسب المكتب",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "office": {
                            "type": "string",
                            "enum": ["", "creative", "engineering", "quality", "ai_data", "council", "sofi"],
                            "description": "فلترة حسب المكتب (اترك فارغاً للكل)"
                        },
                        "limit": {
                            "type": "number",
                            "description": "عدد النتائج (افتراضي: 20)"
                        }
                    }
                }
            },
            {
                "name": "get_handoffs",
                "description": "📦 استرجاع حزم التسليم بين المكاتب",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "office": {
                            "type": "string",
                            "description": "فلترة حسب المكتب"
                        }
                    }
                }
            },
            {
                "name": "get_pipeline",
                "description": "🏭 عرض حالة خط الإنتاج الكامل — أين كل حزمة؟",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_stats",
                "description": "📊 إحصائيات Sniffer — عدد الرسائل، التوجيهات، الأخطاء",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "search_logs",
                "description": "🔍 البحث في سجل تدقيق Sniffer",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "نص البحث"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_office_queue",
                "description": "📬 عرض طابور مكتب معين — ما ينتظره من مهام",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "office": {
                            "type": "string",
                            "enum": ["creative", "engineering", "quality", "ai_data"],
                            "description": "اسم المكتب"
                        }
                    },
                    "required": ["office"]
                }
            }
        ])
    
    async def handle_tool_call(self, name: str, arguments: dict) -> dict:
        if name == "feed_message":
            event_type = arguments.get("event_type", "task.complete")
            source = arguments.get("source_agent", "unknown")
            office = arguments.get("source_office", "unknown")
            content = arguments.get("content", {})
            target = arguments.get("target", "")
            priority = arguments.get("priority", "medium")
            
            result = self.engine.feed_message(
                event_type=event_type,
                source=source,
                source_office=office,
                content=content,
                target=target,
                priority=priority
            )
            
            return self._text_result(json.dumps({
                "captured": True,
                "message_id": result.id,
                "summary": result.summary,
                "forwarded": result.forwarded,
                "forwarded_to": result.forwarded_to,
                "route_decision": result.route_decision,
                "timestamp": result.timestamp
            }, indent=2, ensure_ascii=False))
        
        elif name == "get_captured":
            office = arguments.get("office", "")
            limit = arguments.get("limit", 20)
            messages = self.engine.get_captured(office=office, limit=limit)
            
            return self._text_result(json.dumps([{
                "id": m.id,
                "timestamp": m.timestamp[:19],
                "event": m.event_type.value,
                "source": f"{m.source_office}/{m.source_agent}",
                "target": f"{m.target_office}/{m.target_agent}" if m.target_agent else m.target_office,
                "summary": m.summary,
                "forwarded": m.forwarded,
                "to": m.forwarded_to
            } for m in messages], indent=2, ensure_ascii=False))
        
        elif name == "get_handoffs":
            office = arguments.get("office", "")
            handoffs = self.engine.get_handoffs(office=office)
            
            return self._text_result(json.dumps([{
                "id": h.id,
                "task": h.task_name,
                "from": h.source_office,
                "to": h.target_office,
                "chain": " → ".join(h.chain),
                "created": h.created_at[:19],
                "has_design": bool(h.design_specs),
                "has_code": bool(h.code_output),
                "has_quality": bool(h.quality_report),
                "has_release": bool(h.release_report)
            } for h in handoffs], indent=2, ensure_ascii=False))
        
        elif name == "get_pipeline":
            status = self.engine.get_pipeline_status()
            return self._text_result(json.dumps(status, indent=2, ensure_ascii=False))
        
        elif name == "get_stats":
            stats = self.engine.get_stats()
            return self._text_result(json.dumps(stats, indent=2, ensure_ascii=False))
        
        elif name == "search_logs":
            query = arguments.get("query", "")
            results = self.audit.search(query)
            return self._text_result(json.dumps(results[-20:], indent=2, ensure_ascii=False))
        
        elif name == "get_office_queue":
            office = arguments.get("office", "")
            queue = self.engine.get_office_queue(office)
            return self._text_result(json.dumps({
                "office": office,
                "waiting": len(queue),
                "items": queue[-10:]
            }, indent=2, ensure_ascii=False))
        
        return self._text_error(f"أداة غير معروفة: {name}")


if __name__ == "__main__":
    asyncio.run(SnifferMCP().run())
