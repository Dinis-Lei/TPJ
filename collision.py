from observer import Observer
from signals import *
from spriteloader import CollisionSprite
from actor import Actor
from game_vars import *

import math
import pygame

display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
collision_group = pygame.sprite.Group()

class Collision():

    def __init__(self, parent: Actor, observer: Observer) -> None:
        self.obs = observer
        self.parent = parent

        self.obs.subscribe(Display, self)
        self.obs.subscribe(CheckCollision, self)

    def check_collision(self):
        pass

    def display(self):
        pass

    def delete(self):
        self.obs.unsubscribe(Display, self)
        self.obs.unsubscribe(CheckCollision, self)
        self.parent = None

class CollisionBox(Collision):

    def __init__(self, actor: Actor, observer: Observer, width, height, direction) -> None:
        super().__init__(actor, observer)

        self.width = width
        self.height = height
        self.center = (width//2, height//2)
        self.direction = direction
        self.sprite = CollisionSprite(width=width, height=height)

    def check_collision(self):
        pass


    def display(self):
        img, rect = self.rotate()
        self.sprite.update_sprite(img)
        self.sprite.display_sprite(rect)

    def rotate(self):
        image = self.sprite.get_sprite().image
        # offset from pivot to center
        image_rect = image.get_rect(topleft = (self.parent.position[0] - self.center[0], self.parent.position[1]-self.center[1]))
        offset_center_to_pivot = pygame.math.Vector2(self.parent.position) - image_rect.center
        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-int(-self.direction*180/math.pi-90)%360)

        # rotated image center
        rotated_image_center = (self.parent.position[0] - rotated_offset.x, self.parent.position[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, int(-self.direction*180/math.pi-90)%360)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        return rotated_image, rotated_image_rect

class CollisionCircle(Collision):

    def __init__(self, actor: Actor, observer: Observer, center, radius) -> None:
        super().__init__(actor, observer)
        self.center = center
        self.radius = radius
        self.id = id(self)
        self.is_colliding = False

        self.circle = pygame.sprite.Sprite()
        self.circle.image  = pygame.Surface((self.radius*SCALE, self.radius*SCALE), pygame.SRCALPHA)
        pygame.draw.circle(self.circle.image, (255, 255, 0, 128) if DEBUG_COLLISION else (0,0,0,0) , self.center, self.radius)
        self.circle.rect = pygame.Rect(self.parent.position[0] + self.center[0], 
                                       self.parent.position[1] + self.center[1], 0, 0)
        self.circle.radius = self.radius

        collision_group.add(self.circle)


    def set_enter_func(self, func):
        self.enter_func = func

    def display(self):
        display.blit(self.circle.image, (self.parent.position[0] - self.center[0], self.parent.position[1] - self.center[1]))


    def move(self):
        #self.circle.rect.center = (self.parent.position[0]+self.center[0], self.parent.position[1]+self.center[1])
        self.circle.rect.center = (self.parent.position[0], self.parent.position[1])

    def check_collision(self):
        collide = pygame.sprite.spritecollide(self.circle, collision_group, False, pygame.sprite.collide_circle)

        if len(collide) > 1 and not self.is_colliding:
            self.enter_func()
            self.is_colliding = True
        elif len(collide) < 2:
            self.is_colliding = False
        
        for s in collide:
            pygame.draw.circle(display, (255, 0, 255), s.rect.center, s.rect.width // 2, 2)


    def delete(self):
        super().delete()
        collision_group.remove(self.circle)