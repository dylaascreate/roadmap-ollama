<template>
  <AppLayout v-if="layout === 'default'">
    <router-view />
  </AppLayout>

  <div v-else class="auth-layout">
    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import AppLayout from './layouts/AppLayout.vue';

const route = useRoute();

// Determine layout based on route meta, default to 'empty' to avoid flash
const layout = computed(() => {
  return route.meta.layout || 'empty';
});
</script>

<style>
/* Global Styles can go here */
body { margin: 0; font-family: sans-serif; background-color: #f5f7fa; }
.auth-layout { 
  display: flex; 
  justify-content: center; 
  align-items: center; 
  min-height: 100vh; 
  background: #e9ecef; 
}
.page-container { max-width: 1200px; margin: 0 auto; }
.btn-primary { background-color: #008B8B; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block;}
.btn-primary:hover { background-color: #006666; }
</style>