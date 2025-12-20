<?php

namespace App\Services;

use App\Models\Roadmap;
use Cloudstudio\Ollama\Facades\Ollama;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class RoadmapService
{
    /**
     * Coordinate the Two-Step Generation and Saving
     */
    public function generateAndSave(string $userId, $career, string $skills)
    {
        // Step 1: Generate the Core Roadmap (Phases & Tasks)
        $roadmapData = $this->fetchRoadmapStruct($career, $skills);

        // Step 2: Generate Recommendations (Skills & Projects)
        // We pass the generated title/phases context so the recommendation matches the roadmap
        $recData = $this->fetchRecommendations($career, $skills);

        if (! $roadmapData) {
            throw new \Exception('Failed to generate roadmap structure.');
        }

        // Step 3: Save everything together
        return $this->saveToDatabase($userId, $career, $skills, $roadmapData, $recData);
    }

    /**
     * PROMPT 1: Focus purely on Timeline and Tasks
     */
    protected function fetchRoadmapStruct(string $career, string $skills)
    {
        $schema = '{
            "title": "Roadmap Title",
            "phases": [
                { "title": "Phase Name", "tasks": ["Task 1", "Task 2", "Task 3"] }
            ]
        }';

        $prompt = "Act as a Technical Course Creator.
        Goal: $career. Current Skills: $skills.
        Create a detailed 4-week learning schedule.
        Focus ONLY on the schedule.
        RETURN JSON ONLY.
        Schema: $schema";

        return $this->callAI($prompt);
    }

    /**
     * PROMPT 2: Focus purely on Career Advice (Skills & Projects)
     */
    protected function fetchRecommendations(string $career, string $skills)
    {
        $schema = '{
            "suggested_skills": ["Skill A", "Skill B", "Skill C"],
            "project": "Name of a project : Its description"
        }';

        $prompt = "Act as a Senior Tech Recruiter.
        Goal: $career. Current Skills: $skills.
        1. Suggest 3 modern, complementary tools/skills the user should learn NEXT (exclude current skills).
        2. Suggest 1 impressive portfolio project they can build using these skills.
        3. STRICT LIMIT: Keep the project description under 100 words.
        RETURN JSON ONLY.
        Schema: $schema";

        return $this->callAI($prompt);
    }

    /**
     * Helper: Generic AI Caller to avoid code duplication
     */
    protected function callAI($prompt)
    {
        try {
            set_time_limit(600);

            $response = Ollama::model(env('OLLAMA_MODEL', 'gpt-oss:120b-cloud'))
                ->options(['temperature' => 0.3]) // Slightly higher for creativity
                ->format('json')
                ->prompt($prompt)
                ->ask();

            $raw = str_replace(['```json', '```'], '', $response['response']);
            $data = json_decode(trim($raw), true);

            // Normalize
            return array_change_key_case($data ?? [], CASE_LOWER);

        } catch (\Exception $e) {
            Log::error('AI Call Failed: '.$e->getMessage());

            return null;
        }
    }

    /**
     * Database Saving Logic (Merges both AI results)
     */
    protected function saveToDatabase($userId, $career, $skills, $roadmapData, $recData)
    {
        return DB::transaction(function () use ($userId, $career, $skills, $roadmapData, $recData) {

            // 1. Create Roadmap Parent
            $roadmap = Roadmap::create(['user_id' => $userId,
                // 'title'  => $roadmapData['title'] ?? "$career Roadmap",
                'title' => $roadmapData['title'],
                'career' => $career,
                'skills' => $skills,
            ]);

            // 2. Save Phases (From Prompt 1)
            $phases = $roadmapData['phases'] ?? ($roadmapData['weeks'] ?? []); // Fallback support
            if (! empty($phases)) {
                foreach ($phases as $phaseData) {
                    $phase = $roadmap->phases()->create([
                        'title' => $phaseData['title'] ?? 'Phase',
                    ]);

                    if (! empty($phaseData['tasks'])) {
                        foreach ($phaseData['tasks'] as $taskString) {
                            $phase->tasks()->create(['content' => $taskString]);
                        }
                    }
                }
            }

            // 3. Save Suggestions (From Prompt 2)
            if ($recData) {
                // Skills
                if (! empty($recData['suggested_skills'])) {
                    foreach ($recData['suggested_skills'] as $newSkill) {
                        $roadmap->suggestions()->create([
                            'type' => 'skill',
                            'content' => $newSkill,
                        ]);
                    }
                }

                // Project
                if (! empty($recData['project'])) {
                    $proj = is_array($recData['project']) ? $recData['project'][0] : $recData['project'];
                    $roadmap->suggestions()->create([
                        'type' => 'project',
                        'content' => $proj,
                    ]);
                }
            }

            // Return complete object
            return Roadmap::with(['phases.tasks', 'suggestions'])->find($roadmap->id);
        });
    }
}
