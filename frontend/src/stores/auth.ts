import { defineStore } from "pinia";

export interface User {
    id: number;
    username: string;
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
    },
})
