# دليل MCP الموحد — كيف يستخدم الفريق 28 خادم MCP بذكاء (SOFI-HQ + SOFI-Platform)

> **المرجع الحي:** `opencode.json:13` (28 خادم) + `tools/mcp/*.py` (20 خادم platform)
> **القانون:** لا تفعيل ذاتي — `sec-mcp-vetting` إلزامي لأي خادم جديد (MCP-FLEET:5) — كل شيء مجاني (INT-0003)
> **تحديث 2026-09-01:** حُذف جسر SOFI (`hq/engine/mcp_server/mcp_bridge/server.py`) نهائياً — O-01

## 1) الخريطة الكاملة — 28 خادم حسب الغرفة

| MCP | الملف | الغرفة المالكة | القائد | متى تستخدمه | مثال |
|-----|-------|---------------|--------|-------------|------|
| **Context7** | remote | 04/05/06 | arc-lead/bck-lead | قبل أي كود يمس مكتبة — يمنع الهلوسة | `Context7: "how to use flutter bloc 8.x"` |
| **DeepWiki** | remote | 02/04 | res-lead/arc-lead | التحقق من مستودع خارجي | `DeepWiki: "verify stripe api 2024"` |
| **Sequential-Thinking** | local | 00/04 | brd-ceo/arc-lead | مشكلة متفرعة معقدة — حلل قبل القرار | `sequential 5 steps: auth flow` |
| **Chrome-DevTools** | local | 03/10 | dsn-lead/qa-lead | تدقيق وصولية وأداء واجهة | `analyze_html file.html` |
| **Playwright** | local | 10 | qa-lead | اختبار متصفح حي | `browser_navigate + snapshot` |
| **Kitesurf** | local | 03/10 | dsn-lead | لقطة وصولية دليل Law 4 | `kitesurf screenshot` |
| **Dart-Flutter** | local | 07 | mob-lead | تحليل كود Dart/Flutter | `dart analyze` |
| **Filesystem-Scoped** | local | 14 | gtw-dispatcher | قراءة ملفات المشروع | `read file` |
| **SOFI-Security** | `tools/mcp/security_mcp.py` | 09 | sec-lead | فحص أمني، SAST، تبعيات | `scan_security path=.` |
| **SOFI-Postgres** | `tools/mcp/postgres_mcp.py` | 08 | dat-lead | استعلامات قواعد بيانات | `pg_query "SELECT * from users"` |
| **SOFI-Redis** | `tools/mcp/redis_mcp.py` | 08 | dat-cache-engineer | كاش وطوابير | `redis_get key` |
| **SOFI-Time** | `tools/mcp/time_mcp.py` | 14 | gtw-dispatcher | توقيت وجدولة | `current_time timezone=Asia/Riyadh` |
| **SOFI-WebFetch** | `tools/mcp/webfetch_mcp.py` | 02 | res-web-scout | جلب ويب نظيف | `fetch https://example.com` |
| **SOFI-MemoryHub** | `tools/mcp/memory_hub_mcp.py` | 13 | knw-lead | محور ذاكرة مركزي | `memory_hub store` |
| **SOFI-Sniffer** | `tools/mcp/sniffer_mcp.py` | 12 | obs-lead | مراقبة شبكة وحزم | `sniffer audit` |
| **SOFI-Status** | `tools/mcp/status.py` | 00 | brd-ceo | حالة النظام الكاملة | `system_status` |
| **SOFI-CodeDecomposer** | `tools/mcp/code_decomposer.py` | 04 | arc-lead | تحليل بنية مشروع | `decompose_code path=.` |
| **SOFI-Research** | `tools/mcp/research.py` | 02 | res-lead | بحث عميق متعدد المصادر | `research query="fintech ux"` |
| **SOFI-Consult** | `tools/mcp/consult.py` | 00 | brd-ceo | تشاور بين وكلاء | `consult topic="auth design"` |
| **SOFI-Skills** | `tools/mcp/skills.py` | 13 | knw-lead | سجل مهارات الوكلاء | `skill_registry office=engineering` |
| **SOFI-ToolForge** | `tools/mcp/tool_forge.py` | 04 | arc-lead | بناء أداة Python ديناميكية | `build_tool name=my_tool` |
| **SOFI-WorkingMemory** | `tools/mcp/working_memory.py` | 13 | knw-lead | ذاكرة عاملة مؤقتة TTL | `store_context key=session:123` |
| **SOFI-SemanticMemory** | `tools/mcp/semantic_memory_mcp.py` | 13 | knw-lead | ذاكرة دلالية طويلة | `store_knowledge text="..."` |
| **SOFI-EpisodicMemory** | `tools/mcp/episodic_memory_mcp.py` | 13 | knw-lead | ذاكرة حلقية أحداث | `record_event type=deploy` |
| **SOFI-ProceduralMemory** | `tools/mcp/procedural_memory_mcp.py` | 13 | knw-lead | ذاكرة إجرائية (إجراءات) | `store_procedure name=deploy_api` |
| **SOFI-Broker** | `tools/mcp/broker.py` | 00 | brd-ceo | تفويض هرمي 533 وكيل | `delegate task_name="build api"` |
| **SOFI-Network** | `tools/mcp/network.py` | 11 | ops-lead | إحصائيات شبكة الوكلاء | `network_stats` |
| **SOFI-ChromeDevTools-Platform** | `tools/mcp/chrome_devtools_mcp.py` | 03 | dsn-lead | تدقيق HTML/CSS/JS محلي | `analyze_html file` |

## 2) قواعد التوجيه الذكي — لكل غرفة

### القاعدة الذهبية: البوابة أولاً
- **أي كود يمس مكتبة → Context7 أولاً** (MCP-FLEET:1) — لا تخمن API
- **أي ادعاء عن مستودع خارجي → DeepWiki** (MCP-FLEET:2) — HiveFence lesson
- **أي لقطة وصولية → Kitesurf** (MCP-FLEET:3, Law 4)
- **مشكلة متفرعة → Sequential-Thinking** (MCP-FLEET:4)

### حسب الغرفة:

**00 Boardroom (brd-ceo):** `SOFI-Consult` + `SOFI-Broker` + `SOFI-Status` + `SOFI-Skills`
- متى: اتخاذ قرار مصيري، استشارة مجلس (Law 6)، تفويض هرمي، فحص صحة النظام

**02 Research (res-lead):** `SOFI-Research` + `SOFI-WebFetch` + `DeepWiki` + `Context7`
- متى: بحث سوق، تحقق منافس، جلب محتوى ويب، فهم مكتبة جديدة

**03 Design (dsn-lead):** `SOFI-ChromeDevTools-Platform` + `Chrome-DevTools` + `Kitesurf`
- متى: تدقيق وصولية، تباين ألوان، SEO، لقطة قبل/بعد

**04 Architecture (arc-lead):** `SOFI-CodeDecomposer` + `SOFI-ToolForge` + `Context7` + `Sequential-Thinking`
- متى: تحليل بنية مشروع، بناء أداة Python جديدة، قرار معماري معقد

**05 Backend (bck-lead):** `SOFI-Postgres` + `SOFI-Redis` + `Context7`
- متى: استعلام DB، فحص كاش، كتابة API

**08 Data (dat-lead):** `SOFI-Postgres` + `SOFI-Redis` + `SOFI-MemoryHub` + `SOFI-SemanticMemory`
- متى: مخطط، هجرة، كاش، ذاكرة دلالية

**09 Security (sec-lead):** `SOFI-Security` + `SOFI-Sniffer`
- متى: فحص أمني، SAST، تدقيق تبعيات، مراقبة شبكة — **فيتو مطلق**

**10 Quality (qa-lead):** `Playwright` + `SOFI-Sniffer` + `Chrome-DevTools`
- متى: اختبار متصفح، تدقيق جودة، انحداري

**11 DevOps (ops-lead):** `SOFI-Network` + `SOFI-Status` + `SOFI-Sniffer`
- متى: نشر، إحصائيات شبكة، صحة خوادم

**13 Knowledge (knw-lead):** `SOFI-MemoryHub` + `SOFI-SemanticMemory` + `SOFI-EpisodicMemory` + `SOFI-ProceduralMemory` + `SOFI-WorkingMemory` + `SOFI-Skills`
- متى: توثيق دروس، إجراءات، معرفة، مهارات

**14 Gateway (gtw-dispatcher):** `SOFI-Time` + `Filesystem-Scoped` + `Sequential-Thinking` + `SOFI-Status`
- متى: تصنيف طلب، فهم نية، توجيه، توقيت

## 3) كيف تستدعي MCP بذكاء — أمثلة عملية

### مثال 1: Backend يبني API جديد (05-bck)
```
# الخطأ: يكتب كود مباشرة بلا Context7
# الصح:
1. Context7: "laravel 11 how to create api resource with envelope"
2. SOFI-CodeDecomposer: decompose_code path=backend/app
3. SOFI-Postgres: pg_tables schema=public (افهم الجداول)
4. اكتب الكود ضد العقد المجمد
5. SOFI-Security: scan_security path=backend/app/Http/Controllers
```

### مثال 2: Design يصمم شاشة (03-dsn)
```
1. DeepWiki: verify "flutter bloc 8.x best practices" (تأكد من النمط)
2. صمم بـ Figma/Tokens
3. SOFI-ChromeDevTools-Platform: analyze_html file=hi-fi.html checks=[a11y,performance]
4. Kitesurf: لقطة قبل/بعد (Law 4)
```

### مثال 3: Research يبحث منافس (02-res)
```
1. SOFI-Research: research query="fintech wallet competitors UAE" depth=deep
2. SOFI-WebFetch: fetch https://competitor.com (جلب محتوى)
3. DeepWiki: verify claim about competitor tech stack
```

### مثال 4: Security يفحص تبعية (09-sec)
```
1. SOFI-Security: check_dependencies file=package.json
2. SOFI-Security: sast_scan file=auth.py severity=high
3. إن وجد GPL → فيتو (Law 15)
```

### مثال 5: Knowledge يوثق درس (13-knw)
```
1. SOFI-EpisodicMemory: record_event event_type=deploy data={summary:"v2 released", status:"success"}
2. SOFI-ProceduralMemory: store_procedure name=deploy_api steps=[...] 
3. SOFI-SemanticMemory: store_knowledge text="DFR must be signed before code"
```

## 4) البنية الجديدة — أين تعيش MCPs

```
SOFI/
├── tools/
│   ├── mcp/                     # 20 خادم MCP من sofi-platform (JSON-RPC stdio)
│   │   ├── base.py              # قاعدة SofiBaseMCP
│   │   ├── security_mcp.py      # 09
│   │   ├── postgres_mcp.py      # 08
│   │   ├── redis_mcp.py         # 08
│   │   ├── memory_hub_mcp.py    # 13
│   │   └── ... (20 total)
│   ├── mcp_broker/              # 9 وحدات وسيط (protocols, message_bus, orchestrator)
│   └── shared/                  # 8 مكتبات (memory_core, agent_memory, broker_lib, sniffer_lib...)
├── opencode.json                # 28 MCP مسجلة (8 أصلية + 20 جديدة)
└── hq/training/mcp-platform-guide.md  # هذا الدليل
```

## 5) الفحص قبل التسليم — كل MCP يجب أن يمر

- [ ] `python3 -c "from tools.mcp.base import SofiBaseMCP; print('OK')"` → exit 0
- [ ] `python3 -m json.tool opencode.json` → Valid
- [ ] `opencode debug config` → 28 MCP ظاهرة
- [ ] `SOFI-Security: scan_security` → لا GPL
- [ ] `SOFI-Status: system_status` → 114 وكيل صحيح

## 6) التحذيرات — ماذا لا تفعل

- ❌ لا تفعل MCP ذاتياً بلا `sec-mcp-vetting` (MCP-FLEET:5)
- ❌ لا تطلب مفتاحاً مدفوعاً (INT-0003 — كل شيء مجاني)
- ❌ لا تستخدم `SOFI-PRJ` كمصدر MCP (حظر أمني — يحتوي مفاتيح مكشوفة)
- ❌ لا تمزج MCPs خارج غرفتك — كل غرفة تملك أدواتها (Law 2 عزل الغرف)
- ✅ عند الشك: `SOFI-Consult` → `brd-ceo` → `brd-arbiter` 24h

---

> **الخلاصة:** 28 MCP ليست زينة — كل واحدة مربوطة بغرفة وقائد وبوابة. استخدمها كطبيب يستخدم أدواته: الأداة الصحيحة في الوقت الصحيح، بدليل `file:line` و`exit code` (Law 4).
