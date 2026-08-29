## FILE: hq/engine/mcp_server/docs/acquaintance-test.md
# اختبار التعارف (Roll Call) — المنظمة كلها تقدم نفسها

> Author: gtw-intake-reformer · 2026-08-29 · type Gateway/Infrastructure
> بعد حذف الـ symlink (structure-standard v4.8 — "لا تكرار")

## ما الاختبار؟
استدعاء أداة `sofi_who_is` على **كل معرّف رسمي** من `hq/core/nexus/registry.yaml` (114 وكيلاً) عبر الجسر — كل وكيل يقدّم نفسه: غرفته، قائده، زملاءه، وهل هو قائد. هو «تعرّف عام» يثبت أن نظام الهوية كامل ومتسق بعد إزالة مجلد الارتباط.

## النتائج (2026-08-29 06:10 +03)

| الفحص | النتيجة |
|---|---|
| الوكلاء الرسميون من السجل | 114 (بدون تكرار ✓) |
| **مُقدَّم بنجاح (تعارف كامل)** | **114/114** خلال 0.6 ثانية |
| القادة عرّفوا أنفسهم كقادة | **15/15** (بما فيها brd-ceo و gtw-dispatcher — إصلاح lead) |
| تطابق الغرف مع السجل | **114/114** |
| وكيل بدون قائد | 0 |
| كل وكيل له زملاء | نعم ✓ |

## التوزيع بالغرف (السجل ← المُقدَّم)

| الغرفة | السجل | المُقدَّم |
|---|---:|---:|
| 00-boardroom | 7 | 7 ✓ |
| 01-strategy | 8 | 8 ✓ |
| 02-research | 8 | 8 ✓ |
| 03-design | 10 | 10 ✓ |
| 04-architecture | 9 | 9 ✓ |
| 05-backend | 8 | 8 ✓ |
| 06-frontend | 8 | 8 ✓ |
| 07-mobile | 6 | 6 ✓ |
| 08-data | 7 | 7 ✓ |
| 09-security | 9 | 9 ✓ |
| 10-quality | 7 | 7 ✓ |
| 11-devops | 8 | 8 ✓ |
| 12-observability | 6 | 6 ✓ |
| 13-knowledge | 6 | 6 ✓ |
| 14-gateway | 7 | 7 ✓ |
| **المجموع** | **114** | **114 ✓** |

## ملاحظة عن المعرّفات
- معرّفات القادة داخل قوائم agents في السجل (str-lead، gtw-dispatcher… إلخ) — ملفاتهم ضمن نفس الغرفة (تدقيق 114/114 سابق).
- إصلاح أثناء الاختبار: `_room_lead()` كان يعطي البوابة قائداً وهمياً `gtw-lead` — صُحح إلى `gtw-dispatcher` (السجل الرسمي) فأصبح التعارف 15/15.

## الأدلة
- السجلات: `hq/core/nexus/registry.yaml` (مصدر الحقيقة — Law 12) · الجسر `hq/engine/mcp_server/mcp_bridge/server.py:sofi_who_is` · القاعدة `server.py:_room_lead`
- التشغيل: stdio MCP client initialize OK — sofi v1.27.2 — 13/13 أدوات
- بنية v4.8: `hq/core/structure-standard.md` (حذف الـ symlink، لا تكرار)