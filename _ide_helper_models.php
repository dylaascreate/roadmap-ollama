<?php

// @formatter:off
// phpcs:ignoreFile
/**
 * A helper file for your Eloquent Models
 * Copy the phpDocs from this file to the correct Model,
 * And remove them from this file, to prevent double declarations.
 *
 * @author Barry vd. Heuvel <barryvdh@gmail.com>
 */


namespace App\Models{
/**
 * @property int $id
 * @property string $name
 * @property \Illuminate\Support\Carbon|null $created_at
 * @property \Illuminate\Support\Carbon|null $updated_at
 * @property-read \Illuminate\Database\Eloquent\Collection<int, \App\Models\Skill> $skills
 * @property-read int|null $skills_count
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Career newModelQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Career newQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Career query()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Career whereCreatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Career whereId($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Career whereName($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Career whereUpdatedAt($value)
 */
	class Career extends \Eloquent {}
}

namespace App\Models{
/**
 * @property int $id
 * @property int $roadmap_phase_id
 * @property string $content
 * @property \Illuminate\Support\Carbon|null $created_at
 * @property \Illuminate\Support\Carbon|null $updated_at
 * @property bool $is_completed
 * @property-read \App\Models\RoadmapPhase $phase
 * @method static \Illuminate\Database\Eloquent\Builder<static>|PhaseTask newModelQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|PhaseTask newQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|PhaseTask query()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|PhaseTask whereContent($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|PhaseTask whereCreatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|PhaseTask whereId($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|PhaseTask whereIsCompleted($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|PhaseTask whereRoadmapPhaseId($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|PhaseTask whereUpdatedAt($value)
 */
	class PhaseTask extends \Eloquent {}
}

namespace App\Models{
/**
 * @property int $id
 * @property string $title
 * @property string $career
 * @property string $skills
 * @property \Illuminate\Support\Carbon|null $created_at
 * @property \Illuminate\Support\Carbon|null $updated_at
 * @property string $status
 * @property int $progress_percent
 * @property int|null $user_id
 * @property-read \Illuminate\Database\Eloquent\Collection<int, \App\Models\RoadmapPhase> $phases
 * @property-read int|null $phases_count
 * @property-read \Illuminate\Database\Eloquent\Collection<int, \App\Models\RoadmapSuggestion> $suggestions
 * @property-read int|null $suggestions_count
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Roadmap newModelQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Roadmap newQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Roadmap query()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Roadmap whereCareer($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Roadmap whereCreatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Roadmap whereId($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Roadmap whereProgressPercent($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Roadmap whereSkills($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Roadmap whereStatus($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Roadmap whereTitle($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Roadmap whereUpdatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Roadmap whereUserId($value)
 */
	class Roadmap extends \Eloquent {}
}

namespace App\Models{
/**
 * @property int $id
 * @property int $roadmap_id
 * @property string $title
 * @property \Illuminate\Support\Carbon|null $created_at
 * @property \Illuminate\Support\Carbon|null $updated_at
 * @property-read \App\Models\Roadmap $roadmap
 * @property-read \Illuminate\Database\Eloquent\Collection<int, \App\Models\PhaseTask> $tasks
 * @property-read int|null $tasks_count
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapPhase newModelQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapPhase newQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapPhase query()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapPhase whereCreatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapPhase whereId($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapPhase whereRoadmapId($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapPhase whereTitle($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapPhase whereUpdatedAt($value)
 */
	class RoadmapPhase extends \Eloquent {}
}

namespace App\Models{
/**
 * @property int $id
 * @property int $roadmap_id
 * @property string $type
 * @property string $content
 * @property \Illuminate\Support\Carbon|null $created_at
 * @property \Illuminate\Support\Carbon|null $updated_at
 * @property-read \App\Models\Roadmap $roadmap
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapSuggestion newModelQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapSuggestion newQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapSuggestion query()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapSuggestion whereContent($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapSuggestion whereCreatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapSuggestion whereId($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapSuggestion whereRoadmapId($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapSuggestion whereType($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|RoadmapSuggestion whereUpdatedAt($value)
 */
	class RoadmapSuggestion extends \Eloquent {}
}

namespace App\Models{
/**
 * @property int $id
 * @property string $name
 * @property \Illuminate\Support\Carbon|null $created_at
 * @property \Illuminate\Support\Carbon|null $updated_at
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Skill newModelQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Skill newQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Skill query()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Skill whereCreatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Skill whereId($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Skill whereName($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|Skill whereUpdatedAt($value)
 */
	class Skill extends \Eloquent {}
}

namespace App\Models{
/**
 * @property int $id
 * @property string $name
 * @property string $email
 * @property \Illuminate\Support\Carbon|null $email_verified_at
 * @property string $password
 * @property string|null $remember_token
 * @property \Illuminate\Support\Carbon|null $created_at
 * @property \Illuminate\Support\Carbon|null $updated_at
 * @property-read \Illuminate\Notifications\DatabaseNotificationCollection<int, \Illuminate\Notifications\DatabaseNotification> $notifications
 * @property-read int|null $notifications_count
 * @property-read \Illuminate\Database\Eloquent\Collection<int, \Laravel\Sanctum\PersonalAccessToken> $tokens
 * @property-read int|null $tokens_count
 * @method static \Database\Factories\UserFactory factory($count = null, $state = [])
 * @method static \Illuminate\Database\Eloquent\Builder<static>|User newModelQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|User newQuery()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|User query()
 * @method static \Illuminate\Database\Eloquent\Builder<static>|User whereCreatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|User whereEmail($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|User whereEmailVerifiedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|User whereId($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|User whereName($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|User wherePassword($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|User whereRememberToken($value)
 * @method static \Illuminate\Database\Eloquent\Builder<static>|User whereUpdatedAt($value)
 */
	class User extends \Eloquent {}
}

