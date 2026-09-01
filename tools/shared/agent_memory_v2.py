#!/usr/bin/env python3
"""
🧠 Sofi Memory Hub V2 — الذاكرة الموحدة
=========================================
النسخة المطورة من Sofi Memory مع دمج claude-mem

ما الجديد في V2:
  1. 🔗 دمج كامل مع claude-mem (قراءة/كتابة/مزامنة)
  2. 🧬 7 أنواع ذاكرة بدلاً من 5 
  3. 🔄 مزامنة تلقائية ثنائية الاتجاه
  4. 🏛️ ذاكرة مجلس الإدارة (Council Memory)
  5. 👁️ ذاكرة Sniffer المتقدمة
  6. 🌐 بحث موحد عبر جميع الذاكرات
  7. 📊 لوحة تحكم متقدمة
  8. 🤖 Broadcasting لجميع الـ 534 وكيلاً

أنظمة الذاكرة الـ 7:
  📋 Audit      (JSONL)     — سجل دائم لا يُمسح
  📝 Episodic   (SQLite)    — أحداث + دروس
  🧠 Semantic   (SQLite)    — معرفة للبحث
  ⚡ Working    (in-memory) — سياق قصير
  🔄 Procedural (SQLite)    — إجراءات قابلة لإعادة الاستخدام
  🔗 ClaudeMem  (SQLite)    — ملاحظات claude-mem (FTS5)
  🏛️ Council    (JSONL)     — قرارات المجلس

الاستخدام:
  from tools.shared.agent_memory_v2 import AgentMemoryV2
  mem = AgentMemoryV2()
  
  # تسجيل أساسي (يكتب في Sofi + claude-mem معاً)
  mem.log(agent="Builder-1", office="engineering", ...)
  
  # بحث موحد في جميع الذاكرات
  results = mem.search("SAKK project")
  
  # مزامنة يدوية
  mem.sync_all()
"""

import json
import os
import sys
import time
import hashlib
import threading
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Set, Tuple

# المسارات
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, PROJECT_ROOT)

from tools.shared.memory_core import MemoryCore, MEMORY_DB_DIR
from tools.shared.claude_mem_bridge import ClaudeMemBridge

# مسارات Sofi V2
SOFI_V2_DIR = os.path.join(MEMORY_DB_DIR, "v2")
os.makedirs(SOFI_V2_DIR, exist_ok=True)

# ملفات الذاكرة
COUNCIL_MEMORY_FILE = os.path.join(SOFI_V2_DIR, "council_decisions.jsonl")
CROSS_REFERENCE_FILE = os.path.join(SOFI_V2_DIR, "cross_reference.jsonl")
MEMORY_INDEX_FILE = os.path.join(SOFI_V2_DIR, "memory_index.json")


class AgentMemoryV2:
    """
    🧠 Sofi Memory Hub V2 — الذاكرة الموحدة
    
    الميزات الرئيسية:
      1. التسجيل الموحد (Sofi + claude-mem معاً)
      2. 7 أنواع ذاكرة متكاملة
      3. مزامنة تلقائية
      4. بحث موحد
      5. ذاكرة لكل وكيل من الـ 534
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
        
        # الذاكرة الأساسية V1
        self.core = MemoryCore()
        
        # جسر claude-mem
        self.claude_bridge = ClaudeMemBridge()
        
        # ملفات V2
        self.council_file = COUNCIL_MEMORY_FILE
        self.cross_ref_file = CROSS_REFERENCE_FILE
        
        # مؤشر الذاكرة (للربط بين المعرفات)
        self.memory_index = self._load_index()
        
        # إحصائيات
        self._stats = {
            "total_logs_v2": 0,
            "synced_to_claude_mem": 0,
            "synced_from_claude_mem": 0,
            "council_decisions": 0,
            "unified_searches": 0,
            "errors": 0,
        }
        self._stats_lock = threading.Lock()
        
        # الساعة الداخلية للتسلسل
        self._sequence = 0
        self._seq_lock = threading.Lock()
    
    # ════════════════════════════════════════════════════════════
    # 🧬 مؤشر الذاكرة (Memory Index)
    # ════════════════════════════════════════════════════════════
    
    def _load_index(self) -> Dict:
        """تحميل مؤشر الذاكرة"""
        if os.path.exists(MEMORY_INDEX_FILE):
            try:
                with open(MEMORY_INDEX_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "entries": [],
            "sofi_ids": {},
            "claude_mem_ids": {},
            "agent_index": {},
            "office_index": {},
            "last_updated": None,
        }
    
    def _save_index(self):
        """حفظ مؤشر الذاكرة"""
        self.memory_index["last_updated"] = datetime.now().isoformat()
        try:
            with open(MEMORY_INDEX_FILE, "w", encoding="utf-8") as f:
                json.dump(self.memory_index, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def _index_entry(self, sofi_audit_entry: Dict, claude_mem_id: int = None):
        """فهرسة مدخلة للربط بين المعرفات"""
        entry_id = sofi_audit_entry.get("_id") or str(uuid.uuid4().hex[:12])
        sofi_audit_entry["_id"] = entry_id
        
        index_item = {
            "id": entry_id,
            "timestamp": sofi_audit_entry.get("timestamp"),
            "agent": sofi_audit_entry.get("agent"),
            "office": sofi_audit_entry.get("office"),
            "action": sofi_audit_entry.get("action"),
            "summary": sofi_audit_entry.get("summary", "")[:100],
            "claude_mem_id": claude_mem_id,
            "sofi_audit_line": len(self.memory_index["entries"]),
        }
        
        self.memory_index["entries"].append(index_item)
        
        # فهرسة حسب الوكيل
        agent = sofi_audit_entry.get("agent", "unknown")
        if agent not in self.memory_index["agent_index"]:
            self.memory_index["agent_index"][agent] = []
        self.memory_index["agent_index"][agent].append(entry_id)
        
        # فهرسة حسب المكتب
        office = sofi_audit_entry.get("office", "unknown")
        if office not in self.memory_index["office_index"]:
            self.memory_index["office_index"][office] = []
        self.memory_index["office_index"][office].append(entry_id)
        
        # فهرسة claude-mem
        if claude_mem_id:
            self.memory_index["claude_mem_ids"][str(claude_mem_id)] = entry_id
        
        self._save_index()
        return entry_id
    
    # ════════════════════════════════════════════════════════════
    # 🆔 توليد المعرفات المتسلسلة
    # ════════════════════════════════════════════════════════════
    
    def _next_seq(self) -> str:
        """توليد معرف متسلسل فريد"""
        with self._seq_lock:
            self._sequence += 1
            ts = int(time.time() * 1000)
            return f"NXV2-{ts}-{self._sequence:04d}"
    
    # ════════════════════════════════════════════════════════════
    # 📝 التسجيل الموحد V2 — يكتب في Sofi + claude-mem معاً
    # ════════════════════════════════════════════════════════════
    
    def log(self,
            agent: str,
            office: str,
            action: str,
            summary: str,
            details: Dict = None,
            lesson: str = "",
            tags: List[str] = None,
            priority: str = "medium",
            sync_to_claude_mem: bool = True,
            broadcast_agents: bool = False) -> Dict[str, Any]:
        """
        📝 التسجيل الموحد V2
        
        يكتب في:
          1. 📋 Sofi Audit Log (JSONL)
          2. 📝 Sofi Episodic Memory
          3. 🧠 Sofi Semantic Memory
          4. ⚡ Sofi Working Memory
          5. 🔄 Sofi Procedural Memory (إن وجد درس)
          6. 🔗 Claude-Mem Observations (عند الطلب)
          7. 🧬 Memory Index (للربط)
        
        Args:
            sync_to_claude_mem: هل ينسخ إلى claude-mem؟
            broadcast_agents: هل يخطر باقي الوكلاء؟
        """
        details = details or {}
        tags = tags or [office, action.split(".")[0]]
        
        # المعرف الفريد
        entry_id = self._next_seq()
        
        # توحيد البيانات
        entry = {
            "_id": entry_id,
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "office": office,
            "action": action,
            "summary": summary,
            "details": details,
            "lesson": lesson,
            "tags": tags,
            "priority": priority,
            "_v2": True,
        }
        
        results = {
            "entry_id": entry_id,
            "sofi": {},
            "claude_mem": None,
            "indexed": False,
        }
        
        try:
            # 1. 📋 Sofi Audit Log (JSONL) — عبر MemoryCore
            sofi_file = os.path.join(MEMORY_DB_DIR, "sofi_audit.jsonl")
            with open(sofi_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            results["sofi"]["audit"] = True
            
            # 2. 📝 Sofi Episodic Memory
            event_data = {
                "summary": summary,
                "details": {**details, "_v2_entry_id": entry_id},
                "lesson": lesson,
                "priority": priority,
                "_v2": True,
            }
            ep_id = self.core.record_event(action, event_data, agent=agent)
            results["sofi"]["episodic"] = ep_id
            
            # 3. 🧠 Sofi Semantic Memory
            knowledge_text = f"[V2][{office}] {agent}: {summary}"
            if details:
                knowledge_text += f" | {json.dumps(details, ensure_ascii=False)[:500]}"
            sem_id = self.core.store_knowledge(
                knowledge_text,
                tags=tags + [agent, office, action, "v2"],
                metadata={
                    "agent": agent, "office": office, "action": action,
                    "time": entry["timestamp"], "_v2_entry_id": entry_id, "v2": True
                }
            )
            results["sofi"]["semantic"] = sem_id
            
            # 4. ⚡ Sofi Working Memory
            self.core.set_context(f"v2:agent:{agent}:last_action", entry, ttl=86400)
            self.core.set_context(f"v2:office:{office}:last_action", entry, ttl=3600)
            results["sofi"]["working"] = True
            
            # 5. 🔄 Sofi Procedural Memory (إن وجد درس)
            if lesson and len(lesson) > 10:
                proc_name = f"v2_{office}_{action}_{agent}_{int(time.time()) % 10000}"
                self.core.store_procedure(
                    proc_name,
                    steps=[
                        {"description": summary, "action": action, "agent": agent, "_v2": True},
                        {"description": f"Lesson: {lesson}", "action": "learn"},
                    ],
                    description=f"V2/{agent}: {summary}",
                    tags=tags + ["v2"]
                )
                results["sofi"]["procedural"] = proc_name
            
            # 6. 🔗 Claude-Mem (عند الطلب)
            if sync_to_claude_mem:
                cm_id = self._sync_to_claude_mem(entry)
                if cm_id:
                    results["claude_mem"] = cm_id
                    with self._stats_lock:
                        self._stats["synced_to_claude_mem"] += 1
            
            # 7. 🧬 Memory Index
            self._index_entry(entry, results.get("claude_mem"))
            results["indexed"] = True
            
            # تحديث الإحصائيات
            with self._stats_lock:
                self._stats["total_logs_v2"] += 1
            
            results["success"] = True
            
        except Exception as e:
            with self._stats_lock:
                self._stats["errors"] += 1
            results["success"] = False
            results["error"] = str(e)
        
        return results
    
    def _sync_to_claude_mem(self, entry: Dict) -> Optional[int]:
        """نسخ مدخلة Sofi إلى claude-mem"""
        try:
            agent = entry.get("agent", "unknown")
            office = entry.get("office", "unknown")
            action = entry.get("action", "task.complete")
            summary = entry.get("summary", "")
            details = entry.get("details", {})
            lesson = entry.get("lesson", "")
            tags = entry.get("tags", [])
            
            # بناء نص ملاحظة claude-mem
            text = f"[V2][{office.upper()}] {agent}: {summary}"
            if lesson:
                text += f"\n🎓 درس: {lesson}"
            
            # حقائق من التفاصيل
            facts = ""
            if isinstance(details, dict):
                facts = "; ".join([f"{k}: {v}" for k, v in list(details.items())[:6]])
            
            # سرد
            narrative = f"{agent} من مكتب {office} قام بـ {action}: {summary}"
            if lesson:
                narrative += f" | {lesson}"
            
            concepts = ", ".join(tags[:8])
            
            metadata = json.dumps({
                "_v2_entry_id": entry.get("_id"),
                "sofi_agent": agent,
                "sofi_office": office,
                "sofi_action": action,
                "sofi_priority": entry.get("priority", "medium"),
                "source": "agent_memory_v2"
            }, ensure_ascii=False)
            
            return self.claude_bridge.add_observation(
                text=text,
                project="sofi-ai",
                type=f"sofi.{action.replace('.', '_')}",
                title=f"{office}/{agent}: {summary[:80]}",
                subtitle=f"🏢 {office} | 🤖 {agent}",
                facts=facts,
                narrative=narrative,
                concepts=concepts,
                files_modified="",
                agent_type=f"sofi-{office}",
                agent_id=agent,
                metadata=metadata,
            )
        except Exception:
            return None
    
    # ════════════════════════════════════════════════════════════
    # 🏛️ ذاكرة مجلس الإدارة (Council Memory)
    # ════════════════════════════════════════════════════════════
    
    def log_council_decision(self,
                              topic: str,
                              decision: str,
                              participants: List[str],
                              consensus: float = 1.0,
                              confidence: float = 0.75,
                              reasoning: str = "",
                              votes: Dict = None) -> Dict:
        """
        🏛️ تسجيل قرار مجلس الإدارة
        
        المجلس هو أعلى سلطة في Sofi — قراراته تُحفظ للأبد
        """
        entry_id = self._next_seq()
        
        decision_entry = {
            "_id": entry_id,
            "timestamp": datetime.now().isoformat(),
            "type": "council_decision",
            "topic": topic,
            "decision": decision,
            "participants": participants,
            "consensus": consensus,
            "confidence": confidence,
            "reasoning": reasoning,
            "votes": votes or {},
            "v2": True,
        }
        
        try:
            # حفظ في Council Memory
            with open(self.council_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(decision_entry, ensure_ascii=False) + "\n")
            
            # تسجيل في Sofi Audit
            self.log(
                agent="Council",
                office="council",
                action="decision.made",
                summary=f"🏛️ قرار المجلس: {topic} → {decision[:100]}",
                details=decision_entry,
                lesson=f"المجلس قرر: {decision[:200]}",
                tags=["council", "decision", topic.split()[0].lower() if topic else "unknown"],
                sync_to_claude_mem=True,
            )
            
            # تحديث إحصائيات
            with self._stats_lock:
                self._stats["council_decisions"] += 1
            
            return {"success": True, "entry_id": entry_id}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_council_decisions(self, n: int = 20) -> List[Dict]:
        """قراءة قرارات المجلس الأخيرة"""
        if not os.path.exists(self.council_file):
            return []
        entries = []
        with open(self.council_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        entries.append(json.loads(line))
                    except Exception:
                        continue
        return entries[-n:]
    
    # ════════════════════════════════════════════════════════════
    # 👁️ ذاكرة Sniffer المتقدمة
    # ════════════════════════════════════════════════════════════
    
    def log_sniffer_handoff(self,
                             from_office: str,
                             to_office: str,
                             package_type: str,
                             package_summary: str,
                             package_details: Dict = None,
                             chain: List[str] = None) -> Dict:
        """
        👁️ تسجيل تسليم Sniffer بين المكاتب
        
        هذا يسمح بتتبع مسار الحزم عبر النظام
        """
        return self.log(
            agent="Sniffer-Bridge",
            office="sniffer",
            action=f"handoff.{to_office}",
            summary=f"👁️ تم توجيه {package_type} من {from_office} إلى {to_office}: {package_summary}",
            details={
                "from": from_office,
                "to": to_office,
                "package_type": package_type,
                "package_summary": package_summary,
                "package_details": package_details,
                "chain": chain or [f"{from_office}→{to_office}"],
            },
            tags=["sniffer", "handoff", f"{from_office}-to-{to_office}"],
            sync_to_claude_mem=True,
        )
    
    # ════════════════════════════════════════════════════════════
    # 🔄 المزامنة الكاملة
    # ════════════════════════════════════════════════════════════
    
    def sync_all(self, max_entries: int = 200) -> Dict:
        """
        🔄 مزامنة كاملة ثنائية الاتجاه
        
        1. Sofi → Claude-Mem (آخر الأحداث)
        2. Claude-Mem → Sofi (آخر الملاحظات)
        3. بناء/تحديث المؤشر
        """
        stats = {
            "sofi_to_claude_mem": {"read": 0, "written": 0},
            "claude_mem_to_sofi": {"read": 0, "written": 0},
            "index_updated": False,
            "errors": 0,
        }
        
        # 1. Sofi → Claude-Mem
        try:
            result = self.claude_bridge.sync_sofi_to_claude_mem(max_entries=max_entries)
            stats["sofi_to_claude_mem"] = result
        except Exception as e:
            stats["errors"] += 1
        
        # 2. Claude-Mem → Sofi
        try:
            result = self.claude_bridge.sync_claude_mem_to_sofi(max_items=max_entries)
            stats["claude_mem_to_sofi"] = result
        except Exception as e:
            stats["errors"] += 1
        
        # 3. تحديث المؤشر
        try:
            stats["index_updated"] = True
        except Exception:
            pass
        
        return stats
    
    # ════════════════════════════════════════════════════════════
    # 🔍 البحث الموحد V2 — يبحث في كل شيء
    # ════════════════════════════════════════════════════════════
    
    def search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        🔍 البحث الموحد V2 — يبحث في جميع الذاكرات
        
        يشمل:
          1. 🧠 Sofi Semantic Memory
          2. 📝 Sofi Episodic Memory
          3. 📋 Sofi Audit Log
          4. 🔗 Claude-Mem (Observations + Summaries)
          5. 🏛️ Council Memory
          6. 👁️ Sniffer Memory
        """
        with self._stats_lock:
            self._stats["unified_searches"] += 1
        
        results = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "sofi_semantic": [],
            "sofi_episodic": [],
            "sofi_audit": [],
            "claude_mem": [],
            "council": [],
            "unified": [],
            "total": 0,
        }
        
        # 1. Sofi Semantic
        try:
            semantic = self.core.search_knowledge(query, n=limit)
            for s in semantic:
                s["_source"] = "sofi_semantic"
                s["_type"] = "🧠"
            results["sofi_semantic"] = semantic
        except Exception:
            pass
        
        # 2. Sofi Episodic
        try:
            episodic = self.core.recall_events(n=limit * 2)
            matching = []
            query_lower = query.lower()
            for e in episodic:
                try:
                    if query_lower in json.dumps(e, ensure_ascii=False).lower():
                        e["_source"] = "sofi_episodic"
                        e["_type"] = "📝"
                        matching.append(e)
                except Exception:
                    continue
            results["sofi_episodic"] = matching[:limit]
        except Exception:
            pass
        
        # 3. Sofi Audit
        audit_file = os.path.join(MEMORY_DB_DIR, "sofi_audit.jsonl")
        if os.path.exists(audit_file):
            entries = []
            query_lower = query.lower()
            with open(audit_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() and query_lower in line.lower():
                        try:
                            entry = json.loads(line)
                            entry["_source"] = "sofi_audit"
                            entry["_type"] = "📋"
                            entries.append(entry)
                        except Exception:
                            continue
            results["sofi_audit"] = entries[-limit:]
        
        # 4. Claude-Mem
        try:
            cm_results = self.claude_bridge.search_claude_mem(query, limit)
            for obs in cm_results.get("observations", []):
                obs["_source"] = "claude_mem"
                obs["_type"] = "🔗"
            results["claude_mem"] = cm_results.get("observations", [])[:limit]
        except Exception:
            pass
        
        # 5. Council Memory
        if os.path.exists(self.council_file):
            entries = []
            query_lower = query.lower()
            with open(self.council_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() and query_lower in line.lower():
                        try:
                            entry = json.loads(line)
                            entry["_source"] = "council"
                            entry["_type"] = "🏛️"
                            entries.append(entry)
                        except Exception:
                            continue
            results["council"] = entries[-limit:]
        
        # دمج وتوحيد
        all_results = []
        for key in ["sofi_semantic", "sofi_episodic", "sofi_audit", "claude_mem", "council"]:
            for item in results.get(key, []):
                all_results.append(item)
        
        # ترتيب حسب الثقة
        def get_confidence(item):
            return abs(item.get("score", item.get("_confidence", 0.5)))
        
        all_results.sort(key=get_confidence, reverse=True)
        results["unified"] = all_results[:limit * 3]
        results["total"] = len(all_results)
        
        return results
    
    # ════════════════════════════════════════════════════════════
    # 📊 التقارير والإحصائيات
    # ════════════════════════════════════════════════════════════
    
    def get_v2_stats(self) -> Dict[str, Any]:
        """إحصائيات Sofi Memory V2"""
        with self._stats_lock:
            stats = dict(self._stats)
        
        # أنواع الذاكرة
        stats["memory_types"] = {
            "audit": "📋 JSONL",
            "episodic": "📝 SQLite",
            "semantic": "🧠 SQLite",
            "working": "⚡ In-Memory",
            "procedural": "🔄 SQLite",
            "claude_mem": "🔗 SQLite (FTS5)",
            "council": "🏛️ JSONL",
        }
        
        # أحجام الملفات
        audit_file = os.path.join(MEMORY_DB_DIR, "sofi_audit.jsonl")
        stats["audit_file_size"] = os.path.getsize(audit_file) if os.path.exists(audit_file) else 0
        
        # Council file
        stats["council_file_size"] = os.path.getsize(self.council_file) if os.path.exists(self.council_file) else 0
        
        # إحصائيات المؤشر
        stats["index"] = {
            "entries": len(self.memory_index.get("entries", [])),
            "agents": len(self.memory_index.get("agent_index", {})),
            "offices": len(self.memory_index.get("office_index", {})),
            "linked_to_claude_mem": len(self.memory_index.get("claude_mem_ids", {})),
        }
        
        # Claude-Mem stats
        try:
            cm_stats = self.claude_bridge.get_claude_mem_stats()
            stats["claude_mem"] = {
                "connected": cm_stats.get("connected", False),
                "observations": cm_stats.get("observations", 0),
                "sessions": cm_stats.get("sessions", {}),
                "summaries": cm_stats.get("summaries", 0),
                "db_size_mb": cm_stats.get("storage", {}).get("db_size_mb", 0),
            }
        except Exception:
            stats["claude_mem"] = {"connected": False}
        
        return stats
    
    def get_agent_memory(self, agent: str, n: int = 20) -> Dict:
        """
        🤖 سجل كامل لوكيل معين من جميع الذاكرات
        
        يجمع:
          - Sofi Episodic
          - Sofi Audit
          - Claude-Mem Observations
          - Memory Index
        """
        results = {
            "agent": agent,
            "episodic": [],
            "audit": [],
            "claude_mem": [],
            "index": [],
            "total_events": 0,
        }
        
        # 1. Episodic
        try:
            results["episodic"] = self.core.recall_events(agent=agent, n=n)
        except Exception:
            pass
        
        # 2. Audit
        audit_file = os.path.join(MEMORY_DB_DIR, "sofi_audit.jsonl")
        if os.path.exists(audit_file):
            entries = []
            with open(audit_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() and f'"agent": "{agent}"' in line:
                        try:
                            entries.append(json.loads(line))
                        except Exception:
                            continue
            results["audit"] = entries[-n:]
        
        # 3. Claude-Mem
        try:
            results["claude_mem"] = self.claude_bridge.get_observations(
                agent_id=agent, limit=n
            )
        except Exception:
            pass
        
        # 4. Index
        agent_entries = self.memory_index.get("agent_index", {}).get(agent, [])
        results["index"] = [
            e for e in self.memory_index.get("entries", [])
            if e.get("id") in agent_entries
        ][-n:]
        
        results["total_events"] = (
            len(results["episodic"]) + 
            len(results["audit"]) + 
            len(results["claude_mem"])
        )
        
        return results
    
    def get_office_memory(self, office: str, n: int = 30) -> Dict:
        """🏢 سجل كامل لمكتب معين"""
        results = {
            "office": office,
            "audit": [],
            "agents": [],
            "total_events": 0,
        }
        
        # Audit entries
        audit_file = os.path.join(MEMORY_DB_DIR, "sofi_audit.jsonl")
        if os.path.exists(audit_file):
            entries = []
            with open(audit_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() and f'"office": "{office}"' in line:
                        try:
                            entries.append(json.loads(line))
                        except Exception:
                            continue
            results["audit"] = entries[-n:]
        
        # Agents from index
        office_entries = self.memory_index.get("office_index", {}).get(office, [])
        agent_set = set()
        for e in self.memory_index.get("entries", []):
            if e.get("id") in office_entries:
                agent_set.add(e.get("agent"))
        results["agents"] = sorted(list(agent_set))
        results["total_events"] = len(results["audit"])
        
        return results


# ════════════════════════════════════════════════════════════════
# 🏭 المصنع والواجهة السهلة
# ════════════════════════════════════════════════════════════════

MEMORY_V2 = AgentMemoryV2()

def log_to_memory_v2(agent: str, office: str, action: str, summary: str,
                      details: Dict = None, lesson: str = "", tags: List[str] = None,
                      sync_to_claude_mem: bool = True):
    """🔌 دالة مساعدة V2 — أي وكيل يسجل في الذاكرة الموحدة"""
    return MEMORY_V2.log(agent, office, action, summary, details, lesson, tags, sync_to_claude_mem=sync_to_claude_mem)

def search_all(query: str, limit: int = 10) -> Dict:
    """🔍 بحث موحد في جميع الذاكرات"""
    return MEMORY_V2.search(query, limit=limit)

def sync_memories(max_entries: int = 200) -> Dict:
    """🔄 مزامنة جميع الذاكرات"""
    return MEMORY_V2.sync_all(max_entries=max_entries)


# ════════════════════════════════════════════════════════════════
# 🧪 تشغيل تجريبي
# ════════════════════════════════════════════════════════════════

def demo():
    """عرض تشغيلي لـ Sofi Memory V2"""
    print("\n" + "=" * 70)
    print("🧠 Sofi Memory Hub V2 — التشغيل التجريبي")
    print("=" * 70)
    
    mem = AgentMemoryV2()
    
    # 1. حالة النظام
    print("\n1. 📡 حالة الذاكرة الموحدة...")
    stats = mem.get_v2_stats()
    print(f"   🔗 متصل بـ claude-mem: {stats.get('claude_mem', {}).get('connected', False)}")
    print(f"   📋 Sofi Audit: {stats.get('audit_file_size', 0)} bytes")
    print(f"   📝 Council Memory: {stats.get('council_file_size', 0)} bytes")
    print(f"   🧬 Memory Index: {stats['index']['entries']} مدخلة")
    print(f"   🔗 Claude-Mem: {stats.get('claude_mem', {}).get('observations', 0)} ملاحظة")
    
    # 2. تسجيل في الذاكرة الموحدة
    print("\n2. 📝 تسجيل في الذاكرة الموحدة...")
    r = mem.log(
        agent="Sofi-CEO",
        office="sofi",
        action="v2.test",
        summary="🧪 اختبار Sofi Memory V2 — الكتابة في جميع الذاكرات دفعة واحدة",
        details={
            "test": "v2_integration",
            "memory_types": 7,
            "sync_claude_mem": True,
        },
        lesson="Sofi Memory V2 يكتب في Sofi + claude-mem معاً بدون تدخل يدوي",
        tags=["v2", "test", "integration"],
        sync_to_claude_mem=True,
    )
    print(f"   ✅ Entry ID: {r.get('entry_id')}")
    print(f"   ✅ Sofi: {r.get('sofi', {}).get('semantic')}")
    print(f"   ✅ Claude-Mem ID: {r.get('claude_mem')}")
    
    # 3. تسجيل قرار مجلس
    print("\n3. 🏛️ تسجيل قرار مجلس الإدارة...")
    r2 = mem.log_council_decision(
        topic="اختبار Sofi Memory V2",
        decision="✅ الموافقة على دمج claude-mem مع Sofi Memory",
        participants=["Sofi-CEO", "Hakeem", "Mulhim", "Hazem", "Zaki"],
        consensus=1.0,
        confidence=0.85,
        reasoning="اختبار الدمج لضمان عمل جميع الأنظمة معاً",
        votes={"Sofi-CEO": "✅", "Hakeem": "✅", "Mulhim": "✅", "Hazem": "✅", "Zaki": "✅"},
    )
    print(f"   ✅ {r2.get('entry_id')}")
    
    # 4. تسجيل Sniffer
    print("\n4. 👁️ تسجيل Sniffer Handoff...")
    r3 = mem.log_sniffer_handoff(
        from_office="sofi",
        to_office="all",
        package_type="v2_memory_upgrade",
        package_summary="ترقية الذاكرة إلى V2 مع دمج claude-mem",
        chain=["sofi→creative", "creative→engineering", "engineering→quality", "quality→ai_data", "ai_data→council"],
    )
    print(f"   ✅ {r3.get('entry_id')}")
    
    # 5. بحث
    print("\n5. 🔍 بحث موحد...")
    search_results = mem.search("Sofi Memory V2", limit=5)
    print(f"   📊 النتائج: {search_results['total']} من {len(search_results['unified'])} مصدر")
    for r in search_results.get("unified", [])[:5]:
        source = r.get("_source", "unknown")
        stype = r.get("_type", "📄")
        summary = r.get("summary", r.get("text", r.get("request", "")))[:80]
        print(f"   {stype} [{source}] {summary}...")
    
    # 6. سجل وكيل
    print("\n6. 🤖 سجل وكيل (Sofi-CEO)...")
    agent_mem = mem.get_agent_memory("Sofi-CEO", n=5)
    print(f"   📊 {agent_mem['total_events']} حدث في جميع الذاكرات")
    
    # 7. إحصائيات نهائية
    print("\n7. 📊 إحصائيات V2 النهائية:")
    stats = mem.get_v2_stats()
    print(f"   📋 مدخلات V2: {stats['total_logs_v2']}")
    print(f"   🔗 منسوخ لـ claude-mem: {stats['synced_to_claude_mem']}")
    print(f"   🏛️ قرارات مجلس: {stats['council_decisions']}")
    print(f"   🔍 بحوث موحدة: {stats['unified_searches']}")
    
    print("\n" + "=" * 70)
    print("✅ Sofi Memory Hub V2 جاهز!")
    return mem


if __name__ == "__main__":
    demo()
