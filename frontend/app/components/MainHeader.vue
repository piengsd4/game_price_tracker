<template>
  <header class="main-header">
    <nav>
      <NuxtLink to="/">Dashboard</NuxtLink>
      <NuxtLink to="/about">About</NuxtLink>
    </nav>
    <div class="nav-actions">
      <button v-if="user" @click="handleLogout">Logout</button>
      <NuxtLink v-else to="/login" class="login-btn">Login</NuxtLink>
    </div>
  </header>
</template>

<script lang="ts" setup>
const user = useUser();

async function handleLogout() {
  await useCsrf();
  const csrfToken = useCookie("csrftoken").value ?? "";

  await $fetch("http://localhost:8000/api/auth/logout/", {
    method: "POST",
    headers: {
      "CSRFToken": csrfToken,
      "Content-Type": "application/json",
    },
    credentials: "include",
  });

  user.value = null;
}
</script>

<style>
.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--panel);
  box-shadow: var(--shadow);
}

nav {
  display: flex;
  gap: 10px;
}

nav a {
  padding: 5px 10px;
  color: var(--text);
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
</style>
