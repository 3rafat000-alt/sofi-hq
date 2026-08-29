## FILE: hq/core/standards/mcp-communication-standard.md
# MCP Communication Standard — بروتوكول التواصل الاحترافي المرن لـ SOFI
> **Status:** Binding — v1.0 — 2026-08-29
> **Authority:** يكمّل القوانين 2 و3 و4 و7 و10 و13 — لا يلغيها — يحوّلها إلى بروتوكول تنفيذي
> **Scope:** كل الغرف الـ15 والقادة والـ114 وكيل — كل تواصل يمر عبر `mcp.local:8765` أو `127.0.0.1:8765`
> **Principle:** مرن في القناة (WS+REST)، صارم في القانون (عزل+تدقيق+أثر) — لا عمل أعمى

---

## 1) الهدف — لماذا هذا البروتوكول؟
- يمنع العمل الأعمى: كل رسالة تحمل سياق + دليل + معرف مهمة — الوكيل لا يبدأ بدونها
- مرن: WS للفورية، REST للطوارئ — يتحول تلقائياً — لا يتوقف
- احترافي: كل شيء موثق file:line + ISO8601 + تدقيق غير قابل للتعديل — لا ضياع

## 2) القناتان — مرونة بلا كسر قانون

| القناة | متى | زمن | كيف |
|---|---|---|---|
| **WebSocket** `/ws/agent/{id}?api_key=KEY` و `/ws/lead/{id}` | أساسي — فوري | ≤50ms | اتصال دائم — يرسل `{content, recipient?, evidence}` ويستقبل `{status:"delivered",id}` |
| **REST** `POST /api/v1/message` + `POST /api/v1/tickets` | احتياطي تلقائي — عند قطع WS أو بين غرف | ≤100ms | نفس النماذج — `X-API-Key` + `X-Sender` |

**القاعدة الذهبية:** العميل يحاول WS أولاً — إن فشل 3 مرات (1ث بين كل محاولة) يتحول لـ REST وحده — لا تدخل بشري — SDK يفعلها

## 3) الهوية — من أنت ومن تخاطب

- **الوكيل:** `bck-api-engineer` ينتمي لـ `backend` وقائده `bck-lead` — يخاطب قائده فقط
- **القائد:** `bck-lead` يخاطب `arc-lead` عبر `POST /api/v1/tickets` — لا يخاطب وكيل غرفة أخرى مباشرة إلا للتصعيد
- **المؤسسة:** `brd-ceo` يستقبل التصعيد بعد 24 ساعة — قرار نهائي

**التحقق:** أول سطر في كل إرسال هو `validate_cross_room(sender, recipient)` — `hq/engine/mcp_server/ticket_bus.py:31` — cross-room agent→agent = 403 + violation

## 4) أنواع الرسائل — 4 فقط — لا غير

| النوع | الحقل `type` | متى | مثال |
|---|---|---|---|
| `task_assignment` | تكليف وكيل بمهمة | قائد → وكيل في غرفته | "نفّذ API الدفع — evidence: backend/spec.md:12" |
| `consultation_request` | استشارة بين قادة | قائد → قائد | "هل نستخدم SQLite؟" |
| `escalation` | تصعيد لـ brd-ceo | نظام → brd-ceo بعد 24h | "تذكرة #101 لم تُحل" |
| `gate_check` | طلب اجتياز بوابة | قائد → 09/10 | "راجع التصميم قبل DFR" |

أي `type` غير معروف → 422 `VALIDATION_ERROR` — Pydantic يرفض

## 5) هيكل الرسالة — لا عمل بدون سياق

**الحد الأدنى لكي لا تعمل أعمى — كل رسالة يجب أن تحمل:**

```json
{
  "recipient": "bck-lead",
  "content": "تم إنجاز API الدفع — الملف backend/app/Payments.php:42",
  "evidence": "hq/engine/mcp_server/main.py:42",
  "task_id": "T-101",
  "context": "نفّذ حسب openapi.yaml: POST /pay — راجع CONTEXT.md:5"
}
```

| الحقل | مطلوب؟ | لماذا يهمك |
|---|---|---|
| `recipient` | نعم | لمن ترسل — بدونها لا يعرف |
| `content` | 1-4096 حرف | ماذا أنجزت — عربي واضح + إنجليزي بين قوسين |
| `evidence` | مستحسن (يصبح مطلوب في Gate) | `file:line` يثبت أنك لم تخترع |
| `task_id` | نعم في المهام | يربط الرسالة بالتذكرة — لا ضياع |
| `context` | نعم في التكليف | مرجع للعقد — يمنع الاجتهاد خارج التصميم |

**رسالة بدون `content` أو أطول من 4096 → 422 — `المحتوى فارغ/يتجاوز الحد`**

## 6) دورة حياة التذكرة — لا تقفز

```
open → in_progress → resolved → closed
```
- إنشاء: `POST /api/v1/tickets` → `open` — يشعر `assignee` عبر WS خلال 50ms — إن `priority=critical` يكتب في `amygdala-incidents.md` فورًا
- تحديث: `PATCH /api/v1/tickets/{id} {"status":"in_progress"}` — أي قفزة (مثل `open→closed`) → 400 `انتقال حالة غير مسموح`
- تصعيد: كل ساعة يفحص `escalate_stale_tickets()` — إن `now - created_at ≥ 24h` و `status=open` → `assignee=brd-ceo` + `type=escalation` + سطر في التدقيق

## 7) التسليم الهرمي — كيف لا تضيع

```
وكيل (bck-api-engineer) --WS--> قائده (bck-lead) --REST /tickets--> قائد آخر (arc-lead) --task_assignment--> وكيله (arc-api-architect)
```

1. الوكيل يرسل لقائده فقط — لا يرى غرفة أخرى — `agents_mcp.py:send_message`
2. القائد يستقبل — يتحقق — يسجل في `messages.db` + `audit_logs` — يدفع عبر WS إن كان المستقبل متصلاً وإلا `pending`
3. الاستشارة بين قادة تمر عبر Ticket Bus فقط — `leads_mcp.py:create_ticket` — لا يوجد `agent→agent` حتى عبر دالة داخلية
4. الانتهاك يسجل `cross_room_attempt blocked` — `ticket_bus.py:validate_cross_room` — لا صف في `messages.db`

## 8) الذاكرة — فصل صارم (Law 7)

- قرار → `POST /api/v1/memory/decision` → `hq/brain/cortex-decisions.md` بصيغة `- [YYYY-MM-DD HH:MM UTC] [room/lead] النص — evidence: file:line` — `memory.py:write_decision`
- جلسة → `hippocampus-sessions.md` — حادث → `amygdala-incidents.md` — درس → `org_lessons/LESSONS.md`
- محاولة كتابة مشروع في `hq/brain/` → مرفوضة — فصل لا يُكسر

## 9) التدقيق — 100% غير قابل للتعديل

- كل عملية تكتب في `audit_logs` — حقول `timestamp ISO8601, agent_id, action, result, evidence, details` — `ticket_bus.py:write_audit`
- الجداول `messages` و `audit_logs` عليها `TRIGGER BEFORE UPDATE/DELETE RAISE(ABORT)` — `schema.sql:CREATE TRIGGER no_update_messages`
- البحث: `GET /api/v1/audit?agent=bck-api-engineer&type=violation&page=1&limit=20`
- التصدير: `GET /api/v1/audit/export?format=json|csv&from=2026-08-20&to=2026-08-29&room=backend`

## 10) الأمان — احترافي

- كل طلب يحتاج `X-API-Key` من `.env SOFI_MCP_API_KEY` — غياب/خطأ → 401 `مفتاح API غير صحيح` — لا يكشف تفاصيل
- معدل: 100/دقيقة لكل `agent_id` — تجاوز → 429 + `Retry-After: 60` + `rate_limited` في التدقيق
- تحقق صارم Pydantic: `content 1-4096`, `priority low/medium/high/critical`, `type` 4 قيم — يمنع حقن SQL/JSON
- لا سر في الكود — `grep -r "sk-" --include="*.py"` → 0 — `.env.example` فقط `sk-REPLACE_ME`

## 11) envelope الموحد — كل استجابة (api-envelope.md v1)

```json
{"success":true,"message":"Message delivered","data":{"id":42},"error":null,"meta":{"request_id":"uuid","timestamp":"2026-08-29T02:23:47Z","envelope_version":"v1","pagination":null}}
{"success":false,"message":"ممنوع التواصل المباشر بين الغرف — أرسل عبر قائد غرفتك","data":null,"error":{"code":"FORBIDDEN","message":"Cross-room blocked by Law 2"},"meta":{}}
```
HTTP → Code: 401 UNAUTHENTICATED, 403 FORBIDDEN, 422 VALIDATION_ERROR, 429 RATE_LIMITED, 500 SERVER_ERROR (بلا تفاصيل)

## 12) ما يمنع العمل الأعمى — 5 قواعد ذهبية

1. **لا تبدأ بدون `task_id` و `context`** — التذكرة هي المصدر — لا رسالة شفهية
2. **لا تسلم بدون `evidence: file:line`** — `backend/app/Payments.php:42` يثبت
3. **لا تتجاوز قائدك** — أي محاولة cross-room = 403 + violation — ستُسجل وتُحاسب
4. **لا تفترض — اسأل عبر Ticket** — `consultation_request` بين القادة — 50ms يصلك الرد
5. **لا تعمل بدون تدقيق** — كل خطوة في `audit_logs` — إن لم تُسجل، لم تحدث

## 13) المرونة — كيف لا يتوقف

- WS مقطوع → SDK يعيد الاتصال 3 مرات 1ث → يتحول REST تلقائياً → الرسالة تصل `pending` وتُسلم عند عودة WS
- DB مقفل → WAL + timeout 10s + retry — لا فقدان
- Rate 429 → اقرأ `Retry-After` وانتظر 60ث — لا ترسل عشوائياً

## 14) الأداء المتوقع

- REST sequential P95 8.9ms (200) — WS avg 6.6ms — 114 concurrent 0 سقوط — Memory 39M/500M — DB 148KB/140KB — `kpi-dashboard.md`

---

*Evidence: hq/engine/mcp_server/main.py:1 — ticket_bus.py:31 — schema.sql:CREATE TRIGGER — api-envelope.md:6 — هذا المعيار مكمل للقوانين، لا يلغيها*

---

## 15) تفكير تسلسلي قبل أي فعل — Sequential-Thinking (لا سكربت أعمى)

> **الفكرة:** الوكيل اليوم لا ينفذ سكربت "احترافي مرن" — بل يفكر خطوة خطوة قبل أي فعل، مثلما يفكّر المهندس: ماذا أريد؟ ما عندي؟ ما الناقص؟ ماذا أفعل؟ ثم يعمل. **التسلسل إلزامي — الخطوات لا تُقفز.**

### السلسلة الإلزامية (5 خطوات — يُمرّرها الوكيل ذهنياً قبل أن يلمس أي ملف)

| # | الخطوة | السؤال | الناتج |
|---|---|---|---|
| 1 | **الفهم** | ما الطلب الحقيقي؟ من الطالب؟ ما الهدف؟ | إعادة صياغة بسطر واحد |
| 2 | **السياق** | أين العقد؟ (openapi/CONTEXT.md) — هل التفاصيل موجودة؟ | مرجع `file:line` — أو **نقص** |
| 3 | **الفحص** | هل كل المدخلات متوفرة؟ هل هناك تعارض؟ | قائمة مدخلات ✓ / ✗ |
| 4 | **الخطة** | ما الخطوات؟ ما الترتيب؟ ما الخطر؟ | 2-4 خطوات + مخاطرة |
| 5 | **التحقق** | كيف أعرف أني انتهيت؟ ما المعيار؟ | معيار قبول + enumerable |

**القاعدة:** إن انتهت الخطوة 2 أو 3 بـ **نقص/غموض/تعارض** → الوكيل لا يخمّن — ينتقل فوراً إلى §16 (حلقة الأسئلة) — التخمين = عمل أعمى = L2.

### متى تستخدم أداة Sequential Thinking فعلياً؟
- معالجة أي طلب يدخل من بوابة `gtw-intake-reformer` — كل خطوة تفكير تظهر كتسلسل قابل للتتبع
- أي عقدة مشكلة معقدة: تعارض، نقص، غموض، تبعية غير واضحة (مثل قانون 13: triple engine للحرج)
- مراجعة التصميم قبل التسليم: 5 خطوات تُظهر "لماذا هذا القرار؟" — لا اجتهاد خارج العقد

---

## 16) حلقة الأسئلة والتصعيد — Time to Think, Ask, Escalate (لا ضياع ولا تخمين)

> الدورة: **فكر → اسأل → صعّد** — أي مشكلة أو نقص وقت العمل يفتح هذه الحلقة — النظام لا يتجاهل ولا يخمّن.

```
[نقص/مشكلة/تعارض يظهر]
      │
      ▼
① توقف فوري — لا تنفّذ "تخميناً" — أعلن الحالة
      │
      ▼
② فكّر تسلسلياً (§15): ما الناقص؟ لماذا انحصر؟ ما الخيارات؟
      │
      ▼
③ اسأل: clarification_request (تذكرة نوع clarification_request)
   - 1 إلى 3 أسئلة حادة فقط — محددة — بلا أسئلة عامة
   - المرسل: الوكيل → قائده | القائد → القائد صاحب القرار
      │
      ▼
④ انتظر الجواب — مهلة 30 دقيقة
      │
      ▼
⑤ أجب؟ ──لا──► صعّد (escalation) فوراً إلى brd-ceo مع الأسئلة والسياق
      │
      ▼
   نعم: أعد تقييم §15 — أكمل العمل على السياق الجديد
```

### حقول تذكرة `clarification_request` — الوصف يحمل 1-3 أسئلة حادة بصيغة JSON

```json
{
  "subject": "نقص: عنوان المهمة",
  "description": "{\"questions\": [\"هل الهدف كذا؟\", \"أين ملف العقد؟\", \"ما المعيار؟\"], \"missing\": \"openapi.yaml غير معتمد\", \"thinking\": \"الخطوة 3 — مدخلات ناقصة\"}",
  "priority": "high",
  "type": "clarification_request",
  "assignee": "bck-lead"
}
```

**مهلة 30 دقيقة** — `escalate_stale_tickets()` يفحصها مع فحص الـ24h — تذكرة `clarification_request` فات موعدها تتحول `escalation` → `brd-ceo` مع نص الأسئلة — القرار النهائي للمؤسسة.

### تصعيد فوري (بدون انتظار 24h) — متى؟
- `priority=critical` (مال/أمان/إنتاج/قاعدة بيانات — قانون 1 حاسم دائماً)
- تعارض مباشر بين قائدين لا يحسم في جولة واحدة (صعّد → brd-arbiter عبر brd-ceo — قانون 14)
- نقص يمنع التقدم كلياً عند وكيل — قائده لا يملك الجواب → صعّد فوراً

### قواعد الحلقة الذهبية
1. **لا تخمين** — توقف واسأل — التخمين عمل أعمى = L2
2. **اسأل حاداً** — 1-3 أسئلة تحسم المسار — لا أسئلة مفتوحة عريضة
3. **صعّد ولا تختبئ** — لا تنتظر أن يحل الوقت المشكلة — التصعيد ليس فشلاً، هو احترافية
4. **كل خطوة تُسجّل** — السؤال والجواب والتصعيد في `audit_logs` + `messages.db`

---

## 17) الخلاصة — كيف يكون الوكيل محترفاً اليوم؟

```
فكّر تسلسلياً (§15) → نقص؟ → اسأل حاداً (§16) → لا جواب؟ → صعّد (§16) → اعمل بالأكيد
```

- بداية أي عمل: **فهم → سياق → فحص → خطة → تحقق** (§15)
- عند أي عقبة: **توقف → فكّر → اسأل 1-3 → انتظر 30 دقيقة → صعّد** (§16)
- لا سكربت "مرن" يخمّن — عقل تسلسلي يسأل ويصعّد — هذا ما يمنع الضياع

*Evidence: hq/core/standards/mcp-communication-standard.md:1 — models.py:TicketType — client/mcp_client.py:clarify — هذا القسم يفعّل Sequential-Thinking وحلقة الأسئلة/التصعيد بحسب أمر المالك 2026-08-29*

---

*v1.1 — 2026-08-29 — أقسام 15/16/17 مضافة بتوجيه المالك: طريقة تفكير تسلسلي + أسئلة وتصعيد — append-only*
