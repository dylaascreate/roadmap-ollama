<!-- connected to GET /careers/{id} -->
<template>
  <div class="page-container" v-if="career">
    <button @click="$router.back()" class="btn-back">← Back to Library</button>
    
    <div class="detail-header">
      <h1>{{ career.name }}</h1>
      <p class="description">{{ career.description }}</p>
    </div>

    <div v-if="career.skills && career.skills.length > 0" class="section">
      <h3>Required Skills</h3>
      <div class="skills-grid">
        <div v-for="skill in career.skills" :key="skill.id" class="skill-tag">
          {{ skill.name }}
        </div>
      </div>
    </div>

    <div class="cta-section">
      <p>Interested in this path?</p>
      <button @click="generateRoadmap" class="btn-primary">Generate Roadmap for {{ career.name }}</button>
    </div>
  </div>
  <div v-else class="loading">Loading...</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../../axios';
import { useRouter } from 'vue-router';

const props = defineProps(['id']);
const career = ref(null);
const router = useRouter();

onMounted(async () => {
  try {
    const res = await api.get(`/careers/${props.id}`);
    career.value = res.data;
  } catch (error) {
    console.error(error);
  }
});

// Shortcut to start the AI generator with this career pre-selected
const generateRoadmap = () => {
  // Pass the career ID to the create page via query param (optional, needs Create.vue logic to handle it)
  // or just redirect for now
  router.push({ path: '/roadmaps/create', query: { career: props.id } });
};
</script>

<style scoped>
.btn-back { background: none; border: none; color: #666; cursor: pointer; margin-bottom: 15px; }
.detail-header { background: #f8f9fa; padding: 30px; border-radius: 8px; margin-bottom: 30px; }
.description { font-size: 1.1rem; line-height: 1.6; color: #444; }

.skills-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px; }
.skill-tag { background: #e3f2fd; color: #0d47a1; padding: 8px 15px; border-radius: 20px; font-weight: 500; }

.cta-section { text-align: center; margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px; }
</style>