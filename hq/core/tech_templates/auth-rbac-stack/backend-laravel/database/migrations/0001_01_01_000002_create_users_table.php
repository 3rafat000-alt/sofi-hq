<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Creates the `users` table with a hard FK to `roles` (RBAC anchor)
 * and a lifecycle status: active | suspended | banned.
 *
 * Runs AFTER `roles` (file order 000002 > 000001) so the FK is valid.
 */
return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('email')->unique();                 // login identity + lookup index
            $table->timestamp('email_verified_at')->nullable();
            $table->string('password');                         // hashed only — never raw
            $table->foreignId('role_id')
                ->constrained()                                 // -> roles.id
                ->restrictOnDelete();                           // block role deletion while users exist
            $table->string('status', 20)->default('active');    // active|suspended|banned
            $table->rememberToken();
            $table->timestamps();

            $table->index('status');                            // hot filter: WHERE status = 'active'
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('users');
    }
};
