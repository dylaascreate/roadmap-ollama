<?php

namespace App\Http\Controllers;

use App\Services\DevNexusAI; // Import the Service
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class AIController extends Controller
{
    protected $aiService;

    // Dependency Injection: Laravel automatically injects the service
    public function __construct(DevNexusAI $aiService)
    {
        $this->aiService = $aiService;
    }

    public function recommend(Request $request)
    {
        $request->validate(['query' => 'required|string|max:1000']);

        // Use the Service!
        $result = $this->aiService->getRecommendation(
            $request->input('query'), 
            Auth::id()
        );

        if (!$result) {
            return response()->json(['error' => 'AI Service unavailable'], 503);
        }

        return response()->json($result);
    }

    public function synergy(Request $request)
    {
        $request->validate(['course_code' => 'required|string']);

        $result = $this->aiService->checkSynergy(
            $request->input('course_code'), 
            Auth::id()
        );

        if (!$result) {
            return response()->json(['error' => 'Analysis failed'], 503);
        }

        return response()->json($result);
    }

    // app/Http/Controllers/AIController.php

public function generateRoadmap(Request $request)
{
    $request->validate([
        'career_goal' => 'required|string',
    ]);

    // 1. Get User Skills (so we don't recommend what they already know)
    // Assuming you have a relationship set up, otherwise pass empty array
    $userSkills = $request->user()->skills->pluck('name')->toArray() ?? [];

    // 2. Call the RAG Service
    $roadmap = $this->aiService->generateAcademicRoadmap(
        $request->input('career_goal'),
        $userSkills
    );

    if (!$roadmap) {
        return response()->json(['error' => 'Could not generate academic roadmap.'], 503);
    }

    // 3. Optional: You could save this to the 'roadmaps' table here if you want
    // strictly structured roadmaps to be saved in the same DB table.

    return response()->json($roadmap);
}
}