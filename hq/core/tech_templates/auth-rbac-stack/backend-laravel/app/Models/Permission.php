<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

/**
 * Atomic ability (e.g. users.create) grouped for admin UI filtering
 * (migrations/0001_01_01_000003).
 */
class Permission extends Model
{
    protected $fillable = ['name', 'group_name', 'display_name'];

    /** Roles granted this permission through permission_role pivot. */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class, 'permission_role');
    }
}
