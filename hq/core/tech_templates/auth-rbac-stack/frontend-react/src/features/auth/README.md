# features/auth — The Authentication Layer (Contract-First)

A React authentication layer built strictly on the official contract:
`tech_templates/auth-rbac-stack/backend-laravel/docs/openapi-auth.md` (OpenAPI 3.1) + the envelope from `hq/core/standards/api-envelope.md`.

## File Map

| File | Role |
|-------|-------|
| `types.ts` | contract types verbatim — User / Role / AuthResponse / ApiError / Envelope\<T\> |
| `schemas.ts` | Zod schemas matching RegisterRequest/LoginRequest + their Arabic messages |
| `api/authApi.ts` | the backbone: unwraps the v1 envelope **once** + register/login/logout/me/assignRole |
| `hooks/useAuth.ts` | TanStack Query: useMe (query) + useLogin/useRegister/useLogout/useAssignRole (mutations) |
| `components/LoginForm.tsx` | login form — react-hook-form + zodResolver, merging backend field errors |
| `components/RegisterForm.tsx` | register form — same pattern with password confirmation |
| `pages/LoginPage.tsx` / `pages/RegisterPage.tsx` | centered RTL cards |

## Required Packages

```bash
npm i @tanstack/react-query@^5 react-hook-form@^7 @hookform/resolvers@^3 zod@^3 react-router-dom@^6
npm i -D tailwindcss@^3
```

> `zod ^3` is mandatory: the schemas use the version-3 API (`z.string().email()` and `superRefine`).

## Quick Setup

### 1) Providers at the entry point

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import LoginPage from './features/auth/pages/LoginPage';
import RegisterPage from './features/auth/pages/RegisterPage';

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
```

### 2) Interface tokens (dark-mode ready)

In `globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: 0 0% 100%;
  --foreground: 222 47% 11%;
  --card: 0 0% 100%;
  --card-foreground: 222 47% 11%;
  --primary: 222 47% 31%;
  --primary-foreground: 210 40% 98%;
  --destructive: 0 84% 60%;
  --muted: 210 40% 96%;
  --muted-foreground: 215 16% 47%;
  --border: 214 32% 91%;
  --input: 214 32% 91%;
  --ring: 222 47% 31%;
}

.dark {
  --background: 240 10% 4%;
  --foreground: 0 0% 98%;
  --card: 240 10% 6%;
  --card-foreground: 0 0% 98%;
  --primary: 210 40% 90%;
  --primary-foreground: 222 47% 11%;
  --destructive: 0 63% 45%;
  --muted: 240 4% 16%;
  --muted-foreground: 240 5% 65%;
  --border: 240 4% 16%;
  --input: 240 4% 16%;
  --ring: 210 40% 80%;
}
```

And in `tailwind.config.js`:

```js
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: { DEFAULT: 'hsl(var(--card))', foreground: 'hsl(var(--card-foreground))' },
        primary: { DEFAULT: 'hsl(var(--primary))', foreground: 'hsl(var(--primary-foreground))' },
        destructive: 'hsl(var(--destructive))',
        muted: { DEFAULT: 'hsl(var(--muted))', foreground: 'hsl(var(--muted-foreground))' },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
      },
    },
  },
};
```

### 3) Route guarding via useMe

```tsx
function RequireAuth({ children }: { children: React.ReactNode }) {
  const me = useMe(); // does nothing without a token in the first place
  if (me.isPending) return <p className="text-center">Loading…</p>;
  if (me.data === undefined) return <Navigate to="/login" replace />;
  return <>{children}</>; // me.data.permissions ready for interface gating
}
```

### 4) The API Address

The default is `/api/v1` — to override when integrating, define `VITE_API_BASE_URL` in `.env`:

```env
VITE_API_BASE_URL=https://api.example.com/api/v1
```

## Architectural Guarantees Proven in Code

1. **The envelope is unwrapped once** in `unwrapEnvelope()` inside `authApi.ts` — no component touches raw JSON.
2. **UNAUTHENTICATED clears the session automatically** (binding-contract note 4) inside the envelope unwrapping.
3. **No mocks and no duplicated Server State**: identity lives only in TanStack Query's memory; the token is a single credential stored in `localStorage` (`auth.token`).
4. **Backend field errors merge into the form**: `error.fields` from 422 are passed to `setError` with field names matching the contract.
5. **The Arabic server message** (`message_ar`) is always what appears in the global banner.

## Operational Notes

- Login/register throttling (10/minute) returns the `RATE_LIMITED` code with an Arabic message — it surfaces automatically in the banner.
- `useAssignRole` is available for changing another user's role (super-admin/manager only; the backend gate enforces it).
