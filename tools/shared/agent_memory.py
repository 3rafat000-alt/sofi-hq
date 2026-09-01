#!/usr/bin/env python3
"""
🧠 Sofi Memory Hub — التسجيل الإلزامي لكل الـ 534 وكيلاً
==========================================================
كل وكيل في النظام يسجّل كل حدث في جميع أنواع الذاكرة.
هذا هو القلب الذي يضمن أن لا شيء يضيع.

أنظمة الذاكرة:
  📝 Episodic  : الأحداث والتجارب (من تعلم ماذا؟)
  🧠 Semantic  : المعرفة والمفاهيم (ماذا يعرف النظام؟)
  ⚡ Working   : السياق القصير (ماذا يحدث الآن؟)
  🔄 Procedural: الإجراءات القابلة لإعادة الاستخدام (كيف نعمل؟)
  📋 Audit     : سجل التدقيق الدائم (JSONL)

الاستخدام:
  from tools.shared.agent_memory import AgentMemory
  mem = AgentMemory()
  mem.log(
      agent="Builder-1",
      office="engineering",
      action="task.complete",
      summary="بنيت واجهة تسجيل الدخول",
      details={"files": ["login.html"], "lines": 120},
      lesson="استخدام Flexbox أسرع من Grid في هذا السياق"
  )
"""

import json
import os
import sys
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any

# استيراد أنواع الذاكرة الأساسية
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, PROJECT_ROOT)
from tools.shared.memory_core import MemoryCore, MEMORY_DB_DIR


class AgentMemory:
    """
    🧠 Sofi Memory Hub — محرك التسجيل الموحد
    
    كل وكيل من الـ 534 وكيلاً يسجل عبر هذه الواجهة.
    التسجيل يتم في 4 أنظمة ذاكرة + سجل تدقيق JSONL.
    
    المبادئ:
      1. كل حدث يُسجل في 5 أماكن دفعة واحدة
      2. لا يوجد حدث بدون تسجيل
      3. التسجيل تلقائي — الوكيل لا يفكر في "أين أسجل؟"
      4. كل شيء مرتبط بزمن + وكيل + مكتب
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        # الذاكرة الأساسية (4 أنواع)
        self.core = MemoryCore()
        
        # سجل التدقيق JSONL
        self.audit_dir = MEMORY_DB_DIR
        self.audit_file = os.path.join(self.audit_dir, "sofi_audit.jsonl")
        os.makedirs(self.audit_dir, exist_ok=True)
        
        # الإحصائيات
        self._stats = {
            "total_logs": 0,
            "errors": 0,
            "by_office": {},
            "by_action": {},
        }
        self._stats_lock = threading.Lock()
        
        # ملف لكل شهر — تسجيل دوري
        self._monthly_file = None
        self._current_month = ""
    
    # ════════════════════════════════════════════════════════════
    # 📝 واجهة التسجيل الموحدة — الوكيل ينادي دالة واحدة
    # ════════════════════════════════════════════════════════════
    
    def log(self, 
            agent: str,              # اسم الوكيل (مثال: Stitch-UI, Builder-3)
            office: str,             # المكتب (creative, engineering, quality, ai_data, council, sofi, sniffer)
            action: str,             # الإجراء (task.complete, task.fail, consult.request, etc.)
            summary: str,            # ملخص بالعربية
            details: Dict = None,    # تفاصيل كاملة (JSON)
            lesson: str = "",        # درس مستفاد (إن وجد)
            tags: List[str] = None,  # وسوم للتصنيف
            priority: str = "medium" # الأولوية
        ) -> Dict[str, Any]:
        """
        📝 التسجيل الموحد — كل شيء في دالة واحدة
        
        هذه الدالة تسجل في 5 أنظمة دفعة واحدة:
          1. 📋 Audit Log (JSONL) — السجل الدائم
          2. 📝 Episodic Memory — الأحداث والتجارب
          3. 🧠 Semantic Memory — المعرفة والمفاهيم
          4. ⚡ Working Memory — السياق القصير
          5. 🔄 Procedural Memory — إنشاء إجراءات قابلة لإعادة الاستخدام
        """
        details = details or {}
        tags = tags or [office, action.split(".")[0]]
        
        # توحيد البيانات
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "office": office,
            "action": action,
            "summary": summary,
            "details": details,
            "lesson": lesson,
            "tags": tags,
            "priority": priority,
        }
        
        results = {}
        
        try:
            # 1. 📋 سجل التدقيق JSONL (دائم، سريع، خفيف)
            results["audit"] = self._write_audit(entry)
            
            # 2. 📝 الذاكرة العرضية (Episodic) — الأحداث والدروس
            event_data = {
                "summary": summary,
                "details": details,
                "lesson": lesson,
                "priority": priority,
            }
            if lesson:
                event_data["lesson"] = lesson
            ep_id = self.core.record_event(action, event_data, agent=agent)
            results["episodic"] = ep_id
            
            # 3. 🧠 الذاكرة الدلالية (Semantic) — المعرفة للبحث المستقبلي
            knowledge_text = f"[{office}] {agent}: {summary}"
            if details:
                knowledge_text += f" | {json.dumps(details, ensure_ascii=False)[:500]}"
            sem_id = self.core.store_knowledge(
                knowledge_text,
                tags=tags + [agent, office, action],
                metadata={"agent": agent, "office": office, "action": action, "time": entry["timestamp"]}
            )
            results["semantic"] = sem_id
            
            # 4. ⚡ الذاكرة العاملة (Working) — آخر حدث لكل وكيل
            self.core.set_context(
                f"agent:{agent}:last_action",
                entry,
                ttl=86400  # 24 ساعة
            )
            # آخر 10 أحداث للمكتب
            self.core.set_context(
                f"office:{office}:last_action",
                entry,
                ttl=3600  # ساعة
            )
            results["working"] = True
            
            # 5. 🔄 الذاكرة الإجرائية (Procedural) — إذا كان هناك درس أو إجراء متكرر
            if lesson and len(lesson) > 10:
                proc_name = f"{office}_{action}_{agent}_{int(time.time()) % 10000}"
                self.core.store_procedure(
                    proc_name,
                    steps=[
                        {"description": summary, "action": action, "agent": agent},
                        {"description": f"Lesson: {lesson}", "action": "learn"},
                    ],
                    description=f"{agent}: {summary}",
                    tags=tags
                )
                results["procedural"] = proc_name
            
            # تحديث الإحصائيات
            with self._stats_lock:
                self._stats["total_logs"] += 1
                self._stats["by_office"][office] = self._stats["by_office"].get(office, 0) + 1
                self._stats["by_action"][action] = self._stats["by_action"].get(action, 0) + 1
            
            results["success"] = True
            
        except Exception as e:
            with self._stats_lock:
                self._stats["errors"] += 1
            results["success"] = False
            results["error"] = str(e)
        
        return results
    
    # ════════════════════════════════════════════════════════════
    # 📋 سجل التدقيق — JSONL
    # ════════════════════════════════════════════════════════════
    
    def _get_audit_file(self) -> str:
        """الحصول على ملف التدقيق الحالي (شهري)"""
        month = datetime.now().strftime("%Y-%m")
        if month != self._current_month:
            self._current_month = month
            self._monthly_file = os.path.join(
                self.audit_dir, f"audit_{month}.jsonl"
            )
        return self._monthly_file or self.audit_file
    
    def _write_audit(self, entry: Dict) -> bool:
        """كتابة مدخلة في سجل التدقيق"""
        try:
            with open(self.audit_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            return True
        except Exception:
            return False
    
    # ════════════════════════════════════════════════════════════
    # 📖 البحث والاسترجاع
    # ════════════════════════════════════════════════════════════
    
    def search(self, query: str, n: int = 10, tags: List[str] = None) -> List[Dict]:
        """البحث في جميع الذكريات"""
        # ذاكرة دلالية
        semantic = self.core.search_knowledge(query, n=n, tags=tags)
        
        # ذاكرة عرضية
        episodic = self.core.recall_events(n=n)
        
        # إجراءات
        procedural = self.core.search_procedures(query, tags=tags)
        
        return {
            "semantic": semantic,
            "episodic": episodic,
            "procedural": procedural,
        }
    
    def get_agent_history(self, agent: str, n: int = 20) -> List[Dict]:
        """سجل وكيل معين"""
        return self.core.recall_events(agent=agent, n=n)
    
    def get_office_history(self, office: str, n: int = 20) -> List[Dict]:
        """سجل مكتب معين"""
        events = self.core.recall_events(n=100)
        return [e for e in events if office in (e.get("data", {}).get("details", {}).get("office", "")
                                               or json.dumps(e).find(office) > -1)][:n]
    
    def get_recent_audit(self, n: int = 50) -> List[Dict]:
        """آخر مدخلات سجل التدقيق"""
        if not os.path.exists(self.audit_file):
            return []
        entries = []
        with open(self.audit_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return entries[-n:]
    
    def get_stats(self) -> Dict[str, Any]:
        """إحصائيات التسجيل"""
        with self._stats_lock:
            stats = dict(self._stats)
        
        stats["audit_file_size"] = os.path.getsize(self.audit_file) if os.path.exists(self.audit_file) else 0
        stats["memory"] = {
            "semantic": self.core.semantic.count(),
            "episodic": self.core.episodic.count(),
            "procedural": len(self.core.procedural.list_all()),
            "working": len(self.core.working.keys()),
        }
        return stats
    
    def get_logs_by_action(self, action: str, n: int = 20) -> List[Dict]:
        """فلترة حسب الإجراء"""
        events = self.core.recall_events(event_type=action, n=n)
        return events
    
    def search_audit(self, query: str, n: int = 20) -> List[Dict]:
        """بحث في سجل التدقيق"""
        entries = self.get_recent_audit(1000)
        return [e for e in entries if query.lower() in json.dumps(e, ensure_ascii=False).lower()][:n]


# ════════════════════════════════════════════════════════════════
# 🏭 المصنع — Memory Factory
# ════════════════════════════════════════════════════════════════

class MemoryFactory:
    """🏭 يبني ويهيئ AgentMemory جاهزاً للاستخدام"""
    
    @staticmethod
    def create() -> AgentMemory:
        """إنشاء AgentMemory مع إعدادات افتراضية"""
        return AgentMemory()
    
    @staticmethod
    def get_instance() -> AgentMemory:
        """الحصول على النسخة الوحيدة (Singleton)"""
        return AgentMemory()


# ════════════════════════════════════════════════════════════════
# 🔌 دالة مساعدة — لأي وكيل يسجل بسرعة
# ════════════════════════════════════════════════════════════════

# المتغير العام — أي وكيل يستدعيه مباشرة
MEMORY = AgentMemory()

def log_to_memory(agent: str, office: str, action: str, summary: str,
                  details: Dict = None, lesson: str = "", tags: List[str] = None):
    """
    🔌 دالة مساعدة — أي وكيل يسجل بسرعة
    
    المثال:
        from tools.shared.agent_memory import log_to_memory
        log_to_memory("Builder-1", "engineering", "task.complete",
                     "بنيت API تسجيل الدخول", {"endpoints": ["POST /login"]})
    """
    return MEMORY.log(agent, office, action, summary, details, lesson, tags)


# ════════════════════════════════════════════════════════════════
# 🧪 تشغيل تجريبي
# ════════════════════════════════════════════════════════════════

def demo():
    """عرض تشغيلي لكيفية تسجل الـ 534 وكيلاً في الذاكرة"""
    print("=" * 70)
    print("🧠 Sofi Memory Hub — التشغيل التجريبي")
    print("= " * 35)
    
    mem = AgentMemory()
    
    # 🎨 المصمم يسجل
    print("\n1. 🎨 المصمم يسجل في الذاكرة...")
    r1 = mem.log(
        agent="Stitch-UI",
        office="creative",
        action="task.complete",
        summary="صممت واجهة تسجيل الدخول مع دعم RTL",
        details={
            "task": "تصميم واجهة الدخول",
            "colors": {"primary": "#4F46E5"},
            "components": ["button", "input", "card"],
            "files": ["login-design.png"]
        },
        lesson="تصاميم RTL تحتاج مساحة 20% أكبر للهوامش",
        tags=["design", "ui", "rtl"]
    )
    print(f"   ✅ Episodic ID: {r1.get('episodic')}")
    print(f"   ✅ Semantic ID: {r1.get('semantic')}")
    print(f"   ✅ Audit: {r1.get('audit')}")
    
    # 🏗️ الباني يسجل
    print("\n2. 🏗️ الباني يسجل في الذاكرة...")
    r2 = mem.log(
        agent="Builder-Core",
        office="engineering",
        action="task.complete",
        summary="بنيت واجهة تسجيل الدخول بـ Flask",
        details={
            "task": "تنفيذ واجهة الدخول",
            "files": ["login.html", "login.css", "login.js"],
            "api_endpoints": ["POST /api/login", "POST /api/logout"],
            "lines_of_code": 342
        },
        tags=["backend", "flask", "api"]
    )
    print(f"   ✅ Episodic ID: {r2.get('episodic')}")
    
    # ⚔️ المختبر يسجل
    print("\n3. ⚔️ المختبر يسجل في الذاكرة...")
    r3 = mem.log(
        agent="Tester-QA",
        office="quality",
        action="task.complete",
        summary="اختبرت واجهة الدخول — كل الاختبارات ناجحة",
        details={
            "task": "اختبار واجهة الدخول",
            "tests": {"unit": "15/15 ✅", "integration": "8/8 ✅"},
            "coverage": "92%",
            "vulnerabilities": 0
        },
        tags=["testing", "qa", "security"]
    )
    print(f"   ✅ Episodic ID: {r3.get('episodic')}")
    
    # 🤖 المُصدر يسجل
    print("\n4. 🤖 المُصدر يسجل في الذاكرة...")
    r4 = mem.log(
        agent="Release-Manager",
        office="ai_data",
        action="task.complete",
        summary="أصدرت v2.1.0 مع توثيق كامل",
        details={
            "version": "2.1.0",
            "release_notes": "إضافة واجهة تسجيل الدخول",
            "docs": ["api-reference.md", "CHANGELOG.md"]
        },
        tags=["release", "documentation", "v2.1.0"]
    )
    print(f"   ✅ Episodic ID: {r4.get('episodic')}")
    
    # 👁️ Sniffer يسجل
    print("\n5. 👁️ Sniffer يسجل في الذاكرة...")
    r5 = mem.log(
        agent="Sniffer-Main",
        office="sniffer",
        action="cross.office",
        summary="وجهت حزمة التصميم من Creative إلى Engineering",
        details={
            "from": "creative",
            "to": "engineering",
            "handoff_id": "h-001",
            "content_summary": "تصميم واجهة الدخول مع RTL"
        },
        tags=["sniffer", "routing", "handoff"]
    )
    print(f"   ✅ Episodic ID: {r5.get('episodic')}")
    
    # 📊 الإحصائيات
    print("\n" + "=" * 70)
    print("📊 إحصائيات الذاكرة:")
    print("=" * 70)
    stats = mem.get_stats()
    print(f"   📝 إجمالي التسجيلات: {stats['total_logs']}")
    print(f"   ❌ أخطاء: {stats['errors']}")
    print(f"   📋 حجم سجل التدقيق: {stats['audit_file_size']} bytes")
    print(f"   🧠 ذاكرة دلالية: {stats['memory']['semantic']} مدخلة")
    print(f"   📝 ذاكرة عرضية: {stats['memory']['episodic']} حدث")
    print(f"   🔄 ذاكرة إجرائية: {stats['memory']['procedural']} إجراء")
    print(f"   ⚡ ذاكرة عاملة: {stats['memory']['working']} مفتاح")
    
    # 🔍 بحث
    print("\n" + "=" * 70)
    print("🔍 بحث في الذاكرة عن 'login':")
    print("=" * 70)
    results = mem.search("login", n=3)
    for r in results.get("semantic", []):
        print(f"   🧠 {r['text'][:100]}...")
    for r in results.get("episodic", [])[:2]:
        print(f"   📝 [{r['event_type']}] {r['summary'][:80]}...")
    
    # 📋 آخر أحداث سجل التدقيق
    print("\n" + "=" * 70)
    print("📋 آخر أحداث سجل التدقيق:")
    print("=" * 70)
    for entry in mem.get_recent_audit(5):
        print(f"   [{entry['timestamp'][:19]}] {entry['office']}/{entry['agent']}: {entry['summary'][:60]}")
    
    print("\n✅ تم! كل الـ 534 وكيلاً يسجلون في الذاكرة الآن.")
    return mem


if __name__ == "__main__":
    demo()
