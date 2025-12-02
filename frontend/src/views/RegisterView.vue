<template>
  <div class="register-page">
    <div class="card">
      <h1>Register</h1>
      <p class="muted">Create an account for your dashboard</p>

      <form @submit.prevent="onSubmit">
        <label>
          Email
          <input
            v-model="email"
            type="text"
            autocomplete="email"
            required
          />
        </label>
        <label>
          Username
          <input
            v-model="username"
            type="text"
            autocomplete="username"
            required
          />
        </label>
        <label>
          Password
          <input
            v-model="password"
            type="password"
            autocomplete="current-password"
            required
          />
        </label>
        <label>
          Confirm Password
          <input
            v-model="confirmPassword"
            type="password"
            autocomplete="current-password"
            required
          />
        </label>
        <button type="submit" :disabled="loading">
          {{ loading ? "Registering..." : "Register" }}
        </button>
      </form>

      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import axios from "axios";
import router from "@/router";
import { ref, onMounted } from "vue";
import { useCsrf } from "@/composables/useCsrf";
import { getCookie } from "@/helper/getCookie";
import { useAuthStore } from "@/stores/auth";

const email = ref("");
const username = ref("");
const password = ref("");
const confirmPassword = ref("");
const error = ref("");
const loading = ref(false);

const auth = useAuthStore();

interface Session {
  authenticated: boolean;
  username?: string | null;
}

onMounted(async () => {
  const res = await axios.get<Session>("http://localhost:8000/api/auth/session/", {
    withCredentials: true,
  });

  if (res.data.authenticated) {
    auth.setUser({
      id: 0,
      username: res.data.username ?? "",
    });
  } else {
    auth.clearUser();
  }
});

const onSubmit = async () => {
  if (password.value !== confirmPassword.value) {
    error.value = "Passwords do not match";
    return;
  }

  await useCsrf();
  const csrfToken = getCookie("csrftoken");

  loading.value = true;
  error.value = "";

  try {
    const res = await axios.post<{
      ok: boolean;
      username: string;
    }>(
      "http://localhost:8000/api/auth/register/",
      {
        email: email.value,
        username: username.value,
        password: password.value,
      },
      {
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-Type": "application/json",
        },
        withCredentials: true,
      }
    );

    auth.setUser({
      id: 0,
      username: res.data.username,
    });

    await router.push("/");
  } catch (e: any) {
    error.value = e?.data?.error || "Register failed";
  } finally {
    loading.value = false;
  }
};
</script>

<style>
.register-page {
  min-height: 85vh;
  display: grid;
  place-items: center;
  background: var(--bg);
  color: var(--text);
  padding: 16px 24px;
}

.card {
  width: 100%;
  max-width: 460px;
  padding: 28px;
}

h1 {
  margin: 0 0 4px;
  font-size: 1.6rem;
}

.muted {
  margin: 0 0 16px;
  color: var(--muted);
}

form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-weight: 600;
  color: var(--text);
}

input {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.1);
  background: var(--panel);
  color: var(--text);
  box-shadow: var(--shadow);
}

button {
  margin-top: 6px;
  border: none;
  border-radius: 10px;
  padding: 10px 14px;
  font-weight: 700;
  cursor: pointer;
  background: green;
  color: white;
  transition: opacity 0.2s ease;
}

button:hover {
  filter: brightness(0.8);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  margin-top: 12px;
  color: #dc2626;
}
</style>
