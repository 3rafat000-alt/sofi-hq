#!/usr/bin/env python3
"""
Sofi MCP Broker — Main Orchestrator
=======================================
المدير الرئيسي للنظام — يربط كل المكونات معاً
"""

import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path

from .message_bus import MessageBus
from .agent_communicator import AgentCommunicator
from .consultation_engine import ConsultationEngine, VoteChoice
from .research_engine import ResearchEngine
from .tool_builder import ToolBuilder
from .skill_registry import SkillRegistry
from .agent_network import AgentNetwork
from .protocols import AgentAddress, MessageType, MessagePriority


class MCPBroker:
    """المدير الرئيسي — ينسق كل مكونات MCP"""
    
    def __init__(self, project_root: str = None):
        if project_root is None:
            project_root = str(Path(__file__).parent.parent.parent)
        self.project_root = project_root
        
        # المكونات الأساسية
        self.message_bus = MessageBus()
        self.consultation_engine = ConsultationEngine()
        self.research_engine = ResearchEngine()
        self.tool_builder = ToolBuilder()
        self.skill_registry = SkillRegistry()
        self.agent_network = AgentNetwork()
        
        # وكلاء النظام
        self.communicators: Dict[str, AgentCommunicator] = {}
        
        # حالة النظام
        self._running = False
    
    async def start(self):
        """تشغيل النظام"""
        print("\n" + "=" * 60)
        print("🚀  SOFI MCP BROKER — بدء تشغيل النظام")
        print("=" * 60)
        
        # بدء معالجة الرسائل
        asyncio.create_task(self.message_bus.start_processing())
        
        # تسجيل وكلاء النظام الأساسيين
        await self._register_system_agents()
        
        self._running = True
        
        print("✅  MCP Broker جاهز للعمل")
        print(f"   {len(self.communicators)} وكيل مسجل")
        print(f"   {len(self.agent_network.nodes)} عقدة في الشبكة")
        print("=" * 60 + "\n")
    
    async def _register_system_agents(self):
        """تسجيل وكلاء النظام"""
        system_agents = [
            ("research-engine", "Research Engine", "باحث رئيسي", "system", 0),
            ("tool-builder", "Tool Builder", "باني أدوات", "system", 0),
            ("consultation-master", "Consultation Master", "منسق تشاور", "system", 0),
        ]
        
        for agent_id, name, title, office, level in system_agents:
            address = AgentAddress(
                agent_id=agent_id, name=name, title=title,
                office=office, level=level
            )
            comm = AgentCommunicator(address, self.message_bus)
            
            # تسجيل معالجات
            comm.on(MessageType.CONSULT_REQUEST.value,
                    lambda m: self._handle_consult_request(m, comm))
            comm.on(MessageType.RESEARCH_REQUEST.value,
                    lambda m: self._handle_research_request(m, comm))
            comm.on(MessageType.TOOL_BUILD.value,
                    lambda m: self._handle_tool_build(m, comm))
            
            self.communicators[agent_id] = comm
            self.agent_network.register_node(
                agent_id, name, title, office, level,
                ["research", "consultation", "tool_building"]
            )
    
    async def _handle_consult_request(self, message, comm):
        """معالجة طلب تشاور"""
        topic = message.content.get("topic", "")
        details = message.content.get("details", {})
        
        session = await self.consultation_engine.start_consultation(
            topic=topic,
            initiator=message.sender,
            participants=list(self.communicators.keys())
        )
        
        # محاكاة آراء
        for agent_id in self.communicators:
            import random
            vote = random.choice(list(VoteChoice))
            await self.consultation_engine.submit_opinion(
                session.id, agent_id,
                self.communicators[agent_id].address.name,
                vote,
                f"تحليل {topic} من منظور {self.communicators[agent_id].address.title}"
            )
        
        await self.consultation_engine.finalize(session.id)
        
        # رد
        if message.reply_to:
            reply = message.reply({
                "session_id": session.id,
                "decision": session.status.value,
                "consensus": session.consensus_score,
                "recommendation": session.final_recommendation
            })
            await comm.send(message.sender, MessageType.CONSULT_RESPONSE, reply.content)
    
    async def _handle_research_request(self, message, comm):
        """معالجة طلب بحث"""
        query = message.content.get("query", "")
        depth = message.content.get("depth", "standard")
        
        report = await self.research_engine.research(query, depth, message.sender)
        
        if message.reply_to:
            reply = message.reply({
                "report_id": report.id,
                "sources_count": len(report.sources),
                "recommendations": report.recommendations,
                "confidence": report.confidence,
                "analysis": report.analysis[:500]
            })
            await comm.send(message.sender, MessageType.RESEARCH_RESPONSE, reply.content)
    
    async def _handle_tool_build(self, message, comm):
        """معالجة بناء أداة"""
        name = message.content.get("name", "")
        code = message.content.get("code", "")
        description = message.content.get("description", "")
        author = message.content.get("author", "unknown")
        
        tool = self.tool_builder.build_tool(
            name=name,
            author=author,
            author_office="system",
            agent_level=3,
            code=code,
            description=description
        )
        
        if message.reply_to:
            reply = message.reply({
                "tool_name": tool.name,
                "status": "built" if tool.safety_score >= 0.3 else "rejected",
                "safety_score": tool.safety_score,
                "filepath": tool.filepath
            })
            await comm.send(message.sender, MessageType.TOOL_SHARE, reply.content)
    
    async def register_agent(self, agent_id: str, name: str, title: str,
                              office: str, level: int, skills: List[str]) -> AgentCommunicator:
        """تسجيل وكيل جديد في النظام"""
        address = AgentAddress(
            agent_id=agent_id, name=name, title=title,
            office=office, level=level
        )
        comm = AgentCommunicator(address, self.message_bus)
        
        self.communicators[agent_id] = comm
        self.agent_network.register_node(agent_id, name, title, office, level, skills)
        
        # تسجيل المهارات
        for skill in skills:
            self.skill_registry.register_agent_skill(agent_id, skill, 0.8, 5)
        
        return comm
    
    def get_agent_communicator(self, agent_id: str) -> Optional[AgentCommunicator]:
        return self.communicators.get(agent_id)
    
    def get_system_status(self) -> Dict:
        """حالة النظام الكاملة"""
        return {
            "broker": {
                "status": "running" if self._running else "stopped",
                "message_bus": self.message_bus.get_stats(),
                "consultation": self.consultation_engine.get_stats(),
                "research": self.research_engine.get_stats(),
                "tool_builder": self.tool_builder.get_stats(),
                "skill_registry": self.skill_registry.get_stats(),
                "agent_network": self.agent_network.get_network_stats()
            },
            "agents": {
                "registered": len(self.communicators),
                "network_nodes": len(self.agent_network.nodes)
            }
        }
    
    def stop(self):
        """إيقاف النظام"""
        self._running = False
        self.message_bus.stop()
        print("\n🛑  MCP Broker متوقف")


async def main():
    """تشغيل تجريبي"""
    broker = MCPBroker()
    await broker.start()
    
    # تسجيل بعض الوكلاء
    leads = [
        ("architect", "Architect", "مهندس بنية", "engineering", 3,
         ["laravel", "api_design", "architecture", "python_programming"]),
        ("builder", "Builder", "مطور رئيسي", "engineering", 3,
         ["laravel", "python_programming", "testing_backend"]),
        ("security-lead", "Security Lead", "محلل أمن", "quality", 3,
         ["sast", "pentest", "owasp", "threat_modeling"]),
    ]
    
    for agent_id, name, title, office, level, skills in leads:
        await broker.register_agent(agent_id, name, title, office, level, skills)
    
    # محاكاة تشاور
    comm = broker.get_agent_communicator("architect")
    if comm:
        await comm.send("consultation-master", MessageType.CONSULT_REQUEST, {
            "topic": "اختيار بنية API للمشروع",
            "details": {"options": ["REST", "GraphQL"], "project": "E-Learning Platform"}
        })
    
    # محاكاة بحث
    comm2 = broker.get_agent_communicator("security-lead")
    if comm2:
        result = await comm2.research("OWASP Top 10 prevention strategies", "deep")
        print(f"\n📊  نتيجة البحث: {result.get('confidence', 0):.0%} ثقة")
    
    # محاكاة بناء أداة
    if comm:
        tool = await comm.build_tool(
            "api_validator",
            "التحقق من صحة استجابات API",
            """def validate_response(status_code, data):
    \"\"\"التحقق من استجابة API\"\"\"
    if status_code >= 500:
        return {"valid": False, "issue": "Server error"}
    if status_code >= 400:
        return {"valid": False, "issue": f"Client error: {data.get('message', '')}"}
    return {"valid": True, "data": data}
"""
        )
        print(f"🔨  أداة جديدة: {tool.get('tool_name', 'unknown')} — {tool.get('status', '?')}")
    
    # حالة النظام
    status = broker.get_system_status()
    print(f"\n📊  حالة النظام: {status['broker']['status']}")
    print(f"   الوكلاء: {status['agents']['registered']}")
    print(f"   الرسائل: {status['broker']['message_bus']['total_messages']}")
    
    broker.stop()


if __name__ == "__main__":
    asyncio.run(main())
