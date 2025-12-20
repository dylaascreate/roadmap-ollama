<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class PhaseTask extends Model
{
    // protected $fillable = ['roadmap_phase_id', 'content'];
    protected $table = 'phase_tasks'; // <--- CRITICAL: Matches your specific table name

    protected $fillable = ['roadmap_phase_id', 'content', 'is_completed'];

    protected $casts = [
        'is_completed' => 'boolean',
    ];

    public function phase()
    {
        return $this->belongsTo(RoadmapPhase::class, 'roadmap_phase_id');
    }
}
