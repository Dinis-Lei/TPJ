from actor import Actor
from observer import Observer
import math

class Asteroid(Actor):
    def __init__(self, observer: Observer, direction = 0, velocity = 1) -> None:
        self.direction = direction
        self.position = (0,0)
        self.velocity = velocity
        self.sprite
        self.observer = observer

    def move(self):
        """ Bullet movement pattern """
        self.position[0] = math.cos(self.direction) * self.velocity
        self.position[1] = math.sin(self.direction) * self.velocity

    def update(self):
        """ Update sprite """
        pass