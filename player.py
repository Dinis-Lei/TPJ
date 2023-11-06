from actor import Actor
from observer import Observer
from signals import Accelerate, Brake, Shoot, Update, Move
from spriteloader import PlayerSprite
import math

AccelerateMAX = 20
BrakeMAX = -10

class Player(Actor):
    def __init__(self, observer: Observer) -> None:
        self.direction = -math.pi/2
        self.position =  [40,20]
        self.velocity = 1
        self.lives = 3
        self.sprite = PlayerSprite(name="player1.png")
        self.observer = observer

        # Subscribe to events
        self.observer.subscribe(Accelerate, self)
        self.observer.subscribe(Brake, self)
        self.observer.subscribe(Shoot, self)
        self.observer.subscribe(Update, self)
        self.observer.subscribe(Move, self)


    def up(self):
        self.direction[1] = -1

    def down(self):
        self.direction[1] = 1
    
    def left(self):
        self.direction[0] = -1

    def right(self):
        self.direction[0] = 1

    def accelerate(self):
        self.velocity += 1 if self.velocity < AccelerateMAX else 0

    def brake(self):
        self.velocity -= 1 if self.velocity > BrakeMAX else 0

    def change_angle(self, angle):
        self.direction = angle

    def move(self):
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity

    def update_sprite(self):
        """ Update sprite """
        if self.lives == 2:
            self.sprite = self.sprite.update_sprite("player2.png")
        elif self.lives == 1:
            self.sprite = self.sprite.update_sprite("player1.png")
        else:
            self.sprite = self.sprite.update_sprite("player3.png")
    
    # def updatedir(self, dir):
    #     super().updatedir(dir)
