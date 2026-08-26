<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Creates the `permissions` table — atomic abilities (e.g. users.create)
 * grouped logically (users | reports | ...) for admin UI filtering.
 */
return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('permissions', function (Blueprint $table) {
            $table->id();
            $table->string('name')->unique();   // machine name: users.create, reports.export ...
            $table->string('group_name');        // logical grouping: users | reports | ...
            $table->string('display_name');      // human-readable label
            $table->timestamps();

            $table->index('group_name');         // hot filter: list permissions by group
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('permissions');
    }
};
