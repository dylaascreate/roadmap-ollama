<?php

namespace Database\Seeders;

use App\Models\Career;
use App\Models\Skill;
use Illuminate\Database\Seeder;

class CareerSkillSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // 1. Create Skills
        $html = Skill::create(['name' => 'HTML']);
        $css = Skill::create(['name' => 'CSS']);
        $js = Skill::create(['name' => 'JavaScript']);
        $vue = Skill::create(['name' => 'Vue.js']);
        $php = Skill::create(['name' => 'PHP']);
        $laravel = Skill::create(['name' => 'Laravel']);
        $sql = Skill::create(['name' => 'SQL']);

        // 2. Create Careers & Attach Skills

        // Frontend: HTML, CSS, JS, Vue
        $fe = Career::create(['name' => 'Frontend Developer']);
        $fe->skills()->attach([$html->id, $css->id, $js->id, $vue->id]);

        // Backend: PHP, Laravel, SQL
        $be = Career::create(['name' => 'Backend Developer']);
        $be->skills()->attach([$php->id, $laravel->id, $sql->id]);

        // Full Stack: All of them
        $fs = Career::create(['name' => 'Full Stack Developer']);
        $fs->skills()->attach([$html->id, $css->id, $js->id, $vue->id, $php->id, $laravel->id, $sql->id]);
    }
}
