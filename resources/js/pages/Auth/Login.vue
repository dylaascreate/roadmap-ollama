<!-- connected to POST /api/login -->
<template>
  <div class="auth-container">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      
      <button type="submit" :disabled="loading">
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <router-link to="/register">Need an account? Register</router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '../../axios';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const loading = ref(false);
const error = ref(null);
const router = useRouter();

const handleLogin = async () => {
    loading.value = true;
    error.value = null;
    try {
        const response = await api.post('/login', { email: email.value, password: password.value });
        localStorage.setItem('token', response.data.token);
        router.push('/roadmaps');
    } catch (err) {
        error.value = err.response?.data?.message || 'Invalid credentials';
    } finally {
        loading.value = false;
    }
};
</script>