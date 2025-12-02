<template>
  <footer class="main-footer">
    <div class="footer-inner">
      <div>
        <p class="eyebrow">Game Price Tracker</p>
        <p class="muted">Track Steam deals and manage your wishlist in one place.</p>
      </div>

      <div class="links">
        <a href="https://github.com/piengsd4/game_price_tracker" target="_blank" rel="noreferrer"><i class="pi pi-github"></i>GitHub</a>
      </div>
    </div>

    <div class="meta">
      <span>Live pricing updates • Session-secured</span>
      <span>© {{ year }}</span>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<style scoped>
.main-footer {
  margin-top: auto;
  padding: 18px 24px;
  background: var(--panel);
  color: var(--text);
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: var(--shadow);
}

.footer-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.eyebrow {
  margin: 0 0 4px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.75rem;
  color: var(--muted);
}

.muted {
  margin: 0;
  color: var(--muted);
}

.links {
  display: flex;
  gap: 12px;
  align-items: center;
}

.links a {
  color: var(--text);
  text-decoration: none;
  font-weight: 600;
}

.links a:hover {
  color: var(--accent);
}

.meta {
  margin-top: 12px;
  display: flex;
  justify-content: space-between;
  gap: 10px;
  font-size: 0.9rem;
  color: var(--muted);
  flex-wrap: wrap;
}

i {
  padding-right: 0.5rem;
}
</style>
