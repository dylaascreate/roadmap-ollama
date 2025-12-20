import './bootstrap'; // Default Laravel bootstrap
import '../css/app.css';

import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import { createPinia } from 'pinia';

// Import the Root Component
import App from './App.vue';
import Login from './pages/Auth/Login.vue';
import Register from './pages/Auth/Register.vue'; // Fixed typo 'REgister' -> 'Register'

// --- ROADMAP COMPONENTS ---
import CreateRoadmap from './pages/Roadmaps/Create.vue';       // The Old/Simple Generator
import SmartGenerator from './pages/Roadmaps/SmartGenerator.vue';

// 1. Define Routes
const routes = [
    { path: '/', component: { template: '<h1>Welcome to DevNexus</h1>' } },
    { path: '/login', component: Login },
    { path: '/register', component: Register },

    // Old Generator
    { path: '/roadmap/create', component: CreateRoadmap },

    // ✅ New Smart Generator Route
    { path: '/roadmap/smart', component: SmartGenerator } 
];

// 2. Setup Router
const router = createRouter({
    history: createWebHistory(),
    routes,
});

// 3. Create Vue Instance
const app = createApp(App);

app.use(router);
app.use(createPinia());

// 4. Mount to the HTML element with id="app"
app.mount('#app');