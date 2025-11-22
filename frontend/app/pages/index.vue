<template>
  <div>
    <h1>Game Price Tracker</h1>

    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Wishlist Games</th>
          <th>Prices</th>
          <th>Wishlisted At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1</td>
          <td>Diablo</td>
          <td>1000 JPY</td>
          <td><span class="status inprogress">In Progress</span></td>
          <td>
            <button class="edit-btn">Edit</button>
            <button class="delete-btn">Delete</button>
          </td>
        </tr>
        <tr>
          <td>2</td>
          <td>My Time at Bedrock</td>
          <td>2000 JPY</td>
          <td><span class="status pending">Pending</span></td>
          <td>
            <button class="edit-btn">Edit</button>
            <button class="delete-btn">Delete</button>
          </td>
        </tr>
        <tr>
          <td>3</td>
          <td>Skyrim</td>
          <td>3000 JPY</td>
          <td><span class="status completed">Completed</span></td>
          <td>
            <button class="edit-btn">Edit</button>
            <button class="delete-btn">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts" setup>
const { data: wishlist, refresh } = await useFetch('/api/wishlist/steam', { credentials: 'include' });
const addToWishlist = async (appid: string) => {
  await $fetch('/api/wishlist/add', { method: 'POST', body: { appid }, credentials: 'include' });
  await refresh();
}
</script>

<style>
* {
    box-sizing: border-box;
    font-family: "Segoe UI", sans-serif;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
}

h1 {
    text-align: center;
    margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: var(--panel);
  color: var(--text);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: var(--shadow);
}

thead {
    background: var(--accent);
    color: white;
}

th, td {
    padding: 14px 16px;
    text-align: left;
}

tr:nth-child(even) {
    background: rgba(255,255,255,0.04);
}

.status {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.9em;
    color: white;
    text-align: center;
    display: inline-block;
}

.status.pending { background: #facc15; }
.status.completed { background: #16a34a; }
.status.inprogress { background: var(--accent-2); }

button {
    border: none;
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9em;
}

.edit-btn { background: var(--accent); color: white; }
.delete-btn { background: #dc2626; color: white; }
</style>
