from actor import Actor
from observer import Observer
import math

from spriteloader import BulletSprite

class Bullet(Actor):
    def __init__(self, observer: Observer, direction) -> None:
        self.direction = 0     # direction angle
        self.position = (0,0)
        self.velocity = 2
        self.sprite = BulletSprite("bullet.png")
        self.observer = observer


    def move(self):
        """ Bullet movement pattern """
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity

    def update_sprite(self):
        """ Update sprite """
        self.sprite = self.sprite.update_sprite("bullethit.png")