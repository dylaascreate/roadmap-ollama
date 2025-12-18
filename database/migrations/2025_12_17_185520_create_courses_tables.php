<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up()
    {
        // 1. COURSES TABLE (Master List)
        Schema::create('courses', function (Blueprint $table) {
            $table->id();
            $table->string('code')->unique(); // e.g., 'DES3023'
            $table->string('name');           // e.g., 'Software Requirements'

            // Self-referencing FK (Roadmap Link)
            $table->string('next_course_code')->nullable();

            // NEW: Store the arrays from your JSON as JSON columns
            // This maps to 'course_content_outline' in your JSON
            $table->json('learning_outline')->nullable();

            // This maps to 'associated_skills' in your JSON
            $table->json('associated_skills')->nullable();

            $table->timestamps();
        });

        // 2. Add the Self-Referencing Foreign Key
        // We do this after creating the table to ensure the 'code' index exists
        Schema::table('courses', function (Blueprint $table) {
            $table->foreign('next_course_code')
                ->references('code')
                ->on('courses')
                ->onDelete('set null');
        });

        // 3. COURSE_USER TABLE (History/Progress)
        Schema::create('course_user', function (Blueprint $table) {
            $table->id();

            // Link to User
            $table->foreignId('user_id')->constrained()->onDelete('cascade');

            // Link to Course (using the string code)
            $table->string('course_code');
            $table->foreign('course_code')
                ->references('code')
                ->on('courses')
                ->onDelete('cascade');

            // Status tracking
            $table->enum('status', ['enrolled', 'completed', 'failed'])->default('enrolled');
            $table->string('grade')->nullable(); // e.g., 'A', 'B'

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        // Drop 'course_user' first because it depends on 'courses'
        Schema::dropIfExists('course_user');

        // Then drop 'courses'
        Schema::dropIfExists('courses');
    }
};
