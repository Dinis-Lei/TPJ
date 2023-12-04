from observer import Observer
from service_locator import ServiceLocator
from signals import *
from spriteloader import CollisionSprite
from actor import Actor
from game_vars import *

import math
import pygame

display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
collision_group = pygame.sprite.Group()
collision_id = dict()

class Collision():

    """ """

    def __init__(self, parent: Actor) -> None:
        self.obs = ServiceLocator.create().get_observer()
        self.parent = parent
        self.is_colliding = False

        self.obs.subscribe(Display, self)
        self.obs.subscribe(CheckCollision, self)

    def set_enter_func(self, func):
        self.enter_func = func

    def move(self):
        pass

    def check_collision(self):
        pass

    def display(self):
        pass

    def delete(self):
        self.obs.unsubscribe(Display, self)
        self.obs.unsubscribe(CheckCollision, self)
        self.parent = None

class CollisionBox(Collision):

    def __init__(self, actor: Actor, width, height, direction, id=None) -> None:
        super().__init__(actor)

        self.width = width
        self.height = height
        self.center = (width//2, height//2)
        self.direction = direction
        self.square = pygame.sprite.Sprite()
        self.square.image = pygame.Surface((width*SCALE, height*SCALE), pygame.SRCALPHA)
        pygame.draw.rect(self.square.image, (255, 255, 0, 128), (0,0, width, height))
        self.square.rect = pygame.Rect(self.parent.position[0], 
                                       self.parent.position[1], width, height)
        collision_group.add(self.square)
        collision_id[self.square] = id

    def check_collision(self):
        collide = pygame.sprite.spritecollide(self.square, collision_group, False, pygame.sprite.collide_circle)

        if len(collide) > 1 and not self.is_colliding:
            collider_id = collision_id[[c for c in collide if c != self.square][0]]
            self.enter_func(collider = collider_id)
            self.is_colliding = True
        elif len(collide) < 2:
            self.is_colliding = False
    
    def move(self):
        self.circle.rect.center = (self.parent.position[0]+self.center[0], self.parent.position[1]+self.center[1])
        #self.square.rect.center = (self.parent.position[0], self.parent.position[1])

    def display(self):
        img, rect = self.rotate()
        #print(rect, self.square.rect)
        display.blit(img, rect)

    def rotate(self):
        image = self.square.image
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
    
    def delete(self):
        super().delete()
        collision_group.remove(self.square)
        collision_id.pop(self.square)

class CollisionCircle(Collision):

    def __init__(self, actor: Actor, center, radius, offset=[0,0], id=None) -> None:
        super().__init__(actor)
        self.center = center
        self.radius = radius
        self.is_colliding = False
        self.offset = offset

        self.circle = pygame.sprite.Sprite()
        self.circle.image  = pygame.Surface((self.radius*SCALE, self.radius*SCALE), pygame.SRCALPHA)
        pygame.draw.circle(self.circle.image, (255, 255, 0, 128) if DEBUG_COLLISION else (0,0,0,0) , self.center, self.radius)
        self.circle.rect = pygame.Rect(self.parent.position[0] - self.offset[0], 
                                       self.parent.position[1] - self.offset[1], 0, 0)
        self.circle.radius = self.radius

        collision_group.add(self.circle)
        collision_id[self.circle] = id

    def display(self):
        display.blit(self.circle.image, (self.parent.position[0] - self.center[0] - self.offset[0], 
                                         self.parent.position[1] - self.center[1] - self.offset[1]))


    def move(self):
        #self.circle.rect.center = (self.parent.position[0]-self.center[0], self.parent.position[1]-self.center[1])
        self.circle.rect.center = (self.parent.position[0] - self.offset[0], self.parent.position[1] - self.offset[1])

    def check_collision(self):
        collide = pygame.sprite.spritecollide(self.circle, collision_group, False, pygame.sprite.collide_circle)

        if len(collide) > 1 and not self.is_colliding:
            collider_id = collision_id[[c for c in collide if c != self.circle][0]]
            self.enter_func(collider = collider_id)
            self.is_colliding = True
        elif len(collide) < 2:
            self.is_colliding = False
        
        for s in collide:
            pygame.draw.circle(display, (255, 0, 255), s.rect.center, s.rect.width // 2, 2)


    def delete(self):
        super().delete()
        collision_group.remove(self.circle)
        collision_id.pop(self.circle)