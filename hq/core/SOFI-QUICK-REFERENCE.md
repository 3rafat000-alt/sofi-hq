# SOFI Quick Reference — مرجع سريع موحّد

> **الهدف:** خريطة قرار واحدة تمنع التشتت والهلوسة — كل قانون/بروتوكول/معيار في سطر واحد، مع المرجع الحقيقي `file:line`. التفاصيل الكاملة في المرجع المذكور — هذا الملف للسرعة فقط.
> **المصدر:** `AGENTS.md:1` + `hq/core/protocols.md:1` + `hq/core/system-state-current.md:1` + `hq/core/nexus/registry.yaml:1`
> **التحديث:** مع كل تغيير مصيري — مسؤول الصيانة: `knw-lead` (T4) + `gtw-dispatcher` (T0)

---

## 1. خريطة القرار — أي قانون أستخدم متى؟

| سؤالك | القانون/البروتوكول | المرجع | ماذا تفعل |
|-------|-------------------|--------|-----------|
| **وصل طلب جديد من المالك/المستخدم؟** | Law 1 + P-01.8 | `AGENTS.md:10` + `hq/core/protocols.md:19` | يبدأ عند `gtw-intake-reformer` → تصنيف Fast/Standard/Fateful → توجيه |
| **طلب غامض >20%؟** | Law 16 + P-01.10 | `AGENTS.md:90` + `hq/core/protocols.md:28` | 1–3 أسئلة حادة + مهلة 24h → بلا إجابة = تصعيد لـ `brd-arbiter` (24h أخرى) — max جولتان |
| **هل أخاطب غرفة أخرى؟** | Law 2 | `AGENTS.md:23` | لا — فقط عبر `context-map.yaml:11` وحافلة التذاكر JSON |
| **هل أسلم للمالك مباشرة؟** | Law 3 + P-02 | `AGENTS.md:26` + `hq/core/protocols.md` P-02 | لا — `agent → lead → brd-ceo → user` — JSON ≤280 حرف |
| **هل أسلم بلا دليل؟** | Law 4 + P-03 | `AGENTS.md:32` + `.opencode/skills/sofi-evidence/SKILL.md` | مرفوض — كل تغيير `file:line` + كل أمر `exit code` |
| **هل أنفذ بلا RCCF؟** | Law 5 | `AGENTS.md:35` | مرفوض — Request→Clarify→Confirm→Fullfil |
| **قرار مصيري (مال/أمن/معمارية)؟** | Law 6 + P-01.8 Fateful | `AGENTS.md:38` | CEO يستشير Board (`brd-*`) + حق نقض `brd-cso` |
| **أين أسجل القرار؟** | Law 7 | `AGENTS.md:42` | مؤسسي `hq/brain/` (CORTEX/HIPPOCAMPUS/AMYGDALA) منفصل عن مشروعي `projects/<slug>/brain/` |
| **هل أسلم بلا مراجعة؟** | Law 8 | `AGENTS.md:49` | مرفوض — لا تسليم بلا مراجعة ولا مراجعة بلا دليل |
| **من المسؤول؟** | Law 9 | `AGENTS.md:52` | الوكيل → الـ lead → الـ CEO → إيقاف المنظومة |
| **أين أعمل؟** | Law 10 | `AGENTS.md:55` | على `main` فقط — فروع مؤقتة ≤72h بصندوق عزل ثم دمج |
| **كيف أخاطب المالك؟** | Law 11 | `AGENTS.md:59` | عربي مبسّط يشرح *لماذا يهمه* — `brd-ceo` و Fast-track ملزمان |
| **هل السجل يطابق القرص؟** | Law 12 | `AGENTS.md:62` | `registry.yaml` = 14 غرفة · 111 وكيلاً — `registry_guard.py:1` يفشل بصخب إن اختلف |
| **هل أعمل بعشوائية؟** | Law 13 | `AGENTS.md:65` | ممنوع — محرك ثلاثي + شجرة `TODO/Phase-NN` + ترويسة `## FILE: <path>` + kebab-case |
| **رُفضت مرتين لنفس السبب؟** | Law 14 | `AGENTS.md:74` | تجميد فوري + تصعيد لـ `brd-arbiter` خلال 24h — حكمه ملزم |
| **هل أضيف مكتبة؟** | Law 15 | `AGENTS.md:82` | لا دمج بلا `sec-license-auditor` — مسموح MIT/Apache/BSD/ISC/MPL — محظور GPL/AGPL/SSPL |
| **هل الطلب غامض؟** | Law 16 | `AGENTS.md:90` | >20% = توقف + 1–3 أسئلة + 24h → تصعيد |

---

## 2. مخطط التدفق البسيط — من الطلب إلى التسليم

```
المالك يكتب (عربي/إنجليزي/مختلط)
        ↓
gtw-intake-reformer (14) — يفهم + يعيد الصياغة 5 أقسام + يفحص الغموض والميزانية والتعارض
        ↓
P-01.8 يصنف: 🟢Fast (read/ملف واحد قابل للعكس) | 🟡Standard (ميزة 1–2 غرف) | 🔴Fateful (مال/أمن/مخطط/إنتاج)
        ↓
Fast → lead واحد → تسليم  |  Standard/Fateful → brd-ceo (00) → يستشير Board إن مصيري
        ↓
T1 Paper: 01-strategy (PRD) → 02-research (JTBD/رحلات) → 04-architecture (ERD ورقي + OpenAPI مجمد) ‖ 03-design (UX + DFR)
        ↓ DFR: توقيع sec-lead + qa-lead قبل أي سطر كود
T2 Code: 05-backend وحده (S4 حي + مفحوص) → 06-frontend ‖ 07-mobile (S5 Flutter/Dart معاً على العقد المجمّد)
        ↓
T3 Shield: 09-security (STRIDE) · 10-quality (22/28/20 نقطة) · 11-devops (نشر + تراجع) · 12-observability (SLO)
        ↓
T4 Memory: 13-knowledge يسجل في CORTEX/HIPPOCAMPUS/AMYGDALA
        ↓
brd-ceo يسلم للمالك عربياً مبسطاً
```

---

## 3. قائمة المصطلحات المختصرة

| المصطلح | المعنى | المرجع |
|---------|--------|--------|
| **RCCF** | Request→Clarify→Confirm→Fullfil — أمر العمل الإلزامي | `AGENTS.md:35` |
| **DFR** | Design-Freeze Review — تجميد التصميم (توقيع 09+10 نهاية S3) | `hq/core/nexus/gates.yaml:1` |
| **Capsule** | مجلد الوكيل `hq/core/domain/rooms/<room>/agents/<name>/{capabilities,senses,memory}.yaml` | `hq/core/domain/context-map.yaml:11` |
| **ADR/SES** | سجل قرار (CORTEX) / سجل جلسة (HIPPOCAMPUS) | `hq/brain/cortex-decisions.md:1` |
| **Stack Lock R3** | React 18+ حصري (06) · Laravel 11+ حصري (05) · Flutter 3.22+ حصري (07) | `AGENTS.md` §Stack Lock |
| **S1→S6** | الفكرة→البيانات/العقد→التجربة→الخلفية الحية→الواجهتان→الدرع | `hq/core/nexus/pipeline.yaml:8` |
| **G0→G8** | بوابات العبور — G0 تصنيف · G3 ERD · DFR · G5 جودة · G8 توثيق | `hq/core/nexus/gates.yaml:1` |
| **MCP** | Model Context Protocol — خادم أدوات (27 خادماً — 100% محلي) | `hq/core/nexus/mcp-routing.yaml:13` |

---

## 4. الأعداد الملزمة الآن (R3.1 + Phase B — 2026-09-05)

- **17 غرفة** · **121 وكيلاً** · **116 مهارة على القرص** · **26 معياراً** · **9 بوابات + DFR** · **17 بروتوكولاً** · **10 عقود**
- **الحراس:** `registry_guard --strict` PASS · `count_sync` PASS · `evidence_guard hq/core --strict` 0 broken · `gitleaks` no leaks

---

## 5. متى أستخدم أي مهارة؟

| أريد أن... | المهارة | الغرفة |
|------------|---------|--------|
| أبني ميزة خلفية | `bck-feature-build` | 05 |
| أبني مكون React | `fnt-component-build` | 06 |
| أبني ميزة Flutter | `mob-feature-build` | 07 |
| أراجع جودة Flutter | `qa-flutter-architect` | 10 |
| أراجع React/DDD | `qa-react-architect` | 10 |
| أراجع Laravel/DDD | `qa-laravel-architect` | 10 |
| أمرر DFR | `sec-threat-model` + `qa-test-plan` | 09+10 |
| أنشر | `ops-deploy-runbook` | 11 |
| أسجل قراراً | `knw-brain-write` | 13 |

---

> **القاعدة الذهبية:** إذا احترت — اسأل البوابة (14) — لا تجتهد. الشك يصعد، لا يهبط.
