
<!-- connected to GET /roadmaps/{id} & PATCH /tasks/{id}/toggle -->
<template>
  <div class="page-container" v-if="roadmap">
    
    <header class="roadmap-header">
      <div class="header-content">
        <h1>{{ roadmap.title }}</h1>
        <p class="description">{{ roadmap.description }}</p>
        <span class="badge" :class="roadmap.status">{{ roadmap.status }}</span>
      </div>

      <div class="progress-section">
        <div class="progress-info">
          <span>Progress</span>
          <span>{{ progressPercentage }}%</span>
        </div>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
      </div>
    </header>

    <hr />

    <div class="tasks-container">
      <h3>Your Learning Path</h3>
      
      <div v-if="loading" class="loading">Loading tasks...</div>
      
      <div v-else class="task-list">
        <div 
          v-for="task in roadmap.tasks" 
          :key="task.id" 
          class="task-item" 
          :class="{ completed: task.is_completed }"
        >
          <div class="checkbox-wrapper">
            <input 
              type="checkbox" 
              :id="'task-' + task.id"
              :checked="task.is_completed" 
              @change="toggleTask(task)"
            />
          </div>
          
          <div class="task-details">
            <label :for="'task-' + task.id" class="task-title">
              {{ task.title }}
            </label>
            <p v-if="task.description" class="task-desc">{{ task.description }}</p>
            
            <a v-if="task.resource_url" :href="task.resource_url" target="_blank" class="resource-link">
              View Resource &rarr;
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="loading" class="page-container">
    Loading Roadmap Details...
  </div>
  
  <div v-else class="page-container error">
    Roadmap not found.
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../../axios';
import { useRoute } from 'vue-router'; // Using route params if props fail

const props = defineProps(['id']); // Passed from router
const roadmap = ref(null);
const loading = ref(true);

// Calculate progress dynamically based on local task state
const progressPercentage = computed(() => {
  if (!roadmap.value || !roadmap.value.tasks || roadmap.value.tasks.length === 0) return 0;
  
  const completed = roadmap.value.tasks.filter(t => t.is_completed).length;
  const total = roadmap.value.tasks.length;
  return Math.round((completed / total) * 100);
});

const fetchRoadmap = async () => {
  try {
    const response = await api.get(`/roadmaps/${props.id}`);
    roadmap.value = response.data;
  } catch (error) {
    console.error("Error fetching roadmap:", error);
  } finally {
    loading.value = false;
  }
};

const toggleTask = async (task) => {
  // 1. Optimistic UI Update: Flip the boolean immediately so the UI feels fast
  const previousState = task.is_completed;
  task.is_completed = !task.is_completed;

  try {
    // 2. Send request to backend
    await api.patch(`/tasks/${task.id}/toggle`);
    // Backend should update the database
  } catch (error) {
    // 3. Revert if API fails
    task.is_completed = previousState;
    alert("Failed to update task. Please try again.");
  }
};

onMounted(fetchRoadmap);
</script>

<style scoped>
.roadmap-header { margin-bottom: 2rem; }
.description { color: #666; margin-bottom: 10px; }
.badge { padding: 4px 8px; background: #eee; border-radius: 4px; font-size: 0.8rem; text-transform: uppercase; }

/* Progress Bar */
.progress-section { margin-top: 20px; }
.progress-info { display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 5px; }
.progress-bar-bg { width: 100%; height: 10px; background: #e0e0e0; border-radius: 5px; overflow: hidden; }
.progress-bar-fill { height: 100%; background: #4caf50; transition: width 0.3s ease; }

/* Task List */
.task-list { display: flex; flex-direction: column; gap: 15px; }
.task-item { display: flex; gap: 15px; padding: 15px; background: #fff; border: 1px solid #ddd; border-radius: 8px; transition: all 0.2s; }
.task-item.completed { background: #f9f9f9; border-color: #eee; }
.task-item.completed .task-title { text-decoration: line-through; color: #888; }

/* Checkbox styling */
.checkbox-wrapper { display: flex; align-items: flex-start; padding-top: 3px; }
input[type="checkbox"] { width: 20px; height: 20px; cursor: pointer; }

.task-title { font-weight: bold; font-size: 1.1rem; cursor: pointer; display: block; }
.task-desc { color: #555; font-size: 0.9rem; margin: 5px 0; }
.resource-link { font-size: 0.85rem; color: #007bff; text-decoration: none; }
.resource-link:hover { text-decoration: underline; }
</style>