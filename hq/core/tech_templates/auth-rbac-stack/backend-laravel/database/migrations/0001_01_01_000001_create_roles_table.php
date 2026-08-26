<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Creates the `roles` table — the anchor of the manual RBAC layer.
 * Ordered FIRST so that `users.role_id` can safely constrain against it.
 *
 * Example names: super-admin | manager | user
 */
return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('roles', function (Blueprint $table) {
            $table->id();
            $table->string('name')->unique();       // machine name: super-admin|manager|user
            $table->string('display_name');          // human-readable label
            $table->text('description')->nullable(); // what this role may do
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('roles');
    }
};
