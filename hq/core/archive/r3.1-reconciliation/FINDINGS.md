# FINDINGS — تحليل الحالة الفعلية قبل التسوية (Baseline & Drift)

> **FILE:** hq/core/archive/r3.1-reconciliation/FINDINGS.md
> **Owner:** knw-lead · **Date:** 2026-09-05 · **Phase:** A (RCCF من brd-ceo)
> **Method:** فحص القرص + السجل + الأدوات — كل رقم موثَّق بأمر تحقق. **كُتب قبل أي تعديل.**

---

## 1) خط الأساس (Baseline hashes — قبل أي تعديل)

- `hq/core/tooling/registry_guard.py` → `90dd04e706544f3b93afe06ff8f914eb50887012b8312a900042c73e86bf3224`
- `hq/core/tooling/count_sync.py` → `8af141e8694941ca1bac1de95bad4fee20b9590a45b4d5e4e3ba6bf06d16e671`
- `hq/core/tooling/evidence_guard.py` → `5e275e81fc00b21168399796740664894f09a1bdbcb5ec812448bb37cfac0da4`
- `hq/core/tooling/port-agents.mjs` → `ee796089111226b6d65800253906196a4a8c9fc5c38723036471b804c53ec275`
- `hq/core/nexus/registry.yaml` → `6f5a87664adcfcbb1901bcc69e3db575e802340701cb04f436227f880c052160`
- `AGENTS.md` → `ab75d2e2fa4986d9ee0dcc128e110ce73c8252978863c2fd8aedcfbc550b0506`
- `hq/core/system-state-current.md` → `11d7d81199ffecf0afaacd9a1fd7836f2c516ddfd83e7cbb862f856f976e14b1`

## 2) الانجراف المكتشف — الوكلاء (الواقع ≠ افتراض أمر العمل "6 ملفات زائدة")

**القرص: 115 ملف `.opencode/agent/*.md` (114 متتبَّعاً + 1 غير متتبَّع) مقابل السجل: 108 وكيلاً.**

### أ) 12 ملفاً متتبَّعاً على القرص وغير مسجَّلة في R3.1:
| الملف | الحالة | التصنيف |
|-------|--------|---------|
| `dat-lead` | غرفة 08 دُمجت في 04 (R3.1) — لا دور dat-lead في السجل | **أرشفة** (بلا غموض) |
| `dat-db-engineer` | مقابل مسجَّل ناقص: `arc-db-engineer` | **غموض → brd-ceo** |
| `dat-cache-engineer` | مقابل مسجَّل ناقص: `arc-cache-engineer` | **غموض → brd-ceo** |
| `dat-etl-engineer` | مقابل مسجَّل ناقص: `arc-etl-engineer` | **غموض → brd-ceo** |
| `dat-analytics-engineer` | مقابل مسجَّل ناقص: `arc-analytics-engineer` | **غموض → brd-ceo** |
| `dat-ml-engineer` | مقابل مسجَّل ناقص: `arc-ml-engineer` | **غموض → brd-ceo** |
| `dat-privacy-officer` | مقابل مسجَّل ناقص: `arc-privacy-officer` | **غموض → brd-ceo** |
| `dsn-content-strategist` | ليس في سجل R3.1 (غرفة 03 بها 8 وكلاء فقط) | **أرشفة** (بلا غموض) |
| `dsn-motion-designer` | ليس في سجل R3.1 | **أرشفة** (بلا غموض) |
| `fnt-vue-engineer` | Vue محظور تماماً في Stack Lock R3.1 | **أرشفة** (بلا غموض) |
| `res-data-researcher` | ليس في سجل R3.1 (غرفة 02 بها 6 وكلاء فقط) | **أرشفة** (بلا غموض) |
| `res-web-scout` | ليس في سجل R3.1 | **أرشفة** (بلا غموض) |

### ب) ملف واحد غير متتبَّع (غير مسجَّل):
| الملف | الحالة | التصنيف |
|-------|--------|---------|
| `qa-flutter-architect` (11820 B · mtime 2026-09-05 00:45) | أنشأته جلسة موازية بعد أمر العمل — قيد صريح: لا يُسجَّل هذه المرحلة (بانتظار تسليم qa-lead → المرحلة B). مهارة `qa-flutter-architect/` (00:46) موجودة أيضاً على القرص خارج INDEX | **أرشفة معلّقة** (لا حذف) |

### ج) 6 وكلاء مسجَّلين في R3.1 **ناقصة ملفاتهم** من القرص:
- `arc-db-engineer` · `arc-cache-engineer` · `arc-etl-engineer` · `arc-analytics-engineer` · `arc-ml-engineer` · `arc-privacy-officer`
- السبب: R3.1 أعاد تسمية dat-* → arc-* في السجل لكن الملفات الفيزيائية لم تُهاجر.
- **السبيل الوحيد للوصول إلى 108=108 دون تأليف محتوى (مُحرَّم): إعادة تسمية محافظة (git mv) dat-* → arc-* بتطابق 1:1.**

## 3) انجرافات موازية (خارج نطاق التعديل — توثيق فقط)

| البند | الحالة الفعلية | المرجع/الإدعاء | الحكم |
|-------|---------------|----------------|-------|
| السجل | 14 غرفة · 108 وكيل (قائمة rooms) | registry.yaml R3.1 | مصدر الحقيقة |
| AGENTS.md | 14 غرفة · 108 وكيل (R3.1) | مكتوب في شجرة العمل (غير ملتزم) | لا يُعدَّل (المرحلة B) |
| system-state-current.md | **قديم**: سطر 22 "114 agents and 109 skills" · سطر 42 "15 rooms · 114 agents" | ادعاءات 15/114/109 | لا يُعدَّل — توثيق الحاجة (المرحلة B) |
| الكبسولات | 114 دليلاً: 04-architecture/agents فيه 9 arc-* فقط (تنقص 6) · 08-data فيها 7 dat-* · 08-data كغرفة ما زالت فيزيائياً | registry: 04 = 15 وكيلاً | هجرة 08→04 فيزيائياً = المرحلة B / أصحاب الغرف → الحارس يحذّر لا يفشل |
| المهارات | 111 دليلاً (SKILL.md) على القرص | INDEX.md: سطر 6 يزعم 109/109 · روابط فريدة = 110 · SKILLS-ASSIGNMENT.md ترويسة "106 skills" | عَدّ حقيقي 111 (غير مستقر حيّاً: 110→111 أثناء الجلسة) — الحارس يطبع ويحذّر لا يفشل |
| git | 193 ملفاً معدَّلاً (منها 5 ملفات .opencode/agent من جلسة موازية: arc-infra-architect · gtw-intake-reformer · ops-cloud-engineer · ops-sandbox-executor · sec-secrets-warden) · .kilo/agent/*.md معدَّلة · docker deleted · privileges-required.sh معدَّل | registry.yaml + AGENTS.md تعديلات R3.1 غير ملتزمة | خارج صلاحية هذه المرحلة |

## 4) أعطال الحُرّاس الثلاثة (موثَّقة بسطر)

1. **registry_guard.py** — سطر 20: `re.match(r'\s+"(\d+-.+?)":', line)` يتوقع قاموساً؛ مع مخطط R3.1 (قائمة `- code:`) لا يُرصَد أي room → "0 rooms". ثوابت `114` مثبّتة في ≈ الأسطر 73-74 (agents check) و130 و137 (capsules + رسالة النجاح). رسالة النجاح: "PASS: registry valid: X rooms, 114 agents". فحص الكبسولات يبحث في `hq/core/domain/rooms/<key>/agents/` (سليم) لكنه سيفشل بسبب 6 كبسولات arc-* ناقصة.
2. **count_sync.py** — سطر ~57: `reg.get("rooms", {}).values()` → `AttributeError: 'list' object has no attribute 'values'` على مخطط R3.1. ثوابت: 15 غرفة · 114 وكيل · 109 مهارات. يفحص AGENTS.md ("15 rooms · 114 agents") وsystem-state (يتوقع 114) وINDEX (109) وport-agents.mjs.
3. **port-agents.mjs** (مذكور في count_sync) — سطر 12-13: `EXPECTED = registryText.match(/\b(\d+) agents\b/)` لا يطابق "108 active agents" → يرمي خطأ "agent counter not found".
4. **evidence_guard.py** — لا عطل؛ استشاري افتراضياً (exit 0 بدون --strict)؛ SKIP_DIRS = {node_modules, .git, .venv, vendor, backups, .kilo, dist, build, .dart_tool} — لا يتضمن "archive" (ملفات الأرشيف تعالج كملفات عادية عند فحصها).

## 5) أرشيف العملية (الوجهة المقترحة)

`hq/core/archive/r3.1-reconciliation/`
- `agents/` — الملفات المؤرشفة (محتوى محفوظ كما هو، لا حذف)
- `MANIFEST.md` + `MANIFEST.sha256` — sha256 لكل ملف + القرار + السبب
- `RESTORE.md` — إرشادات الاستعادة (git mv عكسي)
- `CHECKLIST-C2.md` · `FINDINGS.md` — سجل هذه العملية
- ملاحظة: نمط أرشيف البيت الرسمي = مجلد شقيق خارج الجذر (SOFI-archive-*)؛ هذا الأرشيف داخل الجذر بقرار عملي لمراجعة brd-ceo، والانتقال للنمط الرسمي = المرحلة B إذا قرر النظام.

## 6) التصعيد المطلوب من brd-ceo (3 نقاط قرار)

1. **الأزواج الستة dat-* ↔ arc-***: اعتماد إعادة التسمية المحافظة (git mv) كـ"تسجيل للملف الفيزيائي تحت الاسم الأساسي R3.1" — التوصية: **نعم** (البديل: أرشفة dat-* وترك arc-* بلا ملف = استحالة 108=108 في هذه المرحلة).
2. **أرشفة**: 5 ملفات متقاعدة (dsn-content-strategist · dsn-motion-designer · fnt-vue-engineer · res-data-researcher · res-web-scout) + dat-lead + qa-flutter-architect (معلّقة للمرحلة B) → `hq/core/archive/r3.1-reconciliation/agents/`.
3. **كبسولات/هجرة 08→04 الفيزيائية + مهارات/وثائق**: المرحلة B — الحارس يحذّر (WARN) ولا يفشل في هذه المرحلة.