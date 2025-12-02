<template>
  <header class="main-header">
    <i class="pi pi-car"></i><h1 class="main-title">Game Price Tracker</h1>
    <nav>
      <RouterLink to="/">My Wishlist</RouterLink>
      <RouterLink to="/about">About</RouterLink>
    </nav>
    <div class="nav-actions">
      <div v-if="auth.loading">
      </div>

      <div v-else-if="auth.isAuthenticated">
        <span class="current-user">Current User: <b>{{ auth.user?.username }}</b></span>
        <button
          @click="handleLogout"
          class="logout-btn"
        >
          Logout
        </button>
      </div>

      <div v-else class="auth-buttons">
        <RouterLink to="/register" class="register-btn">Register</RouterLink>
        <RouterLink to="/login" class="login-btn">Login</RouterLink>
      </div>
    </div>

  </header>
</template>

<script lang="ts" setup>
import axios from 'axios';
import { useCsrf } from '@/composables/useCsrf';
import { getCookie } from '@/helper/getCookie';
import { useAuthStore } from '@/stores/auth';
import { useWishlistStore } from '@/stores/wishlist';

const auth = useAuthStore();
const wishlistStore = useWishlistStore();

async function handleLogout() {
  const confirm = window.confirm("Are you sure you want to logout?");

  if (confirm) {
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
    wishlistStore.clear();
  }
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

.auth-buttons {
  display: flex;
  gap: 1rem;
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

.register-btn {
  background: green;
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  text-decoration: none;
}

.register-btn:hover {
  filter: brightness(0.8);
}

.current-user {
  padding-right: 1rem;
}

.logout-btn {
  background: darkred;
}

.logout-btn:hover {
  filter: brightness(0.8);
}
</style>
