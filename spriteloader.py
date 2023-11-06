from pygame import image
import pygame
from game_vars import SCALE, WIDTH, HEIGHT
import os

assetpath = "assets/SpaceShooterRedux/PNG/"
display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
spriteDict = {}
for img in os.listdir("./usedAssets"):
    spriteDict[img.title] = image.load(f"./usedAssets/{img}")

class SpriteLoader:
    def __init__(self) -> None:
        self.sprites = spriteDict
        self.sprite = None

    def update_sprite(self, name):
        self.sprite = self.sprites[name]

    def display_sprite(self, x, y):
        display.blit(self.sprite, (SCALE * x, SCALE * y, SCALE, SCALE))



class PlayerSprite(SpriteLoader):
    def __init__(self, name) -> None:
        self.sprite = self.sprites[name]
    
    def update_sprite(self, name):
        super().update_sprite(name)

    def display_sprite(self, x, y):
        super().display_sprite(x,y)


class AsteroidSprite(SpriteLoader):
    def __init__(self, name) -> None:
        self.sprite = self.sprites[name]
    
    def update_sprite(self, name):
        super().update_sprite(name)

    def display_sprite(self, x, y):
        super().display_sprite(x,y)


class BulletSprite(SpriteLoader):
    def __init__(self, name) -> None:
        self.sprite = self.sprites[name]
    
    def update_sprite(self, name):
        super().update_sprite(name)

    def display_sprite(self, x, y):
        super().display_sprite(x,y)

class EnemySprite(SpriteLoader):
    def __init__(self, name) -> None:
        self.sprite = self.sprites[name]
    
    def update_sprite(self, name):
        super().update_sprite(name)

    def display_sprite(self, x, y):
        super().display_sprite(x,y)