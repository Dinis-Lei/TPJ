import math
import random

import pygame
from actor import Actor
from observer import Observer
from collision import CollisionCircle
from bullet import Bullet
from spriteloader import EnemySprite
from game_vars import *
from signals import *

display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))

class Enemy(Actor):
    def __init__(self, observer: Observer, direction = 0, velocity = 1,  position = [0,0], fire_interval = 3)  -> None:
        self.direction = direction
        self.velocity = velocity
        self.position = position
        self.sprite = EnemySprite("enemy.png")
        self.fire_interval = fire_interval
        self.observer = observer
        self.lives = 3
        self.i = 0
        self.delete = False
        self.rect = self.sprite.get_sprite().get_rect()
        self.observer.subscribe(Display, self)
        self.observer.subscribe(Update, self)
        self.observer.subscribe(Move, self)
        #self.observer.subscribe(EnemyShoot, self)
        self.observer.subscribe(CheckCollision, self)

        self.collision_box = CollisionCircle(self, self.observer, center=self.rect.center, radius=50)
        self.collision_box.set_enter_func(self.damage_taken)
        self.center = (49, 49)

    def check_collision(self):
        self.collision_box.check_collision()

    def rotate(self):
        image = self.sprite.get_sprite()

        # offset from pivot to center
        image_rect = image.get_rect(topleft = (self.position[0] - self.center[0], self.position[1]-self.center[1]))
        offset_center_to_pivot = pygame.math.Vector2(self.position) - image_rect.center
        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-int(-self.direction*180/math.pi-90)%360)

        # rotated image center
        rotated_image_center = (self.position[0] - rotated_offset.x, self.position[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, int(-self.direction*180/math.pi-90)%360)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        return rotated_image, rotated_image_rect
    
    def damage_taken(self):
        self.lives -= 1
        print(f"Damage taken, Lives {self.lives}")
        if self.lives == 0:
            self.delete = True
    
    # def enemy_shoot(self):
    #     print("Enemy shooting you")
    #     if self.i == self.fire_interval:
    #         bullet = Bullet(self.observer, self.direction, self.position)
    #         self.i = 0
    #     else: 
    #         self.i += 1
    def check_bounds(self):
        if not 0 <= self.position[0] <= WIDTH*SCALE or not 0 <= self.position[1] <= HEIGHT*SCALE:
            self.delete = True

    def update(self):
        self.check_bounds()
        if self.delete:
            self.observer.unsubscribe(Display, self)
            self.observer.unsubscribe(Update, self)
            self.observer.unsubscribe(Move, self)
            #self.observer.unsubscribe(EnemyShoot, self)
            self.observer.unsubscribe(CheckCollision, self)
            self.collision_box = self.collision_box.delete()

    @classmethod
    def factory(cls, observer: Observer, player):
        print("Entered enemy factory")
        direction = math.radians(random.randint(0,360))
        print(direction)
        velocity = random.randint(1,3)
        a = random.randint(1,5)
        if a <= 4:
            pass
            #return EnemyLinear(observer, direction, velocity)
        else:
            print("Enemy Crazy Created")
            return EnemyCrazy(observer, player, direction, velocity)
    
    def getInitialPosition(self, direction):
        if math.pi/4 < direction <= math.pi*3/4:
            return [random.randint(0,WIDTH*SCALE),0]
        elif math.pi*3/4 < direction <= math.pi*5/4:
            return [WIDTH*SCALE,random.randint(0,WIDTH*SCALE)]
        elif math.pi*5/4 < direction <= math.pi*7/4:
            return [random.randint(0,WIDTH*SCALE),HEIGHT*SCALE]
        else:
            return [0,random.randint(0,HEIGHT*SCALE)]

class EnemyLinear(Enemy):
    def __init__(self, observer: Observer, direction = 0, velocity = 1) -> None:
        self.position = super().getInitialPosition(direction=direction)
        self.fire_interval = random.randint(1,4)
        super().__init__(observer, direction, velocity, self.position, self.fire_interval)
        

    def move(self):
        """ Enemy movement pattern """
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity
        self.collision_box.move()
    
    def update(self):
        super().update()

    def display(self):
        img, rect = super().rotate()#blitRotate(self.sprite.get_sprite(), self.position, (49,49), self.test_angle)
        self.rect = self.sprite.get_sprite().get_rect()
        display.blit(img, rect)


class EnemyCrazy(Enemy):
    def __init__(self, observer: Observer, player, direction = 0, velocity = 1) -> None:
        self.posPlayer = player.position
        self.position = super().getInitialPosition(direction=direction)
        self.fire_interval = random.randint(1,4)
        super().__init__(observer, direction, velocity, self.position, self.fire_interval)

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

    def update(self):
        super().update()
    
    def display(self):
        img, rect = super().rotate()#blitRotate(self.sprite.get_sprite(), self.position, (49,49), self.test_angle)
        self.rect = self.sprite.get_sprite().get_rect()
        display.blit(img, rect)