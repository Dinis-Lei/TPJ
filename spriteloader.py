from pygame import image
import pygame
from game_vars import SCALE, WIDTH, HEIGHT
import os

assetpath = "assets/SpaceShooterRedux/PNG/"
display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
spriteDict = {}
for img in os.listdir("projeto/TPJ/usedAssets"):
    spriteDict[img] = image.load(f"projeto/TPJ/usedAssets/{img}")

class SpriteLoader:
    def __init__(self) -> None:
        self.sprites = spriteDict
        self.sprite = None

    def update_sprite(self, img = None, name = None ):
        if img != None:
            self.sprite = img
        else:
            self.sprite = self.sprites[name]

    def display_sprite(self, x, y):
        display.blit(self.sprite, (x, y, SCALE, SCALE))



class PlayerSprite(SpriteLoader):
    def __init__(self, name) -> None:
        super().__init__()
        print(self.sprites)
        self.sprite = self.sprites[name]
        self.og = name
    
    def update_sprite(self, img = None, name = None):
        if img != None:
            super().update_sprite(img)
        else:
            super().update_sprite(name)

    def display_sprite(self, x, y):
        super().display_sprite(x,y)
    
    def get_sprite(self):
        return self.sprites[self.og]


class AsteroidSprite(SpriteLoader):
    def __init__(self, name) -> None:
        super().__init__()
        self.sprite = self.sprites[name]
    
    def update_sprite(self, name):
        super().update_sprite(name)

    def display_sprite(self, x, y):
        super().display_sprite(x,y)


class BulletSprite(SpriteLoader):
    def __init__(self, name) -> None:
        super().__init__()
        self.sprite = self.sprites[name]
    
    def update_sprite(self, name):
        super().update_sprite(name)

    def display_sprite(self, x, y):
        super().display_sprite(x,y)

class EnemySprite(SpriteLoader):
    def __init__(self, name) -> None:
        super().__init__()
        self.sprite = self.sprites[name]
    
    def update_sprite(self, name):
        super().update_sprite(name)

    def display_sprite(self, x, y):
        super().display_sprite(x,y)