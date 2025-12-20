<template>
  <div class="app-wrapper">
    
    <aside class="sidebar" :class="{ 'is-open': isMobileMenuOpen }">
      <div class="brand">
        <h2>DevNexus</h2> 
      </div>

      <nav class="nav-links">
        <router-link to="/roadmaps" class="nav-item" @click="closeMobileMenu">
          <span class="icon">🗺️</span> Roadmaps
        </router-link>
        
        <router-link to="/resources" class="nav-item" @click="closeMobileMenu">
          <span class="icon">📚</span> Resources
        </router-link>
        
        <router-link to="/profile" class="nav-item" @click="closeMobileMenu">
          <span class="icon">👤</span> My Profile
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button @click="handleLogout" class="logout-btn">
          <span class="icon">🚪</span> Logout
        </button>
      </div>
    </aside>

    <main class="main-content">
      
      <header class="top-bar">
        <button class="mobile-toggle" @click="toggleMobileMenu">
          ☰
        </button>
        <div class="user-info">
          <span>Welcome, Student</span> 
        </div>
      </header>

      <div class="content-slot">
        <slot></slot> 
      </div>

    </main>
    
    <div v-if="isMobileMenuOpen" class="overlay" @click="closeMobileMenu"></div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../axios';

const router = useRouter();
const isMobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

const handleLogout = async () => {
  try {
    await api.post('/logout'); // Call Laravel API to invalidate token
  } catch (err) {
    console.error("Logout error", err);
  } finally {
    // Always clear local storage and redirect
    localStorage.removeItem('token');
    router.push('/login');
  }
};
</script>

<style scoped>
/* --- THEME VARIABLES --- */
:root {
  --primary: #008B8B; /* Dark Cyan */
  --primary-dark: #006666;
  --sidebar-bg: #1e1e24;
  --text-light: #f4f4f4;
  --bg-light: #f5f7fa;
}

.app-wrapper {
  display: flex;
  height: 100vh;
  background-color: #f5f7fa;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* --- SIDEBAR --- */
.sidebar {
  width: 250px;
  background-color: #1e1e24; /* Dark Sidebar */
  color: #fff;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100%;
  transition: transform 0.3s ease;
  z-index: 1000;
}

.brand {
  padding: 20px;
  background-color: #008B8B; /* Dark Cyan Header */
  text-align: center;
}
.brand h2 { margin: 0; font-size: 1.5rem; letter-spacing: 1px; }

.nav-links { flex: 1; padding-top: 20px; }

.nav-item {
  display: flex;
  align-items: center;
  padding: 15px 25px;
  color: #aaa;
  text-decoration: none;
  transition: all 0.3s;
  border-left: 4px solid transparent;
}

.nav-item:hover { background-color: rgba(255,255,255,0.05); color: #fff; }
.nav-item.router-link-active { 
  background-color: rgba(0, 139, 139, 0.1); 
  color: #008B8B; 
  border-left-color: #008B8B; 
}
.icon { margin-right: 10px; font-size: 1.2rem; }

.sidebar-footer { padding: 20px; border-top: 1px solid #333; }
.logout-btn {
  background: none; border: none; color: #ff6b6b; cursor: pointer;
  font-size: 1rem; display: flex; align-items: center; width: 100%;
}
.logout-btn:hover { color: #ff4c4c; }

/* --- MAIN CONTENT --- */
.main-content {
  flex: 1;
  margin-left: 250px; /* Offset for sidebar */
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.top-bar {
  background: white;
  padding: 15px 30px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.content-slot { padding: 30px; }
.mobile-toggle { display: none; background: none; border: none; font-size: 1.5rem; cursor: pointer; }

/* --- RESPONSIVE --- */
@media (max-width: 768px) {
  .sidebar { transform: translateX(-100%); }
  .sidebar.is-open { transform: translateX(0); }
  .main-content { margin-left: 0; }
  .mobile-toggle { display: block; }
  
  .overlay {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.5); z-index: 900;
  }
}
</style>