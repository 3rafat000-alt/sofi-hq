<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;

/**
 * RBAC anchor table — machine names: super-admin | manager | user
 * (migrations/0001_01_01_000001, ordered first so users.role_id constrains safely).
 */
class Role extends Model
{
    protected $fillable = ['name', 'display_name', 'description'];

    /**
     * Direct FK on users.role_id (restrictOnDelete) → hasMany.
     * Not belongsToMany: there is no role_user pivot in the frozen schema.
     */
    public function users(): HasMany
    {
        return $this->hasMany(User::class);
    }

    /** Grants live in permission_role pivot with cascadeOnDelete. */
    public function permissions(): BelongsToMany
    {
        return $this->belongsToMany(Permission::class, 'permission_role');
    }
}
