from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Game(BaseModel):
    title = models.CharField(max_length=200, unique=True)
    release_date = models.DateField(null=True, blank=True)
    
    # steam_id = models.IntegerField(null=True, blank=True, unique=True)
    # epicgames_id = models.IntegerField(null=True, blank=True, unique=True)
    # ubisoft_id = models.IntegerField(null=True, blank=True, unique=True)
    # xbox_id = models.IntegerField(null=True, blank=True, unique=True)
    # gog_id = models.IntegerField(null=True, blank=True, unique=True)
    # ea_id = models.IntegerField(null=True, blank=True, unique=True) 
    # playstation_id = models.IntegerField(null=True, blank=True, unique=True)
    # nintendo_id = models.IntegerField(null=True, blank=True, unique=True)
    
    def __str__(self):
        return self.title

class Platform(models.TextChoices):
    STEAM = "steam", "Steam"
    EPIC = "epic", "Epic Games Store"
    UBISOFT = "ubisoft", "Ubisoft Store"
    XBOX = "xbox", "Xbox Store"
    GOG = "gog", "GOG"
    EA = "ea", "EA Store"
    PLAYSTATION = "playstation", "PlayStation Store"
    NINTENDO = "nintendo", "Nintendo eShop"
    
class GamePlatform(models.Model):
    game = models.ForeignKey(Game, related_name="platform", on_delete=models.CASCADE)
    platform = models.CharField(max_length=30, choices=Platform.choices, db_index=True)
    platform_game_id = models.CharField(max_length=100)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["game", "platform"], name="unique_game_platform")
        ]
    
    def __str__(self):
        return f"{self.game} on {self.platform}"
    
class GamePriceCurrent(BaseModel):
    game = models.ForeignKey(Game, related_name="current_price", on_delete=models.CASCADE)
    platform = models.CharField(max_length=30, choices=Platform.choices, db_index=True)
    currency = models.CharField(max_length=10, default="USD")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    original_price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_percent = models.IntegerField(default=0)
    last_checked = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["game", "platform"], name="unique_game_platform_pricecurrent")
        ]
        ordering = ["game__title", "platform"]
        
    def __str__(self):
        return f"Current {self.platform} price for {self.game.title} --> {self.price if self.price != 0 else ""} {self.currency} (-{self.discount_percent}%)"
    
class GamePriceHistory(BaseModel):
    game = models.ForeignKey(Game, related_name="price_history", on_delete=models.CASCADE)
    platform = models.CharField(max_length=30, choices=Platform.choices, db_index=True)
    currency = models.CharField(max_length=10, default="USD")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    original_price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_percent = models.IntegerField(default=0)
    last_checked = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return f"[{self.created_at}] {self.platform} price for {self.game.title} --> {self.price if self.price != 0 else ""} {self.currency} (-{self.discount_percent}%)"
    
class WishList(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "game"], name="unique_user_game_wishlist")
        ]
    
    def __str__(self):
        return f"{self.user} is wishing for {self.game}"
