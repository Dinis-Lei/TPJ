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
        self.lives = 100
        self.offset = pygame.math.Vector2(30, 0)
        self.rect = self.sprite.get_sprite().get_rect()
        self.observer = observer
        self.delete = False

        # Subscribe to events
        self.observer.subscribe(Accelerate, self)
        self.observer.subscribe(Brake, self)
        self.observer.subscribe(Shoot, self)
        self.observer.subscribe(Display, self)
        self.observer.subscribe(Move, self)
        self.observer.subscribe(Update, self)
        self.observer.subscribe(CheckCollision, self)

        self.collision_box = CollisionCircle(self, self.observer, center=self.rect.center, radius=50)
        self.collision_box.set_enter_func(self.damage_taken)

        # # draw circle
        # self.circle = pygame.sprite.Sprite()
        # self.circle.image  = pygame.Surface((99, 99), pygame.SRCALPHA)
        # pygame.draw.circle(self.circle.image, (255, 255, 0, 128), self.rect.center, 50)
        
        self.test_angle = 0
        self.center = (49, 49)

    def accelerate(self):
        self.velocity += 1 if self.velocity < AccelerateMAX else 0

    def brake(self):
        self.velocity -= 1 if self.velocity > BrakeMAX else 0

    def change_angle(self, angle):
        self.direction = angle

    def move(self):
        self.position[0] += math.cos(self.direction) * self.velocity
        self.position[1] += math.sin(self.direction) * self.velocity

        self.collision_box.move()

    def check_collision(self):
        self.collision_box.check_collision()

    def update(self):
        """ Update sprite """
        if self.lives == 2:
            self.sprite.update_sprite(name="player2.png")
        elif self.lives == 1:
            self.sprite.update_sprite(name="player1.png")
        else:
            self.sprite.update_sprite(name="player3.png")

        if self.delete:
            self.observer.unsubscribe(Display, self)
            self.observer.unsubscribe(Move, self)
            self.observer.unsubscribe(Update, self)
            self.collision_box = self.collision_box.delete()
            self.observer.notify(Quit)

    def shoot(self):
        bullet = Bullet(self.observer, self.direction, self.position)
        print("shooting")
    

    def rotate(self):
        image = self.sprite.get_sprite()

        x = pygame.mouse.get_pos()[0] - self.position[0]
        y = pygame.mouse.get_pos()[1] - self.position[1]

        new_direction = math.atan2(y,x)
        if abs(self.direction-new_direction) > 5*math.pi/180:
            self.direction = new_direction

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

    def display(self):
        #self.rotate()
        self.test_angle += 2
        #self.sprite.update_sprite(img=pygame.transform.rotate(self.sprite.get_sprite(), int(self.test_angle)%360))

        img, rect = self.rotate()#blitRotate(self.sprite.get_sprite(), self.position, (49,49), self.test_angle)
        self.rect = self.sprite.get_sprite().get_rect()
        display.blit(img, rect)
        #self.sprite.display_sprite(self.position[0] + self.rect[0], self.position[1] + self.rect[1])
        # display.blit(self.circle.image, (self.position[0]-49, self.position[1]-49))


        
        
    
    def damage_taken(self):
        print(f"Damage taken, Lives {self.lives}")
        self.lives -= 1
        if self.lives == 0:
            self.delete = True
    
    



    # def updatedir(self, dir):
    #     super().updatedir(dir)
