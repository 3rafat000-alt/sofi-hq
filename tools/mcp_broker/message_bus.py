#!/usr/bin/env python3
"""
Sofi MCP Broker — Message Bus
=================================
ناقل الرسائل المركزي — توجيه، ترشيح، أولويات، بث
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Callable, Optional, Any, Set
from collections import defaultdict
from .protocols import Message, MessageType, MessagePriority


class MessageBus:
    """الناقل المركزي لكل رسائل الوكلاء"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._queues: Dict[MessagePriority, asyncio.Queue] = {
            p: asyncio.Queue() for p in MessagePriority
        }
        self._history: List[Message] = []
        self._routing_table: Dict[str, str] = {}  # agent_id -> address
        self._running = False
        self._agent_status: Dict[str, str] = {}  # agent_id -> status
    
    def subscribe(self, message_type: str, callback: Callable):
        """اشتراك في نوع رسالة"""
        self._subscribers[message_type].append(callback)
    
    def subscribe_all(self, callback: Callable):
        """اشتراك في كل الرسائل"""
        for mt in MessageType:
            self._subscribers[mt.value].append(callback)
    
    def unsubscribe(self, message_type: str, callback: Callable):
        if callback in self._subscribers[message_type]:
            self._subscribers[message_type].remove(callback)
    
    async def publish(self, message: Message):
        """نشر رسالة في الناقل"""
        message.created_at = datetime.now().isoformat()
        self._history.append(message)
        
        # توجيه حسب الأولوية
        await self._queues[message.priority].put(message)
        
        # إرسال للمشتركين
        if message.type.value in self._subscribers:
            for callback in self._subscribers[message.type.value]:
                await callback(message)
        
        # بث إذا كان بدون مستلم
        if not message.recipient:
            for callbacks in self._subscribers.values():
                for callback in callbacks:
                    await callback(message)
    
    async def publish_request(self, msg_type: MessageType, sender: str,
                               recipient: str, content: dict,
                               priority: MessagePriority = MessagePriority.MEDIUM) -> Message:
        """نشر رسالة وانتظار الرد"""
        msg = Message(
            type=msg_type,
            priority=priority,
            sender=sender,
            recipient=recipient,
            content=content
        )
        
        response_future = asyncio.get_event_loop().create_future()
        
        async def waiter(response_msg: Message):
            if response_msg.reply_to == msg.id:
                response_future.set_result(response_msg)
        
        self.subscribe(msg_type.value, waiter)
        await self.publish(msg)
        
        try:
            return await asyncio.wait_for(response_future, timeout=30.0)
        except asyncio.TimeoutError:
            return Message(
                type=MessageType.SYSTEM_ERROR,
                sender="system",
                recipient=sender,
                content={"error": "timeout", "original_msg": msg.id}
            )
        finally:
            self.unsubscribe(msg_type.value, waiter)
    
    async def broadcast(self, message: Message):
        """بث لكل الوكلاء"""
        original = message.recipient
        message.recipient = ""
        await self.publish(message)
        message.recipient = original
    
    def register_agent(self, agent_id: str, address: str):
        """تسجيل وكيل في جدول التوجيه"""
        self._routing_table[agent_id] = address
        self._agent_status[agent_id] = "online"
    
    def unregister_agent(self, agent_id: str):
        self._routing_table.pop(agent_id, None)
        self._agent_status[agent_id] = "offline"
    
    def get_agent_address(self, agent_id: str) -> Optional[str]:
        return self._routing_table.get(agent_id)
    
    def get_online_agents(self) -> Dict[str, str]:
        return {aid: addr for aid, addr in self._routing_table.items()
                if self._agent_status.get(aid) == "online"}
    
    def get_history(self, limit: int = 50) -> List[Message]:
        return self._history[-limit:]
    
    def get_stats(self) -> dict:
        return {
            "total_messages": len(self._history),
            "online_agents": len([s for s in self._agent_status.values() if s == "online"]),
            "registered_agents": len(self._routing_table),
            "subscribers": sum(len(v) for v in self._subscribers.values()),
            "queue_sizes": {p.value: q.qsize() for p, q in self._queues.items()}
        }
    
    async def start_processing(self):
        """بدء معالجة الطوابير"""
        self._running = True
        while self._running:
            for priority in [MessagePriority.CRITICAL, MessagePriority.HIGH,
                             MessagePriority.MEDIUM, MessagePriority.LOW]:
                try:
                    msg = await asyncio.wait_for(
                        self._queues[priority].get(), timeout=0.1
                    )
                    await self._process_message(msg)
                except asyncio.TimeoutError:
                    continue
    
    async def _process_message(self, message: Message):
        """معالجة رسالة (تسجيل، تحقق، توجيه)"""
        if message.ttl > 0:
            age = (datetime.now() - datetime.fromisoformat(message.created_at)).total_seconds()
            if age > message.ttl:
                return  # رسالة منتهية الصلاحية
        
        await asyncio.sleep(0.01)  # محاكاة معالجة
    
    def stop(self):
        self._running = False
