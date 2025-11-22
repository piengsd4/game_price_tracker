import requests
import traceback
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from tracker.models import Game, GamePlatform, Platform

def print_log(*args):
    print(f"[{str(datetime.now())[:-3]}] ", end="")
    print(*args)

def get_all_steam_apps():
    # get all app id
    req = requests.get(
        "https://api.steampowered.com/IStoreService/GetAppList/v1/?key=3FDBB17B9F57EB8537AEEDFEF5EA052E",
        timeout=10
    )

    if (req.status_code != 200):
        print_log("Failed to get all games on steam.")
        return []
    
    try:
        data = req.json()
    except Exception as e:
        traceback.print_exc(limit=5)
        return {}
    
    apps_data = data['response']['apps']

    apps_ids = []

    for app in apps_data:
        appid = app['appid']
        name = app['name']
        
        # skip apps that have empty name
        if not name:
            continue

        apps_ids.append({
            "appid": appid,
            "name": name
        })

    return apps_ids

class Command(BaseCommand):
    help = "Fetch all game appids for Steam"
    
    def handle(self, *args, **options):
        print_log("Fetching Steam appids...")
        
        apps = get_all_steam_apps()
        if not apps:
            print_log("appids couldn't be fetched. Exiting...")
            return
        
        num_games_added = 0
        num_platforms_added = 0
        
        with transaction.atomic():
            for app in apps:
                game, new_game_added = Game.objects.get_or_create(title=app["name"])
                if new_game_added:
                    num_games_added += 1
                    
                platform, new_platform_added = GamePlatform.objects.get_or_create(
                    game=game,
                    platform=Platform.STEAM,
                    defaults={"platform_game_id": app["appid"]},
                )
                if new_platform_added:
                    num_platforms_added += 1
                    
        print_log(f"Finished ingesting {num_games_added} Steam games. Added {num_platforms_added} new platforms.")