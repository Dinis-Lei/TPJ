import math
import random

import pygame
from actor import Actor
from observer import Observer
from collision import CollisionCircle
from bullet import Bullet
from service_locator import ServiceLocator
from spriteloader import EnemySprite
from game_vars import *
from signals import *

display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))

class Enemy(Actor):
    def __init__(self, direction = 0, velocity = 1,  position = [0,0], fire_interval = 3)  -> None:
        self.direction = direction
        self.velocity = velocity
        self.position = position
        self.sprite = EnemySprite("enemy.png")
        self.fire_interval = fire_interval
        self.serv_locator = ServiceLocator.create()
        self.observer = self.serv_locator.get_observer()
        self.lives = 1
        self.i = 0
        self.delete = False
        self.rect = self.sprite.get_sprite().get_rect()
        
        # Subscribe to events
        self.observer.subscribe(Display, self)
        self.observer.subscribe(Update, self)
        self.observer.subscribe(Move, self)
        self.observer.subscribe(EnemyShoot, self)
        self.observer.subscribe(CheckCollision, self)

        # Collision Set up
        self.collision_box = CollisionCircle(self, center=self.rect.center, radius=50)
        self.collision_box.set_enter_func(self.damage_taken)
        self.center = (49, 49)

    def check_collision(self):
        self.collision_box.check_collision()
    
    def damage_taken(self, collider=None):
        self.lives -= 1
        print(f"Damage taken, Lives {self.lives}")
        if self.lives == 0:
            self.delete = True
    
    def enemy_shoot(self):
        if self.i == self.fire_interval:

            x = self.position[0] + math.cos(self.direction) * 75
            y = self.position[1] + math.sin(self.direction) * 75
            Bullet(self.direction, [x,y])  
            self.serv_locator.get_sound_manager().play("laser2")
            self.i = 0
        else: 
            self.i += 1
    def check_bounds(self):
        if not -200 <= self.position[0] <= WIDTH*SCALE+200 or not -200 <= self.position[1] <= HEIGHT*SCALE+200:
            self.delete = True

    def update(self):
        self.check_bounds()
        if self.delete:
            self.observer.unsubscribe(Display, self)
            self.observer.unsubscribe(Update, self)
            self.observer.unsubscribe(Move, self)
            self.observer.unsubscribe(EnemyShoot, self)
            self.observer.unsubscribe(CheckCollision, self)
            self.collision_box = self.collision_box.delete()

    @classmethod
    def create(cls, player):
        direction = math.radians(random.randint(0,360))
        print(direction)
        velocity = random.randint(2,5)
        a = random.randint(1,5)
        if a <= 4:
            return EnemyLinear(direction, velocity)
        else:
            print("Enemy Crazy Created")
            return EnemyCrazy(player, direction, velocity)
    
    def getInitialPosition(self, direction):
        if math.pi/4 < direction <= math.pi*3/4:
            return [random.randint(0,WIDTH*SCALE),-100]
        elif math.pi*3/4 < direction <= math.pi*5/4:
            return [WIDTH*SCALE+100,random.randint(0,WIDTH*SCALE)]
        elif math.pi*5/4 < direction <= math.pi*7/4:
            return [random.randint(0,WIDTH*SCALE),HEIGHT*SCALE+100]
        else:
            return [-100,random.randint(0,HEIGHT*SCALE)]
        
    def display(self):
        img, rect = self.rotate()
        # self.rect = self.sprite.get_sprite().get_rect()
        display.blit(img, rect)

class EnemyLinear(Enemy):
    def __init__(self, direction = 0, velocity = 1) -> None:
        self.position = super().getInitialPosition(direction=direction)
        self.fire_interval = random.randint(15,30)
        super().__init__( direction, velocity, self.position, self.fire_interval)
        

    def move(self):
        """ Enemy movement pattern """
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity
        self.collision_box.move()


class EnemyCrazy(Enemy):
    def __init__(self, player, direction = 0, velocity = 1) -> None:
        self.posPlayer = player.position
        self.position = super().getInitialPosition(direction=direction)
        self.fire_interval = random.randint(7,15)
        super().__init__(direction, velocity, self.position, self.fire_interval)

    def move(self):
        """ Enemy movement pattern """
        self.calculate_angle()
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity
        self.collision_box.move()
    
    def calculate_angle(self):
        x = self.posPlayer[0] - self.position[0]
        y = self.posPlayer[1] - self.position[1]
        if x != 0:
            if x<0:
                self.direction = math.atan(y/x) + math.pi
            else:
                self.direction = math.atan(y/x)