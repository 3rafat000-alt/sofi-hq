<?php

namespace App\Http\Middleware;

use App\Http\Responses\ApiResponse;
use Closure;
use Illuminate\Http\Request;

/**
 * Route-level RBAC gate. Accepts comma-separated role names:
 *   ->middleware('role:super-admin,manager')
 *
 * Laravel delivers parameters as ONE string, so we explode here.
 * Fail-closed: an empty role list denies everyone by design.
 */
class EnsureUserHasRole
{
    public function handle(Request $request, Closure $next, string $roles): mixed
    {
        $user = $request->user();

        if ($user === null) {
            return ApiResponse::unauthenticated();
        }

        // Lifecycle gate — suspended/banned never pass, even with the right role.
        if (! $user->isActive()) {
            return ApiResponse::forbidden(
                'الحساب غير نشط.',
                'Account is not active.',
            );
        }

        foreach (explode(',', $roles) as $role) {
            if ($user->hasRole(trim($role))) { // reuses the loaded relation
                return $next($request);
            }
        }

        return ApiResponse::forbidden(); // 403 FORBIDDEN envelope
    }
}
