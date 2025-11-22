from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.search_games, name="search_games"),
    path("wishlist/steam", views.get_wishlist_steam, name="get_wishlist_steam"),
    path("wishlist/add/", views.add_to_wishlist, name="add_to_wishlist"),
]
