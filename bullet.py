from actor import Actor
import math
from service_locator import ServiceLocator
from signals import *
from game_vars import *
from collision import CollisionCircle
from spriteloader import SpriteLoader
from pygame.math import Vector2

class Bullet(Actor):
    """ Initiate bullet """
    def __init__(self, direction, position, creator_id=None, velocity=15) -> None:
        self.serv_loc = ServiceLocator.create()
        self.direction = direction 
        self.position = position
        self.center = (5,5)
        self.velocity = velocity
        self.sprite = SpriteLoader("bullet.png") if creator_id == "player" else SpriteLoader("enemybullet.png")
        self.observer = self.serv_loc.get_observer()
        self.creator_id = creator_id

        """ Signals that bullet subscribes """
        self.observer.subscribe(Display, self)
        self.observer.subscribe(Move, self)
        self.observer.subscribe(Update, self)
        self.observer.subscribe(DestroyAll, self)
        self.observer.subscribe(Quit, self)

        rotated_img, self.rotated_rect = self.rotate()
        self.sprite.update_sprite(rotated_img)

        collision_vectors = [
            Vector2([0,0]),
            Vector2([12,0]),
            Vector2([24,0]),
            Vector2([36,0]),            
        ]

        for i, vector in enumerate(collision_vectors):
            collision_vectors[i] = vector.rotate(-int(-(self.direction-math.pi/2)*180/math.pi-90)%360)

        """ colllision group for bullet, to make it more true to the bullet size """
        self.collision_box = [
            CollisionCircle(self, center=self.center, radius=5, offset=collision_vectors[0], id=f"{creator_id}_bullet"),
            CollisionCircle(self, center=self.center, radius=5, offset=collision_vectors[1], id=f"{creator_id}_bullet"),
            CollisionCircle(self, center=self.center, radius=5, offset=collision_vectors[2], id=f"{creator_id}_bullet"),
            CollisionCircle(self, center=self.center, radius=5, offset=collision_vectors[3], id=f"{creator_id}_bullet"),
        ]

        for c in self.collision_box:
            c.set_enter_func(self.hit)
        
        self.delete = False

    def hit(self, collider=None):
        """ check if bullet is colliding """
        if collider == self.creator_id:
            return
        self.delete = True
        self.serv_loc.get_sound_manager().play("hit", volume=1)

    def quit(self):
        """ delete bullet on endgame """
        self.delete = True


    def move(self):
        """ Bullet movement pattern """
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity

        for c in self.collision_box:
            c.move()
    
    def check_bounds(self):
        """ if bullet is not on screen, bullet can be deleted"""
        if not -100 < self.position[0] < WIDTH*SCALE+100 or not -100 < self.position[1] < HEIGHT*SCALE+100:
            self.delete = True

    def update(self):
        """ checking if bullet is going to be deleted """
        self.check_bounds()
        if self.delete:
            self.observer.unsubscribe(Display, self)
            self.observer.unsubscribe(Move, self)
            self.observer.unsubscribe(Update, self)
            self.observer.unsubscribe(DestroyAll, self)
            for c in self.collision_box:
                c.delete()
    
    def display(self):
        """ displaying bullet """
        img, rect = self.rotate()
        self.sprite.update_sprite(img)
        self.sprite.display_sprite(rect)

    def destroy_all(self):
        """ destroying all bullets when nuke power up is used """
        self.delete = True

        