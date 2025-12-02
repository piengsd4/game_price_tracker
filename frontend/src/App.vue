<script setup lang="ts">
import MainHeader from '@/components/MainHeader.vue';
import MainFooter from '@/components/MainFooter.vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <div class="app">
    <MainHeader />
    <main class="page">
      <RouterView />
    </main>
    <MainFooter />
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
