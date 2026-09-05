# CORTEX — سجل القرارات المصيرية (Law 7 — Organization Memory)
# FILE: hq/brain/cortex-decisions.md
# أعيد إنشاؤه 2026-08-26 بعد الأرشفة حسب hq/core/system-state-current.md:30

## ADR-20260826-001 — إصلاح النواقص الأربعة لمؤسسة SOFI (مصيري 🔴)
- محتفظ به — المرجع الأصلي غير مرتبط بصك

## ADR-20260831-RESET-SAKK — تنظيف كامل لذاكرة صك بأمر مالك مباشر
- **التاريخ:** 2026-08-31
- **الأمر:** تنظيف من الجذر + الذواكر + التذاكر + كل ملفات .md الخاصة بصك — بداية نظيفة
- **الإجراء:** حذف كل ملفات brain/*.md (67) + docs/*.md (112) + brain subfolders (26) + backend/brain (1) — إبقاء CONTEXT.md فقط (PRD v2.0 — 273 سطر)
- **الذاكرة المؤسسية:** أرشفة cortex (1029 سطر) و hippo (2061 سطر) إلى /tmp — إعادة تهيئة من الصفر
- **التذاكر:** 40 تذكرة مفتوحة مؤرشفة للمراجعة — لا حذف عشوائي (Law 7)
- **النتيجة:** المشروع الآن يبدأ من S1 بملف PRD واحد فقط — لا كود قبل ERD+OpenAPI مجمدين

## ADR-20260831-9AXIS-FIX — إصلاح المحاور التسعة الجذري لمستودع SOFI-HQ (مصيري 🔴)
- **التاريخ:** 2026-08-31 · **المرجع الدستوري:** AGENTS.md:10 (16 قانوناً) + hq/core/system-state-current.md:1 + hq/core/nexus/registry.yaml:1 (15 غرفة · 114 وكيلاً)
- **التصنيف:** مصيري — يمس المعمارية والأمن والامتثال والتوثيق والذاكرة — مسار: gtw-intake-reformer → brd-ceo → كل الغرف (00-14) عبر البوابة (Law 1 proportional flow — لا تجاوز للبوابة = L4)
- **المحفز:** تقرير 9 محاور (2026-08-31) كشف مخاطر حرجة: بيروقراطية مسارات متوسطة، تضخم سياق 114 وكيلاً، نقاط فشل symlink، شلل تحليلي بحلقة التوضيح بلا timeout، اختناق brd-ceo، هلوسة file:line بلا خطاف آلي، sudo واسع في النشر، ذاكرة مؤرشفة بلا تلخيص، توثيق 109 skills بلا فهرس آلي.
- **القرارات (9 محاور — كلها منفذة على الشجرة الرئيسية حصراً Law 10):**
  - **المحور 1 — المعمارية والهيكل (Law 12):** أتمتة فحص Registry في Gate-0 — `hq/core/tooling/registry_guard.py:1` (15 غرفة · 114 وكيلاً + capsules) + `hq/core/tooling/count_sync.py:1` (114 agents · 109 skills · 16 laws) + `node hq/core/tooling/port-agents.mjs:6` (قراءة EXPECTED ديناميكياً من registry.yaml). Gate-0: `hq/core/gate_checklists/gate-0.md:29` (3 checks إلزامية ب-exit code).
  - **المحور 2 — نقاط التكامل (Law 13):** إزالة symlink المتبقي `caddy → hq/engine` (كان نقطة فشل أحادية) — التحقق `ls -l caddy` = not found (exit 2). Canon الآن `hq/engine/Caddyfile` مستورد مباشرة عبر `hq/engine/scripts/bootstrap-live.sh:6` (كتابة /etc/caddy/Caddyfile الوحيدة بصلاحية جذر).
  - **المحور 3 — الوظائف الجوهرية / حلقة التوضيح (Law 16):** إضافة timeout 24 ساعة + anti-paralysis (max 2 جولات) عبر `hq/core/protocols.md:28` (P-01.10) + `hq/core/domain/rooms/14-gateway/charter.md:85` + `.opencode/agent/gtw-intake-reformer.md:252` (Annex LAW-16 amended 2026-08-31). بعد 24h بلا جواب → تصعيد تلقائي إلى `brd-arbiter` (24h نافذة ملزمة — Law 14).
  - **المحور 4 — التواصل بين المكونات (Law 1):** تفويض Fast Track كاملاً إلى Room Lead مع تدقيق لاحق — `hq/core/protocols.md:19` (P-01.8 amended: gateway auto-authorize + gtw-dispatcher weekly post-audit إلى brd-ceo) + `hq/core/domain/rooms/14-gateway/charter.md:87` — يزيل اختناق brd-ceo في S1 للعمل البسيط القابل للعكس.
  - **المحور 5 — مخاطر الهلوسة والموثوقية (Law 4/13):** خطاف تحقق آلي `hq/core/tooling/evidence_guard.py:1` (يفحص كل file:line ويتحقق من وجود الملف + رقم السطر) — مدمج في Gate-0 (`hq/core/gate_checklists/gate-0.md:31`) + Gate-5/DFR + pre-commit hook (`hq/core/tooling/hooks/pre-commit:32`).
  - **المحور 6 — الجوانب التشغيلية (Least Privilege):** تشديد `hq/engine/scripts/bootstrap-live.sh:10` (فحص EUID + إزالة symlink المتبقي + تفضيل caddy reload عبر admin API بلا sudo) + `hq/engine/scripts/validate.sh:1` (read-only بلا sudo) + `hq/engine/scripts/deploy.sh:7` (admin-API أولاً ثم sudo fallback) + بديل `ops-sandbox-executor` للحاويات.
  - **المحور 7 — الأمن والامتثال (Law 15 + P-08.1):** فرض `gitleaks` كـ pre-commit hook إلزامي — `gitleaks.toml:1` (allowlist vendor/node_modules/.git/skills) + `hq/core/tooling/hooks/pre-commit:12` (gitleaks git --staged --pre-commit) + `hq/core/tooling/hooks/install.sh:1` — يمنع أي secret في الكود (=L4). تذكير Law 15 على تغير manifests (composer/pubspec/package.json).
  - **المحور 8 — الأداء وقابلية التوسع (P-06.7):** طقس تلخيص ذاكرة دوري عبر knw-reflector — `hq/core/tooling/memory_summarizer.py:1` (hippocampus >800 أو amygdala >600 → احتفاظ بآخر 5 جلسات كاملة + تلخيص الأقدم + إزالة تكرار تصعيد التذاكر + نسخ .bak) + `hq/core/domain/rooms/13-knowledge/charter.md:86` (P-06.7 ritual كل 10 turns + Gate-8).
  - **المحور 9 — التوثيق وقابلية الصيانة (Law 13):** أتمتة فهرس الروابط عبر knw-doc-writer في Gate-6 — `hq/core/gate_checklists/gate-6.md:26` (law13_path_guard.py + evidence_guard.py على hq/core ب-exit code) + `hq/core/domain/rooms/13-knowledge/charter.md:91` + تحديث `.opencode/skills/INDEX.md:4` (106/106 → 109/109) و `.opencode/skills/` 109 skills.
- **الدليل (Law 4 — Evidence Required — كل ادعاء بـ file:line + exit code):**
  - `python3 hq/core/tooling/registry_guard.py --strict` → "114/114 agents · capsules OK" exit 0 (hq/core/tooling/registry_guard.py:1)
  - `python3 hq/core/tooling/count_sync.py` → "CLAIMS OK" 114 agents · 109 skills · 16 laws exit 0 (hq/core/tooling/count_sync.py:1)
  - `python3 hq/core/tooling/evidence_guard.py hq/core --strict` → "0 broken file:line" exit 0 (hq/core/tooling/evidence_guard.py:1)
  - `gitleaks git --staged --pre-commit --config gitleaks.toml` → "no leaks found" exit 0 (gitleaks 8.30.1)
  - `bash hq/engine/scripts/validate.sh` → "✓ Caddyfile canon sound" exit 0 + "✓ live Caddyfile sound" + "✓ sakk.conf syntax sound" (hq/engine/scripts/validate.sh:6)
  - `bash .git/hooks/pre-commit` → "pre-commit PASS — all SOFI guards green" exit 0 (hq/core/tooling/hooks/pre-commit:1)
  - `ls -l caddy` → "No such file or directory" exit 2 (symlink removed — system-state-current.md:17)
  - `ls .opencode/agent | wc -l` = 114 · `ls .opencode/skills/*/SKILL.md | wc -l` = 109
- **الذاكرة (Law 7):** هذا ADR سجل هنا في CORTEX + الجلسة في `hq/brain/hippocampus-sessions.md` + الحوادث في `hq/brain/amygdala-incidents.md` (إن وجدت) — الذاكرة المؤسسية والذاكرة المشروعية معزولتان تماماً (لا كتابة لمشروع في ذاكرة المؤسسة إلا بقرار brd-ceo).
- **التراجع:** كل تغيير يملك .bak أو git diff قابل للعكس — إزالة hook: `rm .git/hooks/pre-commit` — إلغاء registry guard: إزالة الفقرة من gate-0.md — إلغاء timeout: إزالة P-01.10 من protocols.md — الاستعادة الكاملة: `git restore` للملفات التسعة.
- **المصادقة:** DFR غير مطلوب هنا (لا كود مشروع sakk — هذه إصلاحات حوكمة hq/ فقط). التنفيذ على الشجرة الرئيسية مباشرة (Law 10) — لا worktree — التحقق `git worktree list` = bare only.

## ADR-20260831-SAKK-DOUBLE-VERIFY — تعارض حوكمة + إعادة تحقق شامل ثانٍ لمنظومة SAKK (مصيري 🔴)
- **التاريخ:** 2026-08-31 · **البوابة:** gtw-intake-reformer (Law 1) → **brd-ceo** · **المصدر:** مدخل مالك + توضيح محسوم (intake_id SAKK-INT-002)
- **تعارض حوكمي حُسم (توجيه مالك):** `ADR-20260831-RESET-SAKK` (أعلن "من س1 بلا كود") يتعارض مع الشجرة الحية الواقعية — التحقق الميداني يُثبت أن SAKK قرب الإنتاج: 16 Domain (`backend/app/Domains/*`)، 45+ هجرة (`backend/database/migrations`)، **1309 اختباراً في cache** (`backend/.phpunit.result.cache`) + Feature/Unit wings، 22 Feature موبايل (`mobile/lib/features`)، 28 صفحة React إدارية (`apps/admin/src/pages`). **القرار: الشجرة الحية هي الحقيقة — نواصل عليها**، ويُلحق هذا التصحيح لـ RESET-SAKK (المرجع الأصلي لا يُحرَّر — Law 13 يكمل عبر ملحق).
- **تصحيح افتراض مدخل:** الويب (اللوحة/الموقع/البوابة) **React 19 + Vite** وليس Flutter — `projects/sakk/brain/CONTEXT.md:12` ("Mobile Flutter — Web React+Vite") — الموكّل: "الواقع الموجود صحيح" — لا إعادة بناء.
- **طلب المالك النهائي (إجابة حرة):** "لكل النواحي والجوانب وكل شيئ بالكامل" = **تحقق جراحي شامل ثانٍ مستقل (double-pass) 360°** يجري على الواقع الراهن (باك + داتا + تطبيق Flutter + لوحة/موقع/بوابة React + برمجة + API/Envelope/OpenAPI + ربط E2E)، يغلق مخاطر الجراحة الأولى المفتوحة (`handoff.md:60-64`: Fee/FeeSchedule، HasSoftDeletes المتبقي، golden 1 فشل، تعديلات غير committed) ويُثبت انحداري أخضر 100% بلا كسر توافق عكسي.
- **مقاييس إلزامية:** تكرار <2% · تغطية ≥85% · انحداري 100% · ثلاثية هجرات خضراء · p95 بلا تدهور >10% · 60fps · حجم ≤5% · 8 تواقيع جراحية محدثة قبل أي كود (INT-0004) · As-Is موثق file:line + لقطة لكل تغيير.
- **الدليل (Law 4):** `projects/sakk/brain/edit-full-audit-intake.md:1` (Intake Report خمسة أقسام) + `hq/brain/evidence/surgical-review-full-2026-09-01.md` (8 تواقيع) + `backend/.phpunit.result.cache` (1309) + `apps/admin/package.json` (React 19) + `mobile/pubspec.yaml` (flutter) + `git log` (DDD-P0..P5, RB-T25, W2 AM-01).
- **الذاكرة (Law 7):** CORTEX هذا الـADR + الجلسة `hq/brain/hippocampus-sessions.md:SES-20260831-SAFF-INT-REOPEN` + لا حادثة أميغدالا — الذاكرتان معزولتان.
- **التراجع:** إلغاء double-pass = شطب هذا الـADR + إيقاف أوامر التنفيذ — كل تغيير يملك git diff قابل للعكس.
- [2026-08-31 16:10 UTC] [boardroom] [اجتماع] قرار حوكمي — تبني ADR-20260831-SAKK-DOUBLE-VERIFY — تبني ADR-20260831-SAKK-DOUBLE-VERIFY كسجل حوكمة نهائي — الشجرة الحية هي الحقيقة والمصدر الوحيد للعمل — evidence: ADR-20260831-SAKK-DOUBLE-VERIFY logged in CORTEX | Meeting #3 closed | Owner order Ticket #351 documented | Prompt file: projects/sakk/brain/surgical-review-2-prompt.md
- [2026-08-31 16:10 UTC] [boardroom] [اجتماع] قرار حوكمي — تبني ADR-20260831-SAKK-DOUBLE-VERIFY — إلغاء ADR-20260831-RESET-SAKK (الذي أعلن عن البدء من الصفر بلا كود) — متعارض مع الواقع الحي قرب الإنتاج — evidence: ADR-20260831-SAKK-DOUBLE-VERIFY logged in CORTEX | Meeting #3 closed | Owner order Ticket #351 documented | Prompt file: projects/sakk/brain/surgical-review-2-prompt.md
- [2026-08-31 16:10 UTC] [boardroom] [اجتماع] قرار حوكمي — تبني ADR-20260831-SAKK-DOUBLE-VERIFY — تفويض التحقق الجراحي الشامل الثاني (edit-full-audit-2) عبر وكيل فرعي (general sub-agent) بموجب Ticket #351 — evidence: ADR-20260831-SAKK-DOUBLE-VERIFY logged in CORTEX | Meeting #3 closed | Owner order Ticket #351 documented | Prompt file: projects/sakk/brain/surgical-review-2-prompt.md
- [2026-08-31 16:10 UTC] [boardroom] [اجتماع] قرار حوكمي — تبني ADR-20260831-SAKK-DOUBLE-VERIFY — لا سطر كود قبل توقيع 8 قادة على مخرجات التحقق الجراحي الثاني (INT-0004 — الدورة الثانية) — evidence: ADR-20260831-SAKK-DOUBLE-VERIFY logged in CORTEX | Meeting #3 closed | Owner order Ticket #351 documented | Prompt file: projects/sakk/brain/surgical-review-2-prompt.md
- [2026-08-31 16:10 UTC] [boardroom] [اجتماع] قرار حوكمي — تبني ADR-20260831-SAKK-DOUBLE-VERIFY — الowner هو مصدر القرار الأخير — أي تعارض يُحسم بأمره المباشر — evidence: ADR-20260831-SAKK-DOUBLE-VERIFY logged in CORTEX | Meeting #3 closed | Owner order Ticket #351 documented | Prompt file: projects/sakk/brain/surgical-review-2-prompt.md
- [2026-08-31] [boardroom] [تحديث حالة] **جاهزية التحقق الجراحي الثاني (double-pass) اكتملت على مستوى الوثائق الثلاث** — لا تنفيذ بعد — evidence: `projects/sakk/brain/edit-full-audit-2-as-is.md:1` (تشخيص As-Is 10 أقسام، 50+ شاهد) + `projects/sakk/brain/edit-full-audit-2-impact-map.md:1` (مصفوفة مخاطر + 10 قرارات D1-D10) + `projects/sakk/brain/edit-full-audit-2-diff-design.md:1` (24 صفاً جراحياً B1-B24 قبل/بعد+اختبار) — مبنية على 4 تقارير تدقيق فعلية على القرص (Area4/Area5-6/Area7-8/Area9) — بوابة التوقيع العليا: `hq/brain/evidence/surgical-review-2-2026-09-01.md:1` (8 تواقيع بانتظار القادة INT-0004) — القرار: **لا سطر كود قبل 8 تواقيع خضراء** — أولوية التنفيذ: P0 حوكمة git (B24، 1035 مدخلاً غير ملتزم) ← P1 أمان (B10-B13) ← P2 DDD/باك ← P3 ربط/عقد ← P5 Flutter ← P6 داتا ← P7 جودة — الحالة القراءة-فقط (لا ملف كود مُعدَّل في هذه الجلسة).

## ADR-20260831-VISUAL-DIAGRAMS — الطبقة المرئية الحاكمة SOFI-HQ-INT-007 (تحسين توثيقي + UX — مصيري 🟡)
- **التاريخ:** 2026-09-01 · **intake_id:** SOFI-HQ-INT-007 · **المصدر:** `projects/sofi-hq/brain/edit-visual-diagrams-2026-08-31.md:1` (برومبت جراحي 13 قسماً ≥5200 كلمة) · **الغرفة المالكة:** 03 Design (`dsn-lead`) + 13 Knowledge (`knw-lead`) — يُستشار 09 Security (`sec-lead`) + 10 Quality (`qa-lead`) · **المسار:** gtw-intake-reformer → brd-ceo → dsn-lead/knw-lead (STANDARD — feature 1–2 غرف) — Law 1 Proportional Flow
- **التصنيف:** تحسين توثيقي + UX — مصيري أصفر STANDARD — لا يمس YAML/registry/pipeline/Caddyfile/projects/sakk — طبقة اختيارية فوق نص متفوق — توافق عكسي 100% — قابل للعكس `git revert`
- **المشكلة/الفرصة:** الحوكمة النصية متفوقة (16 قانوناً، 15 غرفة، 114 وكيلاً، S1→S6، YAML شاملة، ASCII معمارية) لكنها **غير مرئية** — مطور جديد يحتاج قراءة 400 سطر ليفهم المؤسسة، بينما 9 صور تحقق نفس الفهم في 5 دقائق وتُحمل في عرض تقديمي للمالك/المراجع/المطور الجديد — الفجوة: 0 ملف `*.mmd` في `hq/` — 0 مجلد `diagrams/` — `ls -R` يؤكد الغياب — `hq/core/design/system-ddd-blueprint.md:1` بيت التصميم الحاكم بلا مرئيات
- **القرار (9 مخططات + 3 مبادئ مقفلة):**
  - **المبدأ 1 — لا نهدم المبنى لنصلح نافذة:** المساس `hq/core/design/diagrams/` + `docs/diagrams/` فقط — لا مس لـ `AGENTS.md:1` ولا `hq/core/nexus/registry.yaml:1` ولا `hq/core/nexus/pipeline.yaml:8` ولا `hq/engine/Caddyfile` ولا `projects/sakk/**` — المرئيات تقرأ YAML حرفياً
  - **المبدأ 2 — كل مخرج ببيت حقيقي Law 13:** كل ملف بترويسة `## FILE: <path>` — kebab-case — لا مسار وهمي — `hq/core/structure-standard.md:1` مرجع التسمية
  - **المبدأ 3 — توافق عكسي + انحداري أخضر:** النص يبقى مرجع الحقيقة — العملاء القدامى بلا المرئيات يعملون كما قبل — `python3 hq/core/tooling/registry_guard.py --strict` + `count_sync` + `evidence_guard` + `validate.sh` + `gitleaks` كلها exit 0 قبل التسليم — أي أحمر = `git revert`
  - **التسع صور الحاكمة:** D1 Use-Case (`hq/core/nexus/registry.yaml:6` → `hq/core/design/diagrams/d1-use-case.mmd:1`) — D2 Pipeline S1→S6 (`hq/core/nexus/pipeline.yaml:8`) — D3 Gateway Routing (`README.md:80` + `hq/core/domain/rooms/14-gateway/charter.md:86` P-01.10 timeout 24h) — D4 Layered Architecture (`hq/core/design/system-ddd-blueprint.md:42` 4 طبقات ASCII) — D5 Context-Map (`hq/core/domain/context-map.yaml:11` 15 عقدة) — D6 Gate State Machine (`hq/core/nexus/gates.yaml:1` G0→G8+DFR) — D7 Ticket-Bus Sequence (`AGENTS.md:40` agent→lead→ceo) — D8 Deployment Caddy (`hq/engine/Caddyfile` + `hq/engine/scripts/bootstrap-live.sh:6` canon) — D9 Memory Isolation (`AGENTS.md:44` Law 7)
  - **المواصفة الفنية المقفلة:** الأداة Mermaid CLI ^10.9.0 MIT (مجاني — License-check: allowed — `gitleaks.toml:1`) — الصيغ MMD مصدر + SVG (عرض) + PNG (شرائح ≤200KB) — SVG بـ `alt` + `aria-label` + تباين ≥4.5:1 + خط ≥18sp + RTL مرآة + `prefers-reduced-motion` 200ms — الهوية عنبي #6e1b2d بدل #1f0810 الممنوع — المجلد `hq/core/design/diagrams/` مصدر + `docs/diagrams/` مرآة
- **المخرجات (54 كياناً — كلها بترويسة FILE — `ls` exit 0):**
  - `hq/core/design/diagrams/README.md:1` (دليل المجلد — أمر التصدير `mmdc`) + 9 `*.mmd` (20-47 سطر كل) + 9 `*.svg` (≈5-7KB كل) + 9 `*.png` (≈20-23KB كل، ≤200KB) = 27 في `hq/` — `ls hq/core/design/diagrams/*.{mmd,svg,png} | wc -l` = 27 exit 0
  - `docs/diagrams/` مرآة 18 (9 svg + 9 png) — `ls docs/diagrams/*.{svg,png} | wc -l` = 18 exit 0 — الإجمالي 45 + 1 README = 46 ملف مرئي
  - `README.md` محدث (قسم Visual Diagrams — الخرائط المرئية + جدول 9 روابط + 3 معاينات inline) — `hq/core/design/system-ddd-blueprint.md` محدث (مربع ملاحظة بروابط تحت ASCII `hq/core/design/system-ddd-blueprint.md:42`) — لا حذف لسطر قائم — إضافة روابط فقط
  - `projects/sofi-hq/brain/edit-visual-diagrams-impact-map.md:1` (خريطة أثر داخل/خارج + 5 قرارات D1-D5 + تراجع 4 مستويات) + `projects/sofi-hq/brain/edit-visual-diagrams-diff-design.md:1` (9 صفوف D1-D9 قبل/بعد + اختبار) + `hq/brain/evidence/surgical-review-visual-2026-08-31.md:1` (4 تواقيع APPROVED dsn/knw/sec/qa قبل سطر `*.mmd`)
  - **إصلاح مرافق:** `hq/core/tooling/evidence_guard.py:24` + `hq/core/tooling/evidence_guard.py:59` — إصلاح bug `lstrip("./")` الذي كان يأكل النقطة من `.opencode/` ويُنتج 2 broken — بعد الإصلاح `evidence_guard hq/core --strict` → 0 broken exit 0 (كان 2 broken)
- **الدليل (Law 4 — كل ادعاء بـ file:line + exit code):**
  - `python3 hq/core/tooling/registry_guard.py --strict` → "114/114 agents · capsules OK" exit 0 — `hq/core/tooling/registry_guard.py:1`
  - `python3 hq/core/tooling/count_sync.py` → "CLAIMS OK 114/109/16" exit 0 — `hq/core/tooling/count_sync.py:1`
  - `python3 hq/core/tooling/evidence_guard.py hq/core --strict` → "0 broken" exit 0 — `hq/core/tooling/evidence_guard.py:1` (634→635 scanned بعد التعديل)
  - `python3 hq/core/tooling/evidence_guard.py hq/core/design/diagrams --strict` → "0 broken" exit 0 — `hq/core/design/diagrams/README.md:1`
  - `bash hq/engine/scripts/validate.sh` → "Caddyfile canon sound" exit 0 + "live Caddyfile sound" — `hq/engine/scripts/validate.sh:1`
  - `gitleaks git --staged --pre-commit --config gitleaks.toml` → "no leaks found" exit 0 — `gitleaks.toml:1` (gitleaks 8.30.1)
  - `bash .git/hooks/pre-commit` → "pre-commit PASS — all SOFI guards green" exit 0 — `hq/core/tooling/hooks/pre-commit:1`
  - `ls hq/core/design/diagrams/*.{mmd,svg,png} | wc -l` = 27 exit 0 + `ls docs/diagrams/*.{svg,png} | wc -l` = 18 exit 0 — `du -sh hq/core/design/diagrams` = 336K (≤5% من `hq` 7.0M) + كل PNG 20-23KB ≤200KB — `hq/core/design/diagrams/README.md:1`
  - كل SVG بـ `role="img" aria-label` + `<title>` + `<desc>` + `alt` في markdown — تباين ≥4.5:1 — خط ≥18sp — `prefers-reduced-motion` 200ms — Mermaid CLI MIT — License-check: allowed
- **الذاكرة (Law 7):** هذا ADR هنا في CORTEX + الجلسة `hq/brain/hippocampus-sessions.md:SES-20260901-VISUAL-DIAGRAMS` + لا حادثة AMYGDALA — الذاكرتان معزولتان — `knw-reflector` ritual كل 10 turns + SLA 24h لتحديث المرئي عند تغير YAML — `hq/core/structure-standard.md:1` خريطة قديم←جديد محفوظة
- **التراجع (4 مستويات):** `git revert <hash>` (54 كياناً) أو `rm -rf hq/core/design/diagrams docs/diagrams` + `git checkout -- README.md hq/core/design/system-ddd-blueprint.md` → `ls hq/core/design/diagrams` = exit 2 متوقع — `evidence_guard` أخضر — التراجع الذاكري = `git revert` لهذا الـADR + الجلسة — كل تغيير `.bak` أو `git diff` قابل للعكس
- **المصادقة:** التنفيذ على الشجرة الرئيسية حصراً `AGENTS.md:58` Law 10 — لا worktree — `git worktree list` = bare only — المراجعة الجراحية 4/4 APPROVED قبل سطر `*.mmd` (`hq/brain/evidence/surgical-review-visual-2026-08-31.md:1` — INT-0004) — DFR غير مطلوب (لا كود sakk — هذه طبقة توثيقية hq فقط)

---

## ADR-20260905-GTW-FLUTTER-QA-ARCHITECT — إضافة مهندس جودة فلاتر كتستير رسمي (أمر مالك)
- **date:** 2026-09-05
- **owner decision (this session):** institutionalize the owner's "Flutter Senior Technical Architect & QA Lead" methodology as an official tester in SOFI.
- **owner confirmed choices:** (1) home = Room 10 (Quality) · (2) form = full official agent + dedicated skill · (3) title = distinct (no "QA Lead" collision with qa-lead/Lama) + Arabic persona name.
- **gateway routing verdict:** PASS (gate) · WITHIN (budget) · conflicts RESOLVED · lane = FATEFUL (registry/architecture/operating layer — Law 12) · route_to = brd-ceo exclusively.
- **conflict resolution:** supersedes the 2026-08-26 "no test-engineer duplication" precedent by owner's explicit NEW order; differentiation = Flutter-domain end-to-end reviewer (architecture + perf + a11y + UX + QA methodology), distinct title, **no gate/verdict ownership** (qa-lead + brd-cqo unchanged).
- **Phase B execution (2026-09-05 · knw-lead):** agent restored `hq/core/archive/r3.1-reconciliation/agents/qa-flutter-architect.md` → `.opencode/agent/qa-flutter-architect.md:1` (sha256 قبل=بعد `31f62a09…`) · registry `hq/core/nexus/registry.yaml:209` · persona `hq/core/nexus/personas.yaml:354-357` (Rayan Al-Qadi — ريان القاضي) · capsule `hq/core/domain/rooms/10-quality/agents/qa-flutter-architect/capabilities.yaml:1` · skill `qa-flutter-architect` موجود على القرص (111 دليلاً).
- **evidence refs:** `hq/core/nexus/registry.yaml:11` · `hq/core/nexus/registry.yaml:209` · `hq/core/nexus/personas.yaml:354` · `hq/core/system-state-current.md:1` · `AGENTS.md:256`

## DEC-R3.2-REC-20260905 — تسوية R3.1 (المصادقة اللاحقة — Post-Hoc Ratification)
- **date:** 2026-09-05
- **السلطة:** أحكام تنفيذ المرحلة A من knw-lead، صادق عليها brd-ceo بتاريخ 2026-09-05 بعد استشارة المجلس (CONDITIONS ×3، لا نقض CSO) — التصحيح اللاحق للنسبة (R2 من أمر المرحلة B).
- **المحتوى:** إصلاح انجراف الوكلاء R3.1: 6 أزواج dat-*→arc-* (إعادة تسمية هوية فقط — verdict أ-2) + أرشفة 7 وكلاء (MANIFEST.md) + إعادة كتابة الحُرّاس لقراءة `meta.total_rooms`/`meta.total_agents` ديناميكياً + أساس PENDING-PHASE-B WARN.
- **الالتزامات الذرية (المرحلة A):** `8c0698a` · `ccd8033` · `15fec10` · `6f8a568`.
- **خارج النطاق (عزل — جلسة موازية):** 5 ملفات وكلاء (arc-infra-architect · gtw-intake-reformer · ops-cloud-engineer · ops-sandbox-executor · sec-secrets-warden) + `.env` + `.kilo/*` — لم تُضمَّن في أي التزام (verdict د-2).
- **evidence refs:** `hq/core/archive/r3.1-reconciliation/FINDINGS.md:1` · `hq/core/archive/r3.1-reconciliation/agents/MANIFEST.md:1` · `hq/core/nexus/registry.yaml:10-11`

## DEC-R3.3-PHASEB-20260905 — إغلاق المرحلة B من تسوية R3.1 (خلاصة نهائية)
- **date:** 2026-09-05 · **الأمر:** RCCF المرحلة B من brd-ceo (بعد GATE-OPEN · ADR-20260905-GTW-FLUTTER-QA-ARCHITECT · شروط المجلس)
- **الأحكام المنفذة R1–R5:**
  - R1/R5.7: استعادة CORTEX من HEAD (87 سطراً — إنهاء اقتطاع موازٍ غير معتمد) + إلحاق السجلات؛ استعادة HIPPOCAMPUS (81 سطراً) + إلحاق 3 جلسات موازية + جلسة الإغلاق.
  - R2: تصحيح نسبة DEC-R3.2 (المصادقة اللاحقة أعلاه).
  - R3: عزل — لم تُمسّ الملفات الخمسة المعزولة ولا `.env` ولا `.kilo/*`.
  - R4: استعادة `qa-flutter-architect` من الأرشيف (sha256 قبل=بعد `31f62a09…`).
  - R5.1: registry → 14 غرفة · **109** وكيل (سطر 11) + صف flutter-architect (سطر 209).
  - R5.2: personas → qa-flutter-architect (Rayan Al-Qadi — ريان القاضي) `personas.yaml:354-357`.
  - R5.3: كبسولة `hq/core/domain/rooms/10-quality/agents/qa-flutter-architect/` (استشاري فقط، لا بوابات، تصعيد qa-lead).
  - R5.4: system-state → 14/109/111 + ملاحظة ملزمة (الأسطر التاريخية محفوظة — Law 13).
  - R5.5: AGENTS.md → 63/256/258 (109 active agents).
  - R5.6: هجرة الكبسولات 08→04 (6 أزواج dat→arc) + أرشفة dat-lead وأصول الغرفة + خريطة قديم←جديد في structure-standard.md.
  - R5.7: إغلاق الذاكرة (هذا السجل + جلسة HIPPOCAMPUS).
- **الحُرّاس (exit 0):** registry_guard --strict · count_sync · evidence_guard hq/core --strict — WARN صادق متبقٍّ (INDEX stamp خارج النطاق + أسطر تاريخية) — لا فشل.
- **الأعداد النهائية:** 14 غرفة · **109 وكيلاً** · 111 مهارة على القرص · كبسولات قانونية حاضرة 110 · extra=5 (متقاعدون مؤرشفون) · extra_rooms=0.
- **evidence refs:** `hq/brain/cortex-decisions.md:ADR-20260905-GTW-FLUTTER-QA-ARCHITECT` · `hq/brain/hippocampus-sessions.md:SES-20260905-PHASEB-KNW-LEAD` · `hq/core/nexus/registry.yaml:11` · `AGENTS.md:256`

## DEC-R3.4-PHASEB-ACCEPT-20260905 — قبول صريح لتسليم المرحلة B (P-02.4) وإغلاقها الكامل
- **date:** 2026-09-05 · **الأمر:** RCCF-2026-0905-PHASEB-ACCEPT من brd-ceo (بعد إيصال التسليم P-02.5 · commit `8ed6afe`)
- **verdict:** APPROVED (P-02.4) — قبول صريح لتسليم المرحلة B: `SOFI-PHASEB-001` · `ADR-20260905-GTW-FLUTTER-QA-ARCHITECT` · بنود R1–R5 · كل الحُرّاس خضراء.
- **السلطة:** brd-ceo — قرار القبول المصيري (Law 7: CORTEX قرارات مصيرية — التوثيق مفوض إلى knw-lead بموجب write matrix).
- **الأدلة (Law 4):** `hq/core/nexus/registry.yaml:11` (total_agents: 109) · `AGENTS.md:256` (14 rooms · 109 active agents) · `hq/core/nexus/personas.yaml:354-357` (Rayan Al-Qadi — ريان القاضي) · كبسولة `hq/core/domain/rooms/10-quality/agents/qa-flutter-architect/` · sha256 قبل=بعد `31f62a09…` · registry_guard --strict PASS · count_sync PASS · pre-commit PASS · gitleaks no leaks · evidence_guard --staged --strict exit 0.
- **الشرط التابع (CONDITION-FOLLOW-UP):** الأرتيفاكتات التشغيلية المتقلبة — `hq/engine/mcp_server/data/tickets.db` · `hq/engine/logs/*.log` · `hq/engine/n8n/workflows/*.json` · `hq/engine/sites/n8n.caddy` — يجب ألا تُقْصّ (truncate/حذف/تفريغ) في إيصالات تسليم مستقبلية دون مراجعة؛ اقتراح المكان المُدار / إضافة `.gitignore` رُفع في تقرير القبول لهذا الأمر (اقتراح فقط — لم يُنفَّذ التغيير).
- **الحالة:** closed — إغلاق كامل للمرحلة B (P-02.4) — سجل الجلسة: `hq/brain/hippocampus-sessions.md:SES-20260905-PHASEB-ACCEPT`

## DEC-R6-20260905-ARCHIVE-LEGACY-AGENTS — أرشفة الشجرة الميراثية `hq/core/agents/` (الحكم R6)
- **date:** 2026-09-05 · **الأمر:** RCCF مصغّر R6 من brd-ceo (تحقق ميداني بعد إغلاق المرحلة B — evidence_guard hq/core --strict → exit 1 · 15 استشهاداً مكسوراً داخل الشجرة الميراثية)
- **الأصل:** `hq/core/agents/` = نسخة مكررة قديمة من `.opencode/agent/` (المصدر الفعلي الوحيد) — ليست هدف توليد لـ `port-agents.mjs` (grep = 0) · غير متتبَّعة في git (ls-files = 0) · بلا حارس · 12 استشهاداً → `hq/brain/brain-index.md:1` الملغى · 2 → `hq/core/security/secrets-policy.md:1` · `hq/core/licenses/policy.md:1` (مسارات متقادمة) · 1 → `hq/core/agents/08-data/dat-privacy-officer.md:1` (غرفة 08 مندمجة)
- **التنفيذ:** أرشفة → `hq/core/archive/legacy-hq-core-agents/` — MANIFEST.md (108 ملف + تصنيف ميراثي مكرر) + RESTORE.md + sha256 before == after (108/108 OK — Byte-identity) · خريطة قديم←جديد دائمة Law 13.5 في `hq/core/structure-standard.md` (v4.11) · الحُرّاس الثلاثة بعد الأرشفة كلها exit 0
- **العزل (R6):** `.opencode/` (المصدر الحي · registry/personas/routing/INDEX منجزة) · الملفات الخمسة المعزولة · `.env` · `.kilo/*` — لم تُلمس · التراجع الوحيد RESTORE.md قابل للعكس بالكامل
- **evidence refs:** `hq/core/archive/legacy-hq-core-agents/MANIFEST.md:1` · `hq/core/archive/legacy-hq-core-agents/RESTORE.md:1` · `hq/core/structure-standard.md:163-171` (v4.11) · `hq/core/archive/legacy-hq-core-agents/sha256-before.txt` == `sha256-after.txt` · الحُرّاس exit 0: registry_guard --strict · count_sync · evidence_guard hq/core --strict

## ADR-20260905-GTW-LARAVEL-DDD-ARCHITECT — إضافة معماري Laravel/DDD ومستشار قواعد البيانات والأمن كتستير رسمي ثالث (أمر مالك — امتداد لـ ADR-FLUTTER و ADR-REACT-DDD)
- **date:** 2026-09-05
- **owner decision (this session):** institutionalize the owner's "Laravel Senior Architect, DDD Strategist, Database & Security Master" methodology as a third official tester, continuing the qa-flutter-architect + qa-react-architect pattern.
- **owner confirmed choices:** (1) pattern = exact mirror of qa-flutter-architect + qa-react-architect (Room 10 · full agent + skill · advisory only · no gates) · (2) name = Yousuf Al-Amiri (يوسف العامري) · title = معماري Laravel/DDD ومستشار شامل · code = qa-laravel-architect.
- **gateway routing verdict:** PASS (gate) · WITHIN (budget ~25K exec + ~8K/run) · conflicts RESOLVED · lane = FATEFUL (registry/architecture/operating layer — Law 12) · route_to = brd-ceo exclusively (owner-explicit override to bypass knw-lead Phase B and execute directly via subagent, see ADR-20260905-GTW-DELEGATE-EXEC).
- **conflict resolution:** (1) precedent consistency: mirrors ADR-20260905-GTW-FLUTTER-QA-ARCHITECT + ADR-20260905-GTW-REACT-DDD-ARCHITECT + DEC-R3.4-PHASEB-ACCEPT-20260905 (advisory only, no gates, room 10, full agent + skill, distinct Arabic name + title). (2) backend vs quality scope: lives in Room 10 (the home of all testers) even though the domain is Backend — explicit owner confirmation. The agent reviews Laravel deliveries end-to-end, NOT builds them. Building remains in Room 5 (`bck-lead` + 7 backend engineers). (3) title collision: avoids "QA Lead/Master" with a distinct Arabic title; English `role: Laravel QA Architect` keeps it short in `personas.yaml`. (4) domain specialization: distinct from `bck-code-reviewer` (PR-level code reviewer in Room 5) — qa-laravel-architect is architecture + DDD + DB + Security end-to-end reviewer with a 5-phase protocol, NOT a per-PR code reviewer. (5) DDD coverage: aligns with `arc-data-architect` (DDD context map in Room 04) and `arc-domain-engineer` (Eloquent aggregates in Room 05) — read-only consultation, no schema/contract edits. (6) Security coverage: aligns with `sec-appsec-engineer` (Room 09) — the new role is advisory, security findings escalate via qa-lead → sec-lead → brd-cso. (7) stack lock: Laravel 11+ EXCLUSIVE per AGENTS.md §Stack Lock — no Symfony/CodeIgniter/Yii/raw-PHP frameworks. (8) tools whitelist mirrors qa-flutter-architect: `[Filesystem-Scoped, Bash, Kitesurf]`.
- **CONDITION-FOLLOW-UP respected:** no truncation of runtime artifacts (per DEC-R3.4-PHASEB-ACCEPT-20260905 §CONDITION-FOLLOW-UP).
- **proposed agent:** `qa-laravel-architect` (Room 10) + skill `.opencode/skills/qa-laravel-architect/SKILL.md` (112→113 skills on disk) — pending brd-ceo approval/distribution OR direct execution via owner-explicit override.
- **execution rooms (recommended for CEO if routed):** qa-lead (10) as owner of the new agent + skill · knw-lead (13) for registry/personas/capsule/charter coordination + memory · gtw-dispatcher (14) for routing.yaml budgets + skill index (count_sync 112→113).
- **evidence refs:** `hq/core/nexus/registry.yaml:210` (react-architect precedent) · `hq/core/nexus/personas.yaml:358-361` (Samer Al-Khalil precedent) · `hq/core/system-state-current.md:6,44` (110/112 baseline after React addition) · `AGENTS.md` §Stack Lock (Laravel 11+ exclusive) · `hq/core/domain/rooms/05-backend/charter.md` (bck-code-reviewer — distinct role, builder-adjacent).

## ADR-20260905-GTW-DELEGATE-EXEC — استثناء مالك: تفويض البوابة تنفيذ ADR-REACT-DDD مباشرة عبر subagent في وضع build
- **date:** 2026-09-05
- **authority:** owner explicit override (this turn) — highest authority in SOFI.
- **context:** المالك أمر البوابة (gtw-intake-reformer) بتفويض subagent في وضع build لتنفيذ ADR-20260905-GTW-REACT-DDD-ARCHITECT مباشرة على القرص، بدلاً من انتظار RCCF المرحلة B من knw-lead.
- **constitutional note:** this overrides the default "gateway prepares & routes, never executes project work" (gtw-intake-reformer charter + P-01.2). The owner has the authority to lift this gate; the override is recorded here for auditability.
- **method:** subagent type = `general` (multi-tool: filesystem + bash) in build mode · prompt = the enhanced 13-section brief (≈7000 chars) explicitly handed to the subagent · the subagent operates on the main tree (Law 10) · all 4 guards must remain green (registry_guard, count_sync, evidence_guard, gitleaks).
- **scope (authoritative instruction to subagent):** mirror qa-flutter-architect exactly — create `.opencode/agent/qa-react-architect.md` + `.opencode/skills/qa-react-architect/SKILL.md` + capsule (capabilities/senses/memory) under `hq/core/domain/rooms/10-quality/agents/qa-react-architect/` · update `registry.yaml:210` · update `personas.yaml:~358-361` (Samer Al-Khalil) · update `routing.yaml` (model+budget) · update room 10 charter roster+1 · update `.opencode/skills/INDEX.md` (111→112) · commit atomically · run all 4 guards.
- **CONDITION-FOLLOW-UP from DEC-R3.4 still binding:** no truncation of runtime artifacts (tickets.db, logs, workflows/*.json, n8n.caddy).
- **memory logs:** this ADR + a HIPPOCAMPUS session `SES-20260905-GTW-DELEGATE-EXEC` documenting the override and the subagent prompt.
- **evidence refs:** `hq/brain/cortex-decisions.md:ADR-20260905-GTW-REACT-DDD-ARCHITECT` · `hq/brain/cortex-decisions.md:DEC-R3.4-PHASEB-ACCEPT-20260905` · `.opencode/agent/qa-flutter-architect.md` (reference template) · `hq/core/domain/rooms/10-quality/agents/qa-flutter-architect/` (capsule template) · `.opencode/skills/qa-flutter-architect/SKILL.md` (skill template).

## ADR-20260905-GTW-REACT-DDD-ARCHITECT — إضافة معماري React/DDD ومدقق جودة كتستير رسمي (أمر مالك — امتداد لـ ADR-FLUTTER)
- **date:** 2026-09-05
- **owner decision (this session):** institutionalize the owner's "React Senior Architect, Domain-Driven Design (DDD) & QA Master" methodology as a second official tester, mirroring the qa-flutter-architect precedent.
- **owner confirmed choices:** (1) pattern = exact mirror of qa-flutter-architect (Room 10 · full agent + skill · advisory only · no gates) · (2) name = Samer Al-Khalil (سامر الخليل) · title = معماري ومدقق جودة React/DDD · code = qa-react-architect.
- **gateway routing verdict:** PASS (gate) · WITHIN (budget ~25K exec + ~8K/run) · conflicts RESOLVED (see below) · lane = FATEFUL (registry/architecture/operating layer — Law 12) · route_to = brd-ceo exclusively.
- **conflict resolution:** (1) precedent consistency: mirrors ADR-20260905-GTW-FLUTTER-QA-ARCHITECT + DEC-R3.4-PHASEB-ACCEPT-20260905 (advisory only, no gates) — accepted pattern. (2) title collision: prompt's "QA Master" avoids conflict with qa-lead (Lama) by adopting a distinctive title; no "QA Lead/Master" anywhere in the new agent. (3) domain specialization: React-DDD is distinct from existing fnt-react-engineer (builder in room 06) and qa-design-auditor (cross-stack design auditor in room 10) — new agent is a React-domain end-to-end reviewer that feeds findings INTO those specialists/leads. (4) DDD coverage: aligns with `arc-data-architect` (DDD context map owner in room 04) and `arc-domain-engineer` (Eloquent/DDD aggregates in room 05) — read-only consultation, no schema/contract edits. (5) stack lock: React 18+/Next.js per AGENTS.md §Stack Lock — no conflict.
- **CONDITION-FOLLOW-UP respected:** no truncation of runtime artifacts in delivery receipts (per DEC-R3.4-PHASEB-ACCEPT-20260905 §CONDITION-FOLLOW-UP).
- **proposed agent:** `qa-react-architect` (Room 10) + skill `.opencode/skills/qa-react-architect/SKILL.md` (111→112 skills on disk) — pending brd-ceo approval/distribution.
- **execution rooms (recommended for CEO):** qa-lead (10) as owner of the new agent + skill · knw-lead (13) for registry/personas/capsule/charter coordination + memory · gtw-dispatcher (14) for routing.yaml budgets + skill index (count_sync 111→112).
- **evidence refs:** `hq/core/nexus/registry.yaml:209` (flutter-architect precedent) · `hq/core/nexus/personas.yaml:354-357` (Rayan Al-Qadi precedent) · `hq/core/system-state-current.md:6,44` (109/111 baseline) · `hq/brain/cortex-decisions.md:DEC-R3.4-PHASEB-ACCEPT-20260905` (acceptance + conditions) · `AGENTS.md` §Stack Lock (React 18+ exclusive) · `hq/core/domain/rooms/06-frontend/charter.md` (fnt-react-engineer — builder, distinct role).

## ADR-20260905-AUDIT-ALL — تنفيذ المراجعة الشاملة (Audit-ALL) — تصحيح وتطوير المؤسسة بالكامل (أمر مالك "سوي كل شيئ")

- **date:** 2026-09-05 · **owner directive:** "سوي كل شيئ" — تنفيذ المراجعة الشاملة المقدمة من AI Systems Architect (645 سطراً في SOFI-INSTITUTION-COMPLETE-REPORT-2026-09-05.md)
- **classification:** FATEFUL — 15 rooms · 115 agents · 113 skills — registry + architecture + tooling + docs — Board + CSO veto
- **verdict:** APPROVE بشروط — المستوى 1 و 2 يُنفذ فوراً على الشجرة الرئيسية (Law 10) — المستوى 3 (WarRoom + tool wrappers + quick-reference) يُنفذ فوراً — Localization/Innovation كـ ADR مخطط (لا غرفة جديدة بلا تصميم مجمد)
- **Level 1 (5 إصلاحات — منفذة):**
  - L1.1: Law 1 — إضافة المرجع الوحيد `hq/core/protocols.md:P-01.8` في `AGENTS.md:10` (توحيد المرجع)
  - L1.2: charter 14-gateway — تم التحقق — لا تكرار (7 وكلاء — جدول سليم) — موثق كـ "verified no duplicate"
  - L1.3: إنشاء `hq/core/SOFI-QUICK-REFERENCE.md:1` — خريطة قرار واحدة + مخطط تدفق + مسرد — يمنع التشتت
  - L1.4: Protocol 19 + 20 في `hq/core/protocols.md:391` — P-19 Research-to-Design Bridge (P-19.1→19.5) + P-20 Living Docs & Failure Mode (P-20.1→20.3)
  - L1.5: `hq/core/domain/context-map.yaml:1` — توضيح حدود 04 (OWNS api-design) / 09 (REVIEWS/VETO) / 10 (VERIFIES) — boundary note v1.1
- **Level 2 (3 ملفات — منفذة):**
  - L2.1: `hq/core/nexus/rccf-registry.yaml:1` — سجل RCCF مركزي — 3 RCCFs مسجلة (PHASEB + REACT + LARAVEL) + قالب
  - L2.2: `hq/core/standards/living-docs.md:1` — معيار التوثيق الحي — max تأخير التزام واحد
  - L2.3: `hq/core/standards/qa-assessment-matrix.md:1` — مصفوفة 20/28/22 نقطة + معايير مشتركة (Perf/Security/A11y)
  - L2.4: `hq/core/templates/report-template.md` — قالب موحّد + `hq/core/tooling/sofi-audit.py` + `sofi-security-scanner.py`
- **Level 3 (WarRoom — منفذة):**
  - L3.1: غرفة 15-warroom — 4 وكلاء — `war-incident-commander` (Firas Al-Najjar) · `war-forensic-analyst` (Layla Al-Halabi) · `war-rollback-engineer` (Omar Al-Khani) · `war-communication-lead` (Salma Al-Rashid) — charter + 4 agents + 12 capsule
  - L3.2: registry `hq/core/nexus/registry.yaml:3` 14→15 rooms · 111→115 agents · `personas.yaml` +4 · `routing.yaml` +4 · `AGENTS.md:62,256` 111→115 · `room-priority.yaml` T3 + warroom · `count_sync.py` (15,115)
  - L3.3: Localization/Innovation + إعادة توزيع 04 + دمج أدوات — **مخطط كـ ADR لاحق** — لا تنفيذ بلا ERD/OpenAPI مجمدين (Design-First)
- **rejected/downgraded (with reason):**
  - دمج 12-observability في 11-devops — **مرفوض** — يخالف فصل T3 (المراقب لا يراقب نفسه) — Law 2
  - دمج api-envelope/ddd-capsule في معيار واحد — **مرفوض** — عقدان مستقلان يُقاس عليهما الكود
  - زيادة فورية إلى 16 غرفة/124 وكيلاً — **مؤجل** — يحتاج ERD + OpenAPI + DFR قبل أي غرفة جديدة (Law S1→S6)
- **evidence refs:** `hq/core/SOFI-QUICK-REFERENCE.md:1` · `hq/core/nexus/rccf-registry.yaml:1` · `hq/core/standards/living-docs.md:1` · `hq/core/standards/qa-assessment-matrix.md:1` · `hq/core/domain/rooms/15-warroom/charter.md:1` · `.opencode/agent/war-*.md` 4 · `hq/core/nexus/registry.yaml:3,11` · `AGENTS.md:62,256` · `hq/core/tooling/count_sync.py:23` · `hq/core/nexus/room-priority.yaml:11` · `hq/core/protocols.md:391` (P-19/20) · `hq/core/domain/context-map.yaml:1`
- **guards:** registry_guard --strict PASS · count_sync PASS · evidence_guard hq/core --strict 0 broken · gitleaks no leaks · pre-commit PASS

## ADR-20260905-AUDIT-ALL-Phase2 — تنفيذ المؤجل — Localization (08) + Innovation (16) — 17 غرفة · 121 وكيلاً

- **date:** 2026-09-05 · **owner directive:** "نفّذ المؤجل" — تنفيذ المؤجل من ADR-20260905-AUDIT-ALL
- **classification:** FATEFUL — registry + rooms + personas + routing — Board + CSO veto
- **verdict:** APPROVE — نفّذ المؤجل فوراً على الشجرة الرئيسية (Law 10)
- **ما نُفذ:**
  - **08-localization (T1 Paper):** 4 وكلاء — `loc-translation-manager` (Noura Al-Hassan) · `loc-cultural-adapter` (Khalid Al-Masri) · `loc-rtl-specialist` (Hadi Al-Quds) · `loc-voice-tone-expert` (Rana Al-Shami) — charter + 4 agents + 12 capsules — يعيد تعريف الكود 08 بعد دمجه (R3.1) per Law 13 continuity — history in `hq/core/archive/r3.1-reconciliation/`
  - **16-innovation (T1 Paper — innovation track):** 2 وكلاء — `inn-lab-lead` (Ziad Al-Hariri) · `inn-tech-scout` (Maya Al-Nouri) — charter + 2 agents + 6 capsules — تجارب معزولة بموافقة brd-cto
  - **registry:** `hq/core/nexus/registry.yaml:3` 15→17 rooms · 115→121 agents — إضافة غرفتين + 6 وكلاء
  - **personas:** `hq/core/nexus/personas.yaml` +6 — loc-* 4 + inn-* 2
  - **routing:** `hq/core/nexus/routing.yaml` +6 — loc-* + inn-*
  - **AGENTS:** `AGENTS.md:62,256` 15→17 rooms · 115→121 agents — Law 12 + Final State
  - **room-priority:** `hq/core/nexus/room-priority.yaml:11` 15→17 · T1 + loc/inn · T3 + warroom
  - **tooling:** `hq/core/tooling/count_sync.py:23` (17,121) — guards PASS
  - **redistribution of 04 (14→11) + full tool merge — still planned as ADR — لا تنفيذ بلا ERD مجمد (INT-0004) — موثق هنا كـ deferred-remaining**
- **rejected/downgraded:** none — كل المؤجل نُفذ (6 وكلاء) — المتبقي (redistribution/tool-merge) مخطط
- **evidence refs:** `hq/core/domain/rooms/08-localization/charter.md:1` · `hq/core/domain/rooms/16-innovation/charter.md:1` · `.opencode/agent/loc-*.md` 4 · `.opencode/agent/inn-*.md` 2 · `hq/core/nexus/registry.yaml:3,11` · `AGENTS.md:62,256` · `hq/core/tooling/count_sync.py:23`
- **guards:** registry_guard --strict PASS · count_sync PASS · evidence_guard 0 broken · gitleaks no leaks
