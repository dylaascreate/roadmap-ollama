<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Course extends Model
{
    protected $fillable = [
        'code',
        'name',
        'next_course_code',
        'learning_outline',
        'associated_skills',
    ];

    // IMPORTANT: Automatically convert JSON <-> Array
    protected $casts = [
        'learning_outline' => 'array',
        'associated_skills' => 'array',
    ];

    /**
     * Get the next course in the roadmap.
     */
    public function nextCourse()
    {
        return $this->belongsTo(Course::class, 'next_course_code', 'code');
    }

    /**
     * Get the previous course (inverse relationship).
     */
    public function previousCourse()
    {
        return $this->hasOne(Course::class, 'next_course_code', 'code');
    }
}
