import pygame
from actor import Actor
from observer import Observer
import math
from service_locator import ServiceLocator
from signals import Display, Move, Update
from game_vars import *
from collision import CollisionCircle
from spriteloader import BulletSprite

class Bullet(Actor):
    def __init__(self, direction, position, from_player=False) -> None:
        self.serv_loc = ServiceLocator.create()
        self.direction = direction     # direction angle
        self.position = position
        self.from_player = from_player
        self.center = (5,5)
        self.velocity = 15
        self.sprite = BulletSprite("bullet.png")
        self.observer = self.serv_loc.get_observer()

        self.observer.subscribe(Display, self)
        self.observer.subscribe(Move, self)
        self.observer.subscribe(Update, self)

        rotated_img, self.rotated_rect = self.rotate()
        self.sprite.update_sprite(rotated_img)

        self.collision_box = CollisionCircle(self, center=self.center, radius=5, id="player_bullet" if from_player else "enemy_bullet")
        self.collision_box.set_enter_func(self.hit)
        self.delete = False

    def hit(self, collider=None):
        self.delete = True


    def move(self):
        """ Bullet movement pattern """
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity

        self.collision_box.move()
    
    def check_bounds(self):
        if not -100 < self.position[0] < WIDTH*SCALE+100 or not -100 < self.position[1] < HEIGHT*SCALE+100:
            self.delete = True

    def update(self):
        self.check_bounds()
        if self.delete:
            self.observer.unsubscribe(Display, self)
            self.observer.unsubscribe(Move, self)
            self.observer.unsubscribe(Update, self)
            self.collision_box = self.collision_box.delete()
    
    def display(self):
        img, rect = self.rotate()
        self.sprite.update_sprite(img)
        self.sprite.display_sprite(rect)
        