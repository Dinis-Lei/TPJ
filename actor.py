from spriteloader import SpriteLoader
from game_vars import SCALE
import pygame
import math

class Actor:
    """ Base class for actor type objects """
    
    def __init__(self, position, sprite: SpriteLoader) -> None:
        self.direction = (0, 0)
        self.position : list = position
        self.sprite = sprite

    def rotate(self):
        """
            Rotate the actor's sprite

            return rotated image, rotated image rect
        """


        image = self.sprite.get_sprite()

        """ offset from pivot to center"""
        image_rect = image.get_rect(topleft = (self.position[0] - self.center[0], self.position[1]-self.center[1]))
        offset_center_to_pivot = pygame.math.Vector2(self.position) - image_rect.center
        """ rotated offset from pivot to center """
        rotated_offset = offset_center_to_pivot.rotate(-int(-self.direction*180/math.pi-90)%360)

        """ rotated image center """
        rotated_image_center = (self.position[0] - rotated_offset.x, self.position[1] - rotated_offset.y)

        
        """ get a rotated image """
        rotated_image = pygame.transform.rotate(image, int(-self.direction*180/math.pi-90)%360)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        return rotated_image, rotated_image_rect


    def display(self):
        """"
            Display Actor
        """
        self.sprite.display_sprite((self.position[0], self.position[1], SCALE, SCALE))