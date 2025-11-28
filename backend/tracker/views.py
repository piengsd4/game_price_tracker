from django.db.models import Prefetch, Q, Case, When, IntegerField
from django.db.models.functions import Greatest
from django.contrib.postgres.search import TrigramSimilarity, TrigramWordSimilarity
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tracker.models import Game, GamePlatform, GamePriceCurrent, Platform, WishList

@api_view(["GET"])
def search_games(request):
    query = request.GET.get("query", "").strip()
    if not query:
        return Response([])
    
    queryset = (
        Game.objects.filter(platform__platform=Platform.STEAM)
        .annotate(
            char_sim=TrigramSimilarity("title", query),
            word_sim=TrigramWordSimilarity(query, "title"),
            best_sim=Greatest("word_sim", "char_sim"),
            icontains_hit=Case(
                When(title__icontains=query, then=1),
                default=0,
                output_field=IntegerField(),
            ),
        )
        .filter(Q(title__icontains=query) | Q(best_sim__gt=0.01))
        .order_by("-icontains_hit", "-best_sim", "title")
        .prefetch_related(
            Prefetch("platform", queryset=GamePlatform.objects.filter(platform=Platform.STEAM))
        )
        .distinct()[:20]
    )
    
    results = [
        {
            "title": game.title,
            "steam_appid": next(
                (platform.platform_game_id for platform in game.platform.all() if platform.platform == Platform.STEAM),
                None,
            ),
            "similarity": game.best_sim,
        }
        for game in queryset
    ]
    
    return Response(results)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_wishlist_steam(request):
    queryset = (
        WishList.objects.filter(user=request.user)
        .select_related("game")
        .prefetch_related(
            Prefetch("game__platform", queryset=GamePlatform.objects.filter(platform=Platform.STEAM)),
            Prefetch("game__current_price", queryset=GamePriceCurrent.objects.filter(platform=Platform.STEAM)),
        )
    )
    
    data = []
    
    for steam_wishlist in queryset:
        steam_platform = next((platform for platform in steam_wishlist.game.platform.all() if platform.platform == Platform.STEAM), None)
        steam_price = next((price for price in steam_wishlist.game.current_price.all() if price.platform == Platform.STEAM), None)
        data.append({
            "id": steam_wishlist.id,
            "title": steam_wishlist.game.title,
            "steam_appid": steam_platform.platform_game_id if steam_platform else None,
            "price": steam_price.price if steam_price else None,
            "currency": steam_price.currency if steam_price else None,
            "discount_percent": steam_price.discount_percent if steam_price else None,
        })

    return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    appid = request.data.get("appid")
    if not appid:
        return Response({"error": "appid is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    game_platform = (
        GamePlatform.objects.filter(platform=Platform.STEAM, platform_game_id=appid)
        .select_related("game")
        .first()
    )
    if not game_platform:
        return Response({"error": "Cannot find requested appid"}, status=status.HTTP_404_NOT_FOUND)
    
    WishList.objects.get_or_create(user=request.user, game=game_platform.game)
    return Response({ "ok": True })
