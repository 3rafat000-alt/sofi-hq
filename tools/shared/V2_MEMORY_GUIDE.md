# 🧠 SOFI AI Memory Hub V2 — دليل الدمج والتوسيع

## 📋 ملخص

SOFI AI Memory V2 هو نظام الذاكرة الموحد الذي يدمج **SOFI AI Memory** (5 أنواع) مع **Claude-Mem v13.4.0** في نظام واحد متكامل.

## 🏗️ المكونات

```
📁 tools/shared/
├── claude_mem_bridge.py     ← 🔗 جسر claude-mem (قراءة/كتابة/مزامنة)
├── agent_memory_v2.py       ← 🧠 الذاكرة الموحدة V2
├── agent_memory.py          ← 🧠 الذاكرة الأساسية V1 (ما زالت تعمل)
└── memory_core.py           ← 🧬 قلب الذاكرة الأساسي

📁 .claude/memory/v2/
├── council_decisions.jsonl  ← 🏛️ قرارات مجلس الإدارة
├── cross_reference.jsonl    ← 🔗 مرجع متقاطع
└── memory_index.json        ← 🧬 مؤشر الذاكرة للربط
```

## 🧬 7 أنواع ذاكرة

| # | النوع | الموقع | الغرض |
|---|-------|--------|-------|
| 1 | 📋 Audit | `.claude/memory/audit.jsonl` | سجل دائم لا يُمسح |
| 2 | 📝 Episodic | `.claude/memory/episodic.db` | أحداث + دروس مستفادة |
| 3 | 🧠 Semantic | `.claude/memory/semantic.db` | معرفة للبحث المستقبلي |
| 4 | ⚡ Working | In-Memory (24h TTL) | سياق قصير لكل وكيل |
| 5 | 🔄 Procedural | `.claude/memory/procedural.db` | إجراءات قابلة لإعادة الاستخدام |
| 6 | 🔗 Claude-Mem | `~/.claude-mem/claude-mem.db` (FTS5) | ملاحظات + بحث نصي كامل |
| 7 | 🏛️ Council | `.claude/memory/v2/council_decisions.jsonl` | قرارات المجلس |

## 🔗 Claude-Mem Bridge

### الاتصال
```python
from tools.shared.claude_mem_bridge import ClaudeMemBridge
bridge = ClaudeMemBridge()

# 📝 إضافة ملاحظة
bridge.add_observation(
    text="تحليل بنية النظام",
    project="sofi-ai",
    type="analysis",
    title="تحليل بنية API",
    agent_id="Architect-1"
)

# 📖 قراءة ملاحظات
obs = bridge.get_observations(project="sofi-ai", limit=10)

# 🔍 بحث نصي كامل (FTS5)
results = bridge.search_claude_mem("API architecture")

# 🔄 مزامنة SOFI AI → claude-mem
bridge.sync_sofi_to_claude_mem()

# 🔄 مزامنة claude-mem → SOFI AI
bridge.sync_claude_mem_to_SOFI AI()
```

## 🧠 SOFI AI Memory V2

### التسجيل الموحد
```python
from tools.shared.claude/memory_v2 import AgentMemoryV2
mem = AgentMemoryV2()

# يسجل في 7 ذاكرات دفعة واحدة
mem.log(
    agent="Builder-1",
    office="engineering",
    action="task.complete",
    summary="بنيت API مع JWT",
    lesson="استخدام refresh tokens أفضل",
    sync_to_claude_mem=True  # ينسخ تلقائياً لـ claude-mem
)
```

### البحث الموحد
```python
# يبحث في ALL الذاكرات
results = mem.search("API endpoint", limit=10)
# يعيد نتائج من: Semantic + Episodic + Audit + Claude-Mem + Council
```

### المزامنة الكاملة
```python
mem.sync_all()  # SOFI AI ↔ claude-mem دفعة واحدة
```

## 📡 أدوات MCP الجديدة (14 أداة)

| الأداة | الوظيفة |
|--------|---------|
| `agent_memory_v2_log` | تسجيل في الذاكرة الموحدة |
| `agent_memory_v2_search` | بحث في جميع الذاكرات |
| `agent_memory_v2_sync` | مزامنة SOFI AI ↔ claude-mem |
| `agent_memory_v2_status` | حالة الذاكرة الموحدة |
| `agent_memory_v2_agent` | سجل وكيل معين |

## 📊 إحصائيات الدمج

```
🔗 Claude-Mem DB:     ~/.claude-mem/claude-mem.db (SQLite + FTS5)
🧠 SOFI AI Memory:      .claude/memory/ (JSONL + 3 × SQLite + In-Memory)

⬆️ SOFI AI → claude-mem:  74 observation
⬇️ claude-mem → SOFI AI:   74 event logged
🔄 متصل:                 ✅ نعم
📊 حجم قاعدة claude-mem: 0.47MB
```

## 🎯 لكل وكيل من الـ 534

كل وكيل الآن له:
1. 📝 **سجل في SOFI AI** (Audit + Episodic + Semantic + Working + Procedural)
2. 🔗 **سجل في claude-mem** (Observation + FTS5)
3. 🧬 **مؤشر في Memory Index** (للربط بين المعرفات)
4. 🔍 **قابل للبحث** عبر FTS5 في كلا النظامين

## 📍 المسارات

| المكون | المسار |
|--------|--------|
| SOFI AI Memory | `/home/es3dlll/Desktop/sofi-ai-v7-ultimate/.claude/memory/` |
| Claude-Mem DB | `/home/es3dlll/.claude-mem/claude-mem.db` |
| Claude-Mem Viewer | `http://localhost:37700` |
| Memory V2 Index | `.claude/memory/v2/memory_index.json` |
| Council Decisions | `.claude/memory/v2/council_decisions.jsonl` |
