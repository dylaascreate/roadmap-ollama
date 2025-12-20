<!-- connected to POST /api/register -->
<template>
  <div class="auth-container">
    <h2>Join DevNexus</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="form.name" type="text" placeholder="Full Name" required />
      <input v-model="form.email" type="email" placeholder="Email" required />
      <input v-model="form.password" type="password" placeholder="Password" required />
      <input v-model="form.password_confirmation" type="password" placeholder="Confirm Password" required />
      
      <button type="submit" :disabled="loading">
        {{ loading ? 'Registering...' : 'Register' }}
      </button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <router-link to="/login">Already have an account? Login</router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '../../axios';
import { useRouter } from 'vue-router';

const form = ref({ name: '', email: '', password: '', password_confirmation: '' });
const loading = ref(false);
const error = ref(null);
const router = useRouter();

const handleRegister = async () => {
    loading.value = true;
    error.value = null;
    try {
        const response = await api.post('/register', form.value);
        // Assuming API returns { token: '...', user: ... }
        localStorage.setItem('token', response.data.token);
        router.push('/roadmaps'); // Redirect to dashboard
    } catch (err) {
        error.value = err.response?.data?.message || 'Registration failed';
    } finally {
        loading.value = false;
    }
};
</script>