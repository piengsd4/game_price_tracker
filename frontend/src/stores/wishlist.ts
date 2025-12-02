import { defineStore } from "pinia";

export interface WishlistItem {
    id: number;
    title: string;
    steam_appid: string | null;
    price: number | null;
    currency: string | null;
    discount_percent: number | null;
}

export const useWishlistStore = defineStore("wishlist", {
    state: () => ({
        items: [] as WishlistItem[],
    }),

    actions: {
        set(items: WishlistItem[]) {
            this.items = items;
        },

        clear() {
            this.items = [];
        },
    },
});
