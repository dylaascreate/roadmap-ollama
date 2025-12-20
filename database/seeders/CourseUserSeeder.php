<?php

namespace Database\Seeders;

use App\Models\Course;
use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class CourseUserSeeder extends Seeder
{
    public function run()
    {
        // 1. Get all available User IDs and Course Codes
        $users = User::pluck('id');
        $courseCodes = Course::pluck('code');

        // Safety Check: Stop if parents are missing
        if ($users->isEmpty() || $courseCodes->isEmpty()) {
            $this->command->warn('Skipping CourseUser seeding: Users or Courses table is empty.');

            return;
        }

        foreach ($users as $userId) {
            // 2. Assign 3-5 random courses to each user
            // 'random(3)' picks 3 valid codes from the DB. Safe!
            $randomCourses = $courseCodes->random(min(3, $courseCodes->count()));

            foreach ($randomCourses as $code) {
                DB::table('course_user')->insertOrIgnore([
                    'user_id' => $userId,
                    'course_code' => $code, // This is guaranteed to exist now
                    'status' => 'completed',
                    'grade' => 'A',
                    'created_at' => now(),
                    'updated_at' => now(),
                ]);
            }
        }

    }
}
