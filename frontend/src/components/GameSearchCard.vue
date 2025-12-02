<template>
  <article class="panel">
    <div class="panel-head">
      <div>
        <p class="eyebrow">Add</p>
        <h2>Search results</h2>
      </div>
      <span class="muted">{{ searchResults.length }} found</span>
    </div>

    <div class="search-box">
      <input
        :value="query"
        type="search"
        placeholder="Search Steam games..."
        @input="onInput"
        @focus="$emit('search')"
      />
      <button class="primary" @click="$emit('search')" :disabled="searchLoading">
        {{ searchLoading ? 'Searching...' : 'Search' }}
      </button>
    </div>

    <div v-if="searchLoading" class="empty"><p>Searching…</p></div>

    <div v-else-if="query && searchResults.length" class="list">
      <div
        class="list-row"
        v-for="game in searchResults"
        :key="game.steam_appid || game.title"
      >
        <div>
          <p class="title">{{ game.title }}</p>
          <p class="muted">AppID: {{ game.steam_appid ?? '—' }}</p>
        </div>
        <button
          class="secondary"
          @click="$emit('add-to-wishlist', game.steam_appid)"
          :disabled="wishlistAddLoading || !game.steam_appid"
        >
          Add
        </button>
      </div>
    </div>

    <div v-else-if="query" class="empty">
      <p>No matches. Try another search.</p>
    </div>

    <div v-else class="empty">
      <p>Search to add games to your wishlist.</p>
    </div>
  </article>
</template>

<script setup lang="ts">
type SearchResult = {
  title: string
  steam_appid: string
  similarity?: number
}

interface Props {
  query: string
  searchResults: SearchResult[]
  searchLoading: boolean
  wishlistAddLoading: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:query': [value: string]
  search: []
  'add-to-wishlist': [appid: string | null]
}>()

const onInput = (event: Event) => {
  const value = (event.target as HTMLInputElement).value
  emit('update:query', value)
}
</script>