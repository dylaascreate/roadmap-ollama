<?php

namespace App\Models;

// use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class RoadmapSuggestion extends Model
{
    protected $table = 'roadmap_suggestions';

    protected $fillable = ['roadmap_id', 'type', 'content'];

    public function roadmap()
    {
        return $this->belongsTo(Roadmap::class, 'roadmap_id');
    }
}
//
