<template>
    <div class="login-container">
        <h2>Login to DevNexus</h2>
        <form @submit.prevent="handleLogin">
            <div style="margin-bottom: 1rem;">
                <label>Email:</label>
                <input v-model="form.email" type="email" required placeholder="email@example.com" />
            </div>
            <div style="margin-bottom: 1rem;">
                <label>Password:</label>
                <input v-model="form.password" type="password" required />
            </div>
            <button type="submit">Login</button>
        </form>
        <p v-if="error" style="color: red; margin-top: 10px;">{{ error }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '../../services/api';
import { useRouter } from 'vue-router';

const router = useRouter();
const form = ref({
    email: '',
    password: ''
});
const error = ref('');

const handleLogin = async () => {
    try {
        // 1. Send request to Laravel
        const response = await api.post('/login', form.value);
        
        // 2. Store the token in LocalStorage
        localStorage.setItem('token', response.data.access_token);
        
        // 3. Redirect to Home
        alert('Login Successful!');
        router.push('/');
        
    } catch (err) {
        // Handle errors (e.g., wrong password)
        if (err.response && err.response.data.errors) {
            error.value = Object.values(err.response.data.errors).flat()[0];
        } else {
            error.value = 'An error occurred during login.';
        }
    }
};
</script>

<style scoped>
.login-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
}
input {
    display: block;
    width: 100%;
    padding: 8px;
    margin-top: 5px;
}
button {
    padding: 10px 20px;
    background-color: #008B8B; /* Dark Cyan Theme */
    color: white;
    border: none;
    cursor: pointer;
}
</style>