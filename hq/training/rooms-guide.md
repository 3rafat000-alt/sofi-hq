# The 15 SOFI Rooms Guide — How Does Your AI Team Work?

> **Document type:** a comprehensive reference guide addressed to the owner — explaining SOFI's 15 rooms and how each one works in plain language.
> **Prepared by:** Dana Al-Atari (`knw-doc-writer`) — Knowledge Room 13, executing ticket `HQ-INT-001` by order of room lead Sireen Al-Zein (`knw-lead`).
> **Date prepared:** 2026-08-22
> **Golden rule of this guide:** every piece of information here comes only from official sources: the 15 room charters (`hq/core/room_charters/*/CHARTER.md`), the official room registry (`hq/core/nexus/registry.yaml`), the constitution (`AGENTS.md`), and the memory index (`hq/brain/brain-index.md`). No interpretation or additions from outside them.

---

## 1) Introduction: What Is SOFI and the Idea of "Rooms"?

**SOFI** is a complete AI operating system built in the image of a real company: it has leadership, specialized departments, binding rules, and memory that never forgets.

The core idea is very simple:

- **Agent:** one AI program specialized in a specific mission — such as "UI engineer" or "fact checker". A single agent does not know everything, but is highly proficient within its specialty.
- **Room:** a department grouping agents who share one field, led by a single **room lead** accountable for their team. Exactly like a company: the accounting department has accountants and a department head.
- **CEO (`brd-ceo`):** the final decision-maker across the entire system. They receive requests after sorting, distribute them to rooms, then receive results and hand them to you.
- **Gates:** mandatory checkpoints between work stages — nine gates numbered G0 through G8. No stage moves to the next until it passes its own checkpoint, exactly as no product leaves a factory without passing quality inspection.

With this division SOFI operates as **15 rooms and 106 agents** (per the official registry), so nobody meddles outside their specialty, and no work reaches you except after inspection upon inspection and review.

---

## 2) How Does Work Flow? A Request's Journey from Start to Finish

### Step 1 — The Intake Gateway (reception desk)

Everything you write to SOFI enters first through the **Gateway Room (14)**, specifically an agent named `gtw-intake-reformer`. Its job:

1. To genuinely understand your request (even if vaguely stated).
2. To rephrase it into a clearer, more precise form before sending it inward.
3. To classify the task's size and determine its appropriate track.

There is no other path. Any work started outside this gateway counts as a constitutional violation that halts the system immediately.

### Step 2 — Track Classification: Three Tracks by Task Criticality

After understanding, the gateway classifies the request onto one of three tracks:

| Track | For what? | How does work flow? |
|---|---|---|
| 🟢 **Fast** | reads, checks, and queries, documentation research, or a very simple fix in a single file only — something safely reversible that touches neither money nor security nor the data schema | intake gateway ← one room lead ← delivery to you |
| 🟡 **Standard** | a new feature or medium change engaging one or two rooms | gateway ← CEO ← leads ← agents ← leads ← CEO ← you |
| 🔴 **Critical** | an irreversible decision or high risk | the full path: gateway ← CEO ← Board consultation (the security lead holds an absolute veto) ← rooms ← gates ← CEO ← you — with zero shortcuts |

**Real examples for each track:**

- 🟢 Fast: "How many rooms are in your system?" or "Open this file and tell me what's inside" or "Fix a misspelled word on one page." A question or trivial change reversible in a second.
- 🟡 Standard: "Add an About page to the project's site." A medium feature needing design then interface building — roughly two rooms and a complete flow with quality review before delivery.
- 🔴 Critical: "Change how payment data is stored" or "Deploy a new version to the live user-facing site." It touches money, the data schema, and production — no step may be shortened however small the work looks.

**Rules protecting this classification:**

- Doubt always raises classification upward (when torn between two tracks we choose the stricter).
- Money, security, live production, and the data schema = always critical, even if the change looks small.
- If higher risk appears during execution, the task promotes immediately to a higher track — promotion only ascends, never descends.

### Step 3 — The CEO Distributes Work

On the standard and critical tracks, the CEO (`brd-ceo`) receives the classified request, decides which rooms will participate, and directs each room lead with what their department needs. On critical decisions they consult the **Board** (room 00) before deciding — while remaining the final decision-maker.

### Step 4 — Rooms Execute Within Their Boundaries

Each room executes only its own part; inside it the agents work under their lead's supervision. Rooms do not talk to each other directly — inter-department communication passes exclusively through the leads, just as an employee from one department never negotiates on their own with an employee from another.

### Step 5 — Hierarchical Delivery Back to You

Nobody jumps over anybody. Delivery always follows this chain:

```
Agent → its room lead → CEO → you (the owner)
```

- The agent completes its task, records completion evidence, then hands off to its room lead.
- The lead reviews the work, unifies it, then hands it to the CEO.
- The CEO reviews and delivers the final result to you in understandable language.

Absolutely forbidden: an agent delivering work to you directly, an agent communicating with another room on its own, or a room lead executing the work personally instead of their team.

### Three Core Concepts That Explain the System's Discipline

**First — completion evidence (proof):**
No delivery is accepted on words alone. Every change must arrive with its proof: which file was modified and at exactly which line, the result of running any command (success or failure), and a screenshot or log showing the final result. Think of it like a purchase invoice: without an invoice the shipment is not accepted. Without evidence the delivery is rejected however excellent.

**Second — the work order (RCCF):**
Nobody starts executing anything without a formal work order — one precise sheet answering: what exactly do we want? why? who will execute? and how will we know it succeeded? Like a company's purchase order: it prevents random work and conflicting efforts.

**Third — organization memory versus project memory:**
SOFI has two separate memories that never mix:

| | Organization memory | Project memory |
|---|---|---|
| **Where does it live?** | the central `hq/brain/` folder | inside every project, in its own folder `projects/<project-name>/brain/` |
| **What does it talk about?** | the SOFI system itself and its team: its decisions, rules, incidents, and lessons — not any specific project | that project alone: its context, decisions, deliveries, and lessons |
| **What does it store?** | permanent decisions (the "CORTEX" region), session logs ("HIPPOCAMPUS"), emergencies ("AMYGDALA"), planning ("PREFRONTAL"), routing ("THALAMUS"), daily routine ("BASAL-GANGLIA"), and the tools registry ("TOOLS") | four files per project: context, decisions, delivery log, lessons |

And the decisive rule: a lesson or decision belonging to a particular project is never written directly into organization memory. Promotion happens only with the CEO's approval when the lesson recurs across different projects, or when the decision touches SOFI's own structure.

---

## 3) The 15 Rooms, One by One

> **A note before starting:** the "code" is the abbreviation appearing in each agent's name (for example agent `brd-ceo` takes its first letters from the Board room code `brd`). The full operational agent definitions live in dedicated files — the charters call that folder the single source for fine details.

---

### Room 00 — Boardroom

**Code:** `brd` · **Lead:** `brd-ceo` · **Agents:** 7

**Its mission in two lines:**
This is the room of top leadership, governance, and decisive decision-making. From it directions radiate to all rooms, and to it ascend the big decisions no single department can settle.

| Agent | Its role in one line |
|---|---|
| `brd-ceo` | chief executive officer — the final decision-maker; receives reports, distributes work to room leads, and hands you results |
| `brd-cpo` | chief product officer — consulted on product decisions and stage gates 0–2 |
| `brd-cto` | chief technology officer — consulted on technical and architectural decisions and build gates 3–4 |
| `brd-cqo` | chief quality officer — consulted on quality decisions, the fifth inspection gate, and testing standards |
| `brd-cso` | chief security officer — consulted on all security decisions, holding an absolute veto that stops any ruling |
| `brd-chief-of-staff` | chief of staff — converts the CEO's decisions into organized, execution-ready work orders |
| `brd-arbiter` | supreme arbiter — consulted on conflicts between rooms; their arbitration ruling is final |

**How does work enter it, and how do outputs leave?**
The CEO receives a report from the intake gateway, then consults Board members via a dedicated task per consultation; they decide or recommend, and then the CEO distributes work to room leads. This room owns two gates: G0 (idea inception) and G3 (ratifying the architectural decision). Its delivery is hierarchical too: the member records evidence ← hands off to the CEO as room lead ← review and unification ← handed to you.

**Connected rooms:** Strategy (01) for direction, and Gateway (14) for receiving requests.

---

### Room 01 — Strategy

**Code:** `str` · **Lead:** `str-lead` · **Agents:** 8
*(the official registry also records its name as Product Strategy)*

**Its mission in two lines:**
It analyzes the market, plans the product, manages risk, and charts the growth path. It is the "mastermind" that determines: what do we build? why? in what order? — before anyone spends a single riyal on execution.

| Agent | Its role in one line |
|---|---|
| `str-lead` | room lead — receives direction from the CEO, distributes it to the team, then consolidates results and hands them off |
| `str-product-strategist` | product strategist — charts the product's direction and course |
| `str-business-analyst` | business analyst — studies ideas' feasibility and impact on the business |
| `str-market-analyst` | market analyst — monitors the market, its trends, and competitor movement |
| `str-roadmap-planner` | roadmap planner — sequences what we will build step by step over time |
| `str-risk-analyst` | risk analyst — detects potential dangers early, before they strike |
| `str-monetization-strategist` | monetization strategist — proposes how the system generates revenue |
| `str-agile-orchestrator` | agile & flow orchestrator — watches the task board daily, detects blockers between rooms, enforces the WIP ≤ 2 limit |

**How does work enter it, and how do outputs leave?**
It receives direction from the CEO ← analyzes data and trends ← presents strategic recommendations ← hands off to the CEO. It owns the inception gate G0 where every new idea is sorted before any work (practically managed in cooperation with the intake gateway). Its feeding sources: reports from the Board, and data from the Research room (02).

---

### Room 02 — Research

**Code:** `res` · **Lead:** `res-lead` · **Agents:** 7
*(the official registry also records its name as UX Research)*

**Its mission in two lines:**
It researches the real user: what do they want? how do they behave? what pains them about competing products? It also verifies information before decisions are built on it — so we never make something nobody needs.

| Agent | Its role in one line |
|---|---|
| `res-lead` | room lead — receives research requests, distributes them, and unifies findings |
| `res-ux-researcher` | UX researcher — studies users' behavior and actual needs |
| `res-journey-architect` | journey architect — maps the user's complete steps with the product from start to finish |
| `res-competitor-analyst` | competitor analyst — tracks what others in the same field are doing |
| `res-data-researcher` | data researcher — gathers and analyzes data supporting the research |
| `res-fact-checker` | fact checker — confirms every piece of information before use |
| `res-web-scout` | web scout — searches the internet and collects required information |

**How does work enter it, and how do outputs leave?**
It receives research direction from the CEO or the strategy lead ← executes the research ← presents a findings report ← hands off to the CEO. It is the **owner** of discovery gate G1 — meaning it is the party responsible for passing that stage. Its research findings go out to serve Strategy (01) and Design (03), and are documented with Knowledge (13) when needed.

---

### Room 03 — Design

**Code:** `dsn` · **Lead:** `dsn-lead` · **Agents:** 8
*(the official registry also records its name as Visual Design)*

**Its mission in two lines:**
It crafts form and identity: how do screens look? What are the product's logo and colors? How does the user feel while using it? Its design is the specification the executing rooms build upon.

| Agent | Its role in one line |
|---|---|
| `dsn-lead` | room lead — receives requirements, distributes design work across the team, and unifies it |
| `dsn-ui-designer` | UI designer — draws the screens, buttons, and elements users see |
| `dsn-design-system` | design system architect — builds a unified library of components, colors, and fonts used by all screens |
| `dsn-brand-designer` | brand designer — creates the visual identity: logo, color, general personality |
| `dsn-content-strategist` | content strategist — phrases the words and texts appearing inside interfaces |
| `dsn-motion-designer` | motion designer — designs the tasteful animations and transitions inside the app or site |
| `dsn-a11y-specialist` | accessibility specialist — guarantees people with special needs can use the product |
| `dsn-ux-architect` | UX architect — structures the experience: where everything sits, and why |

**How does work enter it, and how do outputs leave?**
It receives requirements from the CEO ← researches and finds inspiration ← designs and iterates until improved ← presents for evaluation ← hands off to the CEO. It holds design gate G2. Its outputs go to implementation at Frontend (06) and Mobile (07).

---

### Room 04 — Architecture

**Code:** `arc` · **Lead:** `arc-lead` · **Agents:** 7

**Its mission in two lines:**
It designs the system's structure before building it, exactly like the architect who drafts the building blueprint before workers dig. Its decisions here set technologies and wiring between parts — changing them later is very costly, so it works with double care.

| Agent | Its role in one line |
|---|---|
| `arc-lead` | room lead — receives requirements and leads architectural option analysis |
| `arc-system-architect` | systems architect — draws the full picture of the system and its connected parts |
| `arc-api-architect` | API architect — designs the communication channels (APIs) between different parts |
| `arc-data-architect` | data architect — designs how information is organized and flows within the system |
| `arc-infra-architect` | infrastructure architect — sets the hardware and cloud services the system stands on |
| `arc-integration-architect` | integration architect — plans connecting our system with other external systems |
| `arc-review-architect` | review architect — inspects architectural decisions and catches their gaps early |

**How does work enter it, and how do outputs leave?**
It receives requirements from the CEO ← analyzes architectural options ← documents decisions in formal records called ADRs (one paper per architectural decision stating: what did we decide? why? and which alternatives did we reject?) ← presents the implementation plan ← hands off to the CEO. It owns architecture gate G3. Its plans descend for execution to Backend (05), Frontend (06), Data (08), and DevOps (11).

---

### Room 05 — Backend Engineering

**Code:** `bck` · **Lead:** `bck-lead` · **Agents:** 8
*(the official registry also records its name as Backend Engineering)*

**Its mission in two lines:**
It builds "behind the scenes": the server, communication channels, and business logic rules — everything that happens when you press a button and something actually occurs. Users never see it, but nothing works without it.

| Agent | Its role in one line |
|---|---|
| `bck-lead` | room lead — receives specifications from Architecture and distributes building across the team |
| `bck-api-engineer` | API engineer — builds the connection points (APIs) through which parts talk to each other |
| `bck-domain-engineer` | domain engineer — writes the real rules of the business: when is a request accepted? when rejected? |
| `bck-blade-engineer` | view template engineer — builds server-side rendered pages (the Blade technology) |
| `bck-queue-engineer` | queue engineer — organizes deferred background jobs such as message sending |
| `bck-integration-engineer` | integration engineer — connects the system to external services like payment gateways |
| `bck-code-reviewer` | code reviewer — reads colleagues' code before acceptance to catch mistakes early |
| `bck-refactoring-surgeon` | refactoring surgeon — cleans and improves old code without changing its behavior |

**How does work enter it, and how do outputs leave?**
It receives specifications from the Architecture lead (arc-lead) ← develops code TDD-style, writing the test first then the code that passes it ← tests ← reviews code ← hands off to the CEO (it may consult the Architecture lead during work without delivering). Together with Frontend and Mobile it shares build gate G4. Data feeds it from the Data room (08); its work is handed for deployment to DevOps (11) after security screening (09).

---

### Room 06 — Frontend Engineering

**Code:** `fnt` · **Lead:** `fnt-lead` · **Agents:** 8
*(the official registry also records its name as Frontend Interfaces)*

**Its mission in two lines:**
It builds everything the user sees and touches in the browser: screens, buttons, animations. Its task is making the beautiful fast and easy to use for everyone.

| Agent | Its role in one line |
|---|---|
| `fnt-lead` | room lead — receives designs and distributes interface building across the team |
| `fnt-vue-engineer` | Vue engineer — builds interfaces with Vue |
| `fnt-react-engineer` | React engineer — builds interfaces with React |
| `fnt-css-artisan` | CSS artisan — tunes page appearance and style with high precision |
| `fnt-interaction-engineer` | interaction engineer — crafts the interface's response to user movement and clicks |
| `fnt-performance-engineer` | performance engineer — makes pages open and run as fast as possible |
| `fnt-a11y-engineer` | accessibility engineer — implements usability for people with special needs |
| `fnt-code-reviewer` | code reviewer — inspects interface code before acceptance |

**How does work enter it, and how do outputs leave?**
It receives designs from the Design lead (dsn-lead) ← develops components ← tests accessibility and performance ← reviews ← hands off to the CEO (consulting the Design lead allowed, without delivering). It shares build gate G4. It depends on services from Backend (05); its work goes out for Quality inspection (10).

---

### Room 07 — Mobile Engineering

**Code:** `mob` · **Lead:** `mob-lead` · **Agents:** 6
*(the official registry also records its name as Mobile)*

**Its mission in two lines:**
It builds phone applications (Android and iOS) with Flutter, which writes the app once to run on both platforms. It insists the app be light and fast on real devices, not just on paper.

| Agent | Its role in one line |
|---|---|
| `mob-lead` | room lead — receives designs and leads app development |
| `mob-flutter-engineer` | Flutter engineer — builds the app's screens and features with Flutter |
| `mob-platform-engineer` | platform engineer — handles each system's specifics: Android on one side, iOS on the other |
| `mob-state-engineer` | state engineer — manages how the app preserves its living information during use |
| `mob-perf-profiler` | performance profiler — measures the app's battery, memory, and speed consumption on devices |
| `mob-release-engineer` | release engineer — prepares the app and launches it to the stores |

**How does work enter it, and how do outputs leave?**
It receives designs from the Design lead (dsn-lead) ← develops the app ← tests on real devices ← reviews performance ← hands off to the CEO (consulting the Design lead allowed). It shares build gate G4, cooperating with Backend (05) for services and with Quality (10) for inspection.

---

### Room 08 — Data

**Code:** `dat` · **Lead:** `dat-lead` · **Agents:** 7

**Its mission in two lines:**
It guards all information: how is it stored? how retrieved quickly? how leveraged through analysis and prediction? how kept private and secure? Information is the system's capital, and this is its vault room.

| Agent | Its role in one line |
|---|---|
| `dat-lead` | room lead — receives data requirements and distributes them across the team |
| `dat-db-engineer` | database engineer — builds and tends the stores holding the information itself |
| `dat-cache-engineer` | cache engineer — prepares fast temporary copies of data to speed access |
| `dat-etl-engineer` | ETL engineer — pulls data from sources, transforms it, and places it correctly (ETL) |
| `dat-analytics-engineer` | analytics engineer — turns raw data into understandable reports and numbers |
| `dat-ml-engineer` | machine learning engineer — builds programs that learn from data, predict, and recommend (ML) |
| `dat-privacy-officer` | privacy officer — supervises every data interaction's compliance with privacy rules |

**How does work enter it, and how do outputs leave?**
It receives requirements from the CEO or the Architecture lead ← designs the data schema (the map of how information is arranged) ← runs the migration (safe transfer of changes onto existing data structure) ← tests ← hands off to the CEO. It owns no standalone gate — but contributes its data schema inside the architecture and build gates (G3/G4) per the official gates definition file. It serves Backend (05), DevOps (11), and Observability (12).

---

### Room 09 — Security

**Code:** `sec` · **Lead:** `sec-lead` · **Agents:** 9

**Its mission in two lines:**
It attempts to breach our system before anyone else tries, protecting data, secrets, and regulatory compliance. Its voice is heard at every stage, and its lead holds an absolute veto over any unsafe decision.

| Agent | Its role in one line |
|---|---|
| `sec-lead` | room lead — leads security screening across all stages and escalates to the Board when necessary |
| `sec-pentester` | penetration tester — attacks the system deliberately, with permission, discovering its flaws before enemies do |
| `sec-appsec-engineer` | application security engineer — shields the application itself against known attack techniques |
| `sec-authn-engineer` | authentication engineer — secures verifying users' identities and their sign-in |
| `sec-compliance-auditor` | compliance auditor — verifies our adherence to required regulations and standards |
| `sec-incident-responder` | incident responder — intervenes instantly on any breach or security emergency |
| `sec-threat-modeler` | threat modeler — analyzes potential risks and writes them down before they materialize |
| `sec-secrets-warden` | secrets warden — keeps passwords and sensitive keys away from everyone's eyes |
| `sec-license-auditor` | license & IP auditor — checks every dependency's license before merge; vetoes GPL/AGPL contamination with a documented reason (Law 15) |

**How does work enter it, and how do outputs leave?**
Its method: review every stage gate ← perform threat modeling (a written risk analysis) ← inspect code and infrastructure ← report vulnerabilities ← escalate to the security chief on the Board when needed. It owns no single gate but audits cross-cuttingly across **all** gates from G0 to G8 — a standing security controller over everything. Connected rooms: all rooms (in a cross-cutting capacity).

---

### Room 10 — Quality

**Code:** `qa` · **Lead:** `qa-lead` · **Agents:** 7

**Its mission in two lines:**
It inspects everything the rooms produced before it reaches you: does it truly work? did anything break that used to work? Its "approve" or "block" ruling is final at the quality gate — it is the safety valve keeping defects from reaching you.

| Agent | Its role in one line |
|---|---|
| `qa-lead` | room lead — reviews inspection requirements and issues the approve-or-block verdict |
| `qa-test-architect` | test architect — plans scientifically and comprehensively what we inspect and how |
| `qa-automation-engineer` | automation engineer — builds automated checks that run by themselves every time |
| `qa-manual-explorer` | manual explorer — tries the product by hand like a real user, catching what machines miss |
| `qa-perf-analyst` | performance analyst — measures speed and endurance under load |
| `qa-design-auditor` | design auditor — verifies the implementation matches the approved design |
| `qa-regression-warden` | regression warden — confirms the new change broke nothing that used to run |

**How does work enter it, and how do outputs leave?**
It reviews gate requirements ← plans tests ← executes automation ← tests manually ← issues the report ← gives the final verdict: PASS or BLOCK. It owns quality gate G5. Like Security, its work cuts across all rooms.

---

### Room 11 — DevOps

**Code:** `ops` · **Lead:** `ops-lead` · **Agents:** 8

**Its mission in two lines:**
It prepares the operating ground and releases versions online safely, builds automated pipelines that inspect and ship code without manual intervention, and watches the hosting bill. It is the bridge from "works on our machine" to "works in front of users."

| Agent | Its role in one line |
|---|---|
| `ops-lead` | room lead — receives infrastructure from Architecture and leads environment provisioning and deployment |
| `ops-cicd-engineer` | CI/CD engineer — builds the automated production line that inspects code and hands it to deployment automatically |
| `ops-cloud-engineer` | cloud engineer — manages servers and rented internet services |
| `ops-cost-optimizer` | cost optimizer — shrinks the infrastructure bill without hurting performance |
| `ops-domain-warden` | domain warden — manages the site name (domain) and its settings |
| `ops-migration-runner` | migration runner — safely applies database structure changes onto operating environments |
| `ops-release-manager` | release manager — orchestrates launching every new version step by step |
| `ops-sandbox-executor` | sandbox execution engineer — runs build/syntax checks on delivered code inside an isolated container before QA sees it; failures return to the builder with a precise error log |

**How does work enter it, and how do outputs leave?**
It receives infrastructure from the Architecture lead (arc-lead) ← provisions the environment ← builds the pipeline ← deploys ← monitors ← hands off to the CEO. It owns both launch gates: G6 (staging, where we rehearse calmly) and G7 (production, facing real users). It integrates with Observability (12) after every deployment.

---

### Room 12 — Observability

**Code:** `obs` · **Lead:** `obs-lead` · **Agents:** 6

**Its mission in two lines:**
It keeps watch over the system after deployment: does it respond acceptably fast? which part began stumbling? At any incident it guides the path from detection to analysis to lesson learned. It is the system's eyes that never blink.

| Agent | Its role in one line |
|---|---|
| `obs-lead` | room lead — leads monitoring and incident analysis and presents recommendations |
| `obs-monitoring-engineer` | monitoring engineer — builds the instruments permanently measuring system health |
| `obs-alerting-engineer` | alerting engineer — tunes the danger bell that rings the moment any indicator breaks |
| `obs-sre` | site reliability engineer — keeps service continuous within declared reliability bounds (SLOs: measurable service-level promises, e.g., "the site responds within one second 99% of the time") |
| `obs-incident-commander` | incident commander — leads response when a major failure strikes until it is fixed |
| `obs-insights-analyst` | insights analyst — extracts lessons and future recommendations from monitoring data |

**How does work enter it, and how do outputs leave?**
Its perpetual cycle: monitor metrics (SLOs) ← analyze incidents ← present recommendations ← update dashboards (central display screens for system status). It owns follow-up gate G8 — the last checkpoint in the chain. It works side by side with DevOps (11), Backend (05), and Data (08).

---

### Room 13 — Knowledge

**Code:** `knw` · **Lead:** `knw-lead` · **Agents:** 6

**Its mission in two lines:**
It preserves the system's memory: documenting decisions and lessons, organizing knowledge, and answering "when and why did we do X?". Without it the system reinvents the wheel every session and forgets its old mistakes.

*(You are reading right now a living specimen of this room's work — this very guide is its product.)*

| Agent | Its role in one line |
|---|---|
| `knw-lead` | room lead — leads documentation, organizes knowledge, and signs major memory updates |
| `knw-brain-query` | brain query specialist — searches SOFI's memory answering agents' questions about the past |
| `knw-doc-writer` | documentation writer — turns information into tidy clear documents like this guide |
| `knw-historian` | historian — preserves the sequence of events, eras, and changes across the system's lifetime |
| `knw-memory-curator` | memory curator — arranges memory contents, refines them, and maintains their consistency |
| `knw-reflector` | reflector — distills lessons from every experience and records them for future improvement |

**How does work enter it, and how do outputs leave?**
Its cycle: document major decisions ← organize knowledge ← answer agents' inquiries ← reflect and review lessons ← update the CORTEX region (the permanent decisions record). It owns no special gate — instead it supports **every** stage through documentation and retrieval. Connected to all rooms.

---

### Room 14 — Gateway

**Code:** `gtw` · **Lead:** `gtw-dispatcher` · **Agents:** 7

**Its mission in two lines:**
It is the first stop of any request a user writes: understanding it, rephrasing it, classifying it, routing it to the right party, managing budget, and resolving conflicts. Without it the system dissolves into chaos: every room grabs the request as it pleases.

| Agent | Its role in one line |
|---|---|
| `gtw-dispatcher` | dispatcher and room lead — takes the classified request and routes it to the suitable room or rooms |
| `gtw-router` | router — picks the best path for work to reach its destination |
| `gtw-gatekeeper` | gatekeeper — verifies eligibility and permissions before any stage crossing |
| `gtw-budget-warden` | budget warden — watches the resources spent on every task |
| `gtw-conflict-resolver` | conflict resolver — untangles clashes between requests or parties |
| `gtw-external-reviewer` | external reviewer — examines whatever needs a view from outside the room |
| `gtw-intake-reformer` | intake reformer — receives the user's raw request, reshapes it into the clearest possible form, then passes it on |

**How does work enter it, and how do outputs leave?**
This is its official internal flow: `intake-reformer` receives the request ← `dispatcher` routes it to the suitable room ← `gatekeeper` verifies permissions ← `budget-warden` manages budget ← `conflict-resolver` resolves conflicts as they arise. Its gate role is special: intake only at G0, while actual ownership of the inception gate belongs to the Strategy room (01). Connected to all rooms and to the outside world.

---

## 4) Closing Summary Table: Who Does What, and When Do We Call Them?

| # | Room | Role in two words | When do we call on them? |
|---|---|---|---|
| 00 | Board Room | leadership and governance | on every critical decision, work distribution, and settling major conflicts between departments |
| 01 | Strategy | product planning | when we need market analysis, a growth plan, and prioritization before execution |
| 02 | Research | understanding the user | before building any new feature: user and competitor research plus fact verification |
| 03 | Design | crafting form | when we want screen appearance and visual identity before any code |
| 04 | Architecture | designing the system | before any major build: how the system will be built and with which technologies and connections |
| 05 | Backend | the server's mind | for all business logic and connection interfaces behind the scenes |
| 06 | Frontend | the site's face | for building what the user sees and interacts with in the browser |
| 07 | Mobile | phone applications | for building Android and iOS apps, tuning their performance, and launching them |
| 08 | Data | managing information | for databases, reports, analytics, and privacy protection |
| 09 | Security | protection and defense | for inspecting anything touching safety before launch, penetration testing, and secrets protection |
| 10 | Quality | output control | before accepting any final delivery: comprehensive tests and an approve-or-block verdict |
| 11 | DevOps | operations and deployment | for provisioning environments, releasing versions, and cutting hosting costs |
| 12 | Observability | perpetual vigilance | after deployment: watching health and performance, handling incidents, extracting lessons |
| 13 | Knowledge | memory and documentation | for documenting decisions and lessons and answering "when and why did we do this?" |
| 14 | Gateway | intake and routing | first stop of any request: understanding it, classifying its track, routing it, managing its budget |

---

## Conclusion

The whole system rests on three pillars recurring on every page of this guide:

1. **One door for everyone:** no work starts except through the intake gateway, and its path matches its criticality.
2. **A ladder nobody jumps:** agent → lead → CEO → owner, with completion evidence at every rung.
3. **Memory never forgotten:** decisions and lessons preserved in two separate memories — one for the system, one for each project.

On these three pillars operate 15 rooms and 106 agents as one team... no overlap, no loss, no surprises reaching you.

---

### Appendix: Sources of This Guide (for verification)

| Source | What we took from it |
|---|---|
| `hq/core/nexus/registry.yaml` | the official room composition: Arabic and English names, codes, each room's agents (15 rooms, 106 agents), and the intake service |
| `AGENTS.md` (SOFI constitution) | the 13 binding laws, the three tracks and their examples, hierarchical delivery rules, evidence, the work order, and the two memories |
| Room charters `hq/core/room_charters/00..14/CHARTER.md` (15 charters) | each room's mission, lead, roster, procedures, connected rooms, gates, and delivery protocol |
| `hq/brain/brain-index.md` | the memory structure: organization memory's seven regions, project memory and its four files, and the strict separation rule between them |

> **Accuracy note:** the agent descriptions in the room tables are simplified renderings of the role names given in the charters and official registry, with each term explained in plain words — without adding responsibilities absent from the sources. The detailed operational definitions of every agent live in `.opencode/agent/`, the single source for them, as the charters state.

*End of guide — prepared by Dana Al-Atari (`knw-doc-writer`), Knowledge Room 13, dated 2026-08-22.*
