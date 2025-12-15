<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\RoadmapController;

// Public Routes
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);

// Protected Routes (Requires Login)
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', function (Request $request) {return $request->user();});
    Route::post('/logout', [AuthController::class, 'logout']);

    // Add protected routes here
});



Route::get('/options', [RoadmapController::class, 'getOptions']);

Route::post('/generate-roadmap', [RoadmapController::class, 'generate']);
Route::post('/save-roadmap', [RoadmapController::class, 'store']);