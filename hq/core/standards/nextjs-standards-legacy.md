# NEXTJS-STANDARDS — Standard for Building React Interfaces via Next.js App Router

> **Status (updated 2026-08-24 · INT-GTW-033):** fully retired — by owner order Next.js was removed from projects permanently (frontend-web deleted; DEC-0009 revoked). This file remains a documentation reference for existing projects should they ever need historical maintenance.
> **Previous status (R2):** was suspended for new projects in favor of unifying on Flutter/Dart.
> **Historical principle:** React was built exclusively via Next.js App Router — no bare Vite and no CRA, however simpler they appeared.
> **Responses:** every network call adhered to Envelope v1 (`api-envelope.md`) with unwrapping confined to Infrastructure only.
> **Layer discipline:** complemented `ddd-capsule.md` §3 without replacing it — same capsule, powered by a Next.js engine.

## | 1. Why Next.js over Bare React (mandatory justification required for any objection)

| Capability | Bare React (Vite/CRA) | Next.js App Router |
|--------|--------------------------|---------------------|
| SEO and first page paint | Empty SPA until JS executes — search crawlers and slow mobile devices suffer | SSR/SSG: full HTML from the server from the first byte |
| Server components | Nonexistent — everything is a client bundle | Server Components by default: data fetching next to the database and zero JS shipped to the consumer |
| Performance | A single bundle that bloats with every feature | Automatic code-splitting per route + streaming + progressive loading |
| Routing | react-router, manual to configure and guard | File-based routing + nested layouts + ready-made UI states (loading/error) |
| Infrastructure | Requires manual proxy/CDN/env configuration | Built-in middleware, next/image and next/font preconfigured |

**Rule:** any new React project starts with `create-next-app` directly — the "small project" objection is rejected; today's small project is tomorrow's production, and migrating later is always more expensive.

## | 2. Project Tree — Feature Capsule over a Thin App Router

```
src/
├── app/                                  # thin wrappers only — zero business logic
│   ├── layout.tsx                        # html dir="rtl" lang="ar" + fonts + providers
│   ├── page.tsx                          # imports presentation and hands off
│   ├── products/page.tsx                 # <ProductsScreen /> and nothing more
│   ├── loading.tsx                       # route skeleton
│   ├── error.tsx                         # error boundary ('use client')
│   └── not-found.tsx                     # Arabic 404 page
├── features/products/
│   ├── domain/
│   │   ├── product.ts                    # pure Entity + Types — no fetch/axios
│   │   └── rules.ts                      # pure testable business rules
│   ├── application/
│   │   └── useGetProducts.ts             # TanStack Query hooks — for interactivity
│   ├── infrastructure/
│   │   ├── productsApi.ts                # api client — receives Envelope v1 from Laravel
│   │   └── productsMapper.ts             # DTO → Entity — the only envelope-unwrapping boundary
│   └── presentation/
│       ├── components/ProductCard.tsx    # Server Component where possible
│       └── screens/ProductsScreen.tsx    # the composed screen
└── shared/
    ├── lib/apiClient.ts                  # axios instance + unified-envelope interceptor
    └── types/envelope.d.ts               # the official Envelope<T> type
```

**Tree rules:**
- `src/app/**` files are ≤ 10 lines mostly: import a screen from `presentation` and export it — business logic there = L2 violation.
- Importing one feature's `presentation` inside another feature is forbidden — the capsule owns independent boundaries (Law 2 in spirit).
- Every HTTP call passes through `infrastructure` exclusively — no fetch inside a component or hook directly.

### Thin app/ — the binding model
```tsx
// src/app/products/page.tsx — this is all that is permitted here
import { ProductsScreen } from '@/features/products/presentation/screens/ProductsScreen';
export const metadata = { title: 'Products' };
export default function ProductsPage() {
  return <ProductsScreen />;
}
```

## | 3. RSC Discipline — everything is a Server Component by default

- **Default is Server Component:** no `'use client'` — runs on the server, fetches its own data, zero weight on the browser.
- **`'use client'` only when one of three applies:** interactivity (`onClick`/forms) · state (`useState`/`useReducer`) · browser APIs (`window`/localStorage/observers).
- The boundary moves bottom-up: make the leaf the client component — never convert an entire screen because one button is interactive; pass a Server Component as `children` into a client container.
- Forbidden inside a Server Component: `useState/useEffect/onClick` and libraries depending on `window`.

```tsx
// presentation/components/ProductCard.tsx — Server by default, no directive
export function ProductCard({ product }: { product: Product }) {
  return <article>{product.name}</article>;
}

// presentation/components/AddToCartButton.tsx — interactivity ⇒ client
'use client';
export function AddToCartButton({ id }: { id: number }) {
  const { mutate } = useAddToCart();
  return <button onClick={() => mutate(id)}>Add to cart</button>;
}
```

## | 4. Data — OpenAPI Contract + Envelope v1 across two paths

- **Server path (RSC):** direct `fetch` in infrastructure against the frozen OpenAPI contract issued by the backend room (S4) — no mocks and no verbal assumptions (S5 gate).
- **Interactive path (client):** TanStack Query inside `application/` hooks — unified caching, retry, and loading state.

```ts
// infrastructure/productsApi.ts — RSC: fetch + unwrap in the mapper
import { toProduct } from './productsMapper';
export async function fetchProduct(id: string): Promise<Product> {
  const res = await fetch(`${process.env.API_BASE_URL}/products/${id}`, {
    headers: { Accept: 'application/json' }, cache: 'no-store',
  });
  return toProduct(await res.json()); // Envelope v1 enters here alone
}
// application/useGetProducts.ts — client: TanStack Query
'use client';
export function useGetProducts(filters?: ProductFilters) {
  return useQuery({
    queryKey: ['products', filters],
    queryFn: () => productsApi.list(filters),
  });
}
```

- **A unified axios interceptor** in `shared/lib/apiClient.ts`: verifies `success:false` → toast showing the `error.message` text as-is, and 401 → redirect to login — scattered try/catch of network errors inside components is forbidden (the `api-envelope.md` §HTTP pattern).

## | 5. Interface States — loading.tsx / error.tsx / not-found.tsx are mandatory

Every route has its three states before being considered complete (the eight states in `knowledge-cx-uiux.md`):

```tsx
// src/app/products/loading.tsx — skeleton mirroring the screen's own structure
export default function Loading() { return <ProductsSkeleton />; }
// src/app/products/error.tsx — must be client (reset)
'use client';
export default function Error({ reset }: { reset: () => void }) {
  return <div role="alert"><p>Unable to display products</p><button onClick={reset}>Try again</button></div>;
}
// src/app/not-found.tsx — clear Arabic copy plus a way back
export default function NotFound() {
  return <main><h1>Page not found</h1><Link href="/">Back to home</Link></main>;
}
```

- Skeletons match the actual content layout (layout shift = zero) — no generic empty spinner.
- `error.tsx` logs the error to observability and shows a human-readable message — no stack trace for the user.

## | 6. middleware — Sanctum Auth Guard at Route Boundaries

```ts
// src/middleware.ts — the single guard; pages do not inspect the session themselves
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const PROTECTED = ['/dashboard', '/admin'];
export function middleware(req: NextRequest) {
  const authed = req.cookies.has('laravel_session'); // Sanctum cookie
  if (!authed && PROTECTED.some((p) => req.nextUrl.pathname.startsWith(p))) {
    const url = req.nextUrl.clone(); url.pathname = '/login';
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}
export const config = { matcher: ['/dashboard/:path*', '/admin/:path*'] };
```

- The protection decision lives centrally in middleware — scattered per-page protection is forbidden.
- A 401 arriving through the interceptor after session expiry = clear state + redirect `/login` (coordinated with `api-envelope.md`).

## | 7. Performance & Arabic RTL — next/image, next/font, and metadata

```tsx
// src/app/layout.tsx — the root reference
import { Cairo } from 'next/font/google';
const cairo = Cairo({ subsets: ['arabic', 'latin'], variable: '--font-cairo' });
export const metadata: Metadata = { title: { default: 'SOFI', template: '%s | SOFI' } };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl" className={cairo.variable}>
      <body>{children}</body>
    </html>
  );
}
```

- Images always via `next/image`: explicit `sizes` + `priority` only for the LCP image — raw `<img>` is forbidden.
- Fonts via `next/font` at build time (zero FOUT, zero external requests) — a primary Arabic font such as Cairo/Tajawal.
- `lang="ar"` and `dir="rtl"` at the root are mandatory; layout uses logical properties (`ms-*`/`me-*`), not physical left/right — and any isolated LTR component sets its own direction without breaking the root.

## | 8. Secrets — server only, NEXT_PUBLIC_ for the sole exception

| Variable | Where read | Example |
|---------|-----------|------|
| Secret (server-only) | RSC / middleware / route handlers | internal `API_BASE_URL` · Sanctum keys · DB |
| Shared | client + server | `NEXT_PUBLIC_APP_NAME` |

- Anything without the `NEXT_PUBLIC_` prefix never reaches the browser — assume anything else will leak if you put it in a client component.
- `.env*` files are always in `.gitignore`; `.env.example` with no real values is the documented reference.
- Passing a secret via props from a Server to a client component is forbidden — the prefix is the boundary.

## | 9. DO / DON'T Table — binding on room 06

| ✅ Do | ❌ Don't |
|---------|-----------|
| `create-next-app` for every new React project | bare Vite/CRA "because it's simpler" |
| Server Component as the default for every component | `'use client'` at the top of the screen "just in case" |
| `app/page.tsx` imports a screen from presentation | fetching/state/business logic inside `app/` |
| RSC fetches + a mapper unwrapping Envelope v1 | useEffect + raw fetch inside a component |
| TanStack Query in application-layer hooks | server state scattered into useState |
| one unified envelope interceptor → localized toast | try/catch of network errors in every component |
| loading/error/not-found for every route | a generic spinner or white screen on failure |
| central Sanctum-guard middleware | scattered session checks inside each page |
| next/image + next/font + dir="rtl" from the root | raw img + externally linked fonts + manual rtl later |
| server-only secrets and NEXT_PUBLIC_ for shared values | an API key inside NEXT_PUBLIC_ "temporarily" |

*Last updated: 2026-08-23 — standard created and made mandatory on room 06. Any structural change to it = architectural decision routed through brd-ceo.*

## | 10. 🎯 Approved Icons — Heroicons exclusively

- **The only package:** `@heroicons/react` — the official package for the Tailwind stack and the single source of icons in SOFI projects.
- **Sizes:** `outline` 24 (default for interfaces) · `solid` 24 (active/filled states) · `mini` 20 (dense menus) · `micro` 16 (badges).
- **Import:** tree-shakeable named imports only — `import { ArrowRightIcon } from '@heroicons/react/24/outline'`.
- **Forbidden:** any other icon library or duplicated hand-written SVGs.
- **Location:** icons live inside `presentation/` exclusively.
- **Alignment:** Heroicons names align design specs with implementation (example: Heroicon `arrow-right`).
