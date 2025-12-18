<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class SkillSynergy extends Model
{
    use HasFactory;

    // This allows Laravel to save the JSON data into these columns
    protected $fillable = [
        'user_id',
        'course_code',
        'foundation_skill',
        'target_concept',
        'deep_analysis'
    ];

    /**
     * Relationship: Each synergy belongs to one User
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}