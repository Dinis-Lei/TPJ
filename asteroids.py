import random
from actor import Actor
from collision import CollisionCircle
from observer import Observer
import math

from spriteloader import AsteroidSprite
from signals import *

class Asteroid(Actor):
    def __init__(self, observer: Observer, direction = 0, velocity = 1, position = [0,0]) -> None:
        self.observer = observer
        self.direction = direction
        self.position = position
        self.velocity = velocity
        self.delete = False
        self.id = id(self)
        print(f"Spawned asteroid {self.id}")

        self.sprite = AsteroidSprite("asteroid.png")
        self.center = (50, 40)
        self.collision_box = CollisionCircle(self, self.observer, center=self.center, radius=40)
        self.collision_box.set_enter_func(self.hit_object)
        self.observer.subscribe(Display, self)
        self.observer.subscribe(Move, self)
        self.observer.subscribe(Update, self)

    def hit_object(self):
        print(f"Hit object {self.id}")
        self.delete = True

    def move(self):
        """ Asteroid movement pattern """
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity
        self.collision_box.move()

    def display(self):
        self.sprite.display_sprite(self.position[0] - self.center[0], self.position[1] - self.center[1])
        

    def check_collision(self):
        self.collision_box.check_collision()

    def update(self):
        """ Update object """
        if self.delete:
            print(f"Deleted asteroid {self.id}")
            self.observer.unsubscribe(Display, self)
            self.observer.unsubscribe(Move, self)
            self.observer.unsubscribe(Update, self)
            self.collision_box = self.collision_box.delete()

    

    @classmethod
    def factory(cls, observer: Observer):
        direction = math.radians(random.randint(0,359))
        velocity = random.randint(1,5) # testar depois a velocidade

        if math.pi/4 <= direction < 3*math.pi/4:
            mu = 600
            sigma = 100
            position = [random.gauss(mu, sigma), -100]
        elif 3*math.pi/4 <= direction < 5*math.pi/4:
            mu = 450
            sigma = 100
            position = [1300 ,random.gauss(mu, sigma)]
        elif 5*math.pi/4 <= direction < 7*math.pi/4:
            mu = 600
            sigma = 100
            position = [random.gauss(mu, sigma), 1000]
        else:
            mu = 450
            sigma = 100
            position = [-100 ,random.gauss(mu, sigma)]

        return Asteroid(observer, direction, velocity, position)
