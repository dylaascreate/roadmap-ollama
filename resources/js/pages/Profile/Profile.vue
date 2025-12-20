<!-- connected to =>
GET /user/profile/profile-summary
GET /options
POST /profile/career
POST /profile/course -->

<template>
  <div class="page-container">
    <h1>My Profile</h1>

    <div v-if="loading" class="loading">Loading profile...</div>

    <div v-else class="profile-grid">
      
      <div class="card identity-card">
        <div class="avatar-placeholder">{{ userInitials }}</div>
        <h2>{{ user.name }}</h2>
        <p class="email">{{ user.email }}</p>
        <p class="role">Student / Developer</p>
      </div>

      <div class="card career-card">
        <h3>Target Career</h3>
        <p class="hint">This helps the AI recommend roadmaps.</p>
        
        <form @submit.prevent="updateCareer">
          <select v-model="form.career_id" class="full-width">
            <option disabled value="">Select your goal</option>
            <option v-for="career in options.careers" :key="career.id" :value="career.id">
              {{ career.name }}
            </option>
          </select>
          <button type="submit" :disabled="savingCareer" class="btn-secondary">
            {{ savingCareer ? 'Updating...' : 'Update Career Goal' }}
          </button>
        </form>
      </div>

      <div class="card skills-card full-width-card">
        <h3>My Current Skills</h3>
        <p class="hint">Select the technologies you already know.</p>

        <div class="skills-selector">
          <div 
            v-for="skill in options.skills" 
            :key="skill.id" 
            class="skill-chip"
            :class="{ active: form.skill_ids.includes(skill.id) }"
            @click="toggleSkill(skill.id)"
          >
            {{ skill.name }}
            <span v-if="form.skill_ids.includes(skill.id)" class="check">✓</span>
          </div>
        </div>

        <div class="actions">
          <button @click="saveSkills" :disabled="savingSkills" class="btn-primary">
            {{ savingSkills ? 'Saving...' : 'Save Skills' }}
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../../axios';

const loading = ref(true);
const savingCareer = ref(false);
const savingSkills = ref(false);

// Data Storage
const user = ref({ name: '', email: '' });
const options = ref({ careers: [], skills: [] });

// Form Models
const form = ref({
  career_id: '',
  skill_ids: []
});

const userInitials = computed(() => {
  return user.value.name 
    ? user.value.name.split(' ').map(n => n[0]).join('').substring(0,2).toUpperCase() 
    : 'User';
});

// 1. Fetch Data on Load
onMounted(async () => {
  try {
    // Run both requests in parallel
    const [profileRes, optionsRes] = await Promise.all([
      api.get('/user/profile-summary'), // Should return user + current career/skills
      api.get('/options')               // All available choices
    ]);

    user.value = profileRes.data.user;
    options.value = optionsRes.data;

    // Pre-fill forms
    form.value.career_id = profileRes.data.current_career_id || '';
    form.value.skill_ids = profileRes.data.current_skill_ids || [];

  } catch (error) {
    console.error("Failed to load profile", error);
  } finally {
    loading.value = false;
  }
});

// 2. Update Career
const updateCareer = async () => {
  savingCareer.value = true;
  try {
    await api.post('/profile/career', { career_id: form.value.career_id });
    alert('Career goal updated!');
  } catch (error) {
    alert('Failed to update career.');
  } finally {
    savingCareer.value = false;
  }
};

// 3. Toggle Skill Selection locally
const toggleSkill = (id) => {
  const index = form.value.skill_ids.indexOf(id);
  if (index === -1) {
    form.value.skill_ids.push(id); // Add
  } else {
    form.value.skill_ids.splice(index, 1); // Remove
  }
};

// 4. Save Skills to Backend
const saveSkills = async () => {
  savingSkills.value = true;
  try {
    await api.post('/profile/skills', { skill_ids: form.value.skill_ids });
    alert('Skills updated successfully!');
  } catch (error) {
    alert('Failed to update skills.');
  } finally {
    savingSkills.value = false;
  }
};
</script>

<style scoped>
.profile-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #ddd;
  text-align: center;
}

.full-width-card { grid-column: span 2; text-align: left; }

/* Identity Styling */
.avatar-placeholder {
  width: 80px; height: 80px; background: #333; color: white;
  border-radius: 50%; margin: 0 auto 15px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.5rem; font-weight: bold;
}
.role { color: #666; font-size: 0.9rem; }

/* Career Form */
.full-width { width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc; }
.btn-secondary { background: #6c757d; color: white; padding: 8px 15px; border: none; border-radius: 4px; cursor: pointer; }

/* Skills Chips */
.skills-selector {
  display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;
}

.skill-chip {
  padding: 8px 16px;
  border: 1px solid #ccc;
  border-radius: 20px;
  cursor: pointer;
  user-select: none;
  transition: all 0.2s;
  background: #f8f9fa;
}

.skill-chip.active {
  background: #007bff; /* Primary Blue */
  color: white;
  border-color: #0056b3;
}

.check { margin-left: 5px; font-weight: bold; }

.actions { text-align: right; }

/* Responsive */
@media (max-width: 600px) {
  .profile-grid { grid-template-columns: 1fr; }
  .full-width-card { grid-column: span 1; }
}
</style>