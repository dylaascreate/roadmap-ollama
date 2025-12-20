<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Career;
use App\Models\PhaseTask;
use App\Models\Roadmap;
use App\Services\DevNexusAI;
use App\Services\RoadmapService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class RoadmapController extends Controller
{
    protected $roadmapService;
    protected $devNexusAI;

    // Inject BOTH Services
    public function __construct(RoadmapService $roadmapService, DevNexusAI $devNexusAI)
    {
        $this->roadmapService = $roadmapService;
        $this->devNexusAI = $devNexusAI;
    }

    /**
     * GET /api/roadmaps
     * List all roadmaps belonging to the logged-in user
     */
    public function index(Request $request)
    {
        // Use $request->user() to get the ID from the Sanctum Token
        $roadmaps = Roadmap::where('user_id', $request->user()->id)
            ->orderBy('created_at', 'desc')
            ->get();

        return response()->json(['data' => $roadmaps]);
    }

    /**
     * GET /api/roadmaps/{id}
     * Show full details of a specific roadmap
     */
    public function show(Request $request, $id)
    {
        $roadmap = Roadmap::with(['phases.tasks', 'suggestions'])
            ->where('user_id', $request->user()->id) // Security check
            ->findOrFail($id);

        return response()->json(['data' => $roadmap]);
    }

    /**
     * DELETE /api/roadmaps/{id}
     * Delete a roadmap
     */
    public function destroy(Request $request, $id)
    {
        $roadmap = Roadmap::where('user_id', $request->user()->id)->findOrFail($id);
        $roadmap->delete();

        return response()->json(['message' => 'Roadmap deleted successfully']);
    }

    /**
     * PATCH /api/tasks/{id}/toggle
     * Mark a task as complete/incomplete
     */
    public function toggleTask(Request $request, $id)
    {
        $task = PhaseTask::findOrFail($id);

        // Security: Ensure this task belongs to a roadmap owned by the user
        if ($task->phase->roadmap->user_id !== $request->user()->id) {
            return response()->json(['error' => 'Unauthorized'], 403);
        }

        // Toggle status
        $task->is_completed = ! $task->is_completed;
        $task->save();

        // Update Parent Roadmap Progress
        $task->phase->roadmap->updateProgress();

        return response()->json([
            'message' => 'Task updated',
            'is_completed' => $task->is_completed,
            'roadmap_progress' => $task->phase->roadmap->progress_percent,
        ]);
    }

    public function getOptions()
    {
        return response()->json([
            'careers' => Career::with('skills')->get(),
        ]);
    }

    public function generate(Request $request)
    {
        $request->validate([
            'career' => 'required|string',
            'skills' => 'required|string',
        ]);

        try {
            // Call the service to Generate AND Save
            $roadmap = $this->roadmapService->generateAndSave(
                $request->user()->id,
                $request->input('career'),
                $request->input('skills')
            );

            return response()->json([
                'status' => 'success',
                'message' => 'Roadmap generated and saved!',
                'data' => $roadmap,
            ]);

        } catch (\Exception $e) {
            Log::error('Roadmap Generation Error: '.$e->getMessage());

            return response()->json(['error' => 'Generation failed: '.$e->getMessage()], 500);
        }
    }

    /**
     * POST /api/roadmaps/generate-smart
     * Uses DevNexus AI (Python + PKL + RAG) to generate a personalized path
     */
    public function generateSmart(Request $request)
    {
        $request->validate([
            'career' => 'required|string',
        ]);

        $user = $request->user();

        try {
            // 1. Gather User Context for the AI
            // We fetch skills from the DB so the PKL model gets accurate data
            $currentSkills = $user->skills()->pluck('name')->toArray(); 
            
            // 2. Call Python (DevNexusAI)
            // This hits your Flask '/generate-path' endpoint
            $aiResponse = $this->devNexusAI->generateAcademicRoadmap(
                $request->input('career'),
                $currentSkills
            );

            if (! $aiResponse || ! isset($aiResponse['academic_path'])) {
                return response()->json(['error' => 'AI failed to generate a valid path.'], 500);
            }

            // 3. Map Python Response to Laravel Structure
            // Python returns 'academic_path' (courses). We need to convert this 
            // into the structure your RoadmapService expects for saving.
            $formattedData = $this->mapPythonToRoadmap($aiResponse['academic_path']);

            // 4. Save to Database
            // We reuse your existing service to handle the heavy lifting of saving
            $roadmap = $this->roadmapService->saveToDatabase(
                $user->id,
                $request->input('career'),
                implode(', ', $currentSkills), // Store used skills as string
                $formattedData, 
                $formattedData // Passing same data for raw_json
            );

            return response()->json([
                'status' => 'success',
                'message' => 'AI-Driven Roadmap generated via DevNexus AI!',
                'data' => $roadmap,
            ]);

        } catch (\Exception $e) {
            Log::error('Smart Roadmap Error: ' . $e->getMessage());
            return response()->json(['error' => 'Generation failed'], 500);
        }
    }

    /**
     * Helper: Converts Python "Course" list into Laravel "Phases/Tasks"
     */
    private function mapPythonToRoadmap(array $academicPath)
    {
        $phases = [];

        foreach ($academicPath as $index => $course) {
            // Each Course becomes a "Phase" in the roadmap
            $tasks = [];

            // The 'content' (Outline) from Python becomes the "Tasks"
            if (isset($course['content']) && is_array($course['content'])) {
                foreach ($course['content'] as $topic) {
                    $tasks[] = [
                        'name' => $topic, 
                        'is_completed' => false
                    ];
                }
            }

            $phases[] = [
                'title' => $course['course_code'] . ': ' . $course['course_name'],
                'description' => $course['reason'] ?? 'Recommended Course',
                'tasks' => $tasks
            ];
        }

        return ['phases' => $phases];
    }

    // Keep this if you still need manual saving from frontend,
    // otherwise you can delete it since 'generate' now auto-saves.
    public function store(Request $request)
    {
        $data = $request->validate([
            'career' => 'required|string',
            'skills' => 'required|string',
            'json_data' => 'required|array',
        ]);

        try {
            // Reuse the service's save logic!
            $this->roadmapService->saveToDatabase(
                $data['user_id'],
                $data['career'],
                $data['skills'],
                $data['json_data'],
                $data['json_data']
            );

            return response()->json(['message' => 'Roadmap has been saved!']);
        } catch (\Exception $e) {
            return response()->json(['error' => 'Save failed'], 500);
        }
    }
}
