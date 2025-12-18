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
        Schema::table('roadmaps', function (Blueprint $table) {
            $table->string('status')->default('active')->after('skills'); // active, completed, archived
            $table->integer('progress_percent')->default(0)->after('status');
        });

        Schema::table('phase_tasks', function (Blueprint $table) {
            $table->boolean('is_completed')->default(false)->after('content');
        });
    }

    public function down(): void
    {
        Schema::table('roadmaps', function (Blueprint $table) {
            $table->dropColumn(['status', 'progress_percent']);
        });

        Schema::table('phase_tasks', function (Blueprint $table) {
            $table->dropColumn('is_completed');
        });
    }
};
