<?php

use App\Http\Controllers\AIController;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\UserController;
use App\Http\Controllers\Api\CareerController;
use App\Http\Controllers\Api\CourseController;
use App\Http\Controllers\Api\ProfileController;
use App\Http\Controllers\Api\RoadmapController;
use App\Http\Controllers\Api\SkillController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

// Route::get('/{any}', function () {
//     return view('app');
// })->where('any', '.*');

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

    // --- ROADMAPS ---
    Route::get('/roadmaps', [RoadmapController::class, 'index']);
    
    // Options to pick career and its associated skill set.
    Route::get('/options', [RoadmapController::class, 'getOptions']); 
    
    // Standard AI Generation
    Route::post('/roadmaps/generate', [RoadmapController::class, 'generate']); 
    
    // The New "Smart" RAG Generator
    Route::post('/roadmaps/generate-smart', [RoadmapController::class, 'generateSmart']);

    Route::get('/roadmaps/{id}', [RoadmapController::class, 'show']);
    Route::delete('/roadmaps/{id}', [RoadmapController::class, 'destroy']);

    // --- TASKS ---
    Route::patch('/tasks/{id}/toggle', [RoadmapController::class, 'toggleTask']);

    // --- USER PROFILE ---
    Route::post('/profile/skills', [ProfileController::class, 'updateSkills']);
    Route::post('/profile/career', [ProfileController::class, 'updateCareer']);
    Route::get('/user/profile-summary', [UserController::class, 'profileSummary']);

    // --- RESOURCES ---
    Route::get('/careers', [CareerController::class, 'index']);
    Route::get('/careers/{id}', [CareerController::class, 'show']);
    Route::get('/skills', [SkillController::class, 'index']);
    Route::get('/skills/{id}', [SkillController::class, 'show']);
    Route::get('/courses', [CourseController::class, 'index']);
    Route::get('/courses/{id}', [CourseController::class, 'show']);

    // --- DEVNEXUS AI (Direct Access) ---
    Route::post('/recommend', [AIController::class, 'recommend']);
    Route::post('/synergy', [AIController::class, 'synergy']);
    Route::post('/academic-roadmap', [AIController::class, 'generateRoadmap']);

});

Route::middleware(['auth:sanctum', 'role:admin'])->group(function () {

    Route::post('/careers', [CareerController::class, 'store']);
    Route::put('/careers/{career}', [CareerController::class, 'update']);
    Route::delete('/careers/{career}', [CareerController::class, 'destroy']);

    // Admin Only: Manage Skills
    Route::post('/skills', [SkillController::class, 'store']);
    Route::put('/skills/{skill}', [SkillController::class, 'update']);
    Route::delete('/skills/{skill}', [SkillController::class, 'destroy']);

    Route::post('/courses', [CourseController::class, 'store']);
    Route::put('/courses/{id}', [CourseController::class, 'update']);
    Route::delete('/courses/{id}', [CourseController::class, 'destroy']);
});
