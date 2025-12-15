<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class RoadmapPhase extends Model
{
    // use HasFactory;
    protected $fillable = ['roadmap_id', 'title'];

    public function tasks() {
        return $this->hasMany(PhaseTask::class);
    }
}