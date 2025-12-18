<?php
namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Http;
use App\Models\Course;

class SyncCourses extends Command
{
    protected $signature = 'devnexus:sync-courses';
    protected $description = 'Syncs course list from Python AI service to Laravel DB';

    public function handle()
{
    $response = Http::get('http://localhost:5001/sync-courses');
    $courses = $response->json();

    $this->info('Step 1: Creating/Updating course names...');
    foreach ($courses as $c) {
        Course::updateOrCreate(
            ['code' => $c['code']],
            ['name' => $c['name']]
        );
    }

    $this->info('Step 2: Linking roadmap (Next Course Codes)...');
    foreach ($courses as $c) {
        if (!empty($c['next_course_code'])) {
            Course::where('code', $c['code'])->update([
                'next_course_code' => $c['next_course_code']
            ]);
        }
    }

    $this->info('✅ Sync Complete!');
}
}