<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Course extends Model
{
    protected $fillable = ['code', 'name', 'next_course_code'];

    /**
     * Get the next course in the roadmap.
     */
    public function nextCourse()
    {
        // We tell Laravel: Look for 'next_course_code' and match it to 'code' in this same table
        return $this->hasOne(Course::class, 'code', 'next_course_code');
    }

    /**
     * Get the previous course (inverse relationship).
     */
    public function previousCourse()
    {
        return $this->belongsTo(Course::class, 'next_course_code', 'code');
    }
}
