from django.contrib import admin
from tracker.models import Game, GamePlatform, GamePriceCurrent, GamePriceHistory, WishList

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "created_at", "updated_at")
    search_fields = ("title",)

@admin.register(GamePlatform)
class GamePlatformAdmin(admin.ModelAdmin):
    list_display = ("game", "platform", "platform_game_id")
    list_filter = ("platform",)
    search_fields = ("game__title", "platform_game_id")

@admin.register(GamePriceCurrent)
class GamePriceCurrentAdmin(admin.ModelAdmin):
    list_display = ("game", "platform", "currency", "price", "original_price", "discount_percent", "last_checked")
    list_filter = ("platform", "currency")
    search_fields = ("game__title",)

@admin.register(GamePriceHistory)
class GamePriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("game", "platform", "currency", "price", "original_price", "discount_percent", "created_at")
    list_filter = ("platform", "currency")
    search_fields = ("game__title",)

@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "created_at")
    search_fields = ("user__username", "game__title")
