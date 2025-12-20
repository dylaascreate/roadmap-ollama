<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * GET /api/user/profile-summary
     * Returns a quick summary of the user's profile for the AI context.
     */
    public function profileSummary(Request $request)
    {
        $user = $request->user();

        // Count associated skills
        $skillCount = $user->skills()->count();

        // Get current career goal name (if set)
        $careerGoal = $user->career ? $user->career->name : 'Not set';

        return response()->json([
            'id' => $user->id,
            'name' => $user->name,
            'skill_count' => $skillCount,
            'current_career_goal' => $careerGoal,
            // Optional: Send the actual skill names if you want to show them in a tooltip
            'skills_preview' => $user->skills()->limit(5)->pluck('name')
        ]);
    }
}