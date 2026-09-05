# CHECKLIST-C2 — قائمة الفحص المعلنة مسبقاً (Pre-Declared Acceptance Criteria)

> **FILE:** hq/core/archive/r3.1-reconciliation/CHECKLIST-C2.md
> **Owner:** knw-lead (Knowledge room) · **Date declared:** 2026-09-05 (قبل أي تعديل — خط الأساس في FINDINGS.md)
> **Authority:** أمر عمل RCCF من brd-ceo — المرحلة A: إصلاح الحُرّاس + تسوية انجراف الوكلاء (لا حذف · لا تسجيل qa-flutter-architect · لا تعديل محتوى ملفات الوكلاء · لا تعديل AGENTS.md/system-state)
> **Rule:** القبول يُقاس بهذه البنود فقط — لا تُشتق معايير جديدة بعد النتيجة.

---

## معايير القبول (كلها قابلة للقياس)

| # | المعيار (Measurable) | أمر التحقق | حالة النجاح |
|---|----------------------|-----------|-------------|
| C1 | الحارس registry_guard.py يقرأ مخطط R3.1 (rooms قائمة وليس قاموساً) | `python3 hq/core/tooling/registry_guard.py; echo $?` | exit = 0 **و** المخرجات تذكر `14 rooms` و `108 agents` |
| C2 | عدّاد الوكلاء مشتق من السجل لا ثابت: تساوي تام بين السجل (108) والقرص (108 ملف) بعد التسوية | مخرج C1 + `ls .opencode/agent/*.md | wc -l` | 108 = 108 |
| C3 | لا يوجد ملف وكيل غير مسجَّل متبقٍّ في الشجرة النشطة | مخرج C1 (قسم extras فارغ) + grep | القسم الفارغ "extras/missing" |
| C4 | لا يوجد وكيل مسجَّل ناقص الملف | مخرج C1 (قسم missing فارغ) | القسم الفارغ |
| C5 | count_sync.py يعمل بلا استثناء وبأعداد حقيقية | `python3 hq/core/tooling/count_sync.py; echo $?` | exit = 0 · لا traceback · يطبع 14 غرف · 108 وكيل |
| C6 | لا ثوابت قديمة (15 غرفة / 114 وكيل / 109 مهارات مثبّتة) في مصدري الحارسين | `grep -nE '114|15 rooms|109' hq/core/tooling/registry_guard.py hq/core/tooling/count_sync.py` | صفر مطابقة (باستثناء عبارة تحذيرية موثَّقة للدقة) |
| C7 | evidence_guard.py يمر على ملفات الأدوات المغيَّرة | `python3 hq/core/tooling/evidence_guard.py --strict hq/core/tooling/` | exit = 0 |
| C8 | سلامة الأرشيف: كل ملف مؤرشَف له sha256 في MANIFEST والملف موجود فعلياً | `sha256sum -c MANIFEST.sha256` (داخل دليل الأرشيف) | الكل OK |
| C9 | qa-flutter-architect **غير مسجَّل** في السجل (قيود المرحلة A) | `grep -c 'qa-flutter-architect' hq/core/nexus/registry.yaml` | = 0 |
| C10 | لا حذف لأي ملف وكيل — أرشفة/إعادة تسمية فقط | `git diff --name-status -- .opencode/agent` بعد العملية | لا سطور `D`؛ كل تغيير `R100` أو إضافة ملفات أرشيف في `hq/core/archive/` |
| C11 | لم أُعدّل محتوى ملفات وكلاء آخرين | `git diff --stat -- .opencode/agent` مقابل خط الأساس | لا تغيير محتوى جديد من عملي (الـ M الخمسة السابقة من جلسة موازية موثَّقة في FINDINGS) |
| C12 | AGENTS.md و system-state-current.md لم يُغيَّرا مني (توثيق فقط — المرحلة B) | مقارنة sha256 بخط الأساس في FINDINGS.md | hash مطابق لخط الأساس |
| C13 | تشغيل الحُرّاس الثلاثة بعد الإصلاح وتسجيل أرقام exit في كتلة الأدلة (BEFORE) | سجلات أوامر التنفيذ | exit0 = registry_guard · exit0 = count_sync · exit0 = evidence_guard |
| C14 | التسليم: كتلة RCCF + كتلة أدلة إلى brd-ceo (Law 3) — لا تسليم مباشر للمستخدم | حضور الكتلتين في رسالة التسليم | موجود |

---

## ملاحظات معلنة مسبقاً (حالات معروفة)

1. **كبسولات الغرف** (`hq/core/domain/rooms/*/agents/`): الهجرة الفيزيائية 08→04 (6 كبسولات arc-* ناقصة + 08-data باقية) **خارج صلاحية هذه المرحلة** (تغيير شجرة غرف أخرى = المرحلة B / أصحاب الغرف). يُوثَّق الانجراف في FINDINGS.md ويُعالَج كتحذير (WARN) في الحارس — لا فشل.
2. **المهارات** (111 دليلاً على القرص مقابل INDEX.md يزعم 109/109 مع 110 رابطاً): تحديث وثائق المهارات (INDEX/SKILLS-ASSIGNMENT) من المرحلة B — الحارس يطبع الرقم الحقيقي ويحذّر من انحراف التوثيق ولا يفشل بسببه.
3. **شجرة العمل المتسخة**: registry.yaml وAGENTS.md معدّلان R3.1 غير ملتزمين (جلسة موازية)؛ هذه المرحلة لا تلتزم ما لم يأمر brd-ceo.
4. **الأزواج الستة dat-* ↔ arc-***: قرار brd-ceo ملزم (تصعيد) — التنفيذ بعد الحكم وبموجبه فقط.