<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Roadmap extends Model
{
    // use HasFactory;
    protected $fillable = ['title', 'career', 'skills']; // Removed 'content'

    public function phases() {
        return $this->hasMany(RoadmapPhase::class);
    }

    public function suggestions() {
        return $this->hasMany(RoadmapSuggestion::class);
    }
}