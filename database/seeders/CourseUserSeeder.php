<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class CourseUserSeeder extends Seeder
{
    public function run(): void
    {
        // Get our Test User
        $user = User::where('email', 'ali@examle.com')->first();

        if ($user) {
            // Ali has completed "Software Requirements" (DES3023)
            DB::table('course_user')->updateOrInsert(
                [
                    'user_id' => $user->id,
                    'course_code' => 'DES3023',
                ],
                [
                    'status' => 'completed',
                    'grade' => 'A',
                    'updated_at' => now(),
                ]
            );

            // Ali has also completed "Structured Programming" (DTS3013)
            DB::table('course_user')->updateOrInsert(
                [
                    'user_id' => $user->id,
                    'course_code' => 'DTS3013',
                ],
                [
                    'status' => 'completed',
                    'grade' => 'B+',
                    'updated_at' => now(),
                ]
            );
        }
    }
}
