from django.urls import path
from . import views, auth_views

urlpatterns = [
    # Auth
    path("auth/csrf/", auth_views.get_csrf, name="get_csrf"),
    path("auth/session/", auth_views.session_view, name="session"),
    path("auth/login/", auth_views.login_view, name="login"),
    path("auth/logout/", auth_views.logout_view, name="logout"),
    
    # Main App
    path("search/", views.search_games, name="search_games"),
    path("wishlist/steam", views.get_wishlist_steam, name="get_wishlist_steam"),
    path("wishlist/add/", views.add_to_wishlist, name="add_to_wishlist"),
]
