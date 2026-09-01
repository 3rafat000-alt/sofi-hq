## FILE: hq/core/design/diagrams/README.md
# مجلد المرئيات الحاكمة — SOFI HQ Visual Diagrams Layer v1
> **intake_id:** SOFI-HQ-INT-007 · **المالك:** 03 Design (`dsn-lead`) + 13 Knowledge (`knw-lead`)
> **القاعدة:** Mermaid هو المصدر الوحيد — SVG/PNG مُصدّر آلياً — لا تحرر SVG/PNG يدوياً

---

## ما هنا

| # | الملف | المصدر النصي `file:line` | الوصف |
|---|-------|---------------------------|-------|
| D1 | `d1-use-case.mmd` → `.svg` + `.png` | `hq/core/nexus/registry.yaml:6` | Use-Case / Agent Registry — 15 غرفة · 114 وكيلاً |
| D2 | `d2-pipeline-s1-s6.mmd` → `.svg` + `.png` | `hq/core/nexus/pipeline.yaml:8` | Pipeline S1→S6 + DFR gate |
| D3 | `d3-gateway-routing.mmd` → `.svg` + `.png` | `README.md:80` + `hq/core/domain/rooms/14-gateway/charter.md:86` | Gateway Routing + Clarification 24h + Lane |
| D4 | `d4-layered-architecture.mmd` → `.svg` + `.png` | `hq/core/design/system-ddd-blueprint.md:42` | 4 طبقات — Dependency نزولاً فقط |
| D5 | `d5-context-map.mmd` → `.svg` + `.png` | `hq/core/domain/context-map.yaml:11` | Context-Map — 15 عقدة + shared-kernel |
| D6 | `d6-gate-state-machine.mmd` → `.svg` + `.png` | `hq/core/nexus/gates.yaml:1` | Gate State Machine G0→G8 + DFR |
| D7 | `d7-ticket-bus-sequence.mmd` → `.svg` + `.png` | `AGENTS.md:40` + `hq/core/application/bus/` | Ticket-Bus Sequence — agent→lead→ceo→user |
| D8 | `d8-deployment-caddy.mmd` → `.svg` + `.png` | `hq/engine/Caddyfile` + `hq/engine/scripts/bootstrap-live.sh:6` | Deployment — Caddy canon + sites |
| D9 | `d9-memory-isolation.mmd` → `.svg` + `.png` | `AGENTS.md:44` | Memory Isolation — Org vs Project (Law 7) |

**كل مرئي بثلاث صيغ:** `.mmd` (مصدر — 20-40 سطر) + `.svg` (عرض — وضوح لا نهائي) + `.png` (شرائح/بريد — ≤200KB مضغوط)

**المرآة العامة:** `docs/diagrams/` — نسخة 1:1 من `hq/core/design/diagrams/*.{svg,png}` للعرض في GitHub Pages — تُنسخ عبر `cp hq/core/design/diagrams/*.{svg,png} docs/diagrams/`

---

## كيف تُصدّر (أمر واحد — كل شيء محلي مجاني)

```bash
# تثبيت Mermaid CLI (MIT — License-check: allowed)
npm install -g @mermaid-js/mermaid-cli@10.9.0
# أو npx بدون تثبيت:
npx -p @mermaid-js/mermaid-cli@10.9.0 mmdc --help

# تصدير SVG (9 ملفات)
npx @mermaid-js/mermaid-cli@10.9.0 --input hq/core/design/diagrams/d1-use-case.mmd --output hq/core/design/diagrams/d1-use-case.svg --outputFormat svg --backgroundColor transparent
# كرر لـ D2-D9 أو دفعة واحدة (إن دُعم):
for f in hq/core/design/diagrams/d*.mmd; do npx @mermaid-js/mermaid-cli --input "$f" --output "${f%.mmd}.svg"; done

# تصدير PNG (9 ملفات — مضغوط)
for f in hq/core/design/diagrams/d*.mmd; do npx @mermaid-js/mermaid-cli --input "$f" --output "${f%.mmd}.png" --outputFormat png --scale 2; done

# ضغط (اختياري — SVGO + optipng)
npx svgo --multipass hq/core/design/diagrams/*.svg
optipng -o7 hq/core/design/diagrams/*.png

# مرآة docs
cp hq/core/design/diagrams/*.svg docs/diagrams/
cp hq/core/design/diagrams/*.png docs/diagrams/

# فحص
python3 hq/core/tooling/evidence_guard.py hq/core/design/diagrams --strict  # → 0 broken exit 0
ls hq/core/design/diagrams/*.{mmd,svg,png} | wc -l  # → 27
ls docs/diagrams/*.{svg,png} | wc -l          # → 18
```

**عند فشل `mmdc`:** رسالة `Parse error on line X: Unexpected token` → أصلح السطر X في `*.mmd` وأعد — لا تسليم بنصف تصدير.

---

## الهوية البصرية (مقفلة v1)

- **عنبي #6e1b2d** — الغرف الحاكمة/Lead — بدل #1f0810 الممنوع
- **رمادي #f5f5f5** — خلفية groups
- **أزرق #2563eb** — أسهم مسموحة provides/requires
- **أحمر #dc2626** — ممنوع forbidden / خط عزل Memory
- **برتقالي #f59e0b** — on_fail / تحذير
- **تباين ≥4.5:1** — WCAG AA — خط ≥18sp — كل صورة `alt` + `aria-label` — RTL مرآة + `prefers-reduced-motion`

---

## الصيانة

- أي تغيير في `hq/core/nexus/registry.yaml:6` أو `hq/core/nexus/pipeline.yaml:8` أو `hq/core/domain/context-map.yaml:11` → حدث `*.mmd` المقابل في نفس الـ PR — SLA ≤24h
- `knw-reflector` ritual كل 10 turns يذكر بتحديث المرئيات — `hq/core/tooling/count_sync.py` يكشف drift العدد
- لا تحرر SVG/PNG يدوياً — المصدر Mermaid وحده

---

## التراجع

```bash
git revert <commit>                    # يرجع 54 كياناً
# أو حذف مجلد:
rm -rf hq/core/design/diagrams docs/diagrams
git checkout -- README.md hq/core/design/system-ddd-blueprint.md
```

---

## Evidence

- `hq/core/design/system-ddd-blueprint.md:1` (بيت التصميم الحاكم)
- `hq/core/nexus/registry.yaml:6` (المصدر — 15·114)
- `hq/core/tooling/evidence_guard.py:1` (0 broken)
- `hq/core/tooling/registry_guard.py:1` (114/114)
