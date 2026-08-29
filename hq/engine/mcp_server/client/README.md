## FILE: hq/engine/mcp_server/client/README.md
# MCP Client SDK — دليل المطور (Python + JS)

## لماذا SDK؟
حتى لا يعمل الوكيل أعمى — SDK يفرض `evidence + taskId + context` ويختار القناة المرنة تلقائياً (WS → REST).

## Python — استخدام

```python
import asyncio
from hq.engine.mcp_server.client.mcp_client import MCPClient

async def main():
    c = MCPClient("bck-api-engineer")  # يقرأ .env تلقائياً
    # 1) إرسال محمي — لن يرسل بدون سياق
    await c.send_guarded(
        content="تم إنجاز API الدفع — backend/app/Payments.php:42",
        evidence="hq/engine/mcp_server/client/mcp_client.py:42",
        task_id="T-101",
        context="نفّذ حسب openapi.yaml: POST /pay — CONTEXT.md:5",
        recipient="bck-lead"
    )
    # 2) استشارة بين قادة
    await c.consult_lead(subject="هل نستخدم SQLite؟", description="...", assignee="arc-lead", priority="high")
    # 3) كتابة قرار في الذاكرة
    await c.write_decision("اعتمدنا SQLite", room="bck-lead")
    await c.close()

asyncio.run(main())
```

## JS — استخدام

```js
import {MCPClient} from "./hq/engine/mcp_server/client/mcp_client.js";
const c = new MCPClient("bck-api-engineer");
await c.sendGuarded({content:"تم", evidence:"client.js:10", taskId:"T-101", context:"openapi.yaml:5"});
await c.consultLead({subject:"مراجعة", description:"...", assignee:"arc-lead"});
```

## المرونة
- يحاول WS أولاً (6ms avg) — إن فشل 3 مرات 1ث → يتحول REST تلقائياً — لا تدخل بشري
- Rate 429 → يقرأ `Retry-After` ويرمي خطأ واضح
- FORBIDDEN Law2 → يرمي `PermissionError` فوراً — لا يحاول REST

## لا عمل أعمى
`send_guarded` يرفض إن كان `taskId` أو `context` أو `evidence` فارغ — `ValueError: لا ترسل بدون ... — عمل أعمى مرفوض`

*Evidence: hq/engine/mcp_server/client/mcp_client.py:1 — hq/core/standards/mcp-communication-standard.md:12*
