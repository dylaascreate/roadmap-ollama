<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class RoadmapPhase extends Model
{
    // use HasFactory;
    protected $table = 'roadmap_phases'; // Explicit table name

    protected $fillable = ['roadmap_id', 'title'];

    // LOOK UP: Belongs to a Roadmap
    public function roadmap()
    {
        return $this->belongsTo(Roadmap::class, 'roadmap_id');
    }

    // LOOK DOWN: Has many Tasks
    public function tasks()
    {
        return $this->hasMany(PhaseTask::class, 'roadmap_phase_id');
    }
}
