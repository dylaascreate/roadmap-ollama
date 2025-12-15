<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Spatie\Permission\Models\Role;
use Spatie\Permission\Models\Permission;
use Spatie\Permission\PermissionRegistrar;
use App\Models\User;

class RolesAndPermissionsSeeder extends Seeder
{
    public function run(): void
    {
        // Reset cached roles and permissions
        app()[PermissionRegistrar::class]->forgetCachedPermissions();

        // 1. Create Roles
        $adminRole = Role::create(['name' => 'admin']);
        $studentRole = Role::create(['name' => 'student']);

        // 2. Create Specific Permissions (Optional but recommended)
        $manageSkills = Permission::create(['name' => 'manage skills']);

        // 3. Assign Permission to Role
        $adminRole->givePermissionTo($manageSkills);

        // 4. Create the Admin User
        $adminUser = User::factory()->create([
            'name' => 'Super Admin',
            'email' => 'admin@example.com',
            'password' => bcrypt('password'), // Always set a known password for testing
        ]);

        // 5. Assign Role to User
        $adminUser->assignRole($adminRole);

        // Optional: Create a test student user too
        $studentUser = User::factory()->create([
            'name' => 'Test Student',
            'email' => 'student@example.com',
            'password' => bcrypt('password'),
        ]);
        
        $studentUser->assignRole($studentRole);
    }
}