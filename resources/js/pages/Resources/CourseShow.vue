<!-- GET /courses/{id} -->
<template>
  <div class="page-container" v-if="course">
    <button @click="$router.back()" class="btn-back">← Back to Library</button>
    
    <div class="course-layout">
      <div class="main-info">
        <h1>{{ course.title }}</h1>
        <div class="meta-row">
          <span class="badge">{{ course.difficulty }}</span>
          <span class="platform">By: <strong>{{ course.platform }}</strong></span>
          <span class="price" v-if="course.price">{{ course.price }}</span>
        </div>
        
        <p class="description">{{ course.description }}</p>
        
        <a :href="course.url" target="_blank" class="btn-primary visit-btn">
          Go to Course Website ↗
        </a>
      </div>
      
      <div class="side-panel">
         <div class="info-box">
           <h4>Course Info</h4>
           <ul>
             <li><strong>Platform:</strong> {{ course.platform }}</li>
             <li v-if="course.duration"><strong>Duration:</strong> {{ course.duration }}</li>
           </ul>
         </div>
      </div>
    </div>

  </div>
  <div v-else class="loading">Loading...</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../../axios';

const props = defineProps(['id']);
const course = ref(null);

onMounted(async () => {
  try {
    const res = await api.get(`/courses/${props.id}`);
    course.value = res.data;
  } catch (error) {
    console.error(error);
  }
});
</script>

<style scoped>
.btn-back { background: none; border: none; color: #666; cursor: pointer; margin-bottom: 15px; }

.course-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; }

.meta-row { display: flex; gap: 15px; align-items: center; margin: 15px 0; color: #555; }
.badge { background: #333; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; text-transform: uppercase; }

.description { font-size: 1.05rem; line-height: 1.6; margin-bottom: 25px; }

.visit-btn { display: inline-block; text-decoration: none; text-align: center; }

.info-box { background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #ddd; }
.info-box ul { list-style: none; padding: 0; }
.info-box li { margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 10px; }

@media (max-width: 768px) {
  .course-layout { grid-template-columns: 1fr; }
}
</style>