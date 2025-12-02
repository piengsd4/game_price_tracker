<template>
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
          <p class="muted">AppID: {{ item.steam_appid ?? '—' }}</p>
        </div>

        <div
          class="price-badge"
          v-if="item.price !== null && item.price !== undefined"
        >
          <span class="price">{{ item.currency }} {{ item.price }}</span>
          <span class="discount" v-if="item.discount_percent">
            -{{ item.discount_percent }}%
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
}>()
</script>