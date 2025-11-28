<template>
  <MainHeader />
  <NuxtPage />
  <MainFooter />
</template>

<script setup lang="ts">
</script>

<style>
:root {
  --bg: #0b1224;
  --panel: #111827;
  --text: #e5e7eb;
  --muted: #9ca3af;
  --accent: #2563eb;
  --accent-2: #2563eb;
  --shadow: 0 4px 10px rgba(0,0,0,0.35);
}

body {
  background: var(--bg);
  color: var(--text);
}
</style>
