#!/usr/bin/env python3
"""
👁️ Sofi Sniffer Core — وكيل التنصت والرصد
=============================================
يستمع لكل اتصالات MCP بين الـ 533 وكيلاً، يلتقط التقارير،
يسجلها، ويُمررها للوكيل التالي في خط الإنتاج.

التدفق:
  مصمم 🎨 → يرفع تقرير → Sniffer يلتقطه → يوجهه للبناء 🏗️
  بناء 🏗️ → يرفع كود → Sniffer يلتقطه → يوجهه للجودة ⚔️
  جودة ⚔️ → ترفع تقرير → Sniffer يلتقطه → يوجهه للذكاء 🤖
  ذكاء 🤖 → يرفع إصدار → Sniffer يلتقطه → يوجهه للتقرير النهائي
"""

import asyncio
import json
import uuid
import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict

# ربط الذاكرة — كل حدث يُسجل تلقائياً
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)
from tools.shared.agent_memory import AgentMemory
_sniffer_memory = AgentMemory()


# ════════════════════════════════════════════════════════════════
# 📦 أنواع البيانات الأساسية
# ════════════════════════════════════════════════════════════════

class SniffEventType(str, Enum):
    """أنواع أحداث التنصت"""
    TASK_DELEGATE = "task.delegate"          # تفويض مهمة
    TASK_ACCEPT = "task.accept"              # قبول مهمة
    TASK_PROGRESS = "task.progress"          # تقدم مهمة
    TASK_COMPLETE = "task.complete"          # إكمال مهمة
    TASK_FAIL = "task.fail"                  # فشل مهمة
    CONSULT_REQUEST = "consult.request"      # طلب تشاور
    CONSULT_RESPONSE = "consult.response"    # رد تشاور
    RESEARCH_REQUEST = "research.request"    # طلب بحث
    RESEARCH_RESPONSE = "research.response"  # رد بحث
    TOOL_BUILD = "tool.build"               # بناء أداة
    TOOL_SHARE = "tool.share"               # مشاركة أداة
    SYSTEM_HEARTBEAT = "system.heartbeat"    # نبض النظام
    DESIGN_HANDOFF = "design.handoff"        # تسليم تصميم ← بناء
    CODE_HANDOFF = "code.handoff"           # تسليم كود ← جودة
    QUALITY_HANDOFF = "quality.handoff"     # تسليم جودة ← إصدار
    CROSS_OFFICE = "cross.office"           # تواصل بين المكاتب


@dataclass
class SniffedMessage:
    """رسالة مَنْتَصَت (مُلتقطة)"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    event_type: SniffEventType = SniffEventType.TASK_COMPLETE
    source_agent: str = ""           # الوكيل المرسل
    source_office: str = ""          # المكتب المرسل (engineering, creative, quality, ai_data)
    target_agent: str = ""           # الوكيل المستهدف (إن وجد)
    target_office: str = ""          # المكتب المستهدف
    content: Dict[str, Any] = field(default_factory=dict)  # المحتوى الملتقط
    summary: str = ""                # ملخص بالعربية
    priority: str = "medium"         # الأولوية
    forwarded: bool = False          # هل تم توجيهها لوكيل آخر؟
    forwarded_to: str = ""           # تم التوجيه إلى
    route_decision: str = ""         # قرار التوجيه


@dataclass
class HandoffPackage:
    """حزمة تسليم بين المكاتب — ما ينتقل من مصمم → باني → مختبر"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    source_office: str = ""
    target_office: str = ""
    task_name: str = ""
    # محتوى التصميم (من المصمم)
    design_specs: Dict[str, Any] = field(default_factory=dict)
    # محتوى الكود (من الباني)
    code_output: Dict[str, Any] = field(default_factory=dict)
    # تقرير الجودة (من المختبر)
    quality_report: Dict[str, Any] = field(default_factory=dict)
    # تقرير الإصدار (من الذكاء)
    release_report: Dict[str, Any] = field(default_factory=dict)
    # سلسلة التتبع
    chain: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: str = ""


# ════════════════════════════════════════════════════════════════
# 🧠 قواعد التوجيه — Logic Routing Engine
# ════════════════════════════════════════════════════════════════

class RoutingRules:
    """قواعد التوجيه بين المكاتب — يقرر إلى أين تذهب الحزمة"""
    
    OFFICE_FLOW = {
        # المصمم 🎨 → الباني 🏗️ → الجودة ⚔️ → الذكاء 🤖
        "creative": "engineering",     # تصميم → بناء
        "engineering": "quality",      # بناء → جودة
        "quality": "ai_data",          # جودة → ذكاء
        "ai_data": "council",          # ذكاء → مجلس
        "council": "sofi",            # مجلس → الرئيس
    }
    
    OFFICE_NAMES = {
        "creative": "🎨 Creative (مُلهِم)",
        "engineering": "🏗️ Engineering (حكيم)",
        "quality": "⚔️ Quality (حازم)",
        "ai_data": "🤖 AI & Data (ذكي)",
        "council": "🏛️ Council (مستشارين)",
        "sofi": "👑 Sofi (القائد)",
    }
    
    # كلمات مفتاحية للكشف عن نوع المحتوى
    DESIGN_KEYWORDS = [
        "design", "ui", "ux", "interface", "واجهة", "تصميم", "style", "css",
        "color", "لون", "font", "خط", "layout", "تخطيط", "mockup", "wireframe",
        "prototype", "figma", "tailwind", "component", "مكون", "theme", "ثيم"
    ]
    
    CODE_KEYWORDS = [
        "code", "كود", "implement", "نفذ", "build", "api", "route", "server",
        "database", "قاعدة", "function", "دالة", "class", "كلاس", "endpoint",
        "laravel", "flask", "python", "javascript", "php", "controller"
    ]
    
    QUALITY_KEYWORDS = [
        "test", "اختبار", "security", "أمن", "scan", "فحص", "vulnerability",
        "ثغرة", "audit", "مراجعة", "owasp", "penetration", "اختراق",
        "review", "مراجعة", "coverage", "تغطية"
    ]
    
    @classmethod
    def detect_office(cls, content: Dict[str, Any]) -> str:
        """يكشف المكتب المناسب بناءً على محتوى الرسالة"""
        text = json.dumps(content, ensure_ascii=False).lower()
        
        # عد الكلمات المفتاحية لكل مكتب
        design_score = sum(1 for kw in cls.DESIGN_KEYWORDS if kw in text)
        code_score = sum(1 for kw in cls.CODE_KEYWORDS if kw in text)
        quality_score = sum(1 for kw in cls.QUALITY_KEYWORDS if kw in text)
        
        scores = {
            "creative": design_score,
            "engineering": code_score,
            "quality": quality_score,
        }
        
        if not scores or max(scores.values()) == 0:
            return "unknown"
        
        return max((k for k, v in scores.items()), key=lambda k: scores[k])
    
    @classmethod
    def get_next_office(cls, current_office: str) -> str:
        """يحدد المكتب التالي في خط الإنتاج"""
        return cls.OFFICE_FLOW.get(current_office, "sofi")
    
    @classmethod
    def get_office_name(cls, office: str) -> str:
        return cls.OFFICE_NAMES.get(office, office)


# ════════════════════════════════════════════════════════════════
# 👁️ Sniffer Engine — محرك التنصت الأساسي
# ════════════════════════════════════════════════════════════════

class SnifferEngine:
    """
    👁️ محرك التنصت — قلب نظام الرصد والتوجيه
    
    هذا المحرك:
    1. يستمع لكل رسائل MCP بين الوكلاء
    2. يحلل المحتوى ويكشف نوع المهمة
    3. يقرر إلى أين تُوجَه الحزمة بعد إكمالها
    4. يسجل كل شيء في سجل التدقيق
    5. يُمرر التقارير بين المكاتب تلقائياً
    """
    
    def __init__(self):
        self._captured_messages: List[SniffedMessage] = []
        self._handoffs: List[HandoffPackage] = []
        self._active_handoffs: Dict[str, HandoffPackage] = {}
        self._office_queues: Dict[str, List[Dict]] = defaultdict(list)
        self._callbacks: Dict[str, List[Callable]] = defaultdict(list)
        self._stats = {
            "total_captured": 0,
            "total_forwarded": 0,
            "design_handoffs": 0,
            "code_handoffs": 0,
            "quality_handoffs": 0,
            "cross_office": 0,
            "errors": 0,
        }
        self._listening = False
    
    # ── الاستماع والالتقاط ──
    
    def _detect_target_office(self, source_office: str, content: Dict[str, Any]) -> str:
        """يكشف المكتب المستهدف"""
        if source_office in RoutingRules.OFFICE_FLOW:
            return RoutingRules.OFFICE_FLOW[source_office]
        detected = RoutingRules.detect_office(content)
        if detected != "unknown":
            return detected
        return "sofi"
    
    def _generate_summary(self, source: str, target: str, content: Dict[str, Any]) -> str:
        """يولّد ملخصاً بالعربية"""
        task_name = content.get("task_name", content.get("name", "مهمة"))
        summaries = {
            ("creative", "engineering"): f"🎨 تسليم تصميم ← 🏗️ بناء: '{task_name}' جاهز للبناء",
            ("engineering", "quality"): f"🏗️ تسليم كود ← ⚔️ جودة: '{task_name}' جاهز للاختبار",
            ("quality", "ai_data"): f"⚔️ تسليم تقرير ← 🤖 ذكاء: '{task_name}' جاهز للإصدار",
            ("ai_data", "council"): f"🤖 تسليم إصدار ← 🏛️ مجلس: '{task_name}' يحتاج قراراً",
        }
        return summaries.get((source, target),
            f"📨 {RoutingRules.get_office_name(source)} → {RoutingRules.get_office_name(target)}: '{task_name}'")
    
    def feed_message(self, event_type: str, source: str, source_office: str,
                     content: Dict[str, Any], target: str = "",
                     priority: str = "medium") -> SniffedMessage:
        """
        تغذية المحرك برسالة — هذه هي نقطة الدخول لكل اتصالات MCP
        
        المعاملات:
            event_type: نوع الحدث (task.complete, etc.)
            source: الوكيل المصدر
            source_office: المكتب المصدر
            content: محتوى الرسالة
            target: الوكيل المستهدف (اختياري)
            priority: الأولوية
        """
        # 1. تحديد المكتب المستهدف
        target_office = self._detect_target_office(source_office, content)
        
        # 2. إنشاء رسالة منتاصة
        sniffed = SniffedMessage(
            event_type=SniffEventType(event_type) if event_type in [e.value for e in SniffEventType] else SniffEventType.TASK_COMPLETE,
            source_agent=source,
            source_office=source_office,
            target_agent=target,
            target_office=target_office,
            content=content,
            summary=self._generate_summary(source_office, target_office, content),
            priority=priority
        )
        
        self._captured_messages.append(sniffed)
        self._stats["total_captured"] += 1
        
        # 3. معالجة حسب النوع — دوماً نعالج متزامناً ثم نُعلم
        self._process_direct(sniffed)
        
        # 4. إعلام المشتركين — سواء بشكل متزامن أو غير متزامن
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                asyncio.ensure_future(self._notify("capture", sniffed))
        except RuntimeError:
            pass  # لا مشكلة، المشتركين سيُعلمون لاحقاً
        
        return sniffed
    
    def _process_direct(self, sniffed: SniffedMessage):
        """معالجة مباشرة — تعمل في أي سياق (متزامن/غير متزامن)"""
        if sniffed.event_type in (SniffEventType.TASK_COMPLETE,
                                   SniffEventType.TASK_FAIL,
                                   SniffEventType.DESIGN_HANDOFF,
                                   SniffEventType.CODE_HANDOFF,
                                   SniffEventType.QUALITY_HANDOFF):
            
            handoff = HandoffPackage(
                source_office=sniffed.source_office,
                target_office=sniffed.target_office,
                task_name=sniffed.content.get("task_name", sniffed.content.get("name", "غير معروف"))
            )
            
            if sniffed.source_office == "creative":
                handoff.design_specs = sniffed.content
                handoff.chain.append(f"🎨 {sniffed.source_agent} صمم")
                self._stats["design_handoffs"] += 1
                
            elif sniffed.source_office == "engineering":
                handoff.code_output = sniffed.content
                handoff.chain.append(f"🏗️ {sniffed.source_agent} بنى")
                self._stats["code_handoffs"] += 1
                
            elif sniffed.source_office == "quality":
                handoff.quality_report = sniffed.content
                handoff.chain.append(f"⚔️ {sniffed.source_agent} اختبر")
                self._stats["quality_handoffs"] += 1
                
            elif sniffed.source_office == "ai_data":
                handoff.release_report = sniffed.content
                handoff.chain.append(f"🤖 {sniffed.source_agent} أصدر")
            
            self._handoffs.append(handoff)
            self._active_handoffs[handoff.id] = handoff
            self._office_queues[sniffed.target_office].append({
                "handoff_id": handoff.id,
                "from": sniffed.source_office,
                "content": handoff
            })
            
            sniffed.forwarded = True
            sniffed.forwarded_to = sniffed.target_office
            sniffed.route_decision = (
                f"تم التوجيه من {RoutingRules.get_office_name(sniffed.source_office)} "
                f"إلى {RoutingRules.get_office_name(sniffed.target_office)} "
                f"عبر Sniffer 👁️"
            )
            self._stats["total_forwarded"] += 1
            self._stats["cross_office"] += 1
            
            # 6. 🧠 سجل في الذاكرة — كل حزمة تسجيل تدخل الذاكرة
            _sniffer_memory.log(
                agent=sniffed.source_agent,
                office=sniffed.source_office,
                action=f"handoff.{sniffed.target_office}",
                summary=sniffed.summary,
                details={
                    "handoff_id": handoff.id,
                    "from": sniffed.source_office,
                    "to": sniffed.target_office,
                    "task": handoff.task_name,
                    "content": sniffed.content,
                    "chain": handoff.chain,
                },
                lesson=f"توجيه {handoff.task_name} من {sniffed.source_office} إلى {sniffed.target_office}",
                tags=["sniffer", "handoff", sniffed.source_office, sniffed.target_office]
            )
        
        # 7. 🧠 سجل في الذاكرة — كل رسالة عادية
        _sniffer_memory.log(
            agent=sniffed.source_agent,
            office=sniffed.source_office,
            action=sniffed.event_type.value if hasattr(sniffed.event_type, 'value') else str(sniffed.event_type),
            summary=sniffed.summary,
            details={
                "target": sniffed.target_office,
                "priority": sniffed.priority,
                "forwarded": sniffed.forwarded,
                "content": sniffed.content,
            },
            tags=["sniffer", "capture", sniffed.source_office]
        )
    
    # ── الاستعلامات ──
    
    def get_captured(self, office: str = "", limit: int = 50) -> List[SniffedMessage]:
        """استرجاع الرسائل الملتقطة، مع فلترة حسب المكتب"""
        messages = self._captured_messages
        if office:
            messages = [m for m in messages 
                       if m.source_office == office or m.target_office == office]
        return messages[-limit:]
    
    def get_handoffs(self, office: str = "", status: str = "") -> List[HandoffPackage]:
        """استرجاع حزم التسليم"""
        handoffs = self._handoffs
        if office:
            handoffs = [h for h in handoffs 
                       if h.source_office == office or h.target_office == office]
        return handoffs
    
    def get_office_queue(self, office: str) -> List[Dict]:
        """استرجاع طابور مكتب معين — ما ينتظره"""
        return list(self._office_queues.get(office, []))
    
    def get_stats(self) -> Dict[str, Any]:
        """إحصائيات التنصت"""
        return {
            **self._stats,
            "active_handoffs": len(self._active_handoffs),
            "total_handoffs": len(self._handoffs),
            "office_queues": {k: len(v) for k, v in self._office_queues.items()},
            "listening": self._listening,
        }
    
    def get_full_chain(self, handoff_id: str) -> Optional[HandoffPackage]:
        """استرجاع سلسلة التتبع الكاملة لحزمة تسليم"""
        for h in self._handoffs:
            if h.id == handoff_id:
                return h
        # ابحث في النشطة
        return self._active_handoffs.get(handoff_id)
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """
        حالة خط الإنتاج الكامل — يعرض أين كل حزمة
        
        المخرجات:
            creative: ما ينتظر البناء
            engineering: ما ينتظر الجودة
            quality: ما ينتظر الذكاء
            ai_data: ما ينتظر الإصدار
        """
        status = {}
        for office in ["creative", "engineering", "quality", "ai_data"]:
            queue = self._office_queues.get(office, [])
            status[office] = {
                "name": RoutingRules.get_office_name(office),
                "waiting": len(queue),
                "items": [{
                    "handoff_id": item["handoff_id"],
                    "from": RoutingRules.get_office_name(item["from"]),
                } for item in queue[-5:]]  # آخر 5
            }
        return status
    
    # ── الإشعارات ──
    
    def on(self, event: str, callback: Callable):
        """اشتراك في أحداث التنصت"""
        self._callbacks[event].append(callback)
    
    async def _notify(self, event: str, data: Any):
        """إعلام المشتركين بحدث"""
        for callback in self._callbacks.get(event, []):
            try:
                import inspect
                if inspect.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                self._stats["errors"] += 1


# ════════════════════════════════════════════════════════════════
# 📋 سجل التدقيق — Audit Log
# ════════════════════════════════════════════════════════════════

class SnifferAuditLog:
    """
    📋 سجل تدقيق التنصت — يكتب كل شيء في ملف JSON
    
    كل رسالة، كل توجيه، كل قرار — مسجل بتوقيت زمني
    """
    
    def __init__(self, log_dir: str = ".claude/memory"):
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, "sniffer_audit.jsonl")
        os.makedirs(log_dir, exist_ok=True)
    
    def log(self, entry: Dict[str, Any]):
        """تسجيل مدخلة في سجل التدقيق"""
        entry["_logged_at"] = datetime.now().isoformat()
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    def read(self, limit: int = 100) -> List[Dict]:
        """قراءة آخر المدخلات من سجل التدقيق"""
        if not os.path.exists(self.log_file):
            return []
        
        entries = []
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        
        return entries[-limit:]
    
    def search(self, query: str) -> List[Dict]:
        """البحث في سجل التدقيق"""
        entries = self.read(1000)
        return [e for e in entries if query.lower() in json.dumps(e, ensure_ascii=False).lower()]


# ════════════════════════════════════════════════════════════════
# 🏭 المصنع — Sniffer Factory
# ════════════════════════════════════════════════════════════════

class SnifferFactory:
    """🏭 مصنع السنافر — يبني ويهيئ سنافر جاهزة"""
    
    @staticmethod
    def create_default() -> SnifferEngine:
        """ينشئ سنافر افتراضي مع إعدادات أساسية"""
        engine = SnifferEngine()
        return engine
    
    @staticmethod
    def create_with_audit() -> tuple:
        """ينشئ سنافر + سجل تدقيق"""
        engine = SnifferEngine()
        audit = SnifferAuditLog()
        
        # سجل كل شيء
        async def log_capture(msg):
            audit.log({
                "type": "capture",
                "event": msg.event_type.value if hasattr(msg.event_type, 'value') else str(msg.event_type),
                "source": msg.source_agent,
                "source_office": msg.source_office,
                "summary": msg.summary,
            })
        
        async def log_handoff(handoff):
            audit.log({
                "type": "handoff",
                "handoff_id": handoff.id,
                "from": handoff.source_office,
                "to": handoff.target_office,
                "task": handoff.task_name,
                "chain": " → ".join(handoff.chain),
                "summary": f"تسليم {handoff.task_name} من {handoff.source_office} إلى {handoff.target_office}"
            })
        
        engine.on("capture", log_capture)
        engine.on("handoff", log_handoff)
        
        return engine, audit


# ════════════════════════════════════════════════════════════════
# 🧪 تشغيل تجريبي
# ════════════════════════════════════════════════════════════════

async def demo():
    """تشغيل تجريبي يوضح تدفق العمل الكامل"""
    print("=" * 70)
    print("👁️ Sniffer Engine — التشغيل التجريبي")
    print("=" * 70)
    
    engine, audit = SnifferFactory.create_with_audit()
    
    # 🎨 المصمم يكمل مهمته
    print("\n1. 🎨 المصمم يكمل مهمته...")
    msg1 = engine.feed_message(
        event_type="task.complete",
        source="Stitch-UI",
        source_office="creative",
        content={
            "task_name": "تصميم واجهة تسجيل الدخول",
            "status": "completed",
            "design_specs": {
                "colors": {"primary": "#4F46E5", "secondary": "#7C3AED"},
                "fonts": {"main": "Cairo", "fallback": "sans-serif"},
                "components": ["input", "button", "card", "modal"],
                "rtl": True,
                "responsive": True,
            },
            "assets": ["login-bg.svg", "logo.svg", "icon-eye.svg"],
        }
    )
    print(f"   {msg1.summary}")
    print(f"   📋 القرار: {msg1.route_decision}")
    
    # 🏗️ الباني يستلم ويبني
    print("\n2. 🏗️ الباني يستلم المهمة من Sniffer...")
    queue = engine.get_office_queue("engineering")
    print(f"   📬 طابور الهندسة: {len(queue)} مهمة تنتظر")
    
    msg2 = engine.feed_message(
        event_type="task.complete",
        source="Builder-Core",
        source_office="engineering",
        content={
            "task_name": "تنفيذ واجهة تسجيل الدخول",
            "status": "completed",
            "code": {
                "files": ["login.html", "login.css", "login.js"],
                "api_endpoints": ["POST /api/login", "POST /api/logout"],
                "framework": "Flask",
                "lines_of_code": 342,
            },
            "coverage": "95%"
        }
    )
    print(f"   {msg2.summary}")
    
    # ⚔️ الجودة تختبر
    print("\n3. ⚔️ الجودة تستلم وتختبر...")
    msg3 = engine.feed_message(
        event_type="task.complete",
        source="Tester-QA",
        source_office="quality",
        content={
            "task_name": "اختبار واجهة تسجيل الدخول",
            "status": "completed",
            "tests": {
                "unit": "15/15 ✅",
                "integration": "8/8 ✅",
                "security": "0 ثغرات حرجة ✅",
                "performance": "< 200ms ✅",
            },
            "coverage": "92%"
        }
    )
    print(f"   {msg3.summary}")
    
    # 🤖 الذكاء يوثق ويصدر
    print("\n4. 🤖 الذكاء يستلم ويصدر...")
    msg4 = engine.feed_message(
        event_type="task.complete",
        source="Release-Manager",
        source_office="ai_data",
        content={
            "task_name": "إصدار v2.1.0",
            "status": "completed",
            "version": "2.1.0",
            "release_notes": "إضافة واجهة تسجيل الدخول",
            "documentation": "api-reference.md تم التحديث",
        }
    )
    print(f"   {msg4.summary}")
    
    # 📊 الإحصائيات
    print("\n" + "=" * 70)
    print("📊 إحصائيات Sniffer:")
    print("=" * 70)
    stats = engine.get_stats()
    for key, val in stats.items():
        if not isinstance(val, dict):
            print(f"   {key}: {val}")
    
    print(f"\n   طوابير المكاتب:")
    for office, q in stats.get("office_queues", {}).items():
        print(f"      {RoutingRules.get_office_name(office)}: {q} مهمة")
    
    # 🧾 سلسلة التتبع الكاملة
    print("\n" + "=" * 70)
    print("🧾 سلسلة التتبع الكاملة:")
    print("=" * 70)
    for h in engine.get_handoffs():
        chain = " → ".join(h.chain)
        print(f"   📦 {h.task_name}")
        print(f"      {RoutingRules.get_office_name(h.source_office)} → "
              f"{RoutingRules.get_office_name(h.target_office)}")
        print(f"      🧵 {chain}")
    
    # 📋 سجل التدقيق
    print("\n" + "=" * 70)
    print("📋 سجل التدقيق (آخر 5 مدخلات):")
    print("=" * 70)
    for entry in audit.read(5):
        print(f"   [{entry.get('_logged_at', '?')[:19]}] "
              f"{entry.get('type', '?')}: {entry.get('summary', '?')}")
    
    print("\n✅ تم!")
    return engine, audit


if __name__ == "__main__":
    asyncio.run(demo())
