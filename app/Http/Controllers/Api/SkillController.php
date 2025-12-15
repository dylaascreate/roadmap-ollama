<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Skill;
use Illuminate\Http\Request;

class SkillController extends Controller
{
    // List all skills (Publicly visible usually)
    public function index()
    {
        return Skill::all();
    }

    // Get a single skill
    public function show(Skill $skill)
    {
        return $skill;
    }

    // Create a new skill (Admin only)
    public function store(Request $request)
    {
        $request->validate(['name' => 'required|unique:skills,name']);
        return Skill::create(['name' => $request->name]);
    }

    // Update skill name
    public function update(Request $request, Skill $skill)
    {
        $request->validate(['name' => 'required|unique:skills,name,' . $skill->id]);
        $skill->update(['name' => $request->name]);
        return $skill;
    }

    // Delete skill
    public function destroy(Skill $skill)
    {
        // 1. Check if any users are currently learning this skill
        if ($skill->users()->count() > 0) {
            return response()->json([
                'message' => 'Cannot delete skill. It is currently assigned to users.',
                'user_count' => $skill->users()->count()
            ], 409); // 409 = Conflict
        }

        // 2. Also check if it's required by any Careers (Optional but recommended)
        if ($skill->careers()->count() > 0) {
             return response()->json([
                'message' => 'Cannot delete skill. It is required by a Career path.',
                'career_count' => $skill->careers()->count()
            ], 409);
        }

        // 3. Safe to delete
        $skill->delete();
        return response()->json(['message' => 'Skill deleted successfully']);
    }
}