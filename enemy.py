import math
import random

import pygame
from actor import Actor
from collision import CollisionCircle
from bullet import Bullet
from service_locator import ServiceLocator
from spriteloader import SpriteLoader
from game_vars import *
from signals import *

display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))

class Enemy(Actor):
    def __init__(self, direction = 0, velocity = 1,  position = [0,0], fire_interval = 3, spritename = "enemy.png")  -> None:
        super().__init__(position, SpriteLoader(spritename))
        
        self.direction = direction
        self.velocity = velocity
        self.position = position
        self.id = id(self)

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
        self.observer.subscribe(DestroyAll, self)
        self.observer.subscribe(Quit, self)

        # Collision Set up
        self.collision_box = CollisionCircle(self, center=self.rect.center, radius=50, id=self.id)
        self.collision_box.set_enter_func(self.damage_taken)
        self.center = (49, 49)

    def check_collision(self):
        self.collision_box.check_collision()
    
    def damage_taken(self, collider=None):
        if collider == f"{self.id}_bullet" or collider == "powerup":
            return
        elif collider == "player_bullet" and not self.delete:
            self.observer.notify(UpdateScore, score=10)

        self.lives -= 1
        if self.lives == 0:
            self.delete = True
    
    def enemy_shoot(self):
        self.i += 1 if random.random() < 0.85 else 0    # Make fire rate more random
        if self.i == self.fire_interval:

            x = self.position[0] + math.cos(self.direction) * 75
            y = self.position[1] + math.sin(self.direction) * 75
            Bullet(self.direction, [x,y], creator_id=self.id)  
            self.serv_locator.get_sound_manager().play("laser2")
            self.i = 0

    def quit(self):
        self.delete = True
            
    def check_bounds(self):
        if not -200 <= self.position[0] <= WIDTH*SCALE+200 or not -200 <= self.position[1] <= HEIGHT*SCALE+200:
            self.delete = True

    def delete_object(self):
        self.observer.unsubscribe(Display, self)
        self.observer.unsubscribe(Update, self)
        self.observer.unsubscribe(Move, self)
        self.observer.unsubscribe(EnemyShoot, self)
        self.observer.unsubscribe(CheckCollision, self)
        self.observer.unsubscribe(DestroyAll, self)
        self.collision_box = self.collision_box.delete()

    def update(self):
        self.check_bounds()
        if self.delete:
            self.delete_object()

    @classmethod
    def create(cls):
        direction = math.radians(random.randint(0,360))
        velocity = random.randint(2,5)
        a = random.randint(1,5)
        if a <= 4:
            return EnemyLinear(direction, velocity)
        else:
            return EnemyCrazy(direction, velocity)
    
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

    def destroy_all(self):
        self.delete = True

class EnemyLinear(Enemy):
    def __init__(self, direction = 0, velocity = 1) -> None:
        self.position = super().getInitialPosition(direction=direction)
        self.fire_interval = random.randint(15,30)
        self.score = 3
        super().__init__( direction, velocity, self.position, self.fire_interval, spritename="enemy2.png")
        

    def move(self):
        """ Enemy movement pattern """
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity
        self.collision_box.move()

    
    @classmethod
    def create(cls):
        direction = math.radians(random.randint(0,360))
        velocity = random.randint(2,5)
        return EnemyLinear(direction, velocity)


class EnemyCrazy(Enemy):
    def __init__(self, direction = 0, velocity = 1) -> None:
        super().__init__(direction, velocity, spritename="enemy.png")
        self.posPlayer = [0,0]
        self.position = self.getInitialPosition(direction=direction)
        self.fire_interval = random.randint(7,15)
        self.score = 4
        
        self.observer.subscribe(PlayerPosition, self)

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

    def update_player_pos(self, pos):
        self.posPlayer = pos

    def delete_object(self):
        self.observer.unsubscribe(PlayerPosition, self)
        super().delete_object()

    @classmethod
    def create(cls):
        direction = math.radians(random.randint(0,360))
        velocity = random.randint(2,5)
        return EnemyCrazy(direction, velocity)