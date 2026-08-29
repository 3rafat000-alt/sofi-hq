## FILE: hq/engine/mcp_server/brain/CONTEXT.md
# PRD — SOFI HQ Local MCP Infrastructure
> **Status:** Frozen S1 — Approved by brd-ceo — Date: 2026-08-29
> **Law 13:** كل ملف يبدأ بـ ## FILE: والمسار حقيقي — لا وهم
> **Track:** 🔴 Critical/Fateful — يمس الأمن والمعمارية والـ schema

## 1) الرؤية — جملة هدف واحدة
بناء حافلة MCP محلية مجانية تطبق القوانين 2 و3 و4 و6 و7 و10 ككود تنفيذي لا يمكن تجاوزه، وتربط 114 وكيلًا بـ 15 قائدًا بزمن استجابة ≤100ms وسجل تدقيق 100%.

## 2) لماذا الآن — التقنية الخمسة Why
1. لماذا MCP محلي؟ ليتمكن الوكلاء من التواصل فوريًا
2. لماذا التواصل مهم؟ لأن القانون يفرض التسليم الهرمي وعزل الغرف (2 و3)
3. لماذا القوانين مهمة؟ لأن تجاوزات سابقة أسقطت ترحيلات أمنية
4. لماذا أسقطت؟ لعدم وجود حافلة مركزية — عمل معزول (worktree precedent Law 10)
5. إذن الجذر: تحويل الدستور إلى كود يمنع الخطأ قبل حدوثه

## 3) الأطراف المعنية
| الطرف | الدور | التأثر |
|---|---|---|
| قادة 15 غرفة (brd-ceo ... gtw-dispatcher) | مستخدم يومي — تنسيق عبر Ticket Bus | مباشر |
| 114 وكيل | مرسل/مستقبل عبر قائده فقط | مباشر |
| brd-cso | فيتو أمني — أي ثغرة عزل = L3 | حرج |
| المالك (localhost) | مشغل يومي Linux/macOS/Windows | مباشر |

## 4) النطاق — يدخل ويخرج
**يدخل:** 7 ملفات Python + 2 DB + سكربتات + توثيق + اختبارات 3 طبقات
**يخرج:** لا Dashboard — لا سحابة — لا PostgreSQL/Redis — لا OAuth — لا تشفير PII في MVP — لا Clustering

## 5) المقاييس الستة الرقمية (قابلة للقياس)
| # | المقياس | الهدف | طريقة القياس |
|---|---|---|---|
| 1 | REST P95 | ≤100ms | 1000 طلب httpx |
| 2 | WS ACK | ≤50ms | WS latency test |
| 3 | تزامن 114 | 0 سقوط + ≤500MB | load_114.py |
| 4 | تسجيل تدقيق | 100% + ISO8601 + file:line | فحص DB |
| 5 | عزل غرف | 100% رفض cross-room | 5 محاولات اختبار |
| 6 | تغطية | ≥90% وحدة ≥80% تكامل + MIT/Apache فقط | pytest --cov + pip-licenses |

## 6) المتطلبات الوظيفية (F1-F6 مختصر)
- F1 agent→lead عبر WS `/ws/agent/{id}` + REST fallback + منع cross-room 403 + عربي واضح
- F2 lead→lead عبر Ticket Bus `POST /tickets` + حالات open→in_progress→resolved→closed + تصعيد 24h إلى brd-ceo
- F3 فرض عزل صارم `validate_cross_room()` أول سطر + 4 أنواع رسائل Enum + violation append-only
- F4 ذاكرة: كتابة فورية في cortex/hippocampus/amygdala/LESSONS + فصل hq/brain عن projects/*/brain
- F5 تدقيق: audit_logs append-only + تصدير JSON/CSV + بحث مفلتر
- F6 أمان: X-API-Key من .env + Rate 100/دقيقة →429 + Pydantic 1-4096 حرف + لا secret في الكود

## 7) القيود غير الوظيفية
- أداء: نفس الأرقام أعلاه — فهرسة SQLite على sender/recipient/timestamp
- أمان: كل endpoint محمي — WAL+fsync — لا UPDATE/DELETE على logs
- خصوصية: محلي 100% — لا بايت يخرج من localhost
- توافق: Python 3.10+ (مختبر 3.10/3.11/3.12) — يعمل Linux/macOS/Windows
- صيانة: كل ملف ## FILE: + kebab/snake + DDD 4 مجالات + كل دالة ≤50 سطر

## 8) المحظورات المطلقة (خرق = إرجاع فوري)
GPL/AGPL/SSPL ممنوع — secret في الكود ممنوع — cross-room ممنوع — تعديل logs ممنوع — سحابة ممنوعة — كود قبل DFR ممنوع — مسار وهمي ممنوع — worktree ممنوع

## 9) القرارات المقفلة
- WS+REST معًا (فورية + fallback) — لا WS فقط
- Python محلي أساسي + Dockerfile اختياري
- خادم مستقل localhost:8765 — تكامل OpenCode عبر WS client موثق
- ملفان SQLite منفصلان tickets.db + messages.db
- Rate Limit: تطبيق يدوي token-bucket (بدون slowapi) لتبسيط الاعتماديات

## 10) المخاطر — ملخص
عزل L3 + فقدان logs + تراخيص + اختناق 114 + تسريب secret — كلها بخطة تراجع 60 ثانية (backup + stop.sh + restore)

## 11) خطة المراحل S1→S6
S1 استراتيجية + S2 تصميم ورقي + S3 DFR + S4 backend حي + S5 واجهات بعد اكتمال backend + S6 درع وإنتاج — التفاصيل في pipeline-production-line.md

---
*Evidence: hq/core/nexus/registry.yaml:6 يحدد 15 غرفة — قانون 2 و3 في AGENTS.md — البرنامج الخطي في hq/core/nexus/pipeline.yaml*
