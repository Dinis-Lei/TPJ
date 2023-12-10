import random
from actor import Actor
from collision import CollisionCircle
from game_vars import *
import math

from spriteloader import SpriteLoader
from signals import *
from service_locator import ServiceLocator

class Asteroid(Actor):

    """ Initializing asteroids """
    def __init__(self, direction = 0, velocity = 1, position = [0,0], small=False) -> None:
        self.serv_loc = ServiceLocator.create()
        self.observer = self.serv_loc.get_observer()
        self.direction = direction
        self.position = position
        self.velocity = velocity
        self.delete = False
        self.small = small
        self.id = id(self)
        self.sprite = SpriteLoader("asteroid.png" if not small else "smallerasteroid.png")
        self.center = (40, 40) if not small else (15, 10)
        
        """ Signals that asteroid subscribes """
        self.observer.subscribe(Display, self)
        self.observer.subscribe(Move, self)
        self.observer.subscribe(Update, self)
        self.observer.subscribe(DestroyAll, self)
        self.observer.subscribe(Quit, self)

        self.collision_box = CollisionCircle(self, center=self.center, radius=45 if not small else 15)
        self.collision_box.set_enter_func(self.hit_object)

    def hit_object(self, collider=None):
        """ Check if asteroid hits an object
            Power Ups are not affected
            If it hits an object then it either disappears or it creates a smaller asteroid
        """
        if collider == "powerup":
            return
        self.delete = True

    def move(self):
        """ Asteroid movement pattern """
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity
        self.collision_box.move()

    def display(self):
        """Displaying asteroid"""
        self.sprite.display_sprite(
            (self.position[0] - self.center[0], self.position[1] - self.center[1], SCALE, SCALE))
        

    def check_collision(self):
        """Check for collision"""
        self.collision_box.check_collision()

    def quit(self):
        """ Quitting after game is over to remove all active asteroids """
        if(self.collision_box!= None):
            self.collision_box = self.collision_box.delete()
            self.observer.unsubscribe(Display, self)
            self.observer.unsubscribe(Move, self)
            self.observer.unsubscribe(Update, self)
            self.observer.unsubscribe(DestroyAll, self)
            self.delete = False


    def update(self):
        """ Update object """
        if self.delete:
            self.observer.unsubscribe(Display, self)
            self.observer.unsubscribe(Move, self)
            self.observer.unsubscribe(Update, self)
            self.observer.unsubscribe(DestroyAll, self)
            self.collision_box = self.collision_box.delete()

            if random.random() < 0.70 and not self.small:
                Asteroid.factory_small(self.position)

    def destroy_all(self):
        """ Destroy all asteroids, used when the power up nuke is activated"""
        self.delete = True

    @classmethod
    def create(cls):
        """ Normal sized asteroid factory 
            Randomizing direction, velocity and position
        """

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
            
        return Asteroid(direction, velocity, position)
    
    @classmethod
    def factory_small(cls, position):
        """ Small sized asteroid factory 
            Randomizing velocity and giving direction to small asteroids
            Position is equal to Normal asteroid when it got hit
        """
        n = random.randint(1,4)
        directions = [math.pi/4, 3*math.pi/4, 5*math.pi/4, 7*math.pi/4]
        for _ in range(n):
            velocity = random.randint(1,5) # testar depois a velocidade
            direction = directions[random.randint(0, len(directions)-1)]
            directions.remove(direction)
            position = [position[0] + math.cos(direction) * 30, position[1] + math.sin(direction) * 30]
            Asteroid(direction, velocity, position, small=True)

