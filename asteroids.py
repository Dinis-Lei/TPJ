import random
from actor import Actor
from collision import CollisionCircle
from observer import Observer
import math

from spriteloader import AsteroidSprite
from signals import *

class Asteroid(Actor):
    def __init__(self, observer: Observer, direction = 0, velocity = 1) -> None:
        self.direction = direction
        self.position = [300,200]
        self.velocity = velocity
        self.sprite = AsteroidSprite("asteroid.png")
        self.observer = observer

        self.collision_box = CollisionCircle(self, self.observer, center=(50,40), radius=40)
        self.collision_box.set_enter_func(self.hit_object)
        self.observer.subscribe(Display, self)
        self.observer.subscribe(Move, self)

    def hit_object(self):
        print("Hit object")

    def move(self):
        """ Asteroid movement pattern """
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity

        self.collision_box.check_collision()


    def display(self):
        return super().display()

    def update(self):
        """ Update sprite """
        i = random.random()
        if i > 0.85:
            self.sprite = self.sprite.update_sprite("smallerasteroid.png")
        else:
            # destroy
            pass

    @classmethod
    def factory(cls, observer: Observer):
        direction = math.radians(random.randint(0,360))
        velocity = 0 # testar depois a velocidade
        return Asteroid(observer, direction, velocity)
