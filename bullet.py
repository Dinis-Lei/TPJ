import pygame
from actor import Actor
from observer import Observer
import math
from signals import Shoot, Display, Move

from spriteloader import BulletSprite

class Bullet(Actor):
    def __init__(self, observer: Observer, direction, position) -> None:
        self.direction = direction     # direction angle
        self.position = position
        self.velocity = 2
        self.sprite = BulletSprite("bullet.png")
        self.observer = observer

        self.observer.subscribe(Display, self)

    def travel(self):
        """ Bullet movement pattern """
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity

    def update(self):
        """ Update sprite """
        self.sprite = self.sprite.update_sprite("bullethit.png")
    
    def display(self):
        self.travel()
        self.sprite.update_sprite(pygame.transform.rotate(self.sprite.get_sprite(), int(-self.direction*180/math.pi-90)%360))
        self.sprite.display_sprite(self.position[0], self.position[1])
        