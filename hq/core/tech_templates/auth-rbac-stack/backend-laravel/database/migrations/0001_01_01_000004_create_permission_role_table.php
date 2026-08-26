<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Pivot linking `permissions` to `roles` (manual RBAC, no spatie).
 * Composite UNIQUE prevents duplicate grants; explicit role_id index
 * serves the hottest query: "all permissions of a given role".
 */
return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('permission_role', function (Blueprint $table) {
            $table->id();
            $table->foreignId('permission_id')
                ->constrained()
                ->cascadeOnDelete();                    // grant dies with its permission (pivot row only)
            $table->foreignId('role_id')
                ->constrained()
                ->cascadeOnDelete();                    // grant dies with its role (pivot row only)

            $table->unique(['permission_id', 'role_id']); // idempotent grants + leading permission_id lookups
            $table->index('role_id');                     // hot path: SELECT permission_id ... WHERE role_id = ?
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('permission_role');
    }
};
