## FILE: hq/engine/mcp_server/AGENT_GUIDE.md
# دليل الوكيل والقائد — كيف لا تضيع (خطوة بخطوة — لا عمل أعمى)

> **لمن؟** كل وكيل من الـ114 وكل قائد من الـ15 — اقرأ هذا قبل أي إرسال — 5 دقائق تنقذك من 3 ساعات ضياع

---

## الخطوة 0 — قبل أن تكتب حرفاً

1. **افتح التذكرة:** كل عمل له `task_id` (مثل `T-101`) و `context` (سطر في `openapi.yaml` أو `CONTEXT.md`) — إن لم تجده، اطلب عبر `consult_lead` — لا تخترع
2. **جهّز الدليل:** `evidence` هو `file:line` للملف الذي عدّلته — مثال `backend/app/Payments.php:42` — بدونه تسليمك مرفوض في Gate

## الخطوة 0.5 — فكّر تسلسلياً (Sequential-Thinking — إلزامي)

قبل أي فعل، مرّر ذهنياً 5 خطوات — لا تقفز:

```
① الفهم   → ما الطلب الحقيقي؟ (أعد صياغته بسطر)
② السياق  → أين العقد؟ (openapi.yaml / CONTEXT.md) — مرجع file:line
③ الفحص   → هل كل المدخلات موجودة؟ هل في تعارض؟
④ الخطة   → ما الخطوات والترتيب والمخاطرة؟ (2-4 خطوات)
⑤ التحقق  → كيف أعرف أني انتهيت؟ (معيار قبول)
```

**إن انتهت ② أو ③ بـ نقص/غموض/تعارض → لا تخمّن → انتقل فوراً للخطوة 0.6**

## الخطوة 0.6 — لا تخمين: اسأل حاداً ثم صعّد

```
نقص/مشكلة/تعارض
   │
   ▼
توقف فوراً — لا تنفّذ تخميناً
   │
   ▼
فكّر: ما الناقص؟ من يملك الجواب؟
   │
   ▼
اسأل: clarify() — 1-3 أسئلة حادة
```

```python
await c.clarify(
    questions=[
        "هل الهدف هو التكامل مع بوابة الدفع أم إنشاء الصفحات فقط؟",
        "أين ملف العقد المعتمد لهذه المهمة؟",
        "ما معيار القبول — متى نعتبرها منتهية؟"
    ],
    missing="openapi.yaml غير معتمد لمهمة T-101",
    thinking="الخطوة ③ — مدخلات ناقصة",
    assignee="bck-lead"  # أو اتركه فارغاً ليختار SDK قائدك تلقائياً
)
# → تذكرة clarification_request — يصل القائد خلال 50ms — مهلة 30 دقيقة
```

**إن لم يأتِ الجواب خلال 30 دقيقة، أو كانت المشكلة حرجة (مال/أمان/إنتاج/قاعدة بيانات) → صعّد فوراً:**

```python
await c.escalate(
    subject="T-101 عالق: نقص في العقد والقيادة لم تجب",
    description="أسئلتي: [ما الهدف؟ أين العقد؟ ما المعيار؟] — السياق: openapi.yaml غير معتمد — حالت 30 دقيقة"
)
# → هذا التصعيد يذهب فوراً لـ brd-ceo — ليس فشلاً، احترافية
```

**قواعد ذهبية:** لا تخمين (L2) · أسئلة حادة 1-3 فقط · صعّد ولا تختبئ · كل خطوة تُسجّل في التدقيق

## الخطوة 0.7 — أدوات الحافلة (محدّثة 2026-09-01 — جسر SOFI MCP محذوف)

> **تنبيه:** جسر SOFI MCP (`hq/engine/mcp_server/mcp_bridge/server.py`) **حُذف نهائياً** بأمر مالك O-01 — أدوات `sofi_*` عبر opencode لم تعد متاحة — استخدم SDK المباشر `hq/engine/mcp_server/client/mcp_client.py` للحافلة `mcp.local:8765`.

## الخطوة 1 — الوكيل يرسل لقائده (أنت وكيل)

**استخدم SDK — لا تكتب fetch يدوياً:**

```python
from hq.engine.mcp_server.client.mcp_client import MCPClient
c = MCPClient("bck-api-engineer")  # نفس اسمك في registry.yaml
await c.send_guarded(
    content="تم إنجاز API الدفع — backend/app/Payments.php:42 — يطبق openapi.yaml: POST /pay",
    evidence="hq/engine/mcp_server/AGENT_GUIDE.md:15",
    task_id="T-101",
    context="openapi.yaml: خط POST /pay — CONTEXT.md:5 — لا اجتهاد خارج العقد",
    recipient="bck-lead"  # أو اتركه فارغاً ليختار lead غرفتك تلقائياً
)
```

**ماذا يحدث؟** SDK يحاول WS (6ms) — إن فشل يتحول REST — إن حاولت مخاطبة `fnt-react-engineer` مباشرة يُرمى `FORBIDDEN Law 2` فوراً — أرسل لقائدك فقط

**أخطاء شائعة:**
- `المحتوى فارغ` → أرسلت `content=""` — املأ 1-4096 حرف
- `FORBIDDEN` → حاولت cross-room — أرسل لقائدك وهو يستشير القائد الآخر عبر Ticket
- `RATE_LIMITED` → أرسلت 101 رسالة/دقيقة — انتظر 60ث

## الخطوة 2 — القائد يستشير قائداً آخر (أنت Lead)

**لا ترسل لوكيل غرفة أخرى — استشر قائده عبر Ticket:**

```python
c = MCPClient("bck-lead")
await c.consult_lead(
    subject="مراجعة معمارية — هل نستخدم SQLite؟",
    description="نحتاج قرار قبل S2 — الخياران: SQLite محلي (مجاني) vs Postgres (يتطلب خادم). السياق: pipeline-production-line.md S2 — لا DB حية قبل DFR",
    assignee="arc-lead",
    priority="high",  # low/medium/high/critical — critical يكتب فوراً في amygdala
    type_="consultation_request"
)
# يعود: {"ticket_id": 101, "status":"open"} — يصل لـ arc-lead عبر WS خلال 50ms
```

**متابعة التذكرة:**

```python
# غيّر الحالة فقط open→in_progress→resolved→closed — أي قفزة →400
import httpx
httpx.patch("http://mcp.local/api/v1/tickets/101", headers={"X-API-Key":KEY,"X-Sender":"arc-lead"}, json={"status":"in_progress"})
```

**تصعيد تلقائي:** إن بقيت `open` لأكثر من 24 ساعة → النظام يحوّلها لـ `brd-ceo` وحده — لا تحتاج تدخلاً

## الخطوة 3 — القائد يكلف وكيلاً في غرفته

```python
# نفس send_guarded لكن recipient = وكيل غرفتك
await c.send_guarded(content="نفّذ مهمة T-101 — backend/app/Payments.php", evidence="...", task_id="T-101", context="...", recipient="bck-api-engineer")
```

## الخطوة 4 — كتابة القرار في الذاكرة (لا تضيّع المعرفة)

```python
await c.write_decision("اعتمدنا SQLite كقاعدة محلية — evidence: hq/engine/mcp_server/main.py:1", room="bck-lead")
# يظهر فوراً في hq/brain/cortex-decisions.md: - [2026-08-29 02:24 UTC] [bck-lead] اعتمدنا SQLite — evidence: ...
```

## الخطوة 5 — التدقيق — إن لم تُسجل، لم تحدث

```bash
# ابحث عن كل ما فعلته
curl -H "X-API-Key: $KEY" "http://mcp.local/api/v1/audit?agent=bck-api-engineer&type=violation"
# صدّر
curl -H "X-API-Key: $KEY" "http://mcp.local/api/v1/audit/export?format=csv" -o audit.csv
```

## 5 قواعد تمنع الضياع

1. **لا تبدأ بدون `task_id`+`context`** — SDK يرفض
2. **لا تسلم بدون `evidence: file:line`** — Gate يرفض
3. **لا تتجاوز قائدك** — 403 + violation
4. **لا تفترض — اسأل عبر `clarify()`** — 1-3 أسئلة حادة — 30 دقيقة ثم صعّد
5. **لا تعمل بدون تدقيق** — كل خطوة في `audit_logs`

## خارطة سريعة

```
أنت وكيل → فكّر تسلسلياً (5 خطوات) → نقص؟ → clarify() → جواب؟ أكمل : escalate() → brd-ceo
     ↓   تسليم → c.send_guarded → قائدك → c.consult_lead → قائد آخر → يكلف وكيله → يرد → كل شيء في audit + cortex
```

*Evidence: hq/core/standards/mcp-communication-standard.md:12 — client/mcp_client.py:1 — هذا الدليل يمنع العمل الأعمى*
