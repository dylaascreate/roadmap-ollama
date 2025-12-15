<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Career;
use Illuminate\Http\Request;

class CareerController extends Controller
{
    // Public: List all careers (so users can pick one)
    public function index()
    {
        // Return careers WITH their required skills
        return Career::with('skills')->get();
    }

    public function show(Career $career)
    {
        return $career->load('skills');
    }

    // Admin: Create Career + Attach Skills
    public function store(Request $request)
    {
        $request->validate([
            'name' => 'required|unique:careers,name',
            'skills' => 'array',        // Optional: List of Skill IDs
            'skills.*' => 'exists:skills,id'
        ]);

        $career = Career::create(['name' => $request->name]);

        if ($request->has('skills')) {
            $career->skills()->attach($request->skills);
        }

        return $career->load('skills');
    }

    // Admin: Update Career
    public function update(Request $request, Career $career)
    {
        $request->validate([
            'name' => 'unique:careers,name,' . $career->id,
            'skills' => 'array',
            'skills.*' => 'exists:skills,id'
        ]);

        if ($request->has('name')) {
            $career->update(['name' => $request->name]);
        }

        if ($request->has('skills')) {
            $career->skills()->sync($request->skills); // Sync updates the list exactly
        }

        return $career->load('skills');
    }

    public function destroy(Career $career)
    {
        // 1. Check if any users have selected this career
        // Note: We use the relationship name 'users' defined in the Career model
        if ($career->users()->count() > 0) {
            return response()->json([
                'message' => 'Cannot delete career. Users are currently pursuing this path.',
                'user_count' => $career->users()->count()
            ], 409);
        }

        $career->delete();
        return response()->json(['message' => 'Career deleted successfully']);
    }
}