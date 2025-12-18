<?php

use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\CareerController;
use App\Http\Controllers\Api\ProfileController;
use App\Http\Controllers\Api\RoadmapController;
use App\Http\Controllers\Api\SkillController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

// Public Routes
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);

// Protected Routes (Requires Login)
Route::middleware('auth:sanctum')->group(function () {

    // Public Routes for logged users
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/user', function (Request $request) {
        return $request->user();
    });

    // Roadmaps
    Route::get('/roadmaps', [RoadmapController::class, 'index']);
    Route::get('/roadmaps/option', [RoadmapController::class, 'getOptions']);
    Route::post('/roadmaps/generate', [RoadmapController::class, 'generate']); // Create (AI)
    // Route::post('/roadmaps/save', [RoadmapController::class, 'store']);
    Route::get('/roadmaps/{id}', [RoadmapController::class, 'show']);
    Route::delete('/roadmaps/{id}', [RoadmapController::class, 'destroy']);

    // Tasks
    Route::patch('/tasks/{id}/toggle', [RoadmapController::class, 'toggleTask']); // Checkbox

    // User Profile
    Route::post('/profile/skills', [ProfileController::class, 'updateSkills']);
    Route::post('/profile/career', [ProfileController::class, 'updateCareer']);

});

Route::middleware(['auth:sanctum', 'role:admin'])->group(function () {

    Route::post('/careers', [CareerController::class, 'store']);
    Route::put('/careers/{career}', [CareerController::class, 'update']);
    Route::delete('/careers/{career}', [CareerController::class, 'destroy']);

    // Admin Only: Manage Skills
    Route::post('/skills', [SkillController::class, 'store']);
    Route::put('/skills/{skill}', [SkillController::class, 'update']);
    Route::delete('/skills/{skill}', [SkillController::class, 'destroy']);
});
