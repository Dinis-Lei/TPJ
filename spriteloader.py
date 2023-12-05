from pygame import image
from pygame.math import Vector2
import pygame
from game_vars import SCALE, WIDTH, HEIGHT
import os

assetpath = "assets/SpaceShooterRedux/PNG/"
display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
spriteDict = {}
for img in os.listdir("./usedAssets/images"):
    spriteDict[img] = image.load(f"./usedAssets/images/{img}")

class SpriteLoader:
    def __init__(self, name) -> None:
        self.sprite = spriteDict[name]

    def update_sprite(self, img = None, name = None ):
        """
            Change the sprite image by providing either a 
            sprite image 
            or a 
            name of a sprite image
        """
        if img != None:
            self.sprite = img
        else:
            self.sprite = spriteDict[name]

    def display_sprite(self, rect):
        display.blit(self.sprite, rect)

    def get_sprite(self):
        return spriteDict[self.og]



class PlayerSprite(SpriteLoader):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.og = name
    
    def update_sprite(self, img = None, name = None):
        if img != None:
            super().update_sprite(img)
        else:
            super().update_sprite(name)

    def display_sprite(self, x, y):
        display.blit(self.sprite, (x,y, SCALE, SCALE))
    
    def get_sprite(self):
        return spriteDict[self.og]


class AsteroidSprite(SpriteLoader):
    def __init__(self, name) -> None:
        super().__init__(name)
    
    def update_sprite(self, name):
        super().update_sprite(name=name)

    def display_sprite(self, x, y):
        super().display_sprite((x,y, SCALE, SCALE))


class BulletSprite(SpriteLoader):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.og = name
        
    def update_sprite(self, name):
        super().update_sprite(name)

    def display_sprite(self, rect):
        super().display_sprite(rect=rect)
    
    def get_sprite(self):
        return spriteDict[self.og]

class EnemySprite(SpriteLoader):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.og = name
    
    def update_sprite(self, name):
        super().update_sprite(name)

    def display_sprite(self, x,y):
        display.blit(self.sprite, (x,y, SCALE, SCALE))
    
    def get_sprite(self):
        return spriteDict[self.og]
