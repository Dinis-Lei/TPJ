import pygame
from actor import Actor
from signals import *
from spriteloader import SpriteLoader
from collision import *
import math
from bullet import Bullet

AccelerateMAX = 15
BrakeMAX = -5
SHOOTING_COOLDOWN = 5

display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))

class Player(Actor):
    def __init__(self) -> None:
        super().__init__([400,200], SpriteLoader("player3.png"))
        self.direction = -math.pi/2
        self.pivot = [40,57]
        self.velocity = 0
        self.lives = 3
        self.offset = pygame.math.Vector2(30, 0)
        self.rect = self.sprite.get_sprite().get_rect()
        self.serv_loc = ServiceLocator.create()
        self.observer = self.serv_loc.get_observer()
        self.delete = False
        self.nuke_charges = 3
        self.nuke_cooldown = -10
        self.invulnerability = False
        self.invulnerability_cooldown = 0

        # Subscribe to events
        self.observer.subscribe(Accelerate, self)
        self.observer.subscribe(Brake, self)
        self.observer.subscribe(Shoot, self)
        self.observer.subscribe(Nuke, self)
        self.observer.subscribe(Display, self)
        self.observer.subscribe(Move, self)
        self.observer.subscribe(Update, self)
        self.observer.subscribe(CheckCollision, self)
        self.observer.subscribe(CatchPowerUp, self)

        # Collision Set up
        self.collision_box = CollisionCircle(self, center=self.rect.center, radius=50, id="player")
        self.collision_box.set_enter_func(self.damage_taken)
        self.center = (49, 49)

        self.prev_frame = -10

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
        self.observer.notify(PlayerPosition, pos=self.position.copy())

    def check_collision(self):
        self.collision_box.check_collision()

    def update(self):
        if self.invulnerability_cooldown < 0:
            self.invulnerability = False
        else:
            self.invulnerability_cooldown -= 1

        
        if self.delete:
            self.observer.unsubscribe(Display, self)
            self.observer.unsubscribe(Move, self)
            self.observer.unsubscribe(Update, self)
            self.collision_box = self.collision_box.delete()
            self.observer.notify(Quit)

    def shoot(self, frame=0):
        if frame - self.prev_frame > SHOOTING_COOLDOWN:
            self.prev_frame = frame
            x = self.position[0] + math.cos(self.direction) * 75
            y = self.position[1] + math.sin(self.direction) * 75
            Bullet(self.direction, [x,y], creator_id="player", velocity=20)    
            self.serv_loc.get_sound_manager().play("laser1", volume=1)

    def update_direction(self):
        x = pygame.mouse.get_pos()[0] - self.position[0]
        y = pygame.mouse.get_pos()[1] - self.position[1]

        new_direction = math.atan2(y,x)
        if abs(self.direction-new_direction) > 5*math.pi/180:
            self.direction = new_direction

    def display(self):
        self.update_direction()
        img, rect = self.rotate()
        display.blit(img, rect)      
    
    def damage_taken(self, collider=None):
        if self.invulnerability or collider == "player_bullet" or  collider == "powerup":
            return
        self.invulnerability = True
        self.invulnerability_cooldown = 5
        self.lives -= 1
        self.observer.notify(UpdateLives, lives = self.lives)
        if self.lives == 0:
            self.delete = True

    def nuke(self, frame):
    
        if self.nuke_charges > 0 and frame > self.nuke_cooldown+10:
            self.nuke_cooldown = frame
            self.nuke_charges -= 1
            self.observer.notify(DestroyAll)
            self.observer.notify(UpdateNukes, nukes=self.nuke_charges)

    def power_up(self, type):
        if type == "nuke":
            self.nuke_charges += 1 if self.nuke_charges < 3 else 0
            self.observer.notify(UpdateNukes, nukes=self.nuke_charges)
        elif type == "life":
            self.lives += 1
            print(f"Add life {self.lives}")
            self.observer.notify(UpdateLives, lives = self.lives)