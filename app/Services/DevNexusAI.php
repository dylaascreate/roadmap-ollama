<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class DevNexusAI
{
    protected $baseUrl;

    public function __construct()
{
    // Fetches from .env, defaults to localhost if missing
    $this->baseUrl = env('DEVNEXUS_AI_URL', 'http://localhost:5001');
}

    /**
     * Send a query to the Python Recommender
     */
    public function getRecommendation(string $query, int $userId)
    {
        try {
            $response = Http::timeout(60)->post("{$this->baseUrl}/recommend", [
                'query' => $query,
                'user_id' => $userId,
            ]);

            if ($response->failed()) {
                Log::error('AI Recommendation Failed: ' . $response->body());
                return null;
            }

            return $response->json();
        } catch (\Exception $e) {
            Log::error('AI Connection Error: ' . $e->getMessage());
            return null;
        }
    }

    /**
     * Check Skill Synergy
     */
    public function checkSynergy(string $courseCode, int $userId)
    {
        try {
            $response = Http::timeout(45)->post("{$this->baseUrl}/synergy", [
                'course_code' => $courseCode,
                'user_id' => $userId,
            ]);

            return $response->successful() ? $response->json() : null;
        } catch (\Exception $e) {
            return null;
        }
    }

    // app/Services/DevNexusAI.php

public function generateAcademicRoadmap(string $careerGoal, array $currentSkills)
{
    try {
        $response = Http::timeout(600)->post("{$this->baseUrl}/generate-path", [
            'career_goal' => $careerGoal,
            'user_skills' => $currentSkills,
        ]);

        if ($response->failed()) {
            return null;
        }

        return $response->json();
    } catch (\Exception $e) {
        return null;
    }
}
}