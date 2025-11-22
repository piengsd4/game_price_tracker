<template>
  <header class="main-header">
    <nav>
      <NuxtLink to="/">Dashboard</NuxtLink>
      <NuxtLink to="/about">About</NuxtLink>
    </nav>
    <button class="theme-btn" @click="toggleTheme">
      {{ theme === 'dark' ? 'Light' : 'Dark' }} mode
    </button>
  </header>
</template>

<script lang="ts" setup>
const theme = useState<'light' | 'dark'>('theme', () => 'light')
const toggleTheme = () => (theme.value = theme.value === 'dark' ? 'light' : 'dark')
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

.theme-btn {
  background: var(--accent);
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
}
</style>