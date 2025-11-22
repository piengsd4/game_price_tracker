import requests
import traceback
from datetime import datetime

from django.core.management import BaseCommand
from django.db import transaction

from tracker.models import Game, Platform, GamePlatform, GamePriceCurrent, GamePriceHistory

def print_log(*args):
    print(f"[{str(datetime.now())[:-3]}] ", end="")
    print(*args)

class Command(BaseCommand):
    help = "Fetch Steam prices for wishlisted games"
    
    def handle(self, *args, **options):
        print_log("Fetching Steam prices for wishlisted games...")
        
        steam_games = (
            GamePlatform.objects.filter(platform=Platform.STEAM)
            .filter(game__wishlist__isnull=False)
            .distinct()
        )
        
        count = len(steam_games)
        print_log(f"Detected {count} wishlisted Steam games.")
        
        for steam_game in steam_games:
            steam_appid = steam_game.platform_game_id
            url = f"https://store.steampowered.com/api/appdetails?appids={steam_appid}"
            
            try:
                req = requests.get(url, timeout=10)
                data = req.json()
            except Exception:
                traceback.print_exc(limit=5)
                continue
                
            game_data = data.get(str(steam_appid), {})
            if not game_data.get("success"):
                print_log(f"Skipping {steam_appid}: no successful response.")
                continue
            
            price_info = game_data["data"].get("price_overview")
            
            if price_info is not None:
                currency = price_info["currency"]
                price = round(price_info["final"] / 100, 2)
                original_price = round(price_info["initial"] / 100, 2)
                discount_percent = price_info["discount_percent"]
            else:
                currency = "FREE"
                price = 0
                original_price = 0
                discount_percent = 0
            
            with transaction.atomic():
                current, created = GamePriceCurrent.objects.update_or_create(
                    game=steam_game.game,
                    platform=Platform.STEAM,
                    defaults={
                        "currency": currency,
                        "price": price,
                        "original_price": original_price,
                        "discount_percent": discount_percent,
                    }
                )
                print_log(f"Added {current}" if created else f"Updated {current}")
                
                history = GamePriceHistory.objects.create(
                    game=steam_game.game,
                    platform=Platform.STEAM,
                    currency = currency,
                    price = price,
                    original_price = original_price,
                    discount_percent = discount_percent
                )
                
                print_log(f"History added: {history}")
            
            