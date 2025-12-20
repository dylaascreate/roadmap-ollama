<!-- connected to /careers & GET /courses -->
<template>
  <div class="page-container">
    <div class="header-section">
      <h1>Resource Library</h1>
      <p>Explore potential career paths and recommended courses.</p>
    </div>

    <div class="tabs">
      <button 
        :class="{ active: activeTab === 'careers' }" 
        @click="activeTab = 'careers'"
      >
        Careers
      </button>
      <button 
        :class="{ active: activeTab === 'courses' }" 
        @click="activeTab = 'courses'"
      >
        Courses
      </button>
    </div>

    <div v-if="loading" class="loading">Loading library...</div>

    <div v-else class="grid-container">
      
      <template v-if="activeTab === 'careers'">
        <div 
          v-for="career in careers" 
          :key="career.id" 
          class="card career-card"
          @click="$router.push(`/careers/${career.id}`)"
        >
          <h3>{{ career.name }}</h3>
          <p class="excerpt">{{ truncate(career.description) }}</p>
          <span class="link-text">View Career Path &rarr;</span>
        </div>
      </template>

      <template v-if="activeTab === 'courses'">
        <div 
          v-for="course in courses" 
          :key="course.id" 
          class="card course-card"
          @click="$router.push(`/courses/${course.id}`)"
        >
          <span class="badge" :class="course.difficulty">{{ course.difficulty }}</span>
          <h3>{{ course.title }}</h3>
          <p class="platform">Platform: {{ course.platform }}</p>
          <span class="link-text">View Course Details &rarr;</span>
        </div>
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import api from '../../axios';

const activeTab = ref('careers'); // Default tab
const careers = ref([]);
const courses = ref([]);
const loading = ref(false);

// Helper to truncate text
const truncate = (text) => text?.length > 80 ? text.substring(0, 80) + '...' : text;

// Fetch function based on tab
const fetchData = async () => {
  loading.value = true;
  try {
    if (activeTab.value === 'careers' && careers.value.length === 0) {
      const res = await api.get('/careers');
      careers.value = res.data;
    } else if (activeTab.value === 'courses' && courses.value.length === 0) {
      const res = await api.get('/courses');
      courses.value = res.data;
    }
  } catch (error) {
    console.error("Fetch error", error);
  } finally {
    loading.value = false;
  }
};

// Fetch initial data
onMounted(fetchData);

// Watch for tab changes to fetch data if needed
watch(activeTab, fetchData);
</script>

<style scoped>
.header-section { margin-bottom: 20px; text-align: center; }

/* Tabs Styling */
.tabs { display: flex; justify-content: center; margin-bottom: 30px; border-bottom: 2px solid #eee; }
.tabs button {
  background: none; border: none; padding: 10px 20px; font-size: 1rem; cursor: pointer;
  border-bottom: 3px solid transparent; transition: all 0.2s;
}
.tabs button.active { border-bottom-color: #007bff; color: #007bff; font-weight: bold; }

/* Grid Layout */
.grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }

.card {
  background: white; padding: 20px; border-radius: 8px; border: 1px solid #ddd;
  cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }

/* Specific Card Styles */
.career-card h3 { color: #2c3e50; margin-bottom: 10px; }
.course-card .badge { 
  font-size: 0.75rem; padding: 3px 8px; border-radius: 4px; background: #e2e6ea; 
  text-transform: uppercase; float: right; 
}
.course-card .platform { color: #666; font-size: 0.9rem; margin-bottom: 15px; }

.link-text { color: #007bff; font-size: 0.9rem; font-weight: bold; margin-top: auto; display: block; }
</style>