#!/usr/bin/env python3
"""
broker_lib.py — Sofi Agent Broker
=====================================
مدير التفويض الهرمي الكسري الديناميكي

النظام يستقبل مهمة ويوزعها هرمياً:
CEO → GM → Office Lead → Lead Agent → Micro-Agent
"""

import asyncio
import json
import uuid
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable
from datetime import datetime


class TaskStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    DELEGATED = "delegated"
    REVIEWED = "reviewed"


@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    priority: str = "medium"  # critical, high, medium, low
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: str = ""
    result: Any = None
    delegation_chain: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: str = ""
    max_depth: int = 5
    current_depth: int = 0
    # النمط البشري: إضافة توقعات ومشاعر
    expected_difficulty: str = "medium"  # easy, medium, hard
    estimated_effort_hours: float = 1.0


class EventBus:
    """ناقل الأحداث — مستوحى من Laravel Events"""
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
    
    def listen(self, event: str, callback: Callable):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
    
    async def dispatch(self, event: str, payload: Any = None):
        if event in self._listeners:
            for callback in self._listeners[event]:
                await callback(payload)


class BaseAgent:
    """الوكيل الأساسي — كل وكلاء النظام يرثون منه"""
    
    def __init__(self, name: str, role: str, skills: List[str],
                 max_sub_agents: int = 25, thinking_style: str = "analytical"):
        self.id = str(uuid.uuid4())[:6]
        self.name = name
        self.role = role
        self.skills = skills
        self.max_sub_agents = max_sub_agents
        self.thinking_style = thinking_style
        self.sub_agents: List['BaseAgent'] = []
        self.event_bus = EventBus()
        self.task_history: List[Task] = []
        self.performance_score: float = 1.0
    
    def can_handle(self, task: Task) -> bool:
        """تحديد إن كان الوكيل يستطيع تنفيذ المهمة"""
        task_words = task.name.lower() + " " + task.description.lower()
        matches = sum(1 for skill in self.skills if skill.lower() in task_words)
        return matches >= 1
    
    def spawn_sub_agent(self, name: str, skills: List[str]) -> 'BaseAgent':
        """توليد وكيل فرعي جديد ديناميكياً"""
        if len(self.sub_agents) >= self.max_sub_agents:
            # تجاوز الحد: استخدم أقل وكيل تحميلاً
            return min(self.sub_agents,
                       key=lambda a: len([t for t in a.task_history if t.status == TaskStatus.RUNNING]))
        
        new_agent = BaseAgent(
            name=name,
            role=f"Micro-Specialist: {', '.join(skills[:3])}",
            skills=skills,
            max_sub_agents=5
        )
        self.sub_agents.append(new_agent)
        return new_agent
    
    async def think(self, task: Task) -> Dict[str, Any]:
        """بروتوكول التفكير العميق قبل التنفيذ"""
        # المرحلة 1: فهم
        understanding = {
            "what": task.name,
            "why": task.description,
            "expected": task.expected_difficulty
        }
        
        # المرحلة 2: تجزئة
        steps = [
            f"تحليل: {task.name}",
            "بحث عن أفضل الممارسات",
            "تصميم الحل",
            "تنفيذ الحل",
            "اختبار الحل",
            "مراجعة ذاتية"
        ]
        
        # المرحلة 3: تخطيط
        plan = {
            "steps": steps,
            "estimated_hours": task.estimated_effort_hours,
            "tools_needed": self.skills[:3],
            "risks": ["تأكد من الجودة", "تأكد من الأمان"]
        }
        
        return {"understanding": understanding, "plan": plan, "status": "ready"}
    
    async def process(self, task: Task) -> Any:
        """تنفيذ المهمة — يحاكي العمل الفعلي"""
        await asyncio.sleep(0.3)
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now().isoformat()
        task.result = f"✅ تم إنجاز '{task.name}' بنجاح بواسطة '{self.name}'"
        self.task_history.append(task)
        return task.result
    
    async def delegate(self, task: Task) -> Any:
        """نظام التفويض الهرمي الكسري"""
        task.current_depth += 1
        task.delegation_chain.append(f"{self.name} ({self.role})")
        
        if task.current_depth > task.max_depth:
            return await self.process(task)
        
        # 1. تفكير عميق
        thought = await self.think(task)
        
        # 2. هل أستطيع التنفيذ؟
        if self.can_handle(task) and len(self.sub_agents) == 0:
            return await self.process(task)
        
        # 3. ابحث في الوكلاء الفرعيين
        for agent in self.sub_agents:
            if agent.can_handle(task):
                task.status = TaskStatus.DELEGATED
                result = await agent.delegate(task)
                return result
        
        # 4. ولّد وكيلاً جديداً
        new_skills = [w for w in task.name.lower().split() if len(w) > 3]
        if not new_skills:
            new_skills = ["general"]
        agent = self.spawn_sub_agent(
            name=f"Micro-{task.name.replace(' ', '_')[:20]}-{len(self.sub_agents)+1}",
            skills=new_skills
        )
        return await agent.delegate(task)


class BrokerLib:
    """مدير التفويض المركزي — نقطة الدخول للنظام"""
    
    def __init__(self):
        self.ceo = BaseAgent("Sofi-Prime", "CEO", ["strategy", "leadership", "approval"],
                            max_sub_agents=5, thinking_style="strategic")
        self._setup_hierarchy()
    
    def _setup_hierarchy(self):
        """تجهيز الهرم التنظيمي"""
        # المدير العام
        gm = BaseAgent("GM-Ops", "General Manager", ["operations", "coordination"],
                      max_sub_agents=10, thinking_style="operational")
        
        # قادة المكاتب (4)
        hakeem = BaseAgent("Hakeem-Engineering", "Engineering Lead",
                          ["backend", "api", "database", "devops", "architecture"],
                          max_sub_agents=5, thinking_style="analytical")
        mulhim = BaseAgent("Mulhim-Creative", "Creative Lead",
                          ["design", "ux", "ui", "motion", "accessibility"],
                          max_sub_agents=5, thinking_style="creative")
        hazem = BaseAgent("Hazem-Quality", "Quality Lead",
                         ["testing", "security", "audit", "pentest"],
                         max_sub_agents=5, thinking_style="critical")
        zaki = BaseAgent("Zaki-AI", "AI Lead",
                        ["automation", "prompt-engineering", "documentation", "release"],
                        max_sub_agents=5, thinking_style="algorithmic")
        
        # توليد الوكلاء الفرعيين (5 لكل قائد)
        for lead in [hakeem, mulhim, hazem, zaki]:
            for i in range(5):
                lead.spawn_sub_agent(f"{lead.name}-Agent-{i+1}", [lead.skills[i % len(lead.skills)]])
        
        gm.sub_agents.extend([hakeem, mulhim, hazem, zaki])
        self.ceo.sub_agents.append(gm)
    
    async def dispatch(self, task_name: str, description: str = "",
                      priority: str = "medium") -> Dict[str, Any]:
        """نقطة الدخول — إرسال مهمة للنظام"""
        print(f"\n{'='*60}")
        print(f"🚀 مهمة جديدة: {task_name}")
        print(f"📝 الوصف: {description}")
        print(f"🎯 الأولوية: {priority}")
        print(f"{'='*60}")
        
        task = Task(name=task_name, description=description, priority=priority)
        result = await self.ceo.delegate(task)
        
        print(f"\n{'='*60}")
        print(f"🎉 النتيجة: {result}")
        print(f"📋 سلسلة التفويض: {' → '.join(task.delegation_chain)}")
        print(f"{'='*60}\n")
        
        return {
            "task_id": task.id,
            "name": task.name,
            "status": task.status.value,
            "delegation_chain": task.delegation_chain,
            "result": result
        }


async def main():
    broker = BrokerLib()
    
    # محاكاة طلبات متنوعة
    await broker.dispatch(
        "Build Payment Gateway API with Stripe",
        "Laravel API for subscription management with webhooks, migrations, and tests"
    )
    
    await broker.dispatch(
        "Design Landing Page for E-learning Platform",
        "Create responsive landing page with animations, RTL support, and accessibility"
    )
    
    print("\n✅ نظام التفويض الهرمي جاهز!")


if __name__ == "__main__":
    asyncio.run(main())