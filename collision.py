from observer import Observer
from signals import *
from spriteloader import CollisionSprite
from actor import Actor
from game_vars import *

import pygame

display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
collision_group = pygame.sprite.Group()

class Collision():

    def __init__(self, parent: Actor, observer: Observer) -> None:
        self.obs = observer
        self.parent = parent

        self.obs.subscribe(Display, self)
        self.obs.subscribe(CheckCollision, self)

    def delete(self):
        self.obs.unsubscribe(Display, self)
        self.obs.unsubscribe(CheckCollision, self)
        self.parent = None

class CollisionBox(Collision):

    def __init__(self, actor: Actor, observer: Observer, width, height) -> None:
        super().__init__(actor, observer)

        self.width = width
        self.height = height
        self.sprite = CollisionSprite(width=width, height=height)


    def display(self):
        self.sprite.display_sprite(self.parent.position[0], self.parent.position[1])

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
        self.circle.rect.center = (self.parent.position[0]+self.center[0], self.parent.position[1]+self.center[1])

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