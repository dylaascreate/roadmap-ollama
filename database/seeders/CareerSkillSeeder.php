<?php

namespace Database\Seeders;

use App\Models\Career;
use App\Models\Skill;
use App\Models\User; // <--- Don't forget this import!
use Illuminate\Database\Seeder;

class CareerSkillSeeder extends Seeder
{
    public function run(): void
    {
        // 1. Create Skills
        // We use firstOrCreate to prevent duplicates if you run seed twice
        $html = Skill::firstOrCreate(['name' => 'HTML']);
        $css = Skill::firstOrCreate(['name' => 'CSS']);
        $js = Skill::firstOrCreate(['name' => 'JavaScript']);
        $vue = Skill::firstOrCreate(['name' => 'Vue.js']);
        $php = Skill::firstOrCreate(['name' => 'PHP']);
        $laravel = Skill::firstOrCreate(['name' => 'Laravel']);
        $sql = Skill::firstOrCreate(['name' => 'SQL']);

        // 2. Create Careers & Attach Skills

        // Frontend
        $fe = Career::firstOrCreate(['name' => 'Frontend Developer']);
        $fe->skills()->syncWithoutDetaching([$html->id, $css->id, $js->id, $vue->id]);

        // Backend
        $be = Career::firstOrCreate(['name' => 'Backend Developer']);
        $be->skills()->syncWithoutDetaching([$php->id, $laravel->id, $sql->id]);

        // Full Stack
        $fs = Career::firstOrCreate(['name' => 'Full Stack Developer']);
        $fs->skills()->syncWithoutDetaching([$html->id, $css->id, $js->id, $vue->id, $php->id, $laravel->id, $sql->id]);

        // ==========================================
        // 3. SKILL USER SEEDER (Added as requested)
        // ==========================================

        // Ensure User 1 (Ali) exists
        $user = User::firstOrCreate(
            ['email' => 'ali@example.com'],
            ['name' => 'Ali Test', 'password' => bcrypt('password')]
        );

        // Assign skills to Ali (He knows HTML, CSS, and SQL)
        // syncWithoutDetaching ensures we don't erase existing skills or add duplicates
        $user->skills()->syncWithoutDetaching([$html->id, $css->id, $sql->id]);
    }
}
