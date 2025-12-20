<template>
  <div class="container">
    <div class="header-section">
      <h1>DevNexus Smart Roadmap</h1>
      <span class="rag-badge">✨ AI + Profile Integration</span>
    </div>

    <p class="intro-text">
      This tool uses <strong>RAG (Retrieval-Augmented Generation)</strong>. 
      It reads your current skills from your profile and cross-references them with our 
      course syllabus database to create a custom academic path.
    </p>

    <div class="card input-card">
      <div class="input-field">
        <label>Target Career Goal</label>
        <select v-model="selectedCareer" class="styled-select">
          <option disabled value="">Select a Career...</option>
          <option v-for="c in allCareersData" :key="c.id" :value="c.name">
            {{ c.name }}
          </option>
        </select>
      </div>

      <div class="user-context-info" v-if="userProfileLoaded">
        <small>✅ We will analyze your <strong>{{ userSkillCount }} existing skills</strong> for this path.</small>
      </div>

      <button @click="generateSmartRoadmap" :disabled="loading || !selectedCareer" class="btn-primary">
        <span v-if="loading">Running AI Analysis...</span>
        <span v-else>Generate Personalized Path</span>
      </button>

      <div v-if="loading" class="loading-status">
        <p>🔄 Fetching your profile data...</p>
        <p>🤖 Analyzing syllabus with Ollama...</p>
        <p>💾 Constructing roadmap...</p>
      </div>
      
      <p v-if="error" class="error-text">{{ error }}</p>
    </div>

    <div v-if="resultData" class="results-area">
      
      <div class="header-row">
        <h2>{{ resultData.career_goal }} Path</h2>
        <span class="badge-saved">✅ Saved to Dashboard</span>
      </div>

      <div v-for="phase in resultData.phases" :key="phase.id" class="phase-card">
        <div class="phase-header">
           <h3>{{ phase.title }}</h3>
           <span class="course-code-tag">{{ extractCode(phase.title) }}</span>
        </div>
        <p class="phase-desc">{{ phase.description }}</p>
        
        <div class="tasks-list">
          <h4>Course Content Outline:</h4>
          <ul>
            <li v-for="(task, index) in phase.tasks" :key="index">
              {{ task.content || task.name }}
            </li>
          </ul>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios'; // Import directly from node_modules
const api = axios;

// --- STATE ---
const allCareersData = ref([]);
const selectedCareer = ref('');
const resultData = ref(null);
const loading = ref(false);
const error = ref('');
const userSkillCount = ref(0);
const userProfileLoaded = ref(false);

// --- ON LOAD ---
onMounted(async () => {
    try {
        // 1. Fetch Career Options
        const response = await api.get('/options');
        allCareersData.value = response.data.careers;

        // 2. Fetch User Profile Summary (Optional, just for UI feedback)
        // You might need a simple endpoint for this, or use the user store
        const userRes = await api.get('/user/profile-summary'); 
        userSkillCount.value = userRes.data.skill_count || 0;
        userProfileLoaded.value = true;

    } catch (e) {
        console.error("Init failed:", e);
        // Fallback if profile summary fails
        userProfileLoaded.value = true; 
    }
});

// --- GENERATE FUNCTION (SMART) ---
const generateSmartRoadmap = async () => {
    loading.value = true;
    error.value = '';
    resultData.value = null;

    try {
        // We only send the Career. The backend handles the rest!
        const response = await api.post('/generate-smart', {
            career: selectedCareer.value
        });
        
        // The Controller returns: { status, message, data: { ...roadmap } }
        resultData.value = response.data.data; 

    } catch (err) {
        console.error(err);
        error.value = 'AI Analysis failed. Please ensure the Python service is running.';
    } finally {
        loading.value = false;
    }
};

// Helper to make the UI look cleaner
const extractCode = (title) => {
    return title.split(':')[0] || 'Course';
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

/* New Styles for RAG Version */
.rag-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 5px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: bold;
  vertical-align: middle;
  margin-left: 10px;
}

.intro-text {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 25px;
  line-height: 1.5;
}

.user-context-info {
  background: #eef2ff;
  border-left: 4px solid #667eea;
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 4px;
  color: #444;
}

.phase-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-code-tag {
  background: #eee;
  padding: 2px 8px;
  border-radius: 4px;
  font-family: monospace;
  font-weight: bold;
}

.tasks-list ul {
  padding-left: 20px;
  color: #555;
}

/* Reuse your existing card/button styles */
.card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  margin-bottom: 20px;
}

.btn-primary {
  width: 100%;
  padding: 12px;
  background-color: #008080; /* Dark Cyan Theme */
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:disabled {
  background-color: #a0caca;
  cursor: not-allowed;
}
</style>