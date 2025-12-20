<?php

namespace App\Console\Commands;

use App\Models\Course;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Http;

class SyncCourses extends Command
{
    protected $signature = 'devnexus:sync-courses';

    protected $description = 'Syncs course list from Python AI service to Laravel DB';

    public function handle()
    {
        $this->info('📡 Connecting to Python Service...');

        try {
            $response = Http::timeout(10)->get('http://localhost:5001/sync-courses');
        } catch (\Exception $e) {
            $this->error("❌ Connection Failed. Ensure 'python app.py' is running.");

            return;
        }

        if ($response->failed()) {
            $this->error('❌ Python service returned an error.');

            return;
        }

        $courses = $response->json();
        $this->info('✅ Found '.count($courses).' courses. Processing...');

        $this->withProgressBar($courses, function ($c) {

            // 1. SMART KEY DETECTION
            // Try 'course_code' (JSON format), fallback to 'code' (DB format)
            $code = $c['course_code'] ?? $c['code'] ?? null;
            $name = $c['course_name'] ?? $c['name'] ?? 'Unknown Course';
            $outline = $c['course_content_outline'] ?? $c['learning_outline'] ?? [];
            $skills = $c['associated_skills'] ?? [];
            $nextCode = $c['next_course_code'] ?? null;

            if (! $code) {
                // Skip if we can't find a code
                return;
            }

            // 2. UPDATE OR CREATE
            Course::updateOrCreate(
                ['code' => $code],
                [
                    'name' => $name,
                    'learning_outline' => $outline,
                    'associated_skills' => $skills,
                ]
            );

            // 3. STORE NEXT CODE FOR LINKING LATER
            // (We can't link immediately because the next course might not exist yet)
            if ($nextCode) {
                Course::where('code', $code)->update(['next_course_code' => $nextCode]);
            }
        });

        $this->newLine();
        $this->info('✅ Sync Complete! Your database is fixed.');
    }
}
