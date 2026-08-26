# Full Life-Cycle Playbook — Building Projects and Features with DDD
### From Idea to Production via SOFI's Six-Lane Pipeline · hands-on applied edition · 2026-08-24

> **How to read this guide:** every section opens with the rule, then literally executable numbered steps, then the ready-made template. No jumping — order is the method (Law 13: no free points).

---

## First: Understanding Requirements and Room Alignment (before any line)

**Rule:** no execution without a unified vision documented in one home.

1. **Request intake through the gateway:** every request enters on `gtw-intake-reformer` for classification (fast / standard / fateful) and conversion into an RCCF work order approved by brd-ceo — no exceptions.
2. **Room sync meeting:** the room lead gathers the involved agents in one focused meeting:
   - **What is the problem?** (user language, not technical)
   - **What defines "done"?** (measurable acceptance criteria per item)
   - **What will we not do?** (scope boundaries stated explicitly)
3. **The central context document** — its home is mandatory: `projects/<slug>/brain/CONTEXT.md`. Its first section:

```markdown
## Agreed Requirements (S1)
| # | Requirement | Acceptance criterion | Priority |
|---|---------|--------------|----------|
| R1 | ...    | machine- or manually verifiable | Must |

## Assumptions
- A1: ... (every unconfirmed assumption goes here and gets revisited at Gate-3)

## Constraints
- C1: Flutter/Dart binding stack (R2) · C2: Envelope API v1 · C3: no touching live data on paper before S4
```

4. **This stage's exit gate:** a PRD anchored in the same file + brd-ceo approval. No design beyond it without a PRD.

---

## Second: Choosing the Frontend ↔ Backend Communication Protocol

**Rule:** the protocol is an architectural decision recorded in an ADR, not a team habit. SOFI's default: **REST + Envelope v1 + OpenAPI-first** — no change without measured justification.

### Selection Matrix

| Need | Protocol | When | Why |
|---|---|---|---|
| standard CRUD, forms, dashboards | **REST** (default) | 90% of cases | simplicity, caching, OpenAPI generates contract and clients |
| a screen aggregating 6+ data sources in one request | GraphQL | heavy analytical dashboard | one request instead of six, and the client picks the shape |
| internal micro-to-micro services under high load | gRPC | backend↔backend communication only | compact binary, streaming, strict contracts |
| chat, live notifications, live counters | **WebSocket** | only for real-time features | instant push instead of polling |

### The Three Performance Questions (asked before any choice)
1. **Acceptable latency:** >200ms crosses human perception? genuine realtime, or would a 30s refresh suffice (polling is simpler)?
2. **Data volume:** large/frequent payloads? → gzip/brotli compression at Caddy before any protocol change.
3. **Direction:** continuous server→client? Only then is WebSocket justified.

### Decision ADR Template (written into `brain/DECISIONS.md`)
```markdown
## DEC-0NN — protocol for <feature>
- Options considered: REST / WS
- Decision: REST + 30s polling for counters
- Reason: instant updates are not commercially required; WS doubles infrastructure complexity
- Impact: one GET /live-stats endpoint instead of a socket architecture
```

---

## Third: Applying DDD — From Context to Code

### 3.1 Identifying Bounded Contexts

**Rule:** context = an area with one unified language and one owning team. If you need to explain a word to another team under a different meaning → you are standing across two contexts.

1. List the verbs and nouns recurring in the PRD (mini Event Storming): "sale, inventory, invoice, customer".
2. Draw the boundaries: every context **owns its data and never borrows its neighbor's tables** — cross-context communication happens through contracts (API or Domain Events) only.
3. Document them in the contexts table (goes to `docs/design/context-map.md`):

| Context | Its exclusive responsibility | Does not | Talks to |
|---|---|---|---|
| Sales | the sale cycle from cart to completion | never edits inventory directly | Inventory (event), Billing |
| Inventory | quantities and reservations | has no idea what a "cart" is | consumes the SaleCompleted event |

### 3.2 Models: Entity · Value Object · Aggregate

- **Entity:** carries identity; its state changes (Order #102). Equality by identity, not by values.
- **Value Object:** no identity, immutable, equal by value (Money(amount, currency)) — **build a VO for every concept carrying rules** (a valid email, a positive amount).
- **Aggregate:** one consistency block; a **single root** is the gateway to modification; everything inside it persists/deletes together. Golden rule: **references between Aggregates go by ID, never by full object.**

```php
// Domain/Orders/Model/Order.php (Aggregate Root) — domain rules live here exclusively
final class Order {
    /** @var collection<OrderLine> */
    private array $lines;
    private function __construct(
        public readonly OrderId $id,
        private OrderStatus $status,
        array $lines,
        private readonly Money $total,          // Value Object
    ) { $this->lines = $lines; }

    public static function place(OrderId $id, CustomerId $customer, OrderLines $lines): self {
        if ($lines->isEmpty()) throw new EmptyOrderException();
        $order = new self($id, OrderStatus::PLACED, $lines->all(), $lines->total());
        $order->recordThat(new OrderPlaced($id, $customer, $order->total)); // Domain Event
        return $order;
    }
    // never public setters — behavior named after intent
    public function cancel(): void {
        if ($this->status !== OrderStatus::PLACED) throw new CannotCancelException($this->status);
        $this->status = OrderStatus::CANCELLED;
        $this->recordThat(new OrderCancelled($this->id));
    }
}
```

### 3.3 Repositories, Application Services, and Dependency Injection

- **Repository:** interface in the **Domain** layer (signatures in domain language), implementation in **Infrastructure** (Eloquent). The Domain does not know Eloquent exists.
- **Application Service:** use-case coordinator — receives a DTO, calls the Aggregate, persists via Repository, dispatches Events. **Zero business rules inside it** — rules belong to the domain.

```php
// Domain/Orders/Contract/OrderRepository.php
interface OrderRepository {
    public function find(OrderId $id): ?Order;
    public function save(Order $order): void;
}

// Infrastructure/Persistence/EloquentOrderRepository.php
final class EloquentOrderRepository implements OrderRepository {
    public function __construct(private readonly OrderModel $model) {} // container-injected
    public function save(Order $order): void { /* mapping → rows */ }
}

// Application/UseCase/PlaceOrderHandler.php
final class PlaceOrderHandler {
    public function __construct(
        private readonly OrderRepository $orders,     // inject the interface, not the implementation
        private readonly EventDispatcher $events,
    ) {}
    public function handle(PlaceOrderCommand $cmd): OrderId {
        $order = Order::place(OrderId::generate(), $cmd->customerId, $cmd->lines);
        $this->orders->save($order);
        $this->events->dispatch(...$order->releaseEvents());
        return $order->id;
    }
}
// interface wiring: app/Support/Container.php → bind(OrderRepository::class, EloquentOrderRepository::class)
```

**The clean-separation test:** move the `Domain/` folder into a project without Laravel — it must work with zero framework imports. If it does not → layer breach.

---

## Fourth: The Professional Task List (engineering TODO)

**Rule (Law 13):** every plan generates a `Phase-NN → NN-NN → NN-NN-NN` tree — no free points.

1. **Decompose to measurable size:** task = one working day maximum, with a file/commit output that can be inspected. If it cannot be measured → split it further.
2. **Prioritization = business value × technical dependency:** what others depend on comes first (contract before interface, Schema before Handler).

```text
Phase-01 → paper contracts (S2)
├── 01-01 openapi.yaml for the five routes         [bck-api-engineer · day]
├── 01-02 schema-contract + ERD                    [arc-data-architect · day]
└── 01-03 arc-lead review + signature              [arc-lead · half day]
Phase-02 → domain core (S4-a)
├── 02-01 Domain/Orders (Entity+VO+Events)         [bck-domain-engineer]
├── 02-02 Repositories + container wiring          [bck-api-engineer]
└── 02-03 Feature Tests for the Handlers           [qa-automation-engineer]
```

3. **Assignment and dates:** every task has exactly one responsible agent (never shared!) and a due date in the RCCF ticket.
4. **Tracking:** GitHub Projects on the project repository (columns: Backlog / In-Progress / Review / Done) — periodic reporting = entries in HANDOFFS inside `brain/HANDOFFS.md` backed by file:line evidence, not a traceless meeting.

---

## Fifth: Continuous Communication and Documented Decisions

| Rhythm | SOFI tool | Mandatory content |
|---|---|---|
| daily (standup) | paragraph atop the agent session | finished X · working Y · blocker Z (any blocker = immediate escalation to the lead) |
| technical decision | ADR in `brain/DECISIONS.md` | options/decision/reason/impact — no verbal decisions |
| delivery | `sofi-handoff` ticket | file:line evidence + exit codes (Law 4) |
| weekly/gate | gate review | checklist + signed verdict |
| project wiki | `brain/CONTEXT.md` + `docs/` | the single source of truth — knowledge kept only in heads is forbidden |

**Communication iron law:** an agent never addresses another room directly (L2) — anything crossing rooms passes through two leads. Courteous refusal is a duty: a request without an approved design is returned, not executed.

---

## Sixth: Ready-Made Templates

### 6.1 Backend Tree (Laravel — canonical DDD capsule)

```text
app/
├── Domain/                      # the pure heart — zero framework
│   └── Orders/
│       ├── Model/               # Aggregates + Entities + VOs
│       ├── Event/               # OrderPlaced.php ...
│       ├── Contract/            # OrderRepository interface
│       └── Exception/
├── Application/                 # use cases
│   └── Orders/UseCase/          # PlaceOrderHandler.php
├── Infrastructure/              # everything touching the outside
│   └── Persistence/             # EloquentOrderRepository.php
└── Http/                        # thin Controllers calling Handlers
    └── Orders/PlaceOrderController.php
```

### 6.2 Frontend Tree (Flutter/Dart — feature-first per R2)

```text
lib/features/orders/
├── domain/          # entities + value_objects + repository interface
├── application/     # providers/usecases (state logic)
├── infrastructure/  # dio datasource + dto mapping (Envelope v1)
└── presentation/    # screens + widgets (design from tokens exclusively)
lib/shared/          # api_client · theme · l10n
```

### 6.3 Naming Conventions

| Entity | Rule | Example |
|---|---|---|
| Aggregate/Entity | singular PascalCase domain name | `Order`, `Invoice` |
| Value Object | concept's name, not type | `Money`, `Email` not `StringVo` |
| Repository interface | `XRepository` | `OrderRepository` |
| UseCase Handler | `VerbNounHandler` | `PlaceOrderHandler` |
| Domain Event | VerbNoun past tense | `OrderPlaced` |
| Exception | what failed exactly | `EmptyOrderException` |
| Controller | Resource + Controller | `OrderController` |
| Dart widget/screen | functional PascalCase | `OrderSummaryCard` |
| variable/function | intent, not type | `$pendingTotal` not `$arr2` |

### 6.4 Mandatory Patterns When Needed

- **Factory:** creating Aggregates with complex/conditional initialization → `Order::place()` above. `new` outside the Factory is forbidden.
- **Strategy:** business rule varying by context (shipping by country, discount by tier):
```php
interface ShippingStrategy { public function cost(Weight $w): Money; }
final class DomesticShipping implements ShippingStrategy { /* ... */ }
final class ShippingCalculator {
    /** @param array<ShippingStrategy> */
    public function __construct(private readonly array $strategies) {}
}
```
- **Domain Events:** every significant state change → a named Event. Subscribers (sending email, decrementing stock) listen rather than get called — complete separation between contexts.

---

## Seventh: Infrastructure in the Workflow (Caddy · Cloudflare · PHP-FPM · Docker · Git)

| Layer | Operating rule | Checkpoint |
|---|---|---|
| **Git/GitHub** | protected `master` branch · short-lived feature branches merged and deleted **before task closure** (L10 — worktrees forbidden) | one PR per task, room lead review |
| **Docker** (development only) | `docker-compose.dev.yml` for database/queues; **production is native** per decision ADR-059 | `docker compose config -q` before sharing any compose file |
| **PHP-FPM** (production) | pool per project under its user · **opcache.validate_timestamps=Off** ⇒ any PHP change requires `systemctl reload php8.x-fpm` — protective rule from an institutional lesson | fixed item on the pre-deployment checklist |
| **Caddy** | reverse_proxy to the FPM socket · automatic TLS · brotli compression enabled | `caddy validate --config /etc/caddy/Caddyfile` before reload |
| **Cloudflare** | DNS-only A/AAAA when Caddy manages TLS, or Proxied with Full(strict) · cache rules for static assets exclusively · Always HTTPS | after any DNS change: `curl -I` to confirm headers |
| **Deployment** | via the `ops-deploy-runbook` skill: runbook + rollback script + mandatory health-check before crossing Gate-7 | `curl -f https://site/health \|\| rollback` |

**Golden deployment sequence:** green tests → tag `vX.Y.Z` → runbook executes migrate (with documented down steps) → FPM reload → caddy validate + reload → health-check → if any step fails: rollback script immediately and record the incident in AMYGDALA.

---

## ✅ Final Checklist (copy into every feature ticket)

**Shift-left pre-build questions (owner order 2026-08-26) — answered BEFORE code starts:**
- [ ] Did the security representative review the threat model for this scope? (`sec-threat-modeler` signs the roadmap risks — Strategy room rule)
- [ ] Did the quality representative review the test plan / contract testability? (`qa-test-architect` signs the API contract — Architecture room rule)

**Delivery closure:**
- [ ] PRD + acceptance criteria in `brain/CONTEXT.md`
- [ ] ADR for the protocol if departing from REST
- [ ] context-map updated with changed contexts
- [ ] openapi/schema-contract frozen before code (S2)
- [ ] Phase tree approved and every task assigned one owner
- [ ] Domain clean of framework (the relocation test)
- [ ] Events for significant occurrences + Strategy/Factory where rules vary
- [ ] Naming matching the table
- [ ] Sandbox gate PASS from `ops-sandbox-executor` before review/QA (Hard Rule #11)
- [ ] License-check recorded for any dependency change (Law 15)
- [ ] Runbook + rollback + health-check for deployment
- [ ] HANDOFFS logged with evidence after closure

*Owner: knw-doc-writer · governing references: hq/core/nexus/pipeline.yaml + standards/ddd-capsule.md*
