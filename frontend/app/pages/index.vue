<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Your wishlist</p>
        <h1>Game Price Tracker</h1>
        <p class="subhead">Search Steam titles and keep an eye on live prices.</p>
      </div>
    </section>

    <section class="grid">
      <article class="panel">
        <div class="panel-head">
          <div>
            <p class="eyebrow">Add</p>
            <h2>Search results</h2>
          </div>
          <span class="muted">{{ searchResults.length }} found</span>
        </div>
        <div class="search-box">
          <input v-model="query" type="search" placeholder="Search Steam games..." @focus="searchGames" />
          <button class="primary" @click="searchGames" :disabled="searchLoading">
            {{ searchLoading ? "Searching..." : "Search" }}
          </button>
        </div>
        <div v-if="searchLoading" class="empty"><p>Searching…</p></div>
        <div v-else-if="query && searchResults.length" class="list">
          <div class="list-row" v-for="game in searchResults" :key="game.steam_appid || game.title">
            <div>
              <p class="title">{{ game.title }}</p>
              <p class="muted">AppID: {{ game.steam_appid ?? "—" }}</p>
            </div>
            <button class="secondary" @click="addToWishlist(game.steam_appid)" :disabled="addLoading || !game.steam_appid">
              Add
            </button>
          </div>
        </div>
        <div v-else-if="query" class="empty"><p>No matches. Try another search.</p></div>
        <div v-else class="empty"><p>Search to add games to your wishlist.</p></div>
      </article>

      <article class="panel">
        <div class="panel-head">
          <div>
            <p class="eyebrow">Wishlist</p>
            <h2>Your wishlisted games</h2>
          </div>
          <span class="muted">{{ wishlist.length }} total</span>
        </div>
        <div class="list" v-if="wishlist.length">
          <div class="list-row" v-for="item in wishlist" :key="item.id">
            <div>
              <p class="title">{{ item.title }}</p>
              <p class="muted">AppID: {{ item.steam_appid ?? "—" }}</p>
            </div>
            <div class="price-badge" v-if="item.price !== null && item.price !== undefined">
              <span class="price">{{ item.currency }} {{ item.price }}</span>
              <span class="discount" v-if="item.discount_percent">-{{ item.discount_percent }}%</span>
            </div>
            <span class="muted" v-else>Price unavailable</span>
          </div>
        </div>
        <div class="empty" v-else>
          <p>No game wishlisted yet. Add by searching on the left panel</p>
        </div>
      </article>
    </section>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue"

type WishlistItem = {
  id: number
  title: string
  steam_appid: string | null
  price: number | null
  currency: string | null
  discount_percent: number | null
}

type SearchResult = {
  title: string
  steam_appid: string
  similarity?: number
}

const query = ref("")
const wishlist = ref<WishlistItem[]>([])
const searchResults = ref<SearchResult[]>([])
const searchLoading = ref(false)
const addLoading = ref(false)
const error = ref("")
const success = ref("")

const fetchWishlist = async () => {
  error.value = ""
  const data = await $fetch<WishlistItem[]>("http://localhost:8000/api/wishlist/steam", {
    credentials: "include",
  })
  wishlist.value = data
}

const searchGames = async () => {
  if (!query.value.trim()) {
    searchResults.value = []
    return
  }
  searchLoading.value = true
  error.value = ""
  try {
    const data = await $fetch<SearchResult[]>(
      `http://localhost:8000/api/search/?query=${encodeURIComponent(query.value)}`,
      { credentials: "include" }
    )
    searchResults.value = data
  } catch (e: any) {
    error.value = e?.data?.error || "Search failed"
  } finally {
    searchLoading.value = false
  }
}

const addToWishlist = async (appid: string) => {
  addLoading.value = true
  error.value = ""
  success.value = ""
  try {
    await $fetch("http://localhost:8000/api/wishlist/add/", {
      method: "POST",
      body: { appid },
      credentials: "include",
    })
    success.value = "Added to wishlist"
    await fetchWishlist()
  } catch (e: any) {
    error.value = e?.data?.error || "Could not add to wishlist"
  } finally {
    addLoading.value = false
    setTimeout(() => (success.value = ""), 1500)
  }
}

let debounceTimer: ReturnType<typeof setTimeout> | null = null
watch(query, () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => searchGames(), 300)
})

onMounted(() => {
  fetchWishlist()
})
</script>

<style>
* {
  box-sizing: border-box;
  font-family: "Segoe UI", sans-serif;
}

.page {
  padding: 24px;
  color: var(--text);
}

.hero {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-end;
  flex-wrap: wrap;
  margin-bottom: 18px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.75rem;
  color: var(--muted);
  margin: 0 0 6px;
  padding-top: 0.5rem;
}

h1 {
  margin: 0;
  font-size: 1.8rem;
}

.subhead {
  margin: 4px 0 0;
  color: var(--muted);
}

.search-box {
  display: flex;
  gap: 8px;
  width: 100%;
  max-width: 100%;
  margin: 0 0 12px;
}

input[type="search"] {
  flex: 1;
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.08);
  background: var(--panel);
  color: var(--text);
  box-shadow: var(--shadow);
}

.grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}

.panel {
  background: var(--panel);
  border-radius: 14px;
  padding: 14px;
  box-shadow: var(--shadow);
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

h2 {
  margin: 0;
  font-size: 1.1rem;
}

.muted {
  color: var(--muted);
  font-size: 0.9rem;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.list-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(0,0,0,0.04);
  border-radius: 10px;
  padding: 12px;
}

.title {
  margin: 0 0 2px;
  font-weight: 600;
}

.price-badge {
  display: inline-flex;
  gap: 8px;
  align-items: center;
  background: rgba(37, 99, 235, 0.12);
  color: var(--text);
  padding: 6px 10px;
  border-radius: 10px;
}

.discount {
  color: var(--text);
  font-weight: 600;
}

.empty {
  padding: 16px;
  color: var(--muted);
}

.error {
  color: #dc2626;
  margin-top: 12px;
}

.success {
  color: #16a34a;
  margin-top: 12px;
}

.primary,
.secondary {
  border: none;
  cursor: pointer;
  border-radius: 10px;
  padding: 10px 14px;
  font-weight: 600;
  transition: opacity 0.2s ease;
}

.primary {
  background: var(--accent);
  color: white;
}

.secondary {
  background: rgba(37, 99, 235, 0.12);
  color: var(--text);
}

.primary:disabled,
.secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .hero {
    flex-direction: column;
    align-items: flex-start;
  }
  .search-box {
    width: 100%;
  }
}
</style>
