import random
from actor import Actor
from observer import Observer
import math

from spriteloader import AsteroidSprite

class Asteroid(Actor):
    def __init__(self, observer: Observer, direction = 0, velocity = 1) -> None:
        self.direction = direction
        self.position = [0,0]
        self.velocity = velocity
        self.sprite = AsteroidSprite("asteroid.png")
        self.observer = observer

    def move(self):
        """ Asteroid movement pattern """
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity

    def update_sprite(self):
        """ Update sprite """
        i = random.random()
        if i > 0.85:
            self.sprite = self.sprite.update_sprite("smallerasteroid.png")
        else:
            # destroy
            pass

    def factory(cls, observer: Observer):
        direction = math.radians(random.randint(0,360))
        velocity = 1 # testar depois a velocidade
        return Asteroid(observer, direction, velocity)
