<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Course;
use Illuminate\Http\Request;

class CourseController extends Controller
{
    /**
     * GET /api/courses
     * List all courses (supports search)
     */
    public function index(Request $request)
    {
        $query = Course::query();

        // Optional: Search by name or code
        if ($request->has('search')) {
            $search = $request->input('search');
            $query->where('name', 'ILike', "%{$search}%")
                  ->orWhere('code', 'ILike', "%{$search}%");
        }

        // Return sorted list
        return response()->json([
            'data' => $query->orderBy('code')->get()
        ]);
    }

    /**
     * POST /api/courses
     * Create a new course manually
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'code' => 'required|string|unique:courses,code',
            'name' => 'required|string',
            'learning_outline' => 'nullable|array',   // Expecting JSON array
            'associated_skills' => 'nullable|array',  // Expecting JSON array
            'next_course_code' => 'nullable|exists:courses,code',
        ]);

        $course = Course::create($validated);

        return response()->json([
            'message' => 'Course created successfully',
            'data' => $course
        ], 201);
    }

    /**
     * GET /api/courses/{id}
     * Show single course details
     */
    public function show($id)
    {
        // Try to find by ID first, then by CODE
        $course = Course::where('id', $id)->orWhere('code', $id)->firstOrFail();

        return response()->json(['data' => $course]);
    }

    /**
     * PUT /api/courses/{id}
     * Update an existing course
     */
    public function update(Request $request, $id)
    {
        // Allow finding by ID or CODE
        $course = Course::where('id', $id)->orWhere('code', $id)->firstOrFail();

        $validated = $request->validate([
            'code' => 'sometimes|string|unique:courses,code,' . $course->id,
            'name' => 'sometimes|string',
            'learning_outline' => 'sometimes|array',
            'associated_skills' => 'sometimes|array',
            'next_course_code' => 'nullable|exists:courses,code',
        ]);

        $course->update($validated);

        return response()->json([
            'message' => 'Course updated successfully',
            'data' => $course
        ]);
    }

    /**
     * DELETE /api/courses/{id}
     * Remove a course
     */
    public function destroy($id)
    {
        $course = Course::where('id', $id)->orWhere('code', $id)->firstOrFail();
        $course->delete();

        return response()->json(['message' => 'Course deleted successfully']);
    }

}
