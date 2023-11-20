import pygame
from actor import Actor
from observer import Observer
from signals import *
from spriteloader import PlayerSprite
from collision import *
import math
from bullet import Bullet

AccelerateMAX = 20
BrakeMAX = -10

display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))

class Player(Actor):
    def __init__(self, observer: Observer) -> None:
        super().__init__([400,200], PlayerSprite("player3(1).png"))
        self.direction = -math.pi/2
        self.pivot = [40,57]
        self.velocity = 0
        self.lives = 3
        self.offset = pygame.math.Vector2(30, 0)
        self.rect = self.sprite.get_sprite().get_rect()
        self.observer = observer

        # Subscribe to events
        self.observer.subscribe(Accelerate, self)
        self.observer.subscribe(Brake, self)
        self.observer.subscribe(Shoot, self)
        self.observer.subscribe(Display, self)
        self.observer.subscribe(Move, self)

        self.collision_box = CollisionCircle(self, self.observer, center=self.rect.center, radius=50)
        self.collision_box.set_enter_func(self.damage_taken)

        # draw circle
        self.circle = pygame.sprite.Sprite()
        self.circle.image  = pygame.Surface((99, 99), pygame.SRCALPHA)
        pygame.draw.circle(self.circle.image, (255, 255, 0, 128), self.rect.center, 50)
        
        self.test_angle = 0

    def accelerate(self):
        self.velocity += 1 if self.velocity < AccelerateMAX else 0

    def brake(self):
        self.velocity -= 1 if self.velocity > BrakeMAX else 0

    def change_angle(self, angle):
        self.direction = angle

    def move(self):
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity
        self.pivot[0] += math.cos(self.direction) * self.velocity
        self.pivot[1] += math.sin(self.direction) * self.velocity
        #print(self.pivot)

        self.collision_box.check_collision()

    def update(self):
        """ Update sprite """
        if self.lives == 2:
            self.sprite.update_sprite(name="player2.png")
        elif self.lives == 1:
            self.sprite.update_sprite(name="player1.png")
        else:
            self.sprite.update_sprite(name="player3.png")

    def rotate(self):
        x = pygame.mouse.get_pos()[0] - self.position[0]
        y = pygame.mouse.get_pos()[1] - self.position[1]
        # print(self.direction, self.position, pygame.mouse.get_pos())
        if x != 0 and abs(x)>10:
            self.direction = math.atan2(y,x)
            self.sprite.update_sprite(img=pygame.transform.rotate(self.sprite.get_sprite(), int(-self.direction*180/math.pi-90)%360))
            self.rect = self.sprite.get_sprite().get_rect()

            #rotated_offset = self.offset.rotate_rad(self.direction)
            #self.rect = self.sprite.get_sprite().get_rect(center=self.position+rotated_offset)
    
    def shoot(self):
        bullet = Bullet(self.observer, self.direction, self.position)
        print("shooting")
    

    def blitRotate(self,image, pos, originPos, angle):

        # offset from pivot to center
        image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        
        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        # rotated image center
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        # # rotate and blit the image
        # surf.blit(rotated_image, rotated_image_rect)
    
        # # draw rectangle around the image
        # pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)
        return rotated_image, rotated_image_rect

    def display(self):
        #self.rotate()
        self.test_angle += 2
        self.sprite.update_sprite(img=pygame.transform.rotate(self.sprite.get_sprite(), int(self.test_angle)%360))

        img, rect = self.blitRotate(self.sprite.get_sprite(), self.position, (49,49), self.test_angle)
        print(rect)
        self.rect = self.sprite.get_sprite().get_rect()
        display.blit(img, rect)
        #self.sprite.display_sprite(self.position[0] + self.rect[0], self.position[1] + self.rect[1])
        display.blit(self.circle.image, (self.position[0]-49, self.position[1]-49))
        print(f"Player position: {self.position}")
        print(f"Rect center position: {self.rect.center}")
        print(f"Circle center position: {self.circle.image.get_rect().center}")
        print(f"Rect position: {self.rect}")
        print(f"Circle position: {self.circle.image.get_rect()}")

        
        
    
    def damage_taken(self):
        print(f"Damage taken, Lives {self.lives}")
        self.lives -= 1
        if self.lives == 0:
            self.observer.notify(Quit)
    
    



    # def updatedir(self, dir):
    #     super().updatedir(dir)
