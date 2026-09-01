#!/usr/bin/env python3
"""
Sofi MCP Broker — Communication Protocols
============================================
بروتوكولات الاتصال بين الوكلاء — أنواع الرسائل، العناوين، التوقيعات
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime
import uuid


class MessageType(str, Enum):
    """أنواع الرسائل في شبكة الوكلاء"""
    # ── التشاور ──
    CONSULT_REQUEST = "consult.request"          # طلب تشاور
    CONSULT_RESPONSE = "consult.response"        # رد تشاور
    CONSULT_JOIN = "consult.join"                # انضمام لتشاور
    
    # ── البحث ──
    RESEARCH_REQUEST = "research.request"         # طلب بحث
    RESEARCH_RESPONSE = "research.response"       # رد بحث
    RESEARCH_DEEP = "research.deep"              # بحث عميق
    
    # ── الأدوات ──
    TOOL_BUILD = "tool.build"                    # بناء أداة
    TOOL_SHARE = "tool.share"                    # مشاركة أداة
    TOOL_REQUEST = "tool.request"                # طلب أداة
    TOOL_VALIDATE = "tool.validate"              # التحقق من أداة
    
    # ── المهارات ──
    SKILL_CLAIM = "skill.claim"                  # ادعاء مهارة
    SKILL_QUERY = "skill.query"                  # استعلام عن مهارة
    SKILL_ENDORSE = "skill.endorse"              # توثيق مهارة
    
    # ── المهام ──
    TASK_DELEGATE = "task.delegate"              # تفويض مهمة
    TASK_ACCEPT = "task.accept"                  # قبول مهمة
    TASK_COMPLETE = "task.complete"              # إكمال مهمة
    TASK_FAIL = "task.fail"                      # فشل مهمة
    TASK_PROGRESS = "task.progress"              # تقدم مهمة
    
    # ── النظام ──
    SYSTEM_HEARTBEAT = "system.heartbeat"        # نبض النظام
    SYSTEM_STATUS = "system.status"              # حالة النظام
    SYSTEM_SYNC = "system.sync"                  # مزامنة
    SYSTEM_ERROR = "system.error"                # خطأ نظام


class MessagePriority(str, Enum):
    """أولويات الرسائل"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AgentAddress:
    """عنوان وكيل في الشبكة"""
    agent_id: str
    name: str
    title: str
    office: str
    level: int  # 0=CEO, 1=GM, 2=Office, 3=Lead, 4=Micro
    ip: str = "127.0.0.1"
    port: int = 0
    
    @property
    def address(self) -> str:
        return f"{self.office}/{self.name}@{self.level}"


@dataclass
class Message:
    """رسالة موحدة بين الوكلاء"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    type: MessageType = MessageType.SYSTEM_STATUS
    priority: MessagePriority = MessagePriority.MEDIUM
    sender: str = ""
    recipient: str = ""  # "" = broadcast
    content: Dict[str, Any] = field(default_factory=dict)
    reply_to: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    ttl: int = 300  # seconds before expiration
    signature: str = ""
    
    def reply(self, content: Dict[str, Any]) -> 'Message':
        return Message(
            type=self.type,
            priority=self.priority,
            sender=self.recipient,
            recipient=self.sender,
            content=content,
            reply_to=self.id
        )


@dataclass
class CommunicationProtocol:
    """بروتوكول اتصال كامل"""
    protocol_version: str = "7.0.0"
    encoding: str = "json"
    max_message_size: int = 1024 * 1024  # 1MB
    supported_types: List[str] = field(default_factory=lambda: [t.value for t in MessageType])
    encryption: bool = False
    compression: bool = False


@dataclass
class SkillClaim:
    """ادعاء مهارة من وكيل"""
    agent_id: str
    skill_name: str
    proficiency: float  # 0.0 to 1.0
    years_experience: int
    verified_by: List[str] = field(default_factory=list)
    tools_built: List[str] = field(default_factory=list)


@dataclass
class ToolSpec:
    """مواصفات أداة يبنيها وكيل"""
    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    language: str = "python"
    dependencies: List[str] = field(default_factory=list)
    inputs: Dict[str, str] = field(default_factory=dict)
    outputs: Dict[str, str] = field(default_factory=dict)
    safety_rating: str = "safe"  # safe, caution, dangerous
    source: str = ""
