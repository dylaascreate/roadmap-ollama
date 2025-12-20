<template>
  <div class="nexus-container">
    
    <!-- Header Section -->
    <header class="nexus-header">
      <h1>🦋 DevNexus AI Agent</h1>
      <p>Your syllabus-aware career companion</p>
    </header>

    <!-- Navigation Tabs -->
    <div class="tabs">
      <button 
        :class="['tab-btn', { active: mode === 'chat' }]" 
        @click="mode = 'chat'">
        💬 Skill Advisor
      </button>
      <button 
        :class="['tab-btn', { active: mode === 'roadmap' }]" 
        @click="mode = 'roadmap'">
        🗺️ Academic Path
      </button>
    </div>

    <!-- MAIN INPUT AREA -->
    <div class="input-section">
      <input 
        v-model="userInput" 
        @keyup.enter="submitQuery"
        :placeholder="mode === 'chat' ? 'Ask about a skill (e.g., I want to learn API Testing)' : 'Enter your Dream Career (e.g., Data Scientist)'"
        class="nexus-input"
        :disabled="loading"
      />
      
      <button @click="submitQuery" :disabled="loading" class="action-btn">
        <span v-if="loading">Thinking...</span>
        <span v-else>
            {{ mode === 'chat' ? 'Ask AI' : 'Generate Path' }}
        </span>
      </button>
    </div>

    <!-- ERROR MESSAGE -->
    <div v-if="error" class="error-box">
      ⚠️ {{ error }}
    </div>

    <!-- === RESULT AREA: CHAT MODE (RAG ADVISOR) === -->
    <div v-if="mode === 'chat' && chatResult" class="result-card fade-in">
      
      <!-- Career Context Badge -->
      <div v-if="chatResult.target_career" class="career-badge">
        🎯 Tailored for: {{ chatResult.target_career }}
      </div>

      <div class="card-header">
        <span class="course-code">{{ chatResult.course_code }}</span>
        <h3>{{ chatResult.course_name }}</h3>
      </div>
      
      <!-- The AI Message (RAG) -->
      <div class="ai-message-box">
        <p class="ai-text">{{ chatResult.message }}</p>
      </div>
      
      <!-- Status Badge -->
      <div v-if="chatResult.status === 'completed'" class="status-badge completed">
        ✅ Course Completed
      </div>

      <!-- Skills Grid -->
      <div class="skills-section">
        <div class="skill-column">
          <h4>🎓 Skills You Will Learn</h4>
          <div class="tags">
            <span v-for="skill in chatResult.skills_to_learn" :key="skill" class="skill-tag learn">
              {{ skill }}
            </span>
          </div>
        </div>
        
        <div class="skill-column" v-if="chatResult.skills_you_know && chatResult.skills_you_know.length">
          <h4>✅ Skills You Have</h4>
          <div class="tags">
            <span v-for="skill in chatResult.skills_you_know" :key="skill" class="skill-tag known">
              {{ skill }}
            </span>
          </div>
        </div>
      </div>

      <!-- Syllabus Preview (CCO) -->
      <div class="syllabus-preview" v-if="chatResult.course_content">
        <details>
            <summary>View Course Syllabus (Topics)</summary>
            <ul>
                <li v-for="topic in chatResult.course_content" :key="topic">{{ topic }}</li>
            </ul>
        </details>
      </div>

      <!-- SYNERGY BUTTON (Opt-In Feature) -->
      <div class="synergy-action">
        <button @click="getSynergy(chatResult.course_code)" class="synergy-btn">
          ✨ Unlock Deep Skill Connections
        </button>
      </div>

      <!-- SYNERGY CARDS (Hidden until clicked) -->
      <div v-if="synergyData" class="synergy-grid fade-in">
        <div v-for="(insight, i) in synergyData" :key="i" class="synergy-card">
            <div class="synergy-header">
                <span class="found-skill">{{ insight.foundation_skill }}</span>
                <span class="arrow">➔</span>
                <span class="target-concept">{{ insight.target_concept }}</span>
            </div>
            <p class="synergy-text">{{ insight.deep_analysis }}</p>
        </div>
      </div>

    </div>

    <!-- === RESULT AREA: ROADMAP MODE (STRICT PATH) === -->
    <div v-if="mode === 'roadmap' && roadmapResult" class="roadmap-container fade-in">
      <h2>🎓 UPSI Path: {{ roadmapResult.career_goal }}</h2>
      
      <div class="timeline">
        <div v-for="(step, index) in roadmapResult.academic_path" :key="index" class="timeline-item">
          <div class="step-number">{{ step.step }}</div>
          <div class="step-content">
            <h4>{{ step.course_code }} - {{ step.course_name }}</h4>
            <p class="reason"><em>"{{ step.reason }}"</em></p>
            
            <div class="mini-skills">
                <span v-for="s in step.skills.slice(0,3)" :key="s" class="mini-tag">{{ s }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

// State
const mode = ref('chat'); 
const userInput = ref('');
const loading = ref(false);
const error = ref(null);

// Results
const chatResult = ref(null);
const roadmapResult = ref(null);
const synergyData = ref(null); // Stores the deep analysis

// === 1. Main Recommendation Logic ===
const submitQuery = async () => {
  if (!userInput.value.trim()) return;

  loading.value = true;
  error.value = null;
  chatResult.value = null; // Clear previous
  roadmapResult.value = null;
  synergyData.value = null; // Hide synergy until requested

  try {
    // We assume Laravel Sanctum handles Auth cookies automatically
    // Endpoint: /api/ai/recommend OR /api/ai/roadmap
    
    if (mode.value === 'chat') {
        const response = await axios.post('/api/ai/recommend', { query: userInput.value });
        chatResult.value = response.data;
    } else {
        const response = await axios.post('/api/ai/roadmap', { career_goal: userInput.value });
        roadmapResult.value = response.data;
    }

  } catch (err) {
    console.error(err);
    error.value = err.response?.data?.error || "AI Service is currently unreachable.";
  } finally {
    loading.value = false;
  }
};

// === 2. Deep Synergy Logic (Opt-In) ===
const getSynergy = async (courseCode) => {
    try {
        const response = await axios.post('/api/ai/synergy', { course_code: courseCode });
        // The backend returns { synergy_analysis: [ ... ] }
        synergyData.value = response.data.synergy_analysis; 
    } catch (err) {
        alert("Could not fetch synergy analysis.");
    }
};
</script>

<style scoped>
/* --- THEME COLORS --- */
:root {
    --primary: #008b8b; /* Dark Cyan */
    --primary-dark: #006666;
    --bg-light: #f4fcfc;
    --text-main: #2c3e50;
    --text-muted: #666;
}

.nexus-container {
  max-width: 850px;
  margin: 40px auto;
  font-family: 'Inter', sans-serif;
  color: var(--text-main);
}

.nexus-header {
  text-align: center;
  margin-bottom: 30px;
  color: #008b8b;
}

/* Tabs */
.tabs {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 25px;
}
.tab-btn {
  padding: 12px 25px;
  border: 2px solid #ddd;
  background: white;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}
.tab-btn.active {
  background: #008b8b;
  color: white;
  border-color: #008b8b;
  box-shadow: 0 4px 12px rgba(0, 139, 139, 0.25);
  transform: translateY(-2px);
}

/* Input Area */
.input-section {
  display: flex;
  gap: 12px;
  background: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.06);
  border: 1px solid #eee;
}
.nexus-input {
  flex: 1;
  padding: 15px;
  border: 2px solid #eee;
  border-radius: 10px;
  outline: none;
  font-size: 1rem;
  transition: border-color 0.3s;
}
.nexus-input:focus { border-color: #008b8b; }

.action-btn {
  background: #008b8b;
  color: white;
  border: none;
  padding: 0 30px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  transition: background 0.2s;
}
.action-btn:hover { background: #006666; }
.action-btn:disabled { background: #b2dfdb; cursor: not-allowed; }

/* Result Card */
.result-card, .roadmap-container {
  margin-top: 35px;
  background: white;
  padding: 30px;
  border-radius: 16px;
  border-left: 6px solid #008b8b;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
  position: relative;
}

.career-badge {
    position: absolute;
    top: -15px;
    right: 20px;
    background: #2c3e50;
    color: #fff;
    padding: 6px 15px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: bold;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.course-code {
    background: #e0f2f1;
    color: #00695c;
    padding: 4px 8px;
    border-radius: 6px;
    font-weight: bold;
    font-size: 0.9rem;
    margin-right: 10px;
}

.ai-message-box {
    background: #f8fcfc;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
    line-height: 1.6;
    color: #444;
}

/* Skills */
.skills-section {
    display: flex;
    gap: 30px;
    margin-top: 25px;
    padding-top: 20px;
    border-top: 1px solid #eee;
}
.skill-column h4 { margin-bottom: 12px; font-size: 0.95rem; color: #555; text-transform: uppercase; letter-spacing: 0.5px; }
.tags { display: flex; flex-wrap: wrap; gap: 8px; }

.skill-tag {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: 500;
}
.skill-tag.learn { background: #ffebee; color: #c62828; border: 1px solid #ffcdd2; }
.skill-tag.known { background: #e8f5e9; color: #2e7d32; border: 1px solid #c8e6c9; }

/* Synergy */
.synergy-action { text-align: center; margin-top: 30px; }
.synergy-btn {
    background: transparent;
    color: #008b8b;
    border: 2px solid #008b8b;
    padding: 10px 25px;
    border-radius: 25px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
}
.synergy-btn:hover { background: #008b8b; color: white; }

.synergy-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin-top: 20px;
}
.synergy-card {
    background: #fdfdfd;
    border: 1px solid #eee;
    padding: 15px;
    border-radius: 10px;
    border-top: 3px solid #f39c12; /* Accent color */
}
.synergy-header { font-weight: bold; margin-bottom: 8px; font-size: 0.9rem; }
.arrow { color: #aaa; margin: 0 5px; }
.synergy-text { font-size: 0.9rem; color: #666; font-style: italic; }

/* Timeline */
.timeline { margin-top: 30px; padding-left: 15px; }
.timeline-item { display: flex; gap: 20px; margin-bottom: 30px; position: relative; }
.timeline-item::before {
  content: ''; position: absolute; left: 16px; top: 40px; bottom: -30px; width: 2px; background: #e0e0e0;
}
.timeline-item:last-child::before { display: none; }

.step-number {
  background: #008b8b; color: white; width: 35px; height: 35px;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-weight: bold; z-index: 2; border: 3px solid white; box-shadow: 0 0 0 2px #008b8b;
}
.step-content { flex: 1; background: #f9f9f9; padding: 20px; border-radius: 12px; }
.mini-skills { margin-top: 10px; }
.mini-tag { display: inline-block; background: #eee; font-size: 0.8rem; padding: 2px 8px; border-radius: 4px; margin-right: 5px; color: #555; }

.fade-in { animation: fadeIn 0.4s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.error-box { background: #fee2e2; color: #b91c1c; padding: 15px; border-radius: 8px; margin-top: 20px; text-align: center; font-weight: bold; }
</style>