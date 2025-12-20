<template>
  <div class="page-container">
    <h2>Generate AI Roadmap</h2>
    
    <form @submit.prevent="generateRoadmap" class="generator-form">
      
      <div class="form-group">
        <label>Target Career</label>
        <select v-model="form.career_id" required>
          <option disabled value="">Select a career path</option>
          <option v-for="career in options.careers" :key="career.id" :value="career.id">
            {{ career.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label>Specific Goal (Optional)</label>
        <textarea 
          v-model="form.goal" 
          placeholder="e.g., I want to master Laravel APIs in 3 months..."
        ></textarea>
      </div>

      <div class="form-group checkbox">
        <label>
          <input type="checkbox" v-model="useSmartAI"> 
          Use Smart RAG Generation (Better context, slower)
        </label>
      </div>

      <button type="submit" :disabled="loading" class="btn-primary">
        <span v-if="loading">AI is thinking... (This may take a minute)</span>
        <span v-else>Generate Roadmap</span>
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../../axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const options = ref({ careers: [] });
const loading = ref(false);
const error = ref(null);
const useSmartAI = ref(false);

const form = ref({
  career_id: '',
  goal: ''
});

// Fetch dropdown options on load
onMounted(async () => {
  try {
    const response = await api.get('/options');
    // Assuming API returns { careers: [...], skills: [...] }
    options.value = response.data; 
  } catch (err) {
    console.error("Failed to load options");
  }
});

const generateRoadmap = async () => {
  loading.value = true;
  error.value = null;

  // Decide which endpoint to use based on the checkbox
  const endpoint = useSmartAI.value 
    ? '/roadmaps/generate-smart' 
    : '/roadmaps/generate';

  try {
    const response = await api.post(endpoint, form.value);
    
    // Redirect to the new roadmap's detail page
    // Assuming API returns the created roadmap object with an ID
    router.push(`/roadmaps/${response.data.roadmap.id}`); 
  } catch (err) {
    error.value = err.response?.data?.message || 'AI Generation failed. Try again.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.generator-form { max-width: 500px; margin: 0 auto; }
.form-group { margin-bottom: 15px; display: flex; flex-direction: column; }
textarea { height: 100px; }
.error { color: red; margin-top: 10px; }
</style>