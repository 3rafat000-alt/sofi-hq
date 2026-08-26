<?php

namespace App\Http\Responses;

use Illuminate\Http\JsonResponse;

/**
 * Envelope v1 — the single output contract (hq/core/API-ENVELOPE.md).
 * Root keys are fixed forever: success | data | error | meta.
 * Raw exceptions never reach consumers — everything wraps here.
 */
final class ApiResponse
{
    /** Success carrying a data payload. */
    public static function data(mixed $data = null, int $status = 200): JsonResponse
    {
        return response()->json(self::wrap($data, null), $status);
    }

    /** Success carrying only a bilingual message (logout...). */
    public static function success(string $messageAr, string $messageEn, int $status = 200): JsonResponse
    {
        return self::data(['message_ar' => $messageAr, 'message_en' => $messageEn], $status);
    }

    /** Failure with unified code + bilingual messages (+ field errors for validation). */
    public static function error(
        string $code,
        string $messageAr,
        string $messageEn,
        int $status,
        array $fields = [],
    ): JsonResponse {
        return response()->json(self::wrap(null, [
            'code' => $code,
            'message_ar' => $messageAr,
            'message_en' => $messageEn,
            // Stable shape: null when no field errors, map when validation failed.
            'fields' => $fields === [] ? null : $fields,
        ]), $status);
    }

    /* ── Thin semantic shortcuts over error() — codes fixed by API-ENVELOPE.md ── */

    public static function validationFailed(array $fields): JsonResponse
    {
        return self::error('VALIDATION_FAILED', 'الحقول المدخلة غير صحيحة.', 'The given data was invalid.', 422, $fields);
    }

    public static function unauthenticated(): JsonResponse
    {
        return self::error('UNAUTHENTICATED', 'غير مصرح — سجّل الدخول أولاً.', 'Unauthenticated.', 401);
    }

    public static function forbidden(string $messageAr = 'لا تملك الصلاحية للقيام بهذا الإجراء.', string $messageEn = 'You do not have permission to perform this action.'): JsonResponse
    {
        return self::error('FORBIDDEN', $messageAr, $messageEn, 403);
    }

    public static function notFound(): JsonResponse
    {
        return self::error('NOT_FOUND', 'المورد المطلوب غير موجود.', 'Resource not found.', 404);
    }

    public static function rateLimited(): JsonResponse
    {
        return self::error('RATE_LIMITED', 'عدد الطلبات كبير جداً — حاول لاحقاً.', 'Too many requests — slow down.', 429);
    }

    /** The exact envelope skeleton — private so no caller can drift from the contract. */
    private static function wrap(mixed $data, ?array $error): array
    {
        return [
            'success' => $error === null,
            'data' => $data,
            'error' => $error,
            'meta' => [
                // UTC with literal "Z" suffix — pinned byte-for-byte by the spec samples.
                'timestamp' => now()->utc()->format('Y-m-d\TH:i:s\Z'),
                'api_version' => 'v1',
            ],
        ];
    }
}
