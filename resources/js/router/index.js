import { createRouter, createWebHistory } from 'vue-router';

// Import Pages
import Login from '../pages/Auth/Login.vue';
import Register from '../pages/Auth/Register.vue';
import RoadmapList from '../pages/Roadmaps/Index.vue';
import RoadmapShow from '../pages/Roadmaps/Show.vue';
import RoadmapCreate from '../pages/Roadmaps/Create.vue';
import Profile from '../pages/Profile/Profile.vue';
import ResourceIndex from '../pages/Resources/Index.vue';
import CareerShow from '../pages/Resources/CareerShow.vue';
import CourseShow from '../pages/Resources/CourseShow.vue';

const routes = [
    { path: '/login', name: 'Login', component: Login },
    { path: '/register', name: 'Register', component: Register },
    
    // Protected Routes
    { 
        path: '/roadmaps', 
        name: 'Roadmaps', 
        component: RoadmapList,
        meta: { requiresAuth: true }
    },
    { 
        path: '/roadmaps/:id', 
        name: 'RoadmapDetails', 
        component: RoadmapShow, 
        props: true,
        meta: { requiresAuth: true }
    },
    { 
        path: '/roadmaps/create',  // New Route
        name: 'RoadmapCreate', 
        component: RoadmapCreate,
        meta: { requiresAuth: true }
    },
    { 
        path: '/profile', 
        name: 'Profile', 
        component: Profile,
        meta: { requiresAuth: true }
    },
    { 
        path: '/resources', 
        name: 'Resources', 
        component: ResourceIndex,
        meta: { requiresAuth: true }
    },
    { 
        path: '/careers/:id', 
        name: 'CareerDetails', 
        component: CareerShow,
        props: true,
        meta: { requiresAuth: true }
    },
    { 
        path: '/courses/:id', 
        name: 'CourseDetails', 
        component: CourseShow,
        props: true,
        meta: { requiresAuth: true }
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Guard to check for Token
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token');
    if (to.meta.requiresAuth && !token) {
        next('/login');
    } else {
        next();
    }
});

export default router;