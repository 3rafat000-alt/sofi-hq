# DDD-STANDARDS — The Domain-Driven Design Capsule Standard for the Three Stacks

> **The step-by-step operational execution (consultation before starting · TODO · acceptance lists):** `hq/core/tech_templates/ddd-capsule-protocol.md` — binding alongside this standard.

> **Status:** binding standard — **the governing canon for new projects** (STACKS↔DDD settlement · INT-GTW-024); the `app/Domains/<Name>/` structure in stacks-tech.md = legacy for existing projects exclusively — mandatory on the backend (05), frontend (06), and mobile (07) rooms for every new feature or structural change.
> **Principle:** dumb interface + smart core — business logic lives in the `Domain` layer exclusively.
> **Responses:** every network call adheres to Envelope v1 (`api-envelope.md`) and its envelope is unwrapped in Infrastructure only.

## | 1. The Golden Rule

1. **Data flows from outside in:** the request enters Presentation → Application → Domain, and nothing calls back outward.
2. **The Domain layer has zero external dependencies:** no Eloquent, no axios/fetch, no dio, no flutter/material — pure entities and rules only.
3. **Business logic in interfaces is forbidden:** Controller/Component/Widget only displays and delegates; decisions and rules live inside the Domain.
4. **Dependency Inversion:** Infrastructure implements interfaces defined by the Domain — the inside never knows about the outside.

```
              dependencies always point inward ◄◄◄
┌──────────────────────────────────────────────────────┐
│ Presentation (outermost — thin)                       │
│ Laravel: Http/Controllers · React: screens/components │
│ Flutter: pages/widgets                                │
└──────────────────────┬───────────────────────────────┘
                       │ calls ↓
┌──────────────────────▼───────────────────────────────┐
│ Application                                           │
│ Actions (Laravel) · TanStack Query hooks (React)      │
│ usecases + state bloc/provider (Flutter)              │
└──────────────────────┬───────────────────────────────┘
                       │ calls ↓
┌──────────────────────▼───────────────────────────────┐
│ Domain (the core — no external dependency whatsoever) │
│ Entities · Value Objects · business rules · Failures  │
└──────────────────────▲───────────────────────────────┘
                       │ implements Domain interfaces (dependency inversion)
┌──────────────────────┴───────────────────────────────┐
│ Infrastructure                                        │
│ Repositories impl · API clients · Mappers · DB        │
└──────────────────────────────────────────────────────┘
```

## | 2. Laravel — Backend (room 05) — our stack is Laravel, not NestJS

### Folder tree
```
app/
├── Domain/
│   └── Orders/                          # Bounded Context
│       ├── Models/                      # Entities + Value Objects
│       │   ├── Order.php                # Aggregate Root
│       │   └── ValueObjects/
│       │       └── Email.php            # self-validating VO
│       ├── Actions/                     # Use Cases — the single entry point
│       │   └── CancelOrderAction.php
│       ├── DTOs/                        # e.g. CancelOrderData.php
│       ├── Events/                      # e.g. OrderCancelled.php
│       ├── Exceptions/                  # e.g. OrderAlreadyShippedException.php
│       └── Rules/                       # validation rules consumed by FormRequests
│           └── ValidEmailDomain.php
├── Http/                                # thin Presentation
│   ├── Controllers/
│   │   └── OrderController.php          # every statement is a one-line delegation
│   └── Requests/
│       └── CancelOrderRequest.php       # FormRequest — shape validation only
└── Infrastructure/
    └── Persistence/
        └── EloquentOrderRepository.php  # implements the Domain's repository interface
```

### Self-Validating Value Object — `Email`
```php
final class Email
{
    private function __construct(private readonly string $value)
    {
        if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {
            throw new InvalidValueObjectException("email [{$value}]");
        }
    }

    public static function from(string $value): self
    {
        return new self(strtolower(trim($value)));
    }
}
```

### An Aggregate Root Guarding Its Own Rule — `Order`
```php
class Order extends Model
{
    // modifying status directly from anywhere is forbidden — the rule lives here alone
    public function cancelOrder(): void
    {
        if ($this->status === OrderStatus::Shipped->value) {
            throw new OrderAlreadyShippedException($this->id);
        }
        $this->status = OrderStatus::Cancelled->value;
        $this->save();
        event(new OrderCancelled($this->id));
    }
}
```

### A Model Action (Use Case) + the Thin Delegating Controller
```php
final class CancelOrderAction
{
    public function __construct(private readonly EloquentOrderRepository $orders) {}

    /** @throws OrderAlreadyShippedException */
    public function execute(int $orderId): void
    {
        $order = $this->orders->findOrFail($orderId); // Infrastructure
        $order->cancelOrder();                        // the rule inside the Aggregate
    }
}

// Controller — every statement a one-line delegation, zero logic
public function cancel(CancelOrderRequest $request, CancelOrderAction $action): JsonResponse
{
    $action->execute($request->integer('order_id'));
    return response()->json(['success' => true], 200);
}
```

## | 3. React — Frontend (room 06)

### Folder tree — Feature-Sliced
```
src/features/products/
├── domain/
│   ├── product.ts          # pure Entity + Types without axios
│   └── rules.ts            # pure testable business rules
├── application/
│   └── useGetProducts.ts   # hook — TanStack Query
├── infrastructure/
│   ├── productsApi.ts      # api client — consumes Envelope v1
│   └── productsMapper.ts   # DTO → Entity — the sole translation boundary
└── presentation/
    ├── components/ProductCard.tsx
    └── screens/ProductsScreen.tsx
```

### Hook — `useGetProducts` (application) + Mapper (infrastructure)
```ts
export function useGetProducts(filters?: ProductFilters) {
  return useQuery({
    queryKey: ['products', filters],
    queryFn: async () => toProducts(await productsApi.list(filters)),
  });
}

// infrastructure/productsMapper.ts — Envelope v1 unwrapping happens here alone
export function toProducts(envelope: Envelope<ProductDTO[]>): Product[] {
  return envelope.data.map((dto) => ({
    id: dto.id,
    name: dto.name,
    price: Money.fromCents(dto.price_cents), // translation rule lives in the mapper only
  }));
}
```

## | 4. Flutter — Mobile (room 07)

### Folder tree
```
lib/features/orders/
├── domain/
│   ├── entities/order.dart
│   ├── repositories/order_repository.dart   # abstract only — no dio
│   └── failures/failure.dart                # Either<Failure,T>
├── application/
│   ├── usecases/cancel_order_usecase.dart
│   └── state/order_bloc.dart                # bloc/provider for state
├── infrastructure/
│   ├── datasources/order_remote_datasource.dart
│   ├── models/order_model.dart              # fromJson via Envelope<T>
│   └── repositories/order_repository_impl.dart
└── presentation/
    ├── pages/orders_page.dart               # Theme only for styling
    └── widgets/order_card.dart              # hard-coded colors forbidden
```

### Repository abstract + UseCase — `Either<Failure,T>` + Model via Envelope<T>
```dart
abstract class OrderRepository {
  Future<Either<Failure, List<Order>>> getOrders();
}

class CancelOrderUsecase {
  final OrderRepository repository;
  CancelOrderUsecase(this.repository);

  Future<Either<Failure, void>> call(int orderId) =>
      repository.cancelOrder(orderId);
}

// infrastructure/models — envelopes are unwrapped at Infrastructure boundaries only
factory OrderModel.fromEnvelope(Map<String, dynamic> json) =>
    OrderModel.fromJson(json['data']);
```

## | 5. DO / DON'T Table — Binding on All Three Stacks

| ✅ Do | ❌ Don't |
|---------|-----------|
| business logic in `domain` exclusively | business decisions inside Controller/Widget/Component |
| a controller delegating with one statement | direct HTTP/DB logic inside the controller |
| self-validating Value Objects (`Email::from`) | bare strings/numbers passing unchecked |
| state changes through Aggregate methods (`$order->cancelOrder()`) | `$order->status = ...` from outside the Aggregate |
| repositories as an interface in Domain, implemented in Infrastructure | calling Eloquent/axios/dio inside inner layers |
| one DTO→Entity mapper at Infrastructure boundaries | leaking JSON/DTO into domain or presentation |
| unified `Either<Failure,T>` error handling in Flutter | scattered try/catch and error handling inside widgets |
| Theme-only styling in Flutter UI | hard-coded colors and sizes inside widgets |
| TanStack Query inside application-layer hooks | fetch/useEffect sitting inside components |
| every feature as a boundary-independent capsule | importing another feature's presentation |

*Last updated: 2026-08-23 — standard created. Any structural change to it = architectural decision routed through brd-ceo.*

---

## | 6. Aggregate Boundaries & Ubiquitous Language — Enrichment from External Harvesting (2026-08-24)

> **Sources:** `hq/training/internet_knowledge/ddd-stemmler-intro.md` (19.8KB) + `ddd-ms-oriented.md` (14.8KB) + `ddd-vernon-reference.md` — Self-Development Initiative P1.

### 6.1 Designing a Sound Aggregate — The Seven Rules
1. **One governing rule:** the sole public mutation channel is the Aggregate Root — no outside actor ever modifies its children directly.
2. **Boundaries = consistency parameters:** everything that must be consistent instantly (invariant) within one transaction = one Aggregate; everything consistent eventually = Aggregates communicating by events.
3. **As small as possible:** a bloated Aggregate = lock contention and poor performance. Reference by ID instead of embedding whole objects.
4. **The root protects invariants:** validation inside the root on every change — `Order` refuses adding a line item once status is `SHIPPED`.
5. **Value Objects for composite attributes** carrying their own validity (criterion §2 above) — Entities only for what has identity and a lifecycle.
6. **Domain events to cross boundaries:** a significant change in an aggregate ← a Domain Event others listen to (`OrderPaid` → shipping/billing) — never direct calls between Aggregates.
7. **Injecting application services into entities is forbidden:** the entity remains domain-pure; the Action/UseCase (standard §2) is the orchestrator.

### 6.2 Ubiquitous Language — Binding Naming
- **Code terms = the domain expert's terms literally:** if the merchant says "booking" the code says `Booking`, not `ReservationEntity` — and if they say "settlement", no `SettlementProcessor` stands in its place.
- **A domain glossary is mandatory per project** in `projects/<name>/brain/CONTEXT.md`: a table of term ↔ meaning ↔ owning Aggregate — created at stage S2 and frozen with the contract.
- **No translators:** if you need to "explain" a code term to the product owner, that is a breach of the ubiquitous language = rename it, don't explain it.

### 6.3 Additional DO / DON'T Table (extends §5)
| ✅ Do | ❌ Don't |
|---------|-----------|
| ID references between Aggregates | embedding a full Entity inside another Aggregate |
| Domain Events for eventual consistency | DB transactions spanning Aggregate boundaries |
| validation inside the root | checking invariants in a Controller or external service |
| a term glossary frozen in S2 | technical naming with no client-language counterpart |

**Date added:** 2026-08-24 — INT-EVOL P1 (owner order).
