from spriteloader import SpriteLoader
from signals import Display

class Actor:
    def __init__(self, position, sprite: SpriteLoader) -> None:
        self.direction = (0, 0)
        self.position = position
        self.sprite = sprite

    
    def updatedir(self, dir):
        self.direction = dir

    def display(self):
        self.sprite.display_sprite(self.position[0], self.position[1])