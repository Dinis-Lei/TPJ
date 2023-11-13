import math
import random
from actor import Actor
from observer import Observer
from spriteloader import EnemySprite
from game_vars import *

class Enemy(Actor):
    def __init__(self, observer: Observer, direction = 0, velocity = 1) -> None:
        self.direction = 0
        self.position = [0,0]
        self.velocity = 0
        self.sprite = EnemySprite("enemy.png")
        self.fire_interval = 0
        self.observer = observer


    def move(self):
        """ Enemy movement pattern """

    def update(self):
        """ Update sprite """
        pass


    def factory(cls, observer: Observer):
        direction = math.radians(random.randint(0,360))
        velocity = 1 # testar depois a velocidade
        if random.randint(1,5) <= 4:
            return EnemyLinear(observer, direction, velocity)
        else:
            return EnemyCrazy(observer, direction, velocity)
    
    def getInitialPosition(cls, direction):
        if -math.pi/4 < direction <= math.pi/4:
            return [0,random.randint(0,HEIGHT*SCALE)]
        elif math.pi/4 < direction <= math.pi*3/4:
            return [random.randint(0,WIDTH*SCALE),HEIGHT*SCALE]
        elif math.pi*3/4 < direction <= math.pi*-3/4:
            return [WIDTH*SCALE,random.randint(0,WIDTH*SCALE)]
        elif math.pi*-3/4 < direction <= -math.pi/4:
            return [random.randint(0,WIDTH*SCALE),0]

class EnemyLinear(Enemy):
    def __init__(self, observer: Observer, direction = 0, velocity = 1) -> None:
        self.direction = direction
        self.position = super().getInitialPosition(direction=self.direction)
        self.velocity = velocity
        self.sprite = EnemySprite("enemy.png")
        self.fire_interval = 0
        self.observer = observer
        super.__init__(observer, self.direction, self.velocity)

    def move(self):
        """ Enemy movement pattern """
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity

    def update(self):
        """ Update sprite """
        pass

class EnemyCrazy(Enemy):
    def __init__(self, observer: Observer, direction = 0, velocity = 1) -> None:
        self.direction = direction
        self.position = super().getInitialPosition(direction=self.direction)
        self.velocity = velocity
        self.sprite = EnemySprite("enemy.png")
        self.fire_interval = 0
        self.observer = observer
        super.__init__(observer, self.direction, self.velocity)

    def move(self):
        """ Enemy movement pattern """
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity
    
    def calculate_angle(self, posPlayer):
        x = posPlayer[0] - self.position[0]
        y = posPlayer[1] - self.position[1]
        if x != 0:
            self.direction += math.atan(y/x)
        

    def update(self):
        """ Update sprite """
        pass