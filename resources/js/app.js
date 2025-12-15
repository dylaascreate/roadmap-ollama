import './bootstrap'; // Default Laravel bootstrap
import '../css/app.css';

import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import { createPinia } from 'pinia';

// Import the Root Component
import App from './App.vue';
import Login from './pages/Auth/Login.vue';
import CreateRoadmap from './pages/Roadmaps/Create.vue';

// 1. Define Basic Routes (We will add more later)
const routes = [
    { path: '/', component: { template: '<h1>Welcome to DevNexus</h1>' } },
    { path: '/login', component: Login },
    { path: '/roadmap/create', component: CreateRoadmap }
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