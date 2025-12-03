<template>
  <article class="panel">
    <div class="panel-head">
      <div>
        <p class="eyebrow">Wishlist</p>
        <h2>Your wishlisted games</h2>
      </div>
      <span class="muted">{{ wishlist.length }} total</span>
    </div>

    <div v-if="loading" class="fetch-loading">
      <VueSpinnerDots color="var(--accent)" size="80" />
    </div>

    <div class="list" v-else-if="wishlist.length">
      <div class="list-row" v-for="item in wishlist" :key="item.id">
        <div>
          <p class="title">{{ item.title }}</p>
          <p class="muted">AppID: {{ item.steam_appid ?? '—' }}</p>
          <button @click="removeWishlistGame(item.steam_appid ?? '')" class="remove-game-btn">Remove</button>
        </div>

        <div
          class="price-badge"
          v-if="item.price !== null && item.price !== undefined"
        >
          <span class="price"><b>{{ item.price }} {{ item.currency }}</b></span>
          <span class="discount" v-if="item.discount_percent">
            (-{{ item.discount_percent }}%)
          </span>
        </div>

        <span class="muted" v-else>Price unavailable</span>
      </div>
    </div>

    <div class="empty" v-else>
      <p>No game wishlisted yet. Add by searching on the left panel</p>
    </div>
  </article>
</template>

<script setup lang="ts">
import { VueSpinnerDots } from 'vue3-spinners';
import { defineEmits } from 'vue';

type WishlistItem = {
  id: number
  title: string
  steam_appid: string | null
  price: number | null
  currency: string | null
  discount_percent: number | null
}

const props = defineProps<{
  wishlist: WishlistItem[]
  loading?: boolean
}>()

const emit = defineEmits<{
  'remove-wishlist-game': [appid: string | null]
}>()

function removeWishlistGame(appid: string | null) {
  emit('remove-wishlist-game', appid)
}
</script>

<style scoped>
.fetch-loading {
  display: flex;
  justify-content: center;
  padding-top: 2rem;
}

.remove-game-btn {
  background: darkred;
}

.remove-game-btn:hover {
  filter: brightness(0.8);
}
</style>