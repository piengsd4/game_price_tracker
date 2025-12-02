import { defineStore } from "pinia";
import axios from "axios";

export interface User {
    id: number;
    username: string;
}

interface SessionRes {
    authenticated: boolean;
    username?: string | null
}

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null as User | null,
        isAuthenticated: false,
        loading: false,
    }),

    actions: {
        setUser(user: User) {
            this.user = user;
            this.isAuthenticated = true;
        },

        clearUser() {
            this.user = null;
            this.isAuthenticated = false;
        },

        async hydrateSession() {
            this.loading = true
            try {
            const res = await axios.get<SessionRes>('http://localhost:8000/api/auth/session/', { withCredentials: true })
            if (res.data.authenticated) {
                this.setUser({ id: 0, username: res.data.username ?? '' })
            } else {
                this.clearUser()
            }
            } finally {
            this.loading = false
            }
        },
    },
})
