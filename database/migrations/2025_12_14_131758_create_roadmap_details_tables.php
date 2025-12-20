<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
public function up(): void
{
    // 1. Phases Table (e.g., "Week 1: Foundation")
    Schema::create('roadmap_phases', function (Blueprint $table) {
        $table->id();
        $table->foreignId('roadmap_id')->constrained()->onDelete('cascade');
        $table->string('title'); // e.g., "Phase 1"
        $table->timestamps();
    });

    // 2. Tasks Table (The 4 steps inside each phase)
    Schema::create('phase_tasks', function (Blueprint $table) {
        $table->id();
        $table->foreignId('roadmap_phase_id')->constrained()->onDelete('cascade');
        $table->string('content'); // e.g., "Learn PHP Syntax"
        $table->timestamps();
    });

    // 3. Suggestions Table (For Projects & New Skills)
    Schema::create('roadmap_suggestions', function (Blueprint $table) {
        $table->id();
        $table->foreignId('roadmap_id')->constrained()->onDelete('cascade');
        $table->string('type'); // "skill" or "project"
        $table->text('content');
        $table->timestamps();
    });
}

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('roadmap_details_tables');
    }
};
