<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { userAuthStore } from "@/stores/auth.store";

const authStore = userAuthStore();
</script>

<template>
  <div class="app-container">
    <h1><img class="logo" src="src/assets/convergent-beauty-icon.png" alt="logo">convergent beauty<img class="logo" src="src/assets/convergent-beauty-icon.png" alt="logo"></h1>
    <nav v-show="authStore.user" class="navbar navbar-expand float-box">
      <div class="navbar-nav">
        <RouterLink to="/" class="nav-item nav-link">Home</RouterLink>
        <a v-if="authStore.user.bearerToken.length > 1"  @click="authStore.logout()" class="nav-item nav-link" aria-label="Logout">Logout</a>
        <RouterLink v-if="authStore.user.bearerToken.length < 1" to="/login" class="nav-item nav-link">Login</RouterLink>
        <RouterLink v-if="authStore.user.bearerToken.length < 1" to="/signup" class="nav-item nav-link">Sign up</RouterLink>
      </div>
    </nav>
    <Suspense>
      <div class="container">
        <RouterView />
      </div>
    </Suspense>
  </div>
</template>

<style scoped>
</style>
