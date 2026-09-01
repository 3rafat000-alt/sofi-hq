#!/usr/bin/env python3
"""
Sofi MCP Broker — Agent Communicator
========================================
واجهة التواصل بين الوكلاء — إرسال، استقبال، تشاور، تنسيق
"""

import asyncio
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from .protocols import Message, MessageType, MessagePriority, AgentAddress
from .message_bus import MessageBus


class AgentCommunicator:
    """واجهة اتصال الوكيل — كل وكيل لديه واحدة"""
    
    def __init__(self, agent_address: AgentAddress, message_bus: MessageBus):
        self.address = agent_address
        self.bus = message_bus
        self._inbox: List[Message] = []
        self._handlers: Dict[str, Callable] = {}
        self._consultations: Dict[str, dict] = {}
        
        # تسجيل في الناقل
        self.bus.register_agent(self.address.agent_id, self.address.address)
        
        # اشتراك في رسائلي
        self.bus.subscribe_all(self._receive)
    
    async def _receive(self, message: Message):
        """استقبال رسالة"""
        if message.recipient in ("", self.address.agent_id):
            self._inbox.append(message)
            
            if message.type.value in self._handlers:
                await self._handlers[message.type.value](message)
    
    def on(self, message_type: str, handler: Callable):
        """تسجيل معالج لنوع رسالة"""
        self._handlers[message_type] = handler
    
    async def send(self, recipient: str, msg_type: MessageType,
                    content: dict, priority: MessagePriority = MessagePriority.MEDIUM) -> Message:
        """إرسال رسالة لوكيل محدد"""
        msg = Message(
            type=msg_type,
            priority=priority,
            sender=self.address.agent_id,
            recipient=recipient,
            content=content
        )
        await self.bus.publish(msg)
        return msg
    
    async def broadcast(self, msg_type: MessageType, content: dict):
        """بث لكل الوكلاء"""
        msg = Message(
            type=msg_type,
            priority=MessagePriority.MEDIUM,
            sender=self.address.agent_id,
            recipient="",
            content=content
        )
        await self.bus.broadcast(msg)
    
    async def request(self, recipient: str, msg_type: MessageType,
                       content: dict) -> Optional[Message]:
        """إرسال وانتظار رد"""
        return await self.bus.publish_request(
            msg_type, self.address.agent_id, recipient, content
        )
    
    async def consult(self, topic: str, details: dict,
                       with_agents: List[str]) -> List[Message]:
        """تشاور مع وكلاء محددين"""
        responses = []
        for agent_id in with_agents:
            response = await self.request(
                agent_id, MessageType.CONSULT_REQUEST,
                {"topic": topic, "details": details, "from": self.address.name}
            )
            if response:
                responses.append(response)
        return responses
    
    async def research(self, query: str, depth: str = "standard") -> dict:
        """طلب بحث من Research Engine"""
        response = await self.request(
            "research-engine", MessageType.RESEARCH_REQUEST,
            {"query": query, "depth": depth, "requester": self.address.name}
        )
        return response.content if response else {"error": "no response"}
    
    async def build_tool(self, name: str, description: str,
                          code: str) -> dict:
        """طلب بناء أداة من Tool Builder"""
        response = await self.request(
            "tool-builder", MessageType.TOOL_BUILD,
            {"name": name, "description": description, "code": code,
             "author": self.address.name}
        )
        return response.content if response else {"error": "no response"}
    
    def check_mail(self) -> List[Message]:
        """قراءة الرسائل الواردة"""
        messages = list(self._inbox)
        self._inbox.clear()
        return messages
    
    def get_unread_count(self) -> int:
        return len(self._inbox)
    
    def heartbeat(self):
        """إرسال نبض حياة"""
        asyncio.ensure_future(self.bus.publish(Message(
            type=MessageType.SYSTEM_HEARTBEAT,
            priority=MessagePriority.LOW,
            sender=self.address.agent_id,
            content={"status": "alive", "timestamp": datetime.now().isoformat()}
        )))
