<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class ProfileController extends Controller
{
    // Sync skills to the current user
    public function updateSkills(Request $request)
    {
        $request->validate([
            'skills' => 'array',        // Expect a list
            'skills.*' => 'exists:skills,id', // Every item must be a valid Skill ID
        ]);

        $user = $request->user();

        // 'sync' is magic: It adds new ones, removes old ones, and keeps the list exact.
        $user->skills()->sync($request->skills);

        return response()->json([
            'message' => 'Skills updated successfully',
            'user_skills' => $user->skills,
        ]);
    }

    // Update Main Career Goal
    public function updateCareer(Request $request)
    {
        $request->validate([
            'career_id' => 'required|exists:careers,id',
        ]);

        $user = $request->user();
        $user->career_id = $request->career_id;
        $user->save();

        return response()->json([
            'message' => 'Career goal updated successfully',
            'user' => $user->load('career'), // Return user with new career details
        ]);
    }
}
