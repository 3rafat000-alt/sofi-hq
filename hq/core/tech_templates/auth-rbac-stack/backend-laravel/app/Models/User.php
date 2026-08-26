<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Sanctum\HasApiTokens; // first-party tokens only (SPA/mobile)

/**
 * users table (migrations/0001_01_01_000002):
 * role_id FK → roles.id (restrictOnDelete) + status lifecycle gate.
 */
class User extends Authenticatable
{
    use HasApiTokens;

    protected $fillable = ['name', 'email', 'password', 'role_id', 'status'];

    protected $hidden = ['password', 'remember_token'];

    protected function casts(): array
    {
        return [
            'email_verified_at' => 'datetime',
            // Hashes on set — controllers may assign plain input safely.
            'password' => 'hashed',
        ];
    }

    public function role(): BelongsTo
    {
        return $this->belongsTo(Role::class);
    }

    /* ── Lifecycle gates (users.status: active|suspended|banned) ── */

    /** Login and every role gate refuse anything but active. */
    public function isActive(): bool
    {
        return $this->status === 'active';
    }

    /* ── RBAC checks through relations — Eager-Loaded once ── */

    /**
     * Machine-name match against users.role_id. Variadic so callers can pass
     * several roles: $user->hasRole('super-admin', 'manager').
     */
    public function hasRole(string ...$names): bool
    {
        if (! $this->relationLoaded('role')) {
            $this->load('role');
        }

        return in_array($this->role?->name, $names, true);
    }

    /**
     * Permission check through role.permissions.
     * Loads the whole chain once; repeated calls hit memory only (no N+1).
     */
    public function hasPermissionTo(string $name): bool
    {
        $this->loadMissing('role');

        if ($this->role === null) {
            return false;
        }

        $this->role->loadMissing('permissions');

        return $this->role->permissions->contains('name', $name);
    }
}
