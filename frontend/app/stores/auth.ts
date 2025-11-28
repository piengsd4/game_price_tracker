import { defineStore } from "pinia";

type User = { id: number; username: string } | null

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null as User,
        isAuthenticated: false,
        loading: false,
    }),

    actions: {
        setUser(user: any) {
            this.user = user,
            this.isAuthenticated = true
        },
        clearUser() {
            this.user = null,
            this.isAuthenticated = false
        }
    },
})