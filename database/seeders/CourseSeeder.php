<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class CourseSeeder extends Seeder
{
    public function run(): void
    {
        // 1. Insert/Update Courses (Ensure they exist first)
        $courses = [
            ['code' => 'DES3023', 'name' => 'Software Requirements'],
            ['code' => 'DES3043', 'name' => 'Software Design'],
            ['code' => 'DES3073', 'name' => 'Software Engineering Project'],
            ['code' => 'DTS3013', 'name' => 'Structured Programming'],
            ['code' => 'DTS3093', 'name' => 'Object Oriented Programming'],
        ];

        foreach ($courses as $c) {
            DB::table('courses')->updateOrInsert(
                ['code' => $c['code']],
                ['name' => $c['name']]
            );
        }

        // 2. DEFINE THE ROADMAP (The Links)
        // This is the only place you edit the flow now.
        $roadmap = [
            'DES3023' => 'DES3043', // Requirements -> Design
            'DES3043' => 'DES3073', // Design -> Project
            'DTS3013' => 'DTS3093', // Structured -> OOP
        ];

        foreach ($roadmap as $current => $next) {
            DB::table('courses')
                ->where('code', $current)
                ->update(['next_course_code' => $next]);
        }
    }
}
