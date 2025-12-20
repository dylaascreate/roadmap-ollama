<template>
    <div class="login-container">
        <h2>Login</h2>
        
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label>Email</label>
                <input 
                    type="email" 
                    v-model="form.email" 
                    required 
                    placeholder="Enter email"
                >
                <span v-if="errors.email" class="error">{{ errors.email[0] }}</span>
            </div>

            <div class="form-group">
                <label>Password</label>
                <input 
                    type="password" 
                    v-model="form.password" 
                    required 
                    placeholder="Enter password"
                >
            </div>

            <button type="submit" :disabled="loading">
                {{ loading ? 'Logging in...' : 'Login' }}
            </button>

            <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
        </form>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const loading = ref(false);
const errorMessage = ref('');
const errors = ref({});

const form = reactive({
    email: '',
    password: ''
});

const handleLogin = async () => {
    loading.value = true;
    errors.value = {};
    errorMessage.value = '';

    try {
        // 1. Get the CSRF cookie first (Essential for Stateful Auth)
        await axios.get('/sanctum/csrf-cookie');

        // 2. Attempt login
        // Note: We use the web route '/login' or '/api/login' depending on your routes
        await axios.post('/login', form);

        // 3. Redirect on success
        router.push('/'); // Or wherever you want to go
        
    } catch (error) {
        if (error.response?.status === 422) {
            // Validation errors (e.g. wrong email format)
            errors.value = error.response.data.errors;
        } else if (error.response?.status === 401) {
            // Auth failed (Wrong password)
            errorMessage.value = 'Invalid email or password.';
        } else {
            errorMessage.value = 'An error occurred. Please try again.';
        }
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
.error { color: red; font-size: 0.8em; }
.error-msg { color: red; margin-top: 10px; }
.form-group { margin-bottom: 15px; }
input { display: block; width: 100%; padding: 8px; margin-top: 5px; }
button { padding: 10px 20px; cursor: pointer; }
</style>