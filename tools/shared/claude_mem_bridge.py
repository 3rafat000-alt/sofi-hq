#!/usr/bin/env python3
"""
🔗 Claude-Mem Bridge — v1.0.0
==============================
الربط المباشر بين Sofi Memory و claude-mem v13.4.0

هذا الجسر يسمح لـ:
  1. قراءة وكتابة قاعدة claude-mem SQLite مباشرة
  2. تحويل صيغ Sofi Memory ↔ صيغ claude-mem
  3. مزامنة ثنائية الاتجاه بين النظامين
  4. استعلام موحد عبر الذاكرتين معاً

الذاكرتان:
  🧠 Sofi Memory:  .claude/memory/  (5 أنظمة: Audit + Episodic + Semantic + Working + Procedural)
  🔗 Claude-Mem:     ~/.claude-mem/ (7 جداول: observations + sessions + prompts + summaries + pending)

الاستخدام:
  from tools.shared.claude_mem_bridge import ClaudeMemBridge
  bridge = ClaudeMemBridge()
  
  # كتابة ملاحظة في claude-mem
  bridge.add_observation(project="sofi-ai", text="...", type="analysis")
  
  # قراءة ملاحظات من claude-mem
  obs = bridge.get_observations(project="sofi-ai", limit=5)
  
  # مزامنة Sofi → claude-mem
  bridge.sync_sofi_to_claude_mem()
  
  # مزامنة claude-mem → Sofi
  bridge.sync_claude_mem_to_sofi()
  
  # بحث موحد
  results = bridge.unified_search("SAKK project")
"""

import json
import os
import sqlite3
import sys
import time
import hashlib
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# المسارات
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# قاعدة claude-mem
CLAUDE_MEM_DB = os.path.expanduser("~/.claude-mem/claude-mem.db")
CLAUDE_MEM_DIR = os.path.expanduser("~/.claude-mem")

# قاعدة Sofi Memory
SOFI_MEMORY_DIR = os.path.join(PROJECT_ROOT, ".claude/memory")
SOFI_AUDIT_FILE = os.path.join(SOFI_MEMORY_DIR, "sofi_audit.jsonl")
SOFI_SNIFFER_FILE = os.path.join(SOFI_MEMORY_DIR, "sniffer_audit.jsonl")


class ClaudeMemBridge:
    """
    🔗 Claude-Mem Bridge — الواجهة الموحدة بين Sofi و claude-mem
    
    الميزات:
      - قراءة/كتابة مباشرة لقاعدة claude-mem SQLite
      - تحويل تلقائي بين صيغ الذاكرتين
      - مزامنة ثنائية الاتجاه
      - بحث موحد
      - تجنب التكرار عبر التجزئة (hashing)
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
        
        # إحصائيات
        self._stats = {
            "sofi_to_claude": 0,
            "claude_to_sofi": 0,
            "observations_added": 0,
            "errors": 0,
            "last_sync": None,
        }
        self._stats_lock = threading.Lock()
    
    # ════════════════════════════════════════════════════════════
    # 📡 الاتصال بقاعدة claude-mem
    # ════════════════════════════════════════════════════════════
    
    def _connect_claude_mem(self) -> Optional[sqlite3.Connection]:
        """الاتصال بقاعدة claude-mem SQLite"""
        if not os.path.exists(CLAUDE_MEM_DB):
            print(f"⚠️ قاعدة claude-mem غير موجودة: {CLAUDE_MEM_DB}")
            return None
        try:
            conn = sqlite3.connect(CLAUDE_MEM_DB)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            print(f"❌ فشل الاتصال بـ claude-mem: {e}")
            return None
    
    def _get_or_create_session(self, conn: sqlite3.Connection, 
                                project: str = "sofi-ai",
                                platform: str = "sofi") -> Tuple[int, str]:
        """
        إنشاء أو استرجاع معرف جلسة claude-mem لمشروع Sofi
        
        Returns:
            (session_db_id, memory_session_id)
        """
        cursor = conn.cursor()
        
        # هل يوجد جلسة نشطة لمشروع sofi؟
        cursor.execute("""
            SELECT id, memory_session_id FROM sdk_sessions 
            WHERE project = ? AND platform_source = ? AND status = 'active'
            ORDER BY id DESC LIMIT 1
        """, (project, platform))
        
        row = cursor.fetchone()
        if row:
            return (row["id"], row["memory_session_id"])
        
        # إنشاء جلسة جديدة
        import uuid
        memory_session_id = f"sofi-{uuid.uuid4().hex[:12]}"
        now = datetime.now()
        epoch = int(time.time())
        
        cursor.execute("""
            INSERT INTO sdk_sessions 
                (content_session_id, memory_session_id, project, platform_source, 
                 started_at, started_at_epoch, status, custom_title)
            VALUES (?, ?, ?, ?, ?, ?, 'active', ?)
        """, (
            f"sofi-{uuid.uuid4().hex[:16]}",
            memory_session_id,
            project,
            platform,
            now.isoformat(),
            epoch,
            f"SOFI AI — {project}"
        ))
        conn.commit()
        
        return (cursor.lastrowid, memory_session_id)
    
    # ════════════════════════════════════════════════════════════
    # 📝 كتابة في claude-mem
    # ════════════════════════════════════════════════════════════
    
    def _ensure_json_array(self, value: str) -> str:
        """
        🛡️ تأكيد أن القيمة JSON array صالحة للمشاهد
        
        المشاهد (viewer-bundle.js) يتوقع JSON.parse() على هذه الحقول:
        - facts, concepts, files_read, files_modified
        
        إذا كانت القيمة نصاً عادياً، يحولها إلى JSON array ذات عنصر واحد.
        إذا كانت JSON صالحة، يتركها كما هي.
        """
        if not value or value.strip() == '':
            return '[]'
        try:
            # هل هي JSON صالحة فعلاً؟
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return value  # سليمة
            # JSON صالح لكن ليس array → غلفه
            return json.dumps([value], ensure_ascii=False)
        except (json.JSONDecodeError, ValueError):
            # ليست JSON → حول إلى array
            return json.dumps([value], ensure_ascii=False)

    def add_observation(self,
                        text: str,
                        project: str = "sofi-ai",
                        type: str = "analysis",
                        title: str = "",
                        subtitle: str = "",
                        facts: str = "",
                        narrative: str = "",
                        concepts: str = "",
                        files_read: str = "",
                        files_modified: str = "",
                        agent_type: str = "sofi",
                        agent_id: str = "sofi-ceo",
                        metadata: str = "",
                        prompt_number: int = 0) -> Optional[int]:
        """
        📝 إضافة ملاحظة جديدة في claude-mem
        
        هذه هي الوظيفة الأساسية — كل Sofi Memory سجل سيتم نسخه
        إلى claude-mem كـ observation
        
        Returns:
            ID الملاحظة في claude-mem أو None عند الفشل
        """
        conn = self._connect_claude_mem()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            # الحصول على الجلسة
            session_db_id, memory_session_id = self._get_or_create_session(conn, project)
            
            now = datetime.now()
            epoch = int(time.time())
            
            # إنشاء تجزئة للمحتوى لمنع التكرار
            content_hash = hashlib.sha256(
                f"{project}:{text[:200]}:{type}".encode()
            ).hexdigest()[:32]
            
            # هل هذه الملاحظة موجودة بالفعل؟
            cursor.execute("""
                SELECT id FROM observations 
                WHERE memory_session_id = ? AND content_hash = ?
            """, (memory_session_id, content_hash))
            
            if cursor.fetchone():
                # موجودة — لا نكرر
                return None
            
            # 🛡️ تأمين الحقول للمشاهد — كلها JSON arrays
            safe_facts = self._ensure_json_array(facts)
            safe_concepts = self._ensure_json_array(concepts)
            safe_files_read = self._ensure_json_array(files_read)
            safe_files_modified = self._ensure_json_array(files_modified)
            
            # إضافة الملاحظة
            cursor.execute("""
                INSERT INTO observations 
                    (memory_session_id, project, text, type, title, subtitle, 
                     facts, narrative, concepts, files_read, files_modified,
                     prompt_number, created_at, created_at_epoch, 
                     content_hash, agent_type, agent_id, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory_session_id, project, text, type, title, subtitle,
                safe_facts, narrative, safe_concepts, safe_files_read, safe_files_modified,
                prompt_number, now.isoformat(), epoch,
                content_hash, agent_type, agent_id, metadata
            ))
            
            conn.commit()
            obs_id = cursor.lastrowid
            
            with self._stats_lock:
                self._stats["observations_added"] += 1
            
            # إخطار Sniffer
            self._notify_sniffer("claude_mem.observation.added", {
                "observation_id": obs_id,
                "project": project,
                "type": type,
                "title": title or text[:50],
                "agent": agent_id,
            })
            
            return obs_id
            
        except Exception as e:
            with self._stats_lock:
                self._stats["errors"] += 1
            print(f"❌ فشل إضافة ملاحظة في claude-mem: {e}")
            return None
        finally:
            conn.close()
    
    def add_summary(self,
                    project: str,
                    request: str,
                    investigated: str = "",
                    learned: str = "",
                    completed: str = "",
                    next_steps: str = "",
                    notes: str = "",
                    files_read: str = "",
                    files_edited: str = "",
                    agent_type: str = "sofi",
                    agent_id: str = "sofi-ceo") -> Optional[int]:
        """
        📝 إضافة ملخص جلسة في claude-mem
        
        هذا يسمح لـ claude-mem بعرض ملخصات Sofi
        في واجهة web viewer على port 37700
        """
        conn = self._connect_claude_mem()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            session_db_id, memory_session_id = self._get_or_create_session(conn, project)
            
            now = datetime.now()
            epoch = int(time.time())
            
            cursor.execute("""
                INSERT INTO session_summaries 
                    (memory_session_id, project, request, investigated, learned,
                     completed, next_steps, files_read, files_edited, notes,
                     prompt_number, created_at, created_at_epoch, merged_into_project)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory_session_id, project, request, investigated, learned,
                completed, next_steps, files_read, files_edited, notes,
                0, now.isoformat(), epoch, project
            ))
            
            conn.commit()
            summary_id = cursor.lastrowid
            
            self._log(f"📝 ملخص claude-mem: {request[:60]}... (ID: {summary_id})")
            return summary_id
            
        except Exception as e:
            with self._stats_lock:
                self._stats["errors"] += 1
            print(f"❌ فشل إضافة ملخص: {e}")
            return None
        finally:
            conn.close()
    
    def update_session_status(self, project: str = "sofi-ai", 
                              status: str = "completed",
                              title: str = None):
        """تحديث حالة جلسة claude-mem"""
        conn = self._connect_claude_mem()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            if title:
                cursor.execute("""
                    UPDATE sdk_sessions SET status = ?, completed_at = ?,
                    completed_at_epoch = ?, custom_title = ?
                    WHERE project = ? AND platform_source = 'sofi' 
                    AND status = 'active'
                """, (status, datetime.now().isoformat(), int(time.time()), 
                      title, project))
            else:
                cursor.execute("""
                    UPDATE sdk_sessions SET status = ?, completed_at = ?,
                    completed_at_epoch = ?
                    WHERE project = ? AND platform_source = 'sofi' 
                    AND status = 'active'
                """, (status, datetime.now().isoformat(), int(time.time()), project))
            conn.commit()
        finally:
            conn.close()
    
    # ════════════════════════════════════════════════════════════
    # 📖 قراءة من claude-mem
    # ════════════════════════════════════════════════════════════
    
    def get_observations(self, project: str = None, 
                          type: str = None,
                          limit: int = 20,
                          agent_id: str = None) -> List[Dict]:
        """📖 قراءة ملاحظات من claude-mem"""
        conn = self._connect_claude_mem()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            where_clauses = ["1=1"]
            params = []
            
            if project:
                where_clauses.append("project = ?")
                params.append(project)
            if type:
                where_clauses.append("type = ?")
                params.append(type)
            if agent_id:
                where_clauses.append("agent_id = ?")
                params.append(agent_id)
            
            cursor.execute(f"""
                SELECT id, project, text, type, title, subtitle, facts,
                       narrative, concepts, files_read, files_modified,
                       created_at, agent_type, agent_id, metadata
                FROM observations 
                WHERE {' AND '.join(where_clauses)}
                ORDER BY created_at_epoch DESC
                LIMIT ?
            """, params + [limit])
            
            return [dict(row) for row in cursor.fetchall()]
            
        finally:
            conn.close()
    
    def get_sessions(self, project: str = None, 
                      limit: int = 10) -> List[Dict]:
        """📖 قراءة جلسات claude-mem"""
        conn = self._connect_claude_mem()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            if project:
                cursor.execute("""
                    SELECT id, project, platform_source, status, custom_title,
                           started_at, completed_at, user_prompt
                    FROM sdk_sessions
                    WHERE project = ?
                    ORDER BY id DESC LIMIT ?
                """, (project, limit))
            else:
                cursor.execute("""
                    SELECT id, project, platform_source, status, custom_title,
                           started_at, completed_at, user_prompt
                    FROM sdk_sessions
                    ORDER BY id DESC LIMIT ?
                """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
            
        finally:
            conn.close()
    
    def get_summaries(self, project: str = None, limit: int = 10) -> List[Dict]:
        """📖 قراءة ملخصات من claude-mem"""
        conn = self._connect_claude_mem()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            if project:
                cursor.execute("""
                    SELECT id, project, request, investigated, learned,
                           completed, next_steps, notes, created_at
                    FROM session_summaries
                    WHERE project = ?
                    ORDER BY created_at_epoch DESC LIMIT ?
                """, (project, limit))
            else:
                cursor.execute("""
                    SELECT id, project, request, investigated, learned,
                           completed, next_steps, notes, created_at
                    FROM session_summaries
                    ORDER BY created_at_epoch DESC LIMIT ?
                """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
            
        finally:
            conn.close()
    
    def search_claude_mem(self, query: str, limit: int = 10) -> Dict[str, List]:
        """
        🔍 بحث نصي كامل في claude-mem
        
        يستخدم FTS5 (Full Text Search) للبحث في:
        - observations: title, subtitle, narrative, text, facts, concepts
        - session_summaries: request, investigated, learned, completed, next_steps, notes
        """
        conn = self._connect_claude_mem()
        if not conn:
            return {"observations": [], "summaries": []}
        
        results = {"observations": [], "summaries": []}
        
        try:
            cursor = conn.cursor()
            
            # بحث في observations (FTS5)
            try:
                cursor.execute("""
                    SELECT o.id, o.project, o.text, o.type, o.title, o.subtitle,
                           o.created_at, o.agent_id, o.agent_type
                    FROM observations_fts f
                    JOIN observations o ON f.rowid = o.id
                    WHERE observations_fts MATCH ?
                    ORDER BY rank
                    LIMIT ?
                """, (query, limit))
                results["observations"] = [dict(row) for row in cursor.fetchall()]
            except Exception:
                pass
            
            # بحث في session_summaries (FTS5)
            try:
                cursor.execute("""
                    SELECT s.id, s.project, s.request, s.investigated, s.learned,
                           s.completed, s.next_steps, s.created_at
                    FROM session_summaries_fts f
                    JOIN session_summaries s ON f.rowid = s.id
                    WHERE session_summaries_fts MATCH ?
                    ORDER BY rank
                    LIMIT ?
                """, (query, limit))
                results["summaries"] = [dict(row) for row in cursor.fetchall()]
            except Exception:
                pass
            
        finally:
            conn.close()
        
        return results
    
    # ════════════════════════════════════════════════════════════
    # 🔄 المزامنة ثنائية الاتجاه
    # ════════════════════════════════════════════════════════════
    
    def sync_sofi_to_claude_mem(self, 
                                  project: str = "sofi-ai",
                                  max_entries: int = 100) -> Dict[str, int]:
        """
        🔄 مزامنة Sofi Memory → claude-mem
        
        يقرأ آخر الأحداث من سجل تدقيق Sofi Activity Log
        ويحولها إلى ملاحظات (observations) في claude-mem
        
        Returns:
            إحصائيات المزامنة
        """
        stats = {"read": 0, "converted": 0, "skipped": 0, "errors": 0}
        
        if not os.path.exists(SOFI_AUDIT_FILE):
            self._log(f"⚠️ ملف تدقيق Sofi غير موجود: {SOFI_AUDIT_FILE}")
            return stats
        
        try:
            # قراءة أحدث المدخلات
            entries = []
            with open(SOFI_AUDIT_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
            
            # آخر 100 مدخلة
            entries = entries[-max_entries:]
            stats["read"] = len(entries)
            
            conn = self._connect_claude_mem()
            if not conn:
                stats["errors"] = len(entries)
                return stats
            
            try:
                cursor = conn.cursor()
                session_db_id, memory_session_id = self._get_or_create_session(conn, project)
                
                for entry in entries:
                    try:
                        # تحويل Sofi entry → claude-mem observation
                        result = self._convert_sofi_to_observation(entry, memory_session_id)
                        if result:
                            obs_id, content_hash = result
                            
                            # هل موجودة؟
                            cursor.execute("""
                                SELECT id FROM observations 
                                WHERE memory_session_id = ? AND content_hash = ?
                            """, (memory_session_id, content_hash))
                            
                            if not cursor.fetchone():
                                cursor.execute("""
                                    INSERT INTO observations
                                        (memory_session_id, project, text, type, title,
                                         subtitle, facts, narrative, concepts,
                                         files_read, files_modified, prompt_number,
                                         created_at, created_at_epoch, content_hash,
                                         agent_type, agent_id, metadata)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, obs_id)
                                stats["converted"] += 1
                            else:
                                stats["skipped"] += 1
                    except Exception:
                        stats["errors"] += 1
                
                conn.commit()
                
                # إضافة ملخص جلسة
                self._add_sync_summary(conn, project, memory_session_id, stats)
                conn.commit()
                
            finally:
                conn.close()
            
            with self._stats_lock:
                self._stats["sofi_to_claude"] += stats["converted"]
                self._stats["last_sync"] = datetime.now().isoformat()
            
            self._log(f"🔄 مزامنة Sofi→claude-mem: {stats['converted']} محول، {stats['skipped']} مكرر")
            
        except Exception as e:
            stats["errors"] += 1
            self._log(f"❌ فشل المزامنة Sofi→claude-mem: {e}")
        
        return stats
    
    def _convert_sofi_to_observation(self, entry: Dict, 
                                       memory_session_id: str) -> Optional[Tuple]:
        """تحويل Sofi Memory entry إلى row observation"""
        try:
            agent = entry.get("agent", "unknown")
            office = entry.get("office", "unknown")
            action = entry.get("action", "task.complete")
            summary = entry.get("summary", "")
            details = entry.get("details", {})
            lesson = entry.get("lesson", "")
            tags = entry.get("tags", [])
            timestamp = entry.get("timestamp", datetime.now().isoformat())
            
            # بناء الحقول
            now = datetime.now()
            epoch = int(time.time())
            
            # النص الأساسي — ملخص Sofi
            text = f"[{office.upper()}] {agent}: {summary}"
            if lesson:
                text += f"\n🎓 درس: {lesson}"
            
            # العنوان
            title = f"{office}/{agent}: {summary[:80]}"
            
            # المفاهيم — من التاجات (JSON array للمشاهد)
            concepts = json.dumps([str(t)[:40] for t in tags[:10]], ensure_ascii=False)
            
            # حقائق — من التفاصيل (JSON array للمشاهد)
            facts_items = []
            if details:
                if isinstance(details, dict):
                    for k, v in list(details.items())[:8]:
                        v_str = str(v)[:100].replace("'", "").replace("{", "").replace("}", "")
                        facts_items.append(f"{k}: {v_str}")
                else:
                    facts_items.append(str(details)[:500])
            facts = json.dumps(facts_items, ensure_ascii=False)
            
            # سرد — القصة الكاملة
            narrative = f"{agent} من مكتب {office} قام بـ {action}: {summary}"
            if lesson:
                narrative += f" | الدرس المستفاد: {lesson}"
            
            # الملفات (JSON array للمشاهد)
            files_modified_arr = []
            if isinstance(details, dict):
                files = details.get("files", [])
                if isinstance(files, list):
                    files_modified_arr = [str(f) for f in files]
            files_modified = json.dumps(files_modified_arr, ensure_ascii=False)
            
            # تجزئة
            content_hash = hashlib.sha256(
                f"{memory_session_id}:{text[:300]}".encode()
            ).hexdigest()[:32]
            
            metadata_json = json.dumps({
                "sofi_agent": agent,
                "sofi_office": office,
                "sofi_action": action,
                "sofi_priority": entry.get("priority", "medium"),
                "source": "agent_memory_v2"
            }, ensure_ascii=False)
            
            # صيغة observation كاملة
            obs_data = (
                memory_session_id,                     # memory_session_id
                "sofi-ai",                            # project
                text,                                  # text
                f"sofi.{action.replace('.', '_')}",   # type
                title,                                 # title
                f"🏢 {office} | 🤖 {agent}",           # subtitle
                facts,                                 # facts
                narrative,                             # narrative
                concepts,                             # concepts
                "",                                   # files_read
                files_modified,                       # files_modified
                0,                                    # prompt_number
                timestamp,                            # created_at
                epoch,                                # created_at_epoch
                content_hash,                         # content_hash
                f"sofi-{office}",                    # agent_type
                agent,                                # agent_id
                metadata_json                         # metadata
            )
            
            return (obs_data, content_hash)
            
        except Exception as e:
            print(f"⚠️ فشل تحويل Sofi entry: {e}")
            return None
    
    def _add_sync_summary(self, conn: sqlite3.Connection, 
                           project: str, 
                           memory_session_id: str,
                           stats: Dict):
        """إضافة ملخص جلسة المزامنة"""
        cursor = conn.cursor()
        now = datetime.now()
        epoch = int(time.time())
        
        cursor.execute("""
            INSERT INTO session_summaries
                (memory_session_id, project, request, investigated, learned,
                 completed, next_steps, notes, prompt_number,
                 created_at, created_at_epoch, merged_into_project)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            memory_session_id, project,
            "🔄 مزامنة Sofi Memory → claude-mem",
            f"تم استعراض {stats['read']} حدثاً من Sofi",
            f"{stats['converted']} حدثاً جديداً في claude-mem",
            f"{stats['read']} قراءة، {stats['converted']} تحويل، {stats['skipped']} مكرر",
            "المزامنة التلقائية بين Sofi و claude-mem تعمل",
            f"إحصائيات: {json.dumps(stats)}",
            0, now.isoformat(), epoch, project
        ))
    
    def sync_claude_mem_to_sofi(self, 
                                  project: str = "sofi-ai",
                                  max_items: int = 100) -> Dict[str, int]:
        """
        🔄 مزامنة claude-mem → Sofi Memory
        
        يقرأ ملاحظات claude-mem ويسجلها في:
        - Sofi Audit Log (JSONL)
        - Episodic Memory (عند التوفر)
        - Semantic Memory (عند التوفر)
        
        Returns:
            إحصائيات المزامنة
        """
        from tools.shared.agent_memory import log_to_memory
        
        stats = {"read": 0, "logged": 0, "skipped": 0, "errors": 0}
        
        try:
            # قراءة ملاحظات claude-mem
            observations = self.get_observations(project=project, limit=max_items)
            stats["read"] = len(observations)
            
            # قراءة الملاحظات الموجودة بالفعل في Sofi Audit
            sofi_entries = set()
            if os.path.exists(SOFI_AUDIT_FILE):
                with open(SOFI_AUDIT_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        if "claude-mem" in line:
                            sofi_entries.add(hashlib.sha256(line.encode()).hexdigest()[:16])
            
            for obs in observations:
                try:
                    # تجنب التكرار
                    obs_hash = hashlib.sha256(
                        f"claude-mem:{obs.get('id')}:{obs.get('text', '')[:200]}".encode()
                    ).hexdigest()[:16]
                    
                    if obs_hash in sofi_entries:
                        stats["skipped"] += 1
                        continue
                    
                    # تحويل إلى Sofi format
                    agent = obs.get("agent_id", "claude-mem")
                    office = "ai_data"
                    action = f"claude_mem.{obs.get('type', 'observation').replace('.', '_')}"
                    summary = obs.get("text", "")[:200]
                    
                    details = {
                        "claude_mem_id": obs.get("id"),
                        "project": obs.get("project"),
                        "type": obs.get("type"),
                        "title": obs.get("title"),
                        "subtitle": obs.get("subtitle"),
                        "facts": obs.get("facts", "")[:200],
                        "narrative": obs.get("narrative", "")[:200],
                        "concepts": obs.get("concepts", ""),
                        "source": "claude-mem",
                    }
                    
                    tags_raw = obs.get("concepts", "[]")
                    try:
                        concepts_list = json.loads(tags_raw) if isinstance(tags_raw, str) else tags_raw
                        if isinstance(concepts_list, list):
                            tags = [str(t).strip() for t in concepts_list if t]
                        else:
                            tags = ["claude-mem"]
                    except (json.JSONDecodeError, TypeError):
                        # Fallback: comma-separated
                        tags = [t.strip() for t in str(tags_raw).split(",") if t.strip()] if tags_raw else ["claude-mem"]
                    
                    lesson = obs.get("narrative", "")[:200]
                    
                    # تسجيل في Sofi
                    log_to_memory(
                        agent=agent,
                        office=office,
                        action=action,
                        summary=summary,
                        details=details,
                        lesson=lesson,
                        tags=tags + ["claude-mem", "synced"],
                    )
                    
                    stats["logged"] += 1
                    
                except Exception as e:
                    stats["errors"] += 1
                    continue
            
            with self._stats_lock:
                self._stats["claude_to_sofi"] += stats["logged"]
                self._stats["last_sync"] = datetime.now().isoformat()
            
            self._log(f"🔄 مزامنة claude-mem→Sofi: {stats['logged']} مسجل، {stats['skipped']} مكرر")
            
        except Exception as e:
            stats["errors"] += 1
            self._log(f"❌ فشل المزامنة claude-mem→Sofi: {e}")
        
        return stats
    
    # ════════════════════════════════════════════════════════════
    # 🔍 بحث موحد
    # ════════════════════════════════════════════════════════════
    
    def unified_search(self, query: str, limit: int = 10) -> Dict[str, List]:
        """
        🔍 بحث موحد في الذاكرتين معاً
        
        يبحث في:
          1. 🧠 Sofi Semantic Memory
          2. 📝 Sofi Episodic Memory
          3. 📋 Sofi Audit Log
          4. 🔗 Claude-Mem Observations (FTS5)
          5. 🔗 Claude-Mem Summaries (FTS5)
        
        Returns:
            نتائج منظمة حسب المصدر
        """
        results = {
            "sofi_semantic": [],
            "sofi_episodic": [],
            "sofi_audit": [],
            "claude_mem_observations": [],
            "claude_mem_summaries": [],
            "unified": [],
        }
        
        # 1. Sofi Semantic
        try:
            from tools.shared.memory_core import MemoryCore
            core = MemoryCore()
            semantic = core.search_knowledge(query, n=limit)
            for s in semantic:
                s["_source"] = "sofi_semantic"
            results["sofi_semantic"] = semantic
            results["unified"].extend(semantic)
        except Exception:
            pass
        
        # 2. Sofi Episodic
        try:
            from tools.shared.memory_core import MemoryCore
            core = MemoryCore()
            episodic = core.recall_events(n=limit)
            matching = [e for e in episodic if query.lower() in 
                       json.dumps(e, ensure_ascii=False).lower()]
            for e in matching:
                e["_source"] = "sofi_episodic"
            results["sofi_episodic"] = matching
            results["unified"].extend(matching)
        except Exception:
            pass
        
        # 3. Sofi Audit
        if os.path.exists(SOFI_AUDIT_FILE):
            try:
                with open(SOFI_AUDIT_FILE, "r", encoding="utf-8") as f:
                    entries = []
                    for line in f:
                        if line.strip() and query.lower() in line.lower():
                            try:
                                entries.append(json.loads(line))
                            except Exception:
                                pass
                    entries = entries[-limit:]
                    for e in entries:
                        e["_source"] = "sofi_audit"
                    results["sofi_audit"] = entries
                    results["unified"].extend(entries)
            except Exception:
                pass
        
        # 4. Claude-Mem FTS5
        cm_results = self.search_claude_mem(query, limit)
        for obs in cm_results.get("observations", []):
            obs["_source"] = "claude_mem_observation"
        results["claude_mem_observations"] = cm_results.get("observations", [])
        results["unified"].extend(cm_results.get("observations", []))
        
        for summ in cm_results.get("summaries", []):
            summ["_source"] = "claude_mem_summary"
        results["claude_mem_summaries"] = cm_results.get("summaries", [])
        results["unified"].extend(cm_results.get("summaries", []))
        
        # ترتيب موحد حسب الثقة (Score عشوائي للمطابقات النصية)
        for item in results["unified"]:
            if "score" not in item:
                item["_confidence"] = 0.5
            else:
                item["_confidence"] = item.get("score", 0.5)
        
        results["unified"] = sorted(
            results["unified"], 
            key=lambda x: abs(x.get("_confidence", x.get("score", 0.5))),
            reverse=True
        )[:limit * 3]
        
        results["total"] = {
            "sofi_semantic": len(results["sofi_semantic"]),
            "sofi_episodic": len(results["sofi_episodic"]),
            "sofi_audit": len(results["sofi_audit"]),
            "claude_mem_observations": len(results["claude_mem_observations"]),
            "claude_mem_summaries": len(results["claude_mem_summaries"]),
            "unified": len(results["unified"]),
        }
        
        return results
    
    # ════════════════════════════════════════════════════════════
    # 📊 إحصائيات
    # ════════════════════════════════════════════════════════════
    
    def get_bridge_stats(self) -> Dict[str, Any]:
        """إحصائيات الجسر بين الذاكرتين"""
        with self._stats_lock:
            stats = dict(self._stats)
        
        # إحصائيات claude-mem
        conn = self._connect_claude_mem()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM observations WHERE project = 'sofi-ai'")
                stats["claude_mem_sofi_observations"] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM sdk_sessions WHERE platform_source = 'sofi'")
                stats["claude_mem_sofi_sessions"] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM session_summaries WHERE project = 'sofi-ai'")
                stats["claude_mem_sofi_summaries"] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM observations")
                stats["claude_mem_total_observations"] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM sdk_sessions")
                stats["claude_mem_total_sessions"] = cursor.fetchone()[0]
            finally:
                conn.close()
        
        # حجم قاعدة claude-mem
        if os.path.exists(CLAUDE_MEM_DB):
            stats["claude_mem_db_size"] = os.path.getsize(CLAUDE_MEM_DB)
        else:
            stats["claude_mem_db_size"] = 0
        
        # حجم قاعدة Sofi
        if os.path.exists(SOFI_AUDIT_FILE):
            stats["sofi_audit_size"] = os.path.getsize(SOFI_AUDIT_FILE)
        else:
            stats["sofi_audit_size"] = 0
        
        return stats
    
    def get_claude_mem_stats(self) -> Dict[str, Any]:
        """إحصائيات كاملة عن قاعدة claude-mem"""
        stats = {
            "connected": False,
            "tables": {},
            "sessions": {"total": 0, "active": 0, "completed": 0},
            "storage": {},
        }
        
        conn = self._connect_claude_mem()
        if not conn:
            return stats
        
        stats["connected"] = True
        
        try:
            cursor = conn.cursor()
            
            # عدد الجداول
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row["name"] for row in cursor.fetchall()]
            stats["tables"]["count"] = len(tables)
            stats["tables"]["names"] = tables
            
            # إحصاءات الجلسات
            cursor.execute("SELECT COUNT(*) FROM sdk_sessions")
            stats["sessions"]["total"] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM sdk_sessions WHERE status='active'")
            stats["sessions"]["active"] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM sdk_sessions WHERE status='completed'")
            stats["sessions"]["completed"] = cursor.fetchone()[0]
            
            # الملاحظات
            cursor.execute("SELECT COUNT(*) FROM observations")
            stats["observations"] = cursor.fetchone()[0]
            
            # الملخصات
            cursor.execute("SELECT COUNT(*) FROM session_summaries")
            stats["summaries"] = cursor.fetchone()[0]
            
            # الطلبات
            cursor.execute("SELECT COUNT(*) FROM user_prompts")
            stats["prompts"] = cursor.fetchone()[0]
            
            # الرسائل المعلقة
            cursor.execute("SELECT COUNT(*) FROM pending_messages")
            stats["pending_messages"] = cursor.fetchone()[0]
            
            # التخزين
            stats["storage"]["db_path"] = CLAUDE_MEM_DB
            stats["storage"]["db_size_bytes"] = os.path.getsize(CLAUDE_MEM_DB)
            stats["storage"]["db_size_mb"] = round(os.path.getsize(CLAUDE_MEM_DB) / 1024 / 1024, 2)
            
        finally:
            conn.close()
        
        return stats
    
    # ════════════════════════════════════════════════════════════
    # 🔧 أدوات مساعدة
    # ════════════════════════════════════════════════════════════
    
    def _notify_sniffer(self, event: str, data: Dict):
        """إخطار Sniffer بحدث (يكتب في ملف)"""
        try:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "event": event,
                "data": data,
                "source": "claude_mem_bridge"
            }
            sniffer_dir = os.path.join(SOFI_MEMORY_DIR, "sniffer_audit.jsonl")
            with open(SOFI_SNIFFER_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass
    
    def _log(self, msg: str):
        """طباعة مع وسوم"""
        print(f"  🔗 {msg}")
    
    def get_status(self) -> Dict[str, Any]:
        """حالة الجسر كاملة"""
        sofi_stats = self.get_bridge_stats()
        claude_stats = self.get_claude_mem_stats()
        
        return {
            "bridge_version": "1.0.0",
            "connected_to_claude_mem": claude_stats.get("connected", False),
            "claude_mem_db": CLAUDE_MEM_DB,
            "agent_memory_dir": SOFI_MEMORY_DIR,
            "sofi_stats": sofi_stats,
            "claude_mem_stats": claude_stats,
            "last_sync": self._stats.get("last_sync"),
        }


# ════════════════════════════════════════════════════════════
# 🏭 الواجهة السهلة
# ════════════════════════════════════════════════════════════

BRIDGE = ClaudeMemBridge()

def add_to_claude_mem(text: str, project: str = "sofi-ai", 
                       type: str = "analysis", **kwargs) -> Optional[int]:
    """إضافة ملاحظة إلى claude-mem (واجهة سهلة)"""
    return BRIDGE.add_observation(text=text, project=project, type=type, **kwargs)

def sync_to_claude_mem(max_entries: int = 100) -> Dict:
    """مزامنة Sofi → claude-mem (واجهة سهلة)"""
    return BRIDGE.sync_sofi_to_claude_mem(max_entries=max_entries)

def sync_from_claude_mem(max_items: int = 100) -> Dict:
    """مزامنة claude-mem → Sofi (واجهة سهلة)"""
    return BRIDGE.sync_claude_mem_to_sofi(max_items=max_items)

def unified_search(query: str, limit: int = 10) -> Dict:
    """بحث موحد (واجهة سهلة)"""
    return BRIDGE.unified_search(query=query, limit=limit)


# ════════════════════════════════════════════════════════════
# 🧪 تشغيل تجريبي
# ════════════════════════════════════════════════════════════

def demo():
    """عرض تشغيلي لـ Claude-Mem Bridge"""
    print("\n" + "=" * 70)
    print("🔗 Claude-Mem Bridge — التشغيل التجريبي v1.0.0")
    print("=" * 70)
    
    bridge = ClaudeMemBridge()
    
    # 1. حالة الاتصال
    print("\n1. 📡 الاتصال بـ claude-mem...")
    claude_stats = bridge.get_claude_mem_stats()
    if claude_stats.get("connected"):
        print(f"   ✅ متصل! المسار: {claude_stats['storage']['db_path']}")
        print(f"   📊 قاعدة البيانات: {claude_stats['storage']['db_size_mb']}MB")
        print(f"   📝 {claude_stats['observations']} ملاحظة")
        print(f"   💬 {claude_stats['sessions']['total']} جلسة")
    else:
        print(f"   ❌ غير متصل — قاعدة claude-mem غير موجودة")
    
    # 2. إضافة ملاحظة
    print("\n2. 📝 إضافة ملاحظة في claude-mem...")
    obs_id = bridge.add_observation(
        text="🧪 اختبار جسر الذاكرة — Sofi AI يتكامل مع claude-mem",
        project="sofi-ai",
        type="test",
        title="اختبار الدمج",
        subtitle="Sofi AI → claude-mem",
        facts="Sofi AI: CEO, 534 agents, 4 offices, Sniffer",
        narrative="هذا اختبار للتأكد من أن الجسر بين Sofi Memory و claude-mem يعمل بشكل صحيح",
        concepts="test, integration, sofi, claude-mem, bridge",
        agent_type="sofi-ceo",
        agent_id="Sofi-CEO",
        metadata=json.dumps({"test": True, "version": "1.0.0"})
    )
    if obs_id:
        print(f"   ✅ ملاحظة ID: {obs_id}")
    else:
        print(f"   ⚠️ موجودة مسبقاً أو فشل")
    
    # 3. إضافة ملخص
    print("\n3. 📝 إضافة ملخص جلسة في claude-mem...")
    summary_id = bridge.add_summary(
        project="sofi-ai",
        request="🧪 اختبار جسر الذاكرة",
        investigated="Claude-Mem Bridge v1.0.0",
        learned="الربط بين Sofi و claude-mem يعمل عبر SQLite المباشر",
        completed="قراءة/كتابة + بحث FTS5 + مزامنة ثنائية الاتجاه",
        next_steps="توسيع لدعم جميع الـ 534 وكيلاً",
        notes="الدمج يتيح رؤية أحداث Sofi في واجهة claude-mem على port 37700",
        agent_id="Sofi-CEO"
    )
    if summary_id:
        print(f"   ✅ ملخص ID: {summary_id}")
    
    # 4. قراءة ملاحظات Sofi
    print("\n4. 📖 قراءة ملاحظات Sofi من claude-mem...")
    sofi_obs = bridge.get_observations(project="sofi-ai", limit=5)
    print(f"   📊 {len(sofi_obs)} ملاحظة Sofi في claude-mem")
    for obs in sofi_obs[:3]:
        print(f"   📌 [{obs['type']}] {obs['title'][:70]}...")
    
    # 5. إحصائيات
    print("\n5. 📊 إحصائيات الجسر:")
    status = bridge.get_status()
    print(f"   🔗 متصل بـ claude-mem: {status['connected_to_claude_mem']}")
    print(f"   📋 ملاحظات Sofi في claude-mem: {status.get('sofi_stats', {}).get('claude_mem_sofi_observations', 0)}")
    print(f"   📊 حجم قاعدة claude-mem: {status.get('claude_mem_stats', {}).get('storage', {}).get('db_size_mb', 0)}MB")
    
    print("\n" + "=" * 70)
    print("✅ Claude-Mem Bridge جاهز!")
    return bridge


if __name__ == "__main__":
    demo()
