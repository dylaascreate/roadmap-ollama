<template>
    <div class="container">
        <nav style="padding: 1rem; background: #eee; margin-bottom: 20px;">
            <router-link to="/" style="margin-right: 10px;">Home</router-link>
            <router-link to="/roadmap/create" style="margin-right: 10px;">Generate Roadmap</router-link> 
            <router-link to="/login">Login</router-link>
        </nav>
        
        <router-view></router-view>
    </div>
</template>

<script setup>
// Script logic goes here later
</script>

<style>
/* Basic Global Styles */
body {
    font-family: sans-serif;
    margin: 0;
    padding: 0;
}
</style>