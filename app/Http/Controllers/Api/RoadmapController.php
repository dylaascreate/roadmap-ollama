<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Services\RoadmapService;
use App\Models\Career;
use Illuminate\Support\Facades\Log;

class RoadmapController extends Controller
{
    protected $roadmapService;

    // Inject the Service
    public function __construct(RoadmapService $roadmapService)
    {
        $this->roadmapService = $roadmapService;
    }

    public function getOptions()
    {
        return response()->json([
            'careers' => Career::with('skills')->get()
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
                $request->input('career'),
                $request->input('skills')
            );

            return response()->json([
                'status' => 'success',
                'message' => 'Roadmap generated and saved!',
                'data' => $roadmap
            ]);

        } catch (\Exception $e) {
            Log::error("Roadmap Generation Error: " . $e->getMessage());
            return response()->json(['error' => 'Generation failed: ' . $e->getMessage()], 500);
        }
    }

    // Keep this if you still need manual saving from frontend, 
    // otherwise you can delete it since 'generate' now auto-saves.
    public function store(Request $request)
    {
        $data = $request->validate([
            'career' => 'required|string',
            'skills' => 'required|string',
            'json_data' => 'required|array'
        ]);

        try {
            // Reuse the service's save logic!
            $this->roadmapService->saveToDatabase(
                $data['career'], 
                $data['skills'], 
                $data['json_data']
            );

            return response()->json(['message' => 'Roadmap has been saved!']);
        } catch (\Exception $e) {
            return response()->json(['error' => 'Save failed'], 500);
        }
    }
}