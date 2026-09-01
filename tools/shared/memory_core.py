"""
Sofi Memory Core — 4-Type Memory Architecture

Working Memory  : Short-term session context (TTL-based, RAM/Redis)
Semantic Memory : Long-term knowledge storage (Vector DB / ChromaDB)
Episodic Memory : Event recording with timestamps & lessons (PostgreSQL/JSON)
Procedural Memory: Workflows and procedures (code + structured storage)

API:
  set_context(key, value, ttl=300) -> stores in Working
  get_context(key)                  -> retrieves from Working / Semantic fallback
  store_knowledge(text, tags, meta) -> stores in Semantic
  search_knowledge(query, n=5)      -> vector search in Semantic
  record_event(event_type, data)    -> stores in Episodic
  recall_events(event_type, n=10)   -> retrieves recent events
  learn_from_mistakes(outcome, data) -> extracts lesson into Episodic
  store_procedure(name, steps, tags) -> stores in Procedural
  get_procedure(name)               -> retrieves from Procedural
  run_procedure(name, context)      -> executes procedure steps
"""

import json
import time
import hashlib
import sqlite3
import os
import threading
from datetime import datetime, timedelta
from collections import OrderedDict
from typing import Any, Optional

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False

try:
    import psycopg2
    import psycopg2.extras
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False

try:
    import redis as redis_lib
    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False


MEMORY_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".claude/memory")
os.makedirs(MEMORY_DB_DIR, exist_ok=True)

CHROMA_DIR = os.path.join(MEMORY_DB_DIR, "chroma")
EPISODIC_DB_PATH = os.path.join(MEMORY_DB_DIR, "episodic.db")
PROCEDURAL_DB_PATH = os.path.join(MEMORY_DB_DIR, "procedural.db")


class _SimpleEmbedder:
    def __init__(self):
        self.dim = 256

    def embed(self, text: str):
        if HAS_NUMPY:
            h = hashlib.sha256(text.encode()).digest()
            arr = np.frombuffer(h, dtype=np.float32)
            arr = arr[:self.dim]
            if len(arr) < self.dim:
                arr = np.pad(arr, (0, self.dim - len(arr)))
            norm = np.linalg.norm(arr)
            if norm > 0:
                arr = arr / norm
            return arr.tolist()
        h = hashlib.sha256(text.encode()).hexdigest()
        return [int(h[i:i+2], 16) / 255.0 for i in range(0, min(64, self.dim * 2), 2)]


_embedder = _SimpleEmbedder()


class WorkingMemory:
    """Short-term session context with TTL. In-memory dict + optional Redis."""
    def __init__(self, redis_url=None, default_ttl=300):
        self._local = {}
        self._lock = threading.Lock()
        self.default_ttl = default_ttl
        self._redis = None
        self._redis_prefix = "sofi:working:"
        if redis_url and HAS_REDIS:
            try:
                self._redis = redis_lib.from_url(redis_url, decode_responses=True)
            except Exception:
                self._redis = None

    def _redis_key(self, key):
        return f"{self._redis_prefix}{key}"

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        ttl = ttl if ttl is not None else self.default_ttl
        expiry = time.time() + ttl
        with self._lock:
            self._local[key] = {"value": value, "expiry": expiry}
        if self._redis:
            try:
                self._redis.setex(
                    self._redis_key(key),
                    ttl,
                    json.dumps({"value": value, "expiry": expiry}, default=str)
                )
            except Exception:
                pass
        return True

    def get(self, key: str, default=None):
        with self._lock:
            entry = self._local.get(key)
            if entry and time.time() < entry["expiry"]:
                return entry["value"]
            elif entry:
                del self._local[key]
                return default
        if self._redis:
            try:
                data = self._redis.get(self._redis_key(key))
                if data:
                    parsed = json.loads(data)
                    if time.time() < parsed["expiry"]:
                        return parsed["value"]
                    self._redis.delete(self._redis_key(key))
            except Exception:
                pass
        return default

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._local:
                del self._local[key]
        if self._redis:
            try:
                self._redis.delete(self._redis_key(key))
            except Exception:
                pass
        return True

    def keys(self, pattern: str = "*"):
        with self._lock:
            matched = [k for k in self._local.keys()]
        if self._redis:
            try:
                rkeys = self._redis.keys(self._redis_key(pattern.replace("*", "")))
                matched.extend([k.replace(self._redis_prefix, "") for k in rkeys])
            except Exception:
                pass
        return list(set(matched))

    def clear_expired(self):
        now = time.time()
        with self._lock:
            expired = [k for k, v in self._local.items() if now >= v["expiry"]]
            for k in expired:
                del self._local[k]
        return len(expired)

    def __contains__(self, key):
        return self.get(key) is not None

    def __getitem__(self, key):
        val = self.get(key)
        if val is None:
            raise KeyError(key)
        return val

    def __setitem__(self, key, value):
        self.set(key, value)


class SemanticMemory:
    """Long-term knowledge via ChromaDB vector store. Falls back to SQLite."""
    def __init__(self, collection_name="sofi_semantic"):
        self.collection_name = collection_name
        self._client = None
        self._collection = None
        self._sqlite_conn = None
        self._init_chroma()
        if not self._collection:
            self._init_sqlite()

    def _init_chroma(self):
        if not HAS_CHROMA:
            return
        try:
            self._client = chromadb.PersistentClient(
                path=CHROMA_DIR,
                settings=Settings(anonymized_telemetry=False)
            )
            existing = self._client.list_collections()
            names = [c.name for c in existing] if existing else []
            if self.collection_name in names:
                self._collection = self._client.get_collection(self.collection_name)
            else:
                self._collection = self._client.create_collection(self.collection_name)
        except Exception as e:
            print(f"[Memory] ChromaDB init skipped: {e}")
            self._collection = None

    def _init_sqlite(self):
        db_path = os.path.join(MEMORY_DB_DIR, f"semantic_{self.collection_name}.db")
        self._sqlite_conn = sqlite3.connect(db_path)
        self._sqlite_conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                id TEXT PRIMARY KEY,
                text TEXT,
                tags TEXT,
                metadata TEXT,
                embedding TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self._sqlite_conn.commit()

    def store(self, text: str, tags: list = None, metadata: dict = None, doc_id: str = None):
        doc_id = doc_id or hashlib.md5(text.encode()).hexdigest()[:16]
        tags_str = json.dumps(tags or [], ensure_ascii=False)
        meta_str = json.dumps(metadata or {}, ensure_ascii=False)

        if self._collection:
            try:
                embedding = _embedder.embed(text)
                self._collection.add(
                    documents=[text],
                    metadatas=[{**(metadata or {}), "tags": tags_str}],
                    ids=[doc_id],
                    embeddings=[embedding]
                )
                return doc_id
            except Exception as e:
                print(f"[Memory] Chroma store fallback: {e}")

        if self._sqlite_conn:
            embedding = _embedder.embed(text)
            self._sqlite_conn.execute(
                "INSERT OR REPLACE INTO knowledge (id, text, tags, metadata, embedding) VALUES (?, ?, ?, ?, ?)",
                (doc_id, text, tags_str, meta_str, json.dumps(embedding))
            )
            self._sqlite_conn.commit()
        return doc_id

    def search(self, query: str, n: int = 5, tags: list = None):
        if self._collection:
            try:
                q_emb = _embedder.embed(query)
                results = self._collection.query(
                    query_embeddings=[q_emb],
                    n_results=n
                )
                items = []
                if results and results.get("documents"):
                    for i, doc in enumerate(results["documents"][0]):
                        meta = {}
                        if results.get("metadatas") and results["metadatas"][0]:
                            meta = results["metadatas"][0][i]
                        items.append({
                            "text": doc,
                            "metadata": meta,
                            "score": results["distances"][0][i] if results.get("distances") else 0
                        })
                if tags:
                    items = [it for it in items if any(t in json.dumps(it["metadata"]) for t in tags)]
                return items
            except Exception as e:
                print(f"[Memory] Chroma search fallback: {e}")

        if self._sqlite_conn:
            q_emb = _embedder.embed(query)
            cursor = self._sqlite_conn.execute(
                "SELECT id, text, tags, metadata, embedding FROM knowledge ORDER BY created_at DESC LIMIT ?",
                (n * 10,)
            )
            results = []
            for row in cursor.fetchall():
                stored_emb = json.loads(row[4])
                similarity = sum(a * b for a, b in zip(q_emb, stored_emb))
                results.append({
                    "id": row[0],
                    "text": row[1],
                    "tags": json.loads(row[2]),
                    "metadata": json.loads(row[3]),
                    "score": 1 - similarity
                })
            results.sort(key=lambda x: x["score"])
            results = results[:n]
            if tags:
                results = [r for r in results if any(t in r["tags"] for t in tags)]
            return results
        return []

    def get_by_tags(self, tags: list, n: int = 20):
        if self._sqlite_conn:
            placeholders = ",".join("?" for _ in tags)
            cursor = self._sqlite_conn.execute(
                f"SELECT id, text, tags, metadata FROM knowledge WHERE EXISTS (SELECT 1 FROM json_each(tags) WHERE value IN ({placeholders})) ORDER BY created_at DESC LIMIT ?",
                (*tags, n)
            )
            return [{"id": r[0], "text": r[1], "tags": json.loads(r[2]), "metadata": json.loads(r[3])} for r in cursor.fetchall()]
        return []

    def delete(self, doc_id: str):
        if self._collection:
            try:
                self._collection.delete(ids=[doc_id])
                return True
            except Exception:
                pass
        if self._sqlite_conn:
            self._sqlite_conn.execute("DELETE FROM knowledge WHERE id = ?", (doc_id,))
            self._sqlite_conn.commit()
            return True
        return False

    def count(self):
        if self._collection:
            try:
                return self._collection.count()
            except Exception:
                pass
        if self._sqlite_conn:
            cursor = self._sqlite_conn.execute("SELECT COUNT(*) FROM knowledge")
            return cursor.fetchone()[0]
        return 0


class EpisodicMemory:
    """Event recording with timestamps, structured details, and lesson extraction."""
    def __init__(self, pg_connection_string=None):
        self._pg_conn = None
        self._sqlite_conn = None
        if pg_connection_string and HAS_POSTGRES:
            try:
                self._pg_conn = psycopg2.connect(pg_connection_string)
                self._pg_conn.execute("""
                    CREATE TABLE IF NOT EXISTS episodes (
                        id SERIAL PRIMARY KEY,
                        event_type TEXT,
                        agent TEXT,
                        summary TEXT,
                        data JSONB,
                        tags JSONB,
                        lesson TEXT,
                        lesson_applied BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                """)
                self._pg_conn.commit()
                return
            except Exception as e:
                print(f"[Memory] PostgreSQL unavailable: {e}")
                self._pg_conn = None
        self._init_sqlite()

    def _init_sqlite(self):
        self._sqlite_conn = sqlite3.connect(EPISODIC_DB_PATH)
        self._sqlite_conn.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                agent TEXT,
                summary TEXT,
                data TEXT,
                tags TEXT,
                lesson TEXT,
                lesson_applied INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self._sqlite_conn.execute("CREATE INDEX IF NOT EXISTS idx_episodes_type ON episodes(event_type)")
        self._sqlite_conn.execute("CREATE INDEX IF NOT EXISTS idx_episodes_agent ON episodes(agent)")
        self._sqlite_conn.execute("CREATE INDEX IF NOT EXISTS idx_episodes_created ON episodes(created_at)")
        self._sqlite_conn.commit()

    def record(self, event_type: str, data: dict, agent: str = "system", tags: list = None):
        summary = data.get("summary", data.get("message", str(data)[:200]))
        lesson = data.get("lesson", "")
        lesson = self._extract_lesson(event_type, data, lesson)
        data_str = json.dumps(data, ensure_ascii=False, default=str)
        tags_str = json.dumps(tags or [], ensure_ascii=False)

        if self._pg_conn:
            try:
                cur = self._pg_conn.cursor()
                cur.execute(
                    "INSERT INTO episodes (event_type, agent, summary, data, tags, lesson) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    (event_type, agent, summary, json.dumps(data), json.dumps(tags or []), lesson)
                )
                self._pg_conn.commit()
                ep_id = cur.fetchone()[0]
                cur.close()
                return ep_id
            except Exception:
                self._pg_conn.rollback()

        if self._sqlite_conn:
            cur = self._sqlite_conn.execute(
                "INSERT INTO episodes (event_type, agent, summary, data, tags, lesson) VALUES (?, ?, ?, ?, ?, ?)",
                (event_type, agent, summary, data_str, tags_str, lesson)
            )
            self._sqlite_conn.commit()
            return cur.lastrowid
        return None

    def recall(self, event_type: str = None, agent: str = None, n: int = 10, include_lessons: bool = True):
        conditions = []
        params = []
        if event_type:
            conditions.append("event_type = ?")
            params.append(event_type)
        if agent:
            conditions.append("agent = ?")
            params.append(agent)
        if include_lessons:
            conditions.append("lesson != ''")
        where = " AND ".join(conditions) if conditions else "1=1"

        if self._pg_conn:
            try:
                pg_params = [p for p in params]
                pg_where = where.replace("?", "%s")
                cur = self._pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cur.execute(
                    f"SELECT * FROM episodes WHERE {pg_where} ORDER BY created_at DESC LIMIT %s",
                    (*pg_params, n)
                )
                rows = cur.fetchall()
                cur.close()
                return [dict(r) for r in rows]
            except Exception:
                pass

        if self._sqlite_conn:
            cursor = self._sqlite_conn.execute(
                f"SELECT * FROM episodes WHERE {where} ORDER BY created_at DESC LIMIT ?",
                (*params, n)
            )
            return [self._row_to_dict(r) for r in cursor.fetchall()]
        return []

    def recall_by_time_range(self, start: datetime, end: datetime):
        if self._sqlite_conn:
            cursor = self._sqlite_conn.execute(
                "SELECT * FROM episodes WHERE created_at BETWEEN ? AND ? ORDER BY created_at DESC",
                (start.isoformat(), end.isoformat())
            )
            return [self._row_to_dict(r) for r in cursor.fetchall()]
        return []

    def get_lessons(self, applied: bool = None, n: int = 20):
        if applied is not None:
            val = 1 if applied else 0
            cursor = self._sqlite_conn.execute(
                "SELECT * FROM episodes WHERE lesson != '' AND lesson_applied = ? ORDER BY created_at DESC LIMIT ?",
                (val, n)
            )
        else:
            cursor = self._sqlite_conn.execute(
                "SELECT * FROM episodes WHERE lesson != '' ORDER BY created_at DESC LIMIT ?",
                (n,)
            )
        return [self._row_to_dict(r) for r in cursor.fetchall()]

    def mark_lesson_applied(self, episode_id: int):
        if self._pg_conn:
            try:
                cur = self._pg_conn.cursor()
                cur.execute("UPDATE episodes SET lesson_applied = TRUE WHERE id = %s", (episode_id,))
                self._pg_conn.commit()
                cur.close()
                return True
            except Exception:
                self._pg_conn.rollback()
        if self._sqlite_conn:
            self._sqlite_conn.execute("UPDATE episodes SET lesson_applied = 1 WHERE id = ?", (episode_id,))
            self._sqlite_conn.commit()
            return True
        return False

    def count(self):
        if self._pg_conn:
            try:
                cur = self._pg_conn.cursor()
                cur.execute("SELECT COUNT(*) FROM episodes")
                cnt = cur.fetchone()[0]
                cur.close()
                return cnt
            except Exception:
                pass
        if self._sqlite_conn:
            cursor = self._sqlite_conn.execute("SELECT COUNT(*) FROM episodes")
            return cursor.fetchone()[0]
        return 0

    def _extract_lesson(self, event_type: str, data: dict, existing_lesson: str = ""):
        if existing_lesson:
            return existing_lesson
        error = data.get("error") or data.get("failure") or data.get("exception")
        if error:
            return f"Avoid: {error}"
        if event_type in ("success", "milestone"):
            approach = data.get("approach") or data.get("method") or data.get("action")
            if approach:
                return f"Use: {approach}"
        return existing_lesson

    def _row_to_dict(self, row):
        return {
            "id": row[0],
            "event_type": row[1],
            "agent": row[2],
            "summary": row[3],
            "data": json.loads(row[4]) if row[4] else {},
            "tags": json.loads(row[5]) if row[5] else [],
            "lesson": row[6] or "",
            "lesson_applied": bool(row[7]),
            "created_at": row[8]
        }


class ProceduralMemory:
    """Stores and retrieves workflows, procedures, and execution contexts."""
    def __init__(self):
        self._db = sqlite3.connect(PROCEDURAL_DB_PATH)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS procedures (
                name TEXT PRIMARY KEY,
                description TEXT,
                steps TEXT,
                tags TEXT,
                inputs TEXT,
                outputs TEXT,
                version INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS procedure_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                procedure_name TEXT,
                context TEXT,
                result TEXT,
                duration_ms INTEGER,
                success INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self._db.commit()
        self._lock = threading.Lock()

    def store(self, name: str, steps: list, description: str = "", tags: list = None, inputs: dict = None, outputs: dict = None):
        with self._lock:
            existing = self._db.execute("SELECT version FROM procedures WHERE name = ?", (name,)).fetchone()
            version = (existing[0] + 1) if existing else 1
            self._db.execute(
                """INSERT OR REPLACE INTO procedures
                   (name, description, steps, tags, inputs, outputs, version, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                (name, description, json.dumps(steps, ensure_ascii=False),
                 json.dumps(tags or [], ensure_ascii=False),
                 json.dumps(inputs or {}, ensure_ascii=False),
                 json.dumps(outputs or {}, ensure_ascii=False),
                 version)
            )
            self._db.commit()
            return version

    def get(self, name: str):
        row = self._db.execute(
            "SELECT * FROM procedures WHERE name = ?", (name,)
        ).fetchone()
        if not row:
            return None
        return {
            "name": row[0],
            "description": row[1],
            "steps": json.loads(row[2]),
            "tags": json.loads(row[3]) if row[3] else [],
            "inputs": json.loads(row[4]) if row[4] else {},
            "outputs": json.loads(row[5]) if row[5] else {},
            "version": row[6],
            "created_at": row[7],
            "updated_at": row[8]
        }

    def search(self, query: str, tags: list = None, n: int = 10):
        sql = "SELECT * FROM procedures WHERE (name LIKE ? OR description LIKE ? OR steps LIKE ?)"
        params = [f"%{query}%", f"%{query}%", f"%{query}%"]
        if tags:
            placeholders = " OR ".join("tags LIKE ?" for _ in tags)
            sql += f" AND ({placeholders})"
            params.extend([f"%{t}%" for t in tags])
        sql += " ORDER BY updated_at DESC LIMIT ?"
        params.append(n)
        rows = self._db.execute(sql, params).fetchall()
        results = []
        for row in rows:
            results.append({
                "name": row[0],
                "description": row[1],
                "steps": json.loads(row[2]),
                "tags": json.loads(row[3]) if row[3] else [],
                "version": row[6],
                "updated_at": row[8]
            })
        return results

    def delete(self, name: str):
        self._db.execute("DELETE FROM procedures WHERE name = ?", (name,))
        self._db.execute("DELETE FROM procedure_executions WHERE procedure_name = ?", (name,))
        self._db.commit()
        return True

    def list_all(self):
        rows = self._db.execute(
            "SELECT name, description, tags, version, updated_at FROM procedures ORDER BY updated_at DESC"
        ).fetchall()
        return [{
            "name": r[0],
            "description": r[1],
            "tags": json.loads(r[2]) if r[2] else [],
            "version": r[3],
            "updated_at": r[4]
        } for r in rows]

    def record_execution(self, procedure_name: str, context: dict, result: Any, duration_ms: int, success: bool):
        self._db.execute(
            "INSERT INTO procedure_executions (procedure_name, context, result, duration_ms, success) VALUES (?, ?, ?, ?, ?)",
            (procedure_name, json.dumps(context, default=str), json.dumps(result, default=str), duration_ms, 1 if success else 0)
        )
        self._db.commit()

    def get_execution_history(self, procedure_name: str, n: int = 10):
        rows = self._db.execute(
            "SELECT * FROM procedure_executions WHERE procedure_name = ? ORDER BY created_at DESC LIMIT ?",
            (procedure_name, n)
        ).fetchall()
        return [{
            "id": r[0],
            "procedure_name": r[1],
            "context": json.loads(r[2]),
            "result": json.loads(r[3]),
            "duration_ms": r[4],
            "success": bool(r[5]),
            "created_at": r[6]
        } for r in rows]

    def run(self, name: str, context: dict = None) -> dict:
        proc = self.get(name)
        if not proc:
            return {"success": False, "error": f"Procedure '{name}' not found"}
        context = context or {}
        start = time.time()
        try:
            outputs = {}
            for step in proc["steps"]:
                if callable(step):
                    result = step(context)
                elif isinstance(step, dict):
                    action = step.get("action", "")
                    if action in context:
                        result = context[action](**step.get("args", {}))
                    else:
                        result = f"Executed step: {step.get('description', action)}"
                else:
                    result = f"Executed: {step}"
                outputs[step.get("description", step) if isinstance(step, dict) else str(step)] = result
            duration = int((time.time() - start) * 1000)
            self.record_execution(name, context, outputs, duration, True)
            return {"success": True, "outputs": outputs, "duration_ms": duration}
        except Exception as e:
            duration = int((time.time() - start) * 1000)
            self.record_execution(name, context, str(e), duration, False)
            return {"success": False, "error": str(e), "duration_ms": duration}


class MemoryCore:
    """Unified memory interface — all 4 types under one class.

    Usage:
        mc = MemoryCore()
        mc.set_context("task", "build API")
        task = mc.get_context("task")
        mc.store_knowledge("Python 3.12 released", tags=["python", "news"])
        results = mc.search_knowledge("Python version")
        mc.record_event("deploy", {"status": "ok", "summary": "Deployed v2.1"})
        events = mc.recall_events("deploy")
        mc.learn_from_mistakes({"error": "timeout", "action": "increase timeout"})
        mc.store_procedure("deploy_steps", [
            {"description": "Run tests", "action": "test"},
            {"description": "Build image", "action": "build"}
        ])
        proc = mc.get_procedure("deploy_steps")
        mc.run_procedure("deploy_steps", {"test": lambda: "ok"})
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, redis_url=None, pg_connection_string=None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, redis_url=None, pg_connection_string=None):
        if self._initialized:
            return
        self._initialized = True
        self.working = WorkingMemory(redis_url=redis_url)
        self.semantic = SemanticMemory()
        self.episodic = EpisodicMemory(pg_connection_string=pg_connection_string)
        self.procedural = ProceduralMemory()

    # ---- Working Memory API ----
    def set_context(self, key: str, value: Any, ttl: int = 300):
        return self.working.set(key, value, ttl)

    def get_context(self, key: str, default=None):
        return self.working.get(key, default)

    def clear_context(self, key: str):
        return self.working.delete(key)

    # ---- Semantic Memory API ----
    def store_knowledge(self, text: str, tags: list = None, metadata: dict = None):
        return self.semantic.store(text, tags=tags, metadata=metadata)

    def search_knowledge(self, query: str, n: int = 5, tags: list = None):
        return self.semantic.search(query, n=n, tags=tags)

    # ---- Episodic Memory API ----
    def record_event(self, event_type: str, data: dict, agent: str = "system"):
        return self.episodic.record(event_type, data, agent=agent)

    def recall_events(self, event_type: str = None, agent: str = None, n: int = 10):
        return self.episodic.recall(event_type, agent=agent, n=n)

    def learn_from_mistakes(self, outcome: dict, agent: str = "system"):
        lesson = outcome.get("lesson", outcome.get("error", outcome.get("summary", str(outcome)[:200])))
        data = {"summary": f"Lesson learned: {lesson}", **(outcome)}
        return self.episodic.record("lesson", data, agent=agent)

    # ---- Procedural Memory API ----
    def store_procedure(self, name: str, steps: list, description: str = "", tags: list = None):
        return self.procedural.store(name, steps, description=description, tags=tags)

    def get_procedure(self, name: str):
        return self.procedural.get(name)

    def run_procedure(self, name: str, context: dict = None):
        return self.procedural.run(name, context)

    def search_procedures(self, query: str, tags: list = None):
        return self.procedural.search(query, tags=tags)

    # ---- Statistics ----
    def stats(self):
        return {
            "working_memory_keys": len(self.working.keys()),
            "semantic_knowledge_count": self.semantic.count(),
            "episodic_event_count": self.episodic.count(),
            "procedural_count": len(self.procedural.list_all())
        }
