#!/usr/bin/env python3
"""
Sofi MCP Broker — Agent Communication & Tool Building System
==============================================================
نظام التواصل المتقدم بين الوكلاء — تشاور، بحث، بناء أدوات، توزيع مهارات

يتكون من:
  • protocols.py       — بروتوكولات الاتصال وأنواع الرسائل
  • message_bus.py     — نظام توجيه الرسائل
  • agent_communicator.py — تواصل الوكلاء
  • consultation_engine.py — تشاور عميق بين الوكلاء
  • research_engine.py     — بحث وتحليل عميق
  • tool_builder.py        — بناء أدوات PY خاصة
  • skill_registry.py      — إدارة وتوزيع المهارات
  • agent_network.py       — طوبولوجيا الشبكة
"""

from .protocols import (
    MessageType, MessagePriority, Message, AgentAddress,
    CommunicationProtocol, SkillClaim, ToolSpec
)
from .message_bus import MessageBus
from .agent_communicator import AgentCommunicator
from .consultation_engine import ConsultationEngine, ConsultationSession
from .research_engine import ResearchEngine, ResearchReport
from .tool_builder import ToolBuilder, BuiltTool
from .skill_registry import SkillRegistry, SkillDefinition
from .agent_network import AgentNetwork, NetworkTopology
