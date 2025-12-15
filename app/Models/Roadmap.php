<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Roadmap extends Model
{
    // use HasFactory;
    protected $table = 'roadmaps'; // Explicit table name

    protected $fillable = ['user_id', 'title', 'career', 'skills', 'status', 'progress_percent'];

    public function phases()
    {
        return $this->hasMany(RoadmapPhase::class, 'roadmap_id');
    }

    public function suggestions()
    {
        return $this->hasMany(RoadmapSuggestion::class, 'roadmap_id');
    }

    // Helper to recalculate progress
    public function updateProgress()
    {
        $totalTasks = $this->phases->flatMap->tasks->count();
        if ($totalTasks == 0) {
            return;
        }

        $completedTasks = $this->phases->flatMap->tasks->where('is_completed', true)->count();

        $this->progress_percent = round(($completedTasks / $totalTasks) * 100);
        $this->save();
    }
}
