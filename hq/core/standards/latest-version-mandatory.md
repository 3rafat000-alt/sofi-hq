# التوجيه الإجباري — أحدث إصدار أولاً (Latest-Version Mandatory)

> **الحالة:** ملزم لكل غرفة ووكيل ونموذج — 2026-08-29 — أمر مالك مباشر — لا يُتجاوز — يعلو كل اجتهاد
> **المرجع الحي:** `opencode.json:13` (Context7 + DeepWiki) + `hq/core/standards/stacks-tech.md:1` + `AGENTS.md:10`
> **العقوبة:** كود بلا بحث/إثبات لأحدث إصدار = مرفوض L2 — تكرار = L3

---

## 1) القاعدة الذهبية — لا سطر قبل البحث والإثبات

> **أي تقنية تعمل بها — Laravel أو React أو Flutter أو Node أو Python أو مكتبة أو بنية — يجب أن تكون أحدث إصدار مستقر (Stable Latest) وقت التنفيذ — بلا استثناء.**

- إن كتبت `laravel new` أو `composer require` أو `npm install` أو `flutter pub add` أو `pip install` بلا بحث سابق → مرفوض
- البحث ليس اختيارياً — هو **خطوة إجبارية موثقة** قبل أول سطر كود — `file:line + exit code + link` إلزامي
- "أعرف هذه المكتبة" ليست حجة — معرفتك قديمة — الوثائق الحية هي الحكم (Context7)

---

## 2) البروتوكول الإجباري — 3 خطوات: ابحث → أثبت → طوّر

### الخطوة 1: ابحث (Search — إلزامي)

| التقنية | الأداة الإجبارية | ماذا تبحث | ماذا تحفظ كدليل |
|---------|------------------|-----------|-----------------|
| Laravel / PHP | 📚 Context7 + 🌌 DeepWiki | `laravel 11.x latest stable + php 8.3` | رابط Context7 + رقم الإصدار + تاريخ |
| React / Next.js | 📚 Context7 | `react 19.x / next 15.x latest` | رابط + إصدار |
| Flutter / Dart | 📚 Context7 + 🎯 Dart-Flutter MCP | `flutter 3.22.x / dart 3.4.x latest` | رابط + إصدار |
| Node / npm | 📚 Context7 | `node 20 LTS latest + package@latest` | `npm view <pkg> version` exit code |
| Python / pip | 📚 Context7 | `python 3.12.x / package latest` | `pip index versions <pkg>` |
| أي مكتبة | 📚 Context7 أولاً، 🌌 DeepWiki ثانياً | `<library> latest stable` | رابط + إصدار |

> **القاعدة:** `Context7` قبل أي كود يمس مكتبة (MCP-FLEET:1) — `DeepWiki` قبل أي ادعاء عن مستودع خارجي (MCP-FLEET:2) — لا عذر

### الخطوة 2: أثبت (Prove — إلزامي)

كل تسليم يجب أن يحوي كتلة إثبات:

```
## EVIDENCE: Latest-Version Proof
- Tech: Laravel
- Searched: Context7 "laravel 11.x — 2026-08-29 08:58+03:00"
- Found: v11.27.2 (stable) — source: https://laravel.com/docs/11.x/releases
- Installed: `composer create-project laravel/laravel:^11.27` → exit 0
- Verified: `php artisan --version` → Laravel 11.27.2
- File: backend/composer.json:12 — "laravel/framework": "^11.27"
```

- لا إثبات = لا قبول — حتى لو الكود يعمل — يُعاد للغرفة
- الإثبات يشمل `file:line` (أين كُتب الإصدار) + `exit code` (تثبيت ناجح) + `link` (مصدر حي)

### الخطوة 3: طوّر (Develop — على الأحدث)

- طوّر على الأحدث فقط — لا `laravel 10` إن كان `11` مستقراً — لا `react 18` إن كان `19` مستقراً
- إن كان الأحدث `RC` أو `beta` → استخدم آخر `stable` — اذكره صراحة في الإثبات
- حدّث `composer.json / package.json / pubspec.yaml / requirements.txt` إلى `^latest` — لا `~old` — مع `composer update` / `npm update` موثق

---

## 3) البنية والتقنيات — كل شيء أحدث إصدار

- **Laravel:** آخر 11.x مستقر — PHP 8.3 — `laravel/framework ^11.x` — `php >=8.3`
- **React/Next:** آخر 19.x / 15.x — `react ^19` — `next ^15`
- **Flutter/Dart:** آخر 3.22.x / 3.4.x — `flutter upgrade` قبل كل مشروع
- **Node:** آخر 20 LTS — `nvm install --lts`
- **Python:** آخر 3.12.x — `pyenv install 3.12`
- **قواعد البيانات:** PostgreSQL 16.x / Redis 7.x — لا 14 قديم بلا مبرر
- **أي مكتبة/أداة:** `npm view <pkg> version` أو `pip index versions` أو `composer show` — قبل التثبيت

> **الاستثناء الوحيد:** مشروع قائم `projects/sakk` يبقى على إصداره المقفل حتى يأمر `brd-ceo` بترقية مجدولة عبر `migrate + test + rollback` — لا ترقية صامتة في الإنتاج

---

## 4) المسؤولية والعقوبة

- **الوكيل:** مسؤول عن بحثه وإثباته — لا يمرر "أظن أن الإصدار ..." — يمرر `link + exit code`
- **قائد الغرفة:** يراجع الإثبات قبل الدمج — إثبات ناقص = رفض (Law 8)
- **sec-lead:** يفحص التراخيص على الأحدث (Law 15) — GPL في الأحدث = فيتو حتى لو كان قديماً مسموحاً
- **العقوبة:** أول خرق L2 (إعادة) — تكرار L3 (تجميد + brd-arbiter) — إخفاء إصدار قديم = L2

---

## 5) كيف تذكرها في كل تسليم — قالب إجباري

> **قبل كل كود تضع:**
> `// Latest-Version Proof: <tech> <version> via Context7 <link> — 2026-08-29 — exit 0 — file:line`

> **وفي تقرير التسليم تضع:**
> `EVIDENCE: Latest-Version — <tech> <version> — Context7 search 08:58+03:00 — composer.json:12 — exit 0`

---

> **الخلاصة:** من يعلم بهذا التوجيه يجب أن يبحث ويثبت ويطور لأحدث إصدار — لا عذر بالمعرفة القديمة — التقنية تتغير يومياً — وأنت تتغير معها — وإلا فعملك مرفوض.
