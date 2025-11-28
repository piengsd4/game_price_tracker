<template>
  <form @submit.prevent="onSubmit">
    <input v-model="username" type="text" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />
    <button type="submit" :disabled="loading">{{ loading ? "Logging in..." : "Login" }}</button>
    <p v-if="error">{{ error }}</p>
  </form>
</template>

<script lang="ts" setup>
import { ref } from "vue"

const username = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)

const user = useUser()

interface Session {
    authenticated: boolean,
    username?: string | null,
}

onMounted(async () => {
    const res = await $fetch<Session>("http://localhost:8000/api/auth/session/", {
        method: "GET",
        credentials: "include",
    })

    if (res.authenticated) {
        user.value = res.username ?? null;
    }
})

const onSubmit = async () => {
    await useCsrf();

    const csrfToken = useCookie("csrftoken").value ?? "";

    loading.value = true;
    error.value = "";

    try {
        const res = await $fetch<{
            ok: boolean,
            username: string,
        }>("http://localhost:8000/api/auth/login/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/json",
            },
            body: {
                username: username.value,
                password: password.value,
            },
            credentials: "include",
        })

        user.value = res.username

        await navigateTo("/")
    } catch (e: any) {
        error.value = e?.data?.error || "Login failed"
    } finally {
        loading.value = false
    }
}
</script>

<style>

</style>