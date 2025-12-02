<template>
  <header class="main-header">
    <i class="pi pi-github"></i><h1 class="main-title">Game Price Tracker</h1>
    <nav>
      <RouterLink to="/">My Wishlist</RouterLink>
      <RouterLink to="/about">About</RouterLink>
    </nav>
    <div class="nav-actions">
      <button v-if="auth.isAuthenticated" @click="handleLogout" class="logout-btn">Logout</button>
      <RouterLink v-else to="/login" class="login-btn">Login</RouterLink>
    </div>
  </header>
</template>

<script lang="ts" setup>
import axios from 'axios';
import { useCsrf } from '@/composables/useCsrf';
import { getCookie } from '@/helper/getCookie';
import { useAuthStore } from '@/stores/auth';

const auth = useAuthStore();

async function handleLogout() {
  await useCsrf();
  const csrfToken = getCookie("csrftoken");

  await axios.post("http://localhost:8000/api/auth/logout/", {},
    {
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json",
      },
      withCredentials: true,
    }
  );

  auth.clearUser();
}
</script>

<style scoped>
.main-title {
  padding-right: 1rem;
}

.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--panel);
  box-shadow: var(--shadow);
}

i {
  padding-right: 1rem;
}

nav {
  display: flex;
  gap: 10px;
}

nav a {
  padding: 5px 10px;
  color: var(--text);
}

nav a:hover {
  filter: brightness(0.8);
}

.nav-actions {
  margin-left: auto;
}

.login-btn {
  background: var(--accent);
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  text-decoration: none;
}

.login-btn:hover {
  filter: brightness(0.8);
}

.logout-btn {
  background: darkred;
}

.logout-btn:hover {
  filter: brightness(0.8);
}
</style>
