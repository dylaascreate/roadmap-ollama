<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\SkillSynergy;
use Illuminate\Support\Facades\Http;

class CourseController extends Controller
{
    public function getSynergy(Request $request)
    {
        $userId = auth()->id();
        $courseCode = $request->course_code;

        // 1. Check if we already analyzed this for the user
        $existing = SkillSynergy::where('user_id', $userId)
                                ->where('course_code', $courseCode)
                                ->get();

        if ($existing->isNotEmpty()) {
            return response()->json($existing);
        }

        // 2. If not, ask the Python Service (Ollama)
        // We send the request to your Flask app (port 5001)
        $response = Http::post('http://localhost:5001/synergy', [
            'user_id' => $userId,
            'course_code' => $courseCode
        ]);

        if ($response->failed()) {
            return response()->json(['error' => 'AI Service unavailable'], 500);
        }

        $synergies = $response->json(); // Array of foundation_skill, target_concept, etc.

        // 3. Save the new analysis to the Database
        $savedData = [];
        foreach ($synergies as $item) {
            $savedData[] = SkillSynergy::create([
                'user_id' => $userId,
                'course_code' => $courseCode,
                'foundation_skill' => $item['foundation_skill'],
                'target_concept' => $item['target_concept'],
                'deep_analysis' => $item['deep_analysis'],
            ]);
        }

        return response()->json($savedData);
    }
}