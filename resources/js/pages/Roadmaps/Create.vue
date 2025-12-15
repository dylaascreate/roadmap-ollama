<template>
  <div class="container">
    <h1>DevNexus AI Roadmap</h1>

    <div class="input-field">
        <label>Target Career</label>
        <select v-model="selectedCareerId" class="styled-select">
          <option disabled value="">Select a Career...</option>
          <option v-for="c in allCareersData" :key="c.id" :value="c.id">
            {{ c.name }}
          </option>
        </select>
      </div>
      
      <div class="input-field">
        <label>Current Skills (Max 3)</label>
        
        <div v-if="availableSkills.length > 0" class="skills-grid">
          <div 
            v-for="s in availableSkills" 
            :key="s.id" 
            @click="toggleSkill(s.name)"
            :class="['skill-badge', { active: selectedSkills.includes(s.name) }]"
          >
            {{ s.name }}
          </div>
        </div>
        
        <div v-else class="empty-state">
          Please select a career above to see relevant skills.
        </div>

        <p style="font-size: 0.8em; color: gray;">Selected: {{ selectedSkills.join(', ') }}</p>
      </div>

    <button @click="generateRoadmap" :disabled="loading" class="btn-primary">
      {{ loading ? 'Generating & Saving...' : 'Generate Plan' }}
    </button>
    <p v-if="loading" class="status-text">AI is thinking... (Please wait ~60s)</p>
    <p v-if="error" class="error-text">{{ error }}</p>

    <div v-if="resultData" class="results-area">
      
      <div class="header-row">
        <h2>{{ resultData.title }}</h2>
        <span class="badge-saved">✅ Auto-Saved</span>
      </div>
      <p styl`e="color: gray; margin-bottom: 20px;">Target: {{ resultData.career }}</p>

      <div v-for="phase in resultData.phases" :key="phase.id" class="phase-card">
        <h3>{{ phase.title }}</h3>
        <ul>
          <li v-for="task in phase.tasks" :key="task.id">
            {{ task.content }}
          </li>
        </ul>
      </div>

      <div class="suggestions-card">
        <h3>🚀 Recommendations</h3>
        
        <p><strong>New Skills:</strong> 
          <span v-for="s in resultData.suggestions.filter(x => x.type === 'skill')" :key="s.id" class="tag">
            <p>{{ s.content }}, </p>
          </span>
        </p>

        <div v-for="p in resultData.suggestions.filter(x => x.type === 'project')" :key="p.id">
           <p><strong>Project Idea:</strong> {{ p.content }}</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import api from '../../services/api';

// --- 1. STATE VARIABLES ---
const allCareersData = ref([]); // Stores options from DB
const selectedCareerId = ref(''); // Stores the selected ID (e.g., 1)
const selectedSkills = ref([]);   // Stores selected skill names (e.g., ['PHP', 'Laravel'])

const resultData = ref(null);     // Stores the AI result
const loading = ref(false);       // <--- This was missing!
const error = ref('');

// --- 2. FETCH OPTIONS ON LOAD ---
onMounted(async () => {
    try {
        const response = await api.get('/options');
        allCareersData.value = response.data.careers;
    } catch (e) {
        console.error("Failed to load options:", e);
        error.value = "Could not load career options from server.";
    }
});

// --- 3. COMPUTED & WATCHERS ---

// Filter skills based on the chosen career
const availableSkills = computed(() => {
    if (!selectedCareerId.value) return [];
    const career = allCareersData.value.find(c => c.id === selectedCareerId.value);
    return career ? career.skills : [];
});

// Clear skills if user switches career (to prevent mismatched skills)
watch(selectedCareerId, () => {
    selectedSkills.value = [];
});

// Helper to toggle skills (Max 3)
const toggleSkill = (skillName) => {
    if (selectedSkills.value.includes(skillName)) {
        selectedSkills.value = selectedSkills.value.filter(s => s !== skillName);
    } else {
        if (selectedSkills.value.length < 3) {
            selectedSkills.value.push(skillName);
        } else {
            alert("You can only choose 3 skills!");
        }
    }
};

// --- 4. GENERATE FUNCTION ---
const generateRoadmap = async () => {
    // Validation
    if (!selectedCareerId.value) {
        alert("Please select a career first.");
        return;
    }

    loading.value = true;
    error.value = '';
    resultData.value = null;

    // Convert ID back to Name for the AI (AI doesn't know what "ID: 1" is)
    const careerObj = allCareersData.value.find(c => c.id === selectedCareerId.value);
    const careerName = careerObj ? careerObj.name : '';

    try {
        const response = await api.post('/generate-roadmap', {
            career: careerName, 
            skills: selectedSkills.value.join(', ') // Convert array to string "PHP, Laravel"
        });
        
        // Success!
        resultData.value = response.data.data; 

    } catch (err) {
        console.error(err);
        error.value = 'Generation failed. Check backend logs.';
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
/* Add this new style for the badge */
.badge-saved {
  background-color: #d4edda;
  color: #155724;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: bold;
  border: 1px solid #c3e6cb;
}
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
/* ... keep your other styles ... */
</style>