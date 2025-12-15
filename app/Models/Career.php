<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Career extends Model
{
    protected $fillable = ['name'];

    // ...
    public function skills()
    {
        return $this->belongsToMany(Skill::class);
    }

    public function users()
    {
        return $this->hasMany(User::class);
    }
}
