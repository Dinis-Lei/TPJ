import pygame
from actor import Actor
from observer import Observer
from signals import *
from spriteloader import PlayerSprite
from collision import *
import math

AccelerateMAX = 20
BrakeMAX = -10

class Player(Actor):
    def __init__(self, observer: Observer) -> None:
        super().__init__([40,20], PlayerSprite("player1.png"))
        self.direction = -math.pi/2
        self.velocity = 0
        self.lives = 3
        self.observer = observer

        # Subscribe to events
        self.observer.subscribe(Accelerate, self)
        self.observer.subscribe(Brake, self)
        self.observer.subscribe(Shoot, self)
        self.observer.subscribe(Display, self)
        self.observer.subscribe(Move, self)

        self.collision_box = CollisionCircle(self, self.observer, center=(50,40), radius=40)
        self.collision_box.set_enter_func(self.damage_taken)

    def accelerate(self):
        self.velocity += 1 if self.velocity < AccelerateMAX else 0

    def brake(self):
        self.velocity -= 1 if self.velocity > BrakeMAX else 0

    def change_angle(self, angle):
        self.direction = angle

    def move(self):
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity

        self.collision_box.check_collision()

    def update(self):
        """ Update sprite """
        if self.lives == 2:
            self.sprite.update_sprite(name="player2.png")
        elif self.lives == 1:
            self.sprite.update_sprite(name="player1.png")
        else:
            self.sprite.update_sprite(name="player3.png")

    def rotate(self):
        x = pygame.mouse.get_pos()[0] - self.position[0]
        y = pygame.mouse.get_pos()[1] - self.position[1]
        # print(self.direction, self.position, pygame.mouse.get_pos())
        if x != 0 and abs(x)>10:
            self.direction = math.atan2(y,x)
            self.sprite.update_sprite(img=pygame.transform.rotate(self.sprite.get_sprite(), int(-self.direction*180/math.pi-90)%360))
    
    def display(self):
        self.rotate()
        self.sprite.display_sprite(self.position[0], self.position[1])
        
    
    def damage_taken(self):
        print(f"Damage taken, Lives {self.lives}")
        self.lives -= 1
        if self.lives == 0:
            self.observer.notify(Quit)
    
    



    # def updatedir(self, dir):
    #     super().updatedir(dir)
