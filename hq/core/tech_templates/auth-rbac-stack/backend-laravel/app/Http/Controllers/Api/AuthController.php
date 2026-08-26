<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\LoginRequest;
use App\Http\Requests\RegisterRequest;
use App\Http\Responses\ApiResponse;
use App\Models\Role;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

/**
 * Authentication engine — 5 endpoints, every byte wrapped in Envelope v1.
 */
class AuthController extends Controller
{
    private const DEFAULT_ROLE = 'user';

    /** POST /api/v1/register — create user + default role + token (201). */
    public function register(RegisterRequest $request): JsonResponse
    {
        [$user, $token] = DB::transaction(function () use ($request) {
            $validated = $request->validated();

            $user = User::create([
                'name' => $validated['name'],
                'email' => $validated['email'],
                // Plain input is fine — the 'hashed' cast hashes on set.
                'password' => $validated['password'],
                'status' => 'active',
            ]);

            // Default role assigned server-side, never client-supplied.
            $role = Role::query()->where('name', self::DEFAULT_ROLE)->firstOrFail();
            $user->update(['role_id' => $role->id]);

            return [
                $user->setRelation('role', $role),
                $user->createToken('auth')->plainTextToken,
            ];
        });

        return ApiResponse::data([
            'user' => $this->userPayload($user->loadMissing('role.permissions')),
            'token' => $token,
            'token_type' => 'Bearer',
        ], 201);
    }

    /** POST /api/v1/login — credential check + lifecycle gate + token (200). */
    public function login(LoginRequest $request): JsonResponse
    {
        $validated = $request->validated();

        // Eager-load the whole chain once — identity complete after login.
        $user = User::query()
            ->with('role.permissions')
            ->where('email', $validated['email'])
            ->first();

        if ($user === null || ! Hash::check($validated['password'], $user->password)) {
            return ApiResponse::error(
                'UNAUTHENTICATED',
                'بيانات الدخول غير صحيحة.',
                'Invalid credentials.',
                401,
            );
        }

        if (! $user->isActive()) {
            [$msgAr, $msgEn] = $user->status === 'banned'
                ? ['تم حظر هذا الحساب نهائياً.', 'This account has been permanently banned.']
                : ['هذا الحساب موقوف حالياً.', 'This account is currently suspended.'];

            return ApiResponse::error('FORBIDDEN', $msgAr, $msgEn, 403);
        }

        return ApiResponse::data([
            'user' => $this->userPayload($user),
            'token' => $user->createToken('auth')->plainTextToken,
            'token_type' => 'Bearer',
        ]);
    }

    /** POST /api/v1/logout — revokes only the current access token (200). */
    public function logout(Request $request): JsonResponse
    {
        $request->user()->currentAccessToken()?->delete();

        return ApiResponse::success('تم تسجيل الخروج بنجاح.', 'Logged out successfully.');
    }

    /** GET /api/v1/me — current identity with role + permissions (200). */
    public function me(Request $request): JsonResponse
    {
        $user = $request->user()->loadMissing('role.permissions'); // Eager Loading

        return ApiResponse::data(['user' => $this->userPayload($user)]);
    }

    /**
     * PUT /api/v1/users/{user}/role — managers only ('role:super-admin,manager').
     * Changes another user's role; guards privilege escalation to super-admin.
     */
    public function assignRole(Request $request, User $user): JsonResponse
    {
        $validated = $request->validate([
            'role' => ['required', 'string', 'exists:roles,name'],
        ], [
            'role.required' => 'اسم الدور الجديد مطلوب.',
            'role.exists' => 'الدور المحدد غير موجود.',
        ]);

        $newRole = Role::query()->where('name', $validated['role'])->firstOrFail();

        // Escalation guard: only super-admin may grant super-admin or touch its holders.
        if (! $request->user()->hasRole('super-admin')
            && ($newRole->name === 'super-admin' || $user->hasRole('super-admin'))) {
            return ApiResponse::forbidden(
                'لا يمكن لغير مدير النظام التعامل مع دور super-admin.',
                'Only a super-admin may grant or modify the super-admin role.',
            );
        }

        $user->update(['role_id' => $newRole->id]);

        return ApiResponse::data([
            'user' => $this->userPayload(
                $user->setRelation('role', $newRole)
            ),
        ]);
    }

    /* ── Contract shapers — exact field names React/Flutter build against ── */

    /**
     * Canonical user projection — never a raw model.
     * permissions: flat machine-name strings for UI gating.
     */
    private function userPayload(User $user): array
    {
        $user->loadMissing('role');
        $role = $user->role;
        $role?->loadMissing('permissions');

        return [
            'id' => $user->id,
            'name' => $user->name,
            'email' => $user->email,
            'status' => $user->status,
            'created_at' => $user->created_at?->toISOString(),
            'role' => $role === null ? null : [
                'id' => $role->id,
                'name' => $role->name,
                'display_name' => $role->display_name,
            ],
            'permissions' => $role?->permissions
                ?->pluck('name')
                ->values()
                ->all() ?? [],
        ];
    }
}
