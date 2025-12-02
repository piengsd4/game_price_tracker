// stores/auth.ts
import { defineStore } from "pinia";
import axios from "axios";

interface User {
  username: string;
}

interface Session {
  authenticated: boolean;
  username?: string | null;
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as User | null,
    loading: true,
  }),
  getters: {
    isAuthenticated: (state) => !!state.user,
  },
  actions: {
    setUser(user: User) {
      this.user = user;
    },

    clearUser() {
      this.user = null;
    },

    async init() {
      this.loading = true;
      try {
        const res = await axios.get<Session>(
          "http://localhost:8000/api/auth/session/",
          { withCredentials: true }
        );

        if (res.data.authenticated && res.data.username) {
          this.user = {
            username: res.data.username,
          };
        } else {
          this.user = null;
        }
      } catch (e) {
        this.user = null;
      } finally {
        this.loading = false;
      }
    },
  },
});
