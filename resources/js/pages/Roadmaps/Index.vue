<!-- connected to GET /roadmaps -->
<template>
  <div class="page-container">
    <header class="flex justify-between">
      <h1>My Learning Roadmaps</h1>
      <router-link to="/roadmaps/create" class="btn-primary">
        + Generate New Roadmap
      </router-link>
    </header>

    <div v-if="loading">Loading roadmaps...</div>

    <div v-else-if="roadmaps.length === 0" class="empty-state">
      <p>No roadmaps found. Let AI create one for you!</p>
    </div>

    <div v-else class="roadmap-grid">
      <div v-for="map in roadmaps" :key="map.id" class="card">
        <h3>{{ map.title }}</h3> <p>Status: {{ map.status }}</p>
        
        <div class="actions">
          <router-link :to="`/roadmaps/${map.id}`">View Progress</router-link>
          <button @click="deleteRoadmap(map.id)" class="text-red">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios'; // Import directly from node_modules
const api = axios;

const roadmaps = ref([]);
const loading = ref(true);

const fetchRoadmaps = async () => {
  try {
    const response = await api.get('/roadmaps');
    roadmaps.value = response.data; // Ensure your API returns a JSON array
  } catch (error) {
    console.error("Failed to fetch roadmaps", error);
  } finally {
    loading.value = false;
  }
};

const deleteRoadmap = async (id) => {
  if(!confirm('Are you sure?')) return;
  try {
    await api.delete(`/roadmaps/${id}`);
    roadmaps.value = roadmaps.value.filter(r => r.id !== id);
  } catch (error) {
    alert('Failed to delete');
  }
};

onMounted(fetchRoadmaps);
</script>

<style scoped>
/* Basic layout styling */
.roadmap-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
.card { border: 1px solid #ccc; padding: 15px; border-radius: 8px; }
.flex { display: flex; justify-content: space-between; align-items: center; }
</style>