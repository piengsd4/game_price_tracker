<template>
  <div class="wishlist-page">
    <section class="hero">
      <div class="wishlist-title">
        <h1>Your Wishlist</h1>
        <p class="subhead">Search Steam titles and keep an eye on their live prices!</p>
      </div>
    </section>

    <section class="grid">
      <GameSearchCard
        v-model:query="query"
        :search-results="searchResults"
        :search-loading="searchLoading"
        :wishlist-add-loading="wishlistAddLoading"
        @search="searchGames"
        @add-to-wishlist="addToWishlist"
      />

      <WishlistCard :wishlist="wishlistStore.items" :loading="wishlistFetchLoading" />
    </section>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios'
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import GameSearchCard from '@/components/GameSearchCard.vue'
import WishlistCard from '@/components/WishlistCard.vue'
import { useToast } from 'vue-toastification'
import { useCsrf } from '@/composables/useCsrf'
import { getCookie } from '@/helper/getCookie'
import { useWishlistStore } from '@/stores/wishlist'
import { useAuthStore } from '@/stores/auth'

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

const query = ref('')
const wishlistStore = useWishlistStore();
const wishlistAddLoading = ref(false)
const wishlistFetchLoading = ref(false)
const searchResults = ref<SearchResult[]>([])
const searchLoading = ref(false)
const success = ref('')
const error = ref('')

const auth = useAuthStore();
const toast = useToast();

const fetchWishlist = async () => {
  error.value = ''
  wishlistFetchLoading.value = true
  try {
    const res = await axios.get<WishlistItem[]>(
      'http://localhost:8000/api/wishlist/steam',
      { withCredentials: true },
    )
    wishlistStore.set(res.data);
  } finally {
    wishlistFetchLoading.value = false
  }
}

const searchGames = async () => {
  if (!query.value.trim()) {
    searchResults.value = []
    return
  }

  searchLoading.value = true
  error.value = ''
  try {
    const res = await axios.get<SearchResult[]>(
      `http://localhost:8000/api/search/?query=${encodeURIComponent(
        query.value,
      )}`,
      { withCredentials: true },
    )
    searchResults.value = res.data
  } catch (e: any) {
    error.value = e?.data?.error || 'Search failed'
  } finally {
    searchLoading.value = false
  }
}

const addToWishlist = async (appid: string | null) => {
  if (!appid) return

  await useCsrf()
  const csrfToken = getCookie('csrftoken')

  wishlistAddLoading.value = true
  error.value = ''
  success.value = ''

  try {
    await axios.post('http://localhost:8000/api/wishlist/add/',
      { appid },
      {
        withCredentials: true,
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json',
        },
      },
    )
    success.value = 'Added to wishlist successfully'
    toast.success('Game added to wishlist successfully!')
    await fetchWishlist()
  } catch (e: any) {
    error.value = e?.data?.error || 'Could not add to wishlist'
  } finally {
    wishlistAddLoading.value = false
    setTimeout(() => (success.value = ''), 1500)
  }
}

// debounce search on query change
let debounceTimer: ReturnType<typeof setTimeout> | null = null

watch(query, () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => searchGames(), 300)
})

watch(
  () => auth.isAuthenticated,
  (isAuthenticated) => {
    if (!isAuthenticated) {
      query.value = '';
      searchResults.value = [];
    }
  }
)

onMounted(() => {
  fetchWishlist()
})
</script>

<style>
* {
  box-sizing: border-box;
  font-family: "Segoe UI", sans-serif;
}

.wishlist-page {
  max-width: 1800px;
  margin: 0 auto;
  padding: 24px;
  color: var(--text);
  background: var(--bg);
  min-height: 100vh;
}

.wishlist-title h1 {
  margin: 0;
  font-size: 1.8rem;
}

.subhead {
  margin: 4px 0 0;
  color: var(--muted);
}

.hero {
  margin-bottom: 24px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.75rem;
  color: var(--muted);
  margin: 0 0 6px;
  padding-top: 0.5rem;
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
}

.grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  align-items: stretch;
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    align-items: flex-start;
  }
}

.panel {
  background: var(--panel);
  border-radius: 14px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  height: 100%;
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
