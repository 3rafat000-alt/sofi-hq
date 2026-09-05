# QA Assessment Matrix — مصفوفة تقييم موحّدة للمختبرين

> **الغرض:** توحيد منهجية التقييم بين المختبرين الثلاثة الجدد — الحل لفجوة "عدم توحيد منهجية التقييم" (audit 2026-09-05) + اقتراح `qa-assessment-matrix.md` في المراجعة
> **المالك:** `qa-lead` (10-quality) — لمى الطرابلسي — تُحدث مع كل مختبر جديد
> **الاستخدام:** كل تقرير استشاري (qa-flutter/flutter + qa-react + qa-laravel) يقيس نقاطه هنا — لا تقرير بلا مصفوفة

---

## المصفوفة الموحّدة — 3 مختبرين × نقاط + معايير مشتركة

| المختبر | الكود | النقاط | الفئات | الأدوات الملزمة | المرجع |
|---------|-------|--------|--------|------------------|--------|
| **Flutter QA Architect** | `qa-flutter-architect` | **20** | UI/UX 10 · Performance 5 · A11y 5 | adb screencap · uiautomator dump · gfxinfo · meminfo · flutter run --profile | `.opencode/skills/qa-flutter-architect/SKILL.md` |
| **React/DDD QA Architect** | `qa-react-architect` | **28** | UI/UX 10 · Perf/Web Vitals 6 · A11y 6 · Code/DDD 6 | Lighthouse · bundle-analyzer · React Profiler · Axe | `.opencode/skills/qa-react-architect/SKILL.md` |
| **Laravel/DDD QA Architect** | `qa-laravel-architect` | **22** | Code/DDD 6 · DB/Perf 6 · Security 6 · Testing 4 | php artisan · EXPLAIN · Telescope · Pest/PHPUnit | `.opencode/skills/qa-laravel-architect/SKILL.md` |

## المعايير المشتركة — تُقاس في كل المختبرين الثلاثة

| المعيار المشترك | كيف يُقاس | العتبة |
|------------------|-----------|--------|
| **الأداء** | Flutter: FPS 60 · React: LCP<2.5s/FID<100ms/CLS<0.1 · Laravel: p95 <200ms simple / <500ms complex | 100% PASS |
| **الأمان** | Flutter: لا أسرار في الكود · React: CSP + XSS · Laravel: Policies/Gates + FormRequest + rate limiting | 0 ثغرة P0 |
| **الوصولية** | Flutter: Semantics + 48dp · React: ARIA + keyboard + 4.5:1 · Laravel: API لا تكشف PII | WCAG 2.1 AA |

## مقياس التقييم الموحّد

| النتيجة | المعنى | الإجراء |
|---------|--------|---------|
| **PASS** | كل نقاط الفئة خضراء | يُغذي Gate-5 — لا حجب |
| **PASS with warnings** | ≤2 نقاط P1 صفراء | يُغذي Gate-5 مع تحذير — الإطلاق مسموح مع خطة إصلاح |
| **FAIL** | ≥1 نقطة P0 حمراء | يُعيد للمصدر — لا إطلاق — Gate-5 مغلق |
| **HOLD** | مرجع مفقود (لا PRD/OpenAPI/DFR) | **gate return** — لا يُقاس — يُعاد لـ S2/S3 |

## القالب الموحّد — كل تقرير يحمل:

```
### QA Assessment — <ticket-id> — <assessor: riyan|samer|yousuf> — <date>
- Scope: <project/feature> · Stack: <Flutter/React/Laravel + versions>
- References: PRD <file:line> · OpenAPI <file:line> · DFR <file:line>
- Points: <pass>/20 or 28 or 22 — <fail> P0 · <warn> P1
- Shared: Perf <pass/fail> · Security <pass/fail> · A11y <pass/fail>
- Evidence: file:line · exit codes · fingerprints (device/browser/DB)
- Verdict: PASS / PASS with warnings / FAIL / HOLD — advisory only (qa-lead decides)
```

---

## الصيانة

- مع كل مختبر جديد: يُضاف صف جديد هنا + يُحدث `hq/core/domain/rooms/10-quality/charter.md:15` (Agent count) + `SOFI-QUICK-REFERENCE.md` §5
- المسؤول: `qa-lead` — المراجعة: `brd-cqo` — التوثيق: `knw-lead` في CORTEX

---

## المراجع

- `.opencode/agent/qa-flutter-architect.md:1` · `.opencode/agent/qa-react-architect.md:1` · `.opencode/agent/qa-laravel-architect.md:1`
- `.opencode/skills/qa-flutter-architect/SKILL.md` · `qa-react-architect/SKILL.md` · `qa-laravel-architect/SKILL.md`
- `hq/core/domain/rooms/10-quality/charter.md:15`
