# 📦 Unified Response Standard — Envelope v1
**Status:** binding on all ecosystem APIs · **Version:** v1 · **Last updated:** 2026-08-23
> Any endpoint not wrapping its response in this shape = rejection at the quality gate (Law 8). Amending this standard requires a documented brd-ceo decision.

## 1️⃣ The Basic Shape
```json
{
  "success": true,
  "message": "human-readable message shown to the user as-is",
  "data": {},
  "error": {
    "code": "UPPER_SNAKE_CODE",
    "message": "human-readable message on failure",
    "details": []
  },
  "meta": {
    "request_id": "0f8b7c2a-1e4d-4c9a-b6f2-9d3e5a7c1b88",
    "timestamp": "2026-08-23T10:30:00Z",
    "envelope_version": "v1",
    "pagination": {"page": 1, "per_page": 20, "total": 150}
  }
}
```
- `message` ← human-readable text for direct display. `error.code` ← a stable English constant for programming, never shown to the user.
- `data` is always `null` on failure, and `error` is always `null` on success.
- `pagination` appears only in list responses; otherwise `null`.

## 2️⃣ Mapping HTTP Codes to Error Codes
| HTTP | error.code | When |
|------|-----------|-----|
| 200 / 201 | — (`success:true`) | successful read/update (200) or resource creation (201) |
| 204 | — (no response body) | successful delete — not wrapped in the Envelope |
| 401 | `UNAUTHENTICATED` | no token, expired token, or invalid token |
| 403 | `FORBIDDEN` | valid token but insufficient permissions |
| 404 | `NOT_FOUND` | the requested resource does not exist |
| 409 | `CONFLICT` | state conflict: email already in use, stale record version |
| 422 | `VALIDATION_ERROR` | input validation failed — field details in `error.details` |
| 429 | `RATE_LIMITED` | request limit exceeded |
| 500 | `SERVER_ERROR` | internal error — generic message only, with zero technical detail |
| 503 | `SERVICE_UNAVAILABLE` | the service or an external dependency is temporarily unavailable |

## 3️⃣ The Four Reference Examples

### Example 1 — Success: list with pagination (200)
```json
{
  "success": true,
  "message": "Projects fetched successfully",
  "data": [
    {"id": 1, "name": "Customer Platform", "status": "active"},
    {"id": 2, "name": "Payment Gateway", "status": "draft"}
  ],
  "error": null,
  "meta": {
    "request_id": "0f8b7c2a-1e4d-4c9a-b6f2-9d3e5a7c1b88",
    "timestamp": "2026-08-23T10:30:00Z",
    "envelope_version": "v1",
    "pagination": {"page": 1, "per_page": 20, "total": 57}
  }
}
```

### Example 2 — Input validation failure (422 VALIDATION_ERROR)
```json
{
  "success": false,
  "message": "The submitted inputs are invalid",
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The submitted inputs are invalid",
    "details": [
      {"field": "email", "message": "The email format is invalid"},
      {"field": "password", "message": "The password must be at least 8 characters"}
    ]
  },
  "meta": {
    "request_id": "7c1d9e3f-2a5b-4f80-b1c7-3e9a6d2f4c10",
    "timestamp": "2026-08-23T10:31:45Z",
    "envelope_version": "v1",
    "pagination": null
  }
}
```

### Example 3 — Unauthenticated (401 UNAUTHENTICATED)
```json
{
  "success": false,
  "message": "Your session has expired, please sign in again",
  "data": null,
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Your session has expired, please sign in again",
    "details": []
  },
  "meta": {
    "request_id": "a2e4f6b8-3c5d-4970-8e1f-5b7d9c2a4e63",
    "timestamp": "2026-08-23T10:32:12Z",
    "envelope_version": "v1",
    "pagination": null
  }
}
```

### Example 4 — Server error (500 SERVER_ERROR)
```json
{
  "success": false,
  "message": "An unexpected error occurred, contact support with the request number",
  "data": null,
  "error": {
    "code": "SERVER_ERROR",
    "message": "An unexpected error occurred, contact support with the request number",
    "details": []
  },
  "meta": {
    "request_id": "d9b3f1a7-6e2c-4d58-a094-f1c8b5e3d274",
    "timestamp": "2026-08-23T10:33:01Z",
    "envelope_version": "v1",
    "pagination": null
  }
}
```
> ⚠️ On 500 and 503: it is **absolutely forbidden** for any stack trace, file path, table name, or SQL query to appear in any field. Full diagnostics stay in backend logs, linked solely by `request_id`.

## 4️⃣ Laravel Trait — `RespondsWithEnvelope`
```php
<?php

namespace App\Traits;

use Illuminate\Http\JsonResponse;
use Illuminate\Support\Str;

trait RespondsWithEnvelope
{
    protected function success(mixed $data = null, string $message = 'Done successfully',
        int $status = 200, ?array $pagination = null): JsonResponse
    {
        return response()->json([
            'success' => true, 'message' => $message, 'data' => $data,
            'error'   => null, 'meta'    => $this->envelopeMeta($pagination),
        ], $status);
    }

    protected function error(string $code, string $message, int $status = 500,
        array $details = []): JsonResponse
    {
        return response()->json([
            'success' => false, 'message' => $message, 'data' => null,
            'error'   => ['code' => $code, 'message' => $message, 'details' => $details],
            'meta'    => $this->envelopeMeta(null),
        ], $status);
    }

    private function envelopeMeta(?array $pagination): array
    {
        return [
            'request_id'       => request()->header('X-Request-Id') ?: (string) Str::uuid(),
            'timestamp'        => now()->toIso8601String(),
            'envelope_version' => 'v1',
            'pagination'       => $pagination,
        ];
    }
}
```

## 5️⃣ Interface Contracts — Intercepting the Envelope in the Frontend
Principle: program branching uses the stable `error.code`, and human display uses the localized `message`. In every error case the `request_id` is logged locally and surfaced to the user on critical errors so support can trace it.

| HTTP | React — axios interceptor → toast | Flutter — dio interceptor → SnackBar |
|------|-----------------------------------|--------------------------------------|
| 200/201 | normal continuation + `toast.success(res.message)` | continue + green `SnackBar` with `res.message` |
| 204 | update local state, no toast | update local state, no SnackBar |
| 401 | clear token → `navigate('/login')` + `toast.info(message)` | clear token → `/login` + neutral SnackBar |
| 403 | `toast.error(message)` and stay on page | red SnackBar with `message` and stay |
| 404 | `toast.error(message)` or a "not found" page per context | red SnackBar or a "not found" screen |
| 409 | `toast.warning(message)` + refetch the latest version | orange SnackBar + refetch the latest version |
| 422 | bind `error.details` to form fields (field errors) | bind `details` to `TextFormField.errorText` |
| 429 | `toast.warning(message)` + disable the button temporarily (backoff) | orange SnackBar + delay the retry |
| 500 | `toast.error(message)` + log `request_id` for support | red SnackBar + share `request_id` with support |
| 503 | an "under maintenance" banner + automatic retry | maintenance screen + a "retry" button |

## 6️⃣ Binding Rules
1. **`request_id` links to logs:** generated centrally in one middleware, printed in every backend log entry for the same request, and returned in `meta.request_id`. Generating different identifiers in different layers is forbidden.
2. **No server structure leakage:** no stack traces, no file paths, no table/column/SQL query names, no internal service names — neither in `message` nor in `details`. Technical details stay in logs only.
3. **Backward compatibility via `envelope_version`:** adding a new field to `meta` or `data` = a non-breaking, permitted change; deleting a field, changing its type, or changing a `code`'s semantics = breaking → requires releasing `v2` while keeping `v1` until every interface migrates. An interface hitting an unknown version safely rejects the request rather than failing silently.
4. **Messages are always human-readable** in `message` (Law 11); `error.code` alone is a stable English constant for programming.
5. **204 has no body:** the absent body is the agreement — never wrapped in the Envelope.
