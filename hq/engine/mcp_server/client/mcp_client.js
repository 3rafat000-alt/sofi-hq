// FILE: hq/engine/mcp-server/client/mcp_client.js
// SOFI MCP Client SDK — JavaScript (Node/Browser) — مرن واحترافي
// Usage: const c = new MCPClient("bck-api-engineer"); await c.sendGuarded({content, evidence, taskId, context});

const BASE_REST = process.env.MCP_HOST ? `http://${process.env.MCP_HOST}:${process.env.MCP_PORT||8765}` : "http://127.0.0.1:8765";
const BASE_WS = process.env.MCP_HOST ? `ws://${process.env.MCP_HOST}:${process.env.MCP_PORT||8765}` : "ws://127.0.0.1:8765";
const API_KEY = process.env.SOFI_MCP_API_KEY || "dev-key-change-me";

export class MCPClient {
  constructor(agentId, {apiKey=API_KEY, baseRest=BASE_REST, baseWs=BASE_WS}={}) {
    this.agentId = agentId;
    this.apiKey = apiKey;
    this.baseRest = baseRest;
    this.baseWs = baseWs;
    this.ws = null;
  }

  async sendToLeadRest({content, evidence="client/mcp_client.js:send", recipient, taskId, context}) {
    // recipient auto = lead of own room if not given — server will resolve too
    const headers = {"X-API-Key": this.apiKey, "X-Sender": this.agentId, "Content-Type":"application/json"};
    const body = {recipient: recipient || this._leadForAgent(), content, evidence, sender: this.agentId};
    const r = await fetch(`${this.baseRest}/api/v1/message`, {method:"POST", headers, body: JSON.stringify(body)});
    const j = await r.json();
    if (r.status===429) throw new Error(`RATE_LIMITED — انتظر ${r.headers.get("Retry-After")}ث`);
    if (r.status===403) throw new Error(`FORBIDDEN Law2 — ${j.message}`);
    if (!r.ok) throw new Error(j.message || r.statusText);
    return j.data;
  }

  async consultLead({subject, description, assignee, priority="medium", type="consultation_request"}) {
    const headers = {"X-API-Key": this.apiKey, "X-Sender": this.agentId, "Content-Type":"application/json"};
    const body = {subject, description, priority, type, assignee, requester: this.agentId};
    const r = await fetch(`${this.baseRest}/api/v1/tickets`, {method:"POST", headers, body: JSON.stringify(body)});
    const j = await r.json();
    if (!r.ok) throw new Error(j.message);
    return j.data;
  }

  async clarify({questions, missing, thinking="Sequential-Thinking §15 — عائق في الخطوة 2/3", assignee, priority="high"}) {
    if (!questions || questions.length<1 || questions.length>3) throw new Error("اسأل حاداً: 1-3 أسئلة فقط");
    const description = JSON.stringify({questions, missing, thinking});
    return this.consultLead({subject:`[نقص] ${String(missing).slice(0,80)}`, description, assignee: assignee || null, priority, type:"clarification_request"});
  }

  async escalate({subject, description, priority="critical", assignee="brd-ceo"}) {
    return this.consultLead({subject:`[تصعيد] ${String(subject).slice(0,80)}`, description, assignee, priority, type:"escalation"});
  }

  async connectWs() {
    const isLead = this.agentId.includes("-lead") || this.agentId.startsWith("brd-");
    const path = isLead ? "lead" : "agent";
    const uri = `${this.baseWs}/ws/${path}/${this.agentId}?api_key=${this.apiKey}`;
    // Node needs 'ws' package; browser uses native WebSocket
    if (typeof WebSocket !== "undefined") {
      this.ws = new WebSocket(uri);
      await new Promise((res, rej)=>{ this.ws.onopen=res; this.ws.onerror=rej; });
    } else {
      const {default: WS} = await import("ws");
      this.ws = new WS(uri);
      await new Promise((res, rej)=>{ this.ws.once("open", res); this.ws.once("error", rej); });
      this.ws.sendJson = (o)=> this.ws.send(JSON.stringify(o));
      const origOn = this.ws.on;
    }
  }

  async sendToLeadWs({content, evidence="client/mcp_client.js:ws", recipient, retries=3}) {
    for (let attempt=0; attempt<retries; attempt++) {
      try {
        if (!this.ws || this.ws.readyState!==1) await this.connectWs();
        const payload = {content, evidence, ...(recipient?{recipient}:{})};
        this.ws.send(JSON.stringify(payload));
        const raw = await new Promise((res, rej)=>{
          const t=setTimeout(()=>rej(new Error("WS timeout")), 3000);
          this.ws.onmessage = (e)=>{ clearTimeout(t); res(typeof e.data==="string"?e.data:e.data); };
          // for ws lib
          if (this.ws.once) this.ws.once("message", (d)=>{ clearTimeout(t); res(d.toString()); });
        });
        const data = JSON.parse(raw);
        if (data.success===false) {
          if (data.error?.code==="FORBIDDEN") throw new Error(data.message);
          throw new Error(data.message);
        }
        return data;
      } catch(e) {
        this.ws=null;
        if (attempt===retries-1) return this.sendToLeadRest({content, evidence, recipient});
        await new Promise(r=>setTimeout(r,1000));
      }
    }
    return this.sendToLeadRest({content, evidence, recipient});
  }

  async sendGuarded({content, evidence, taskId, context, recipient}) {
    if (!taskId || !context || !evidence) throw new Error("لا ترسل بدون taskId و context و evidence — عمل أعمى مرفوض");
    try { return await this.sendToLeadWs({content, evidence, recipient}); } catch(e) {
      if (e.message.includes("FORBIDDEN")) throw e;
      return await this.sendToLeadRest({content, evidence, recipient});
    }
  }

  _leadForAgent() { return null; } // server resolves to own lead if null

  async close(){ try{ this.ws?.close(); }catch{} }
}
