from actor import Actor
from observer import Observer
import math

class Bullet(Actor):
    def __init__(self, observer: Observer, direction) -> None:
        self.direction = 0     # direction angle
        self.position = (0,0)
        self.velocity = 2
        self.sprite 
        self.observer = observer


    def move(self):
        """ Bullet movement pattern """
        self.position[0] = math.cos(self.direction) * self.velocity
        self.position[1] = math.sin(self.direction) * self.velocity

    def update(self):
        """ Update sprite """
        pass