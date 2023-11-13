from observer import Observer
from signals import *
from spriteloader import CollisionSprite
from actor import Actor
from game_vars import *

import pygame

display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))

class Collision():

    def __init__(self, actor: Actor, observer: Observer) -> None:
        self.obs = observer
        self.actor = actor

        self.obs.subscribe(Display, self)

class CollisionBox(Collision):

    def __init__(self, actor: Actor, observer: Observer, width, height) -> None:
        super().__init__(actor, observer)

        self.width = width
        self.height = height
        self.sprite = CollisionSprite(width=width, height=height)


    def display(self):
        self.sprite.display_sprite(self.actor.position[0], self.actor.position[1])

class CollisionCircle(Collision):

    def __init__(self, actor: Actor, observer: Observer, center, radius) -> None:
        super().__init__(actor, observer)
        self.center = center
        self.radius = radius


    def display(self):
        self.circle  = pygame.Surface((self.radius*SCALE, self.radius*SCALE), pygame.SRCALPHA)
        pygame.draw.circle(self.circle, (255, 255, 0, 128), (50,40), self.radius)
        display.blit(self.circle, self.actor.position)



    