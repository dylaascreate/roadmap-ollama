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
    // 1. Master List of Courses
    Schema::create('courses', function (Blueprint $table) {
        $table->string('code')->primary(); // String ID: "DES3053"
        $table->string('name');
        $table->timestamps();
    });

    // 2. History Table (What has the user finished?)
    Schema::create('course_user', function (Blueprint $table) {
        $table->id();
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        
        // Link to the 'courses' table using the string code
        $table->string('course_code');
        $table->foreign('course_code')->references('code')->on('courses')->onDelete('cascade');
        
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
        Schema::dropIfExists('courses_tables');
    }
};
