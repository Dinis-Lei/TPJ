import random
from actor import Actor
from collision import CollisionCircle
from game_vars import *
from service_locator import ServiceLocator
from signals import *
from spriteloader import SpriteLoader

powerup_counter = 0
POWERUP_MAX = 5

class PowerUp(Actor):

    def __init__(self, position, type) -> None:
        super().__init__(position, None)
        self.delete = False
        self.type = type

        self.serv_loc = ServiceLocator.create()
        self.observer = self.serv_loc.get_observer()

        self.observer.subscribe(Display, self)
        self.observer.subscribe(Update, self)
        self.observer.subscribe(CheckCollision, self)
        self.observer.subscribe(Quit, self)

        self.collision_box = CollisionCircle(self, center=(20, 20), radius=20, offset=[-15,-15], id="powerup")
        self.collision_box.set_enter_func(self.hit_object)

        self.sprite = SpriteLoader("powerupBlue_shield.png" if self.type == "life" else "powerupBlue_bolt.png")

    def check_collision(self):
        self.collision_box.check_collision()

    def update(self):
        if self.delete:
            global powerup_counter
            powerup_counter -= 1
            self.observer.unsubscribe(Display, self)
            self.observer.unsubscribe(Update, self)
            self.observer.unsubscribe(CheckCollision, self)
            self.collision_box = self.collision_box.delete()

    def quit(self):
        self.delete = True
        # if self.collision_box != None:
        #     self.collision_box = self.collision_box.delete()
        #     self.observer.unsubscribe(Display, self)
        #     self.observer.unsubscribe(Update, self)
        #     self.observer.unsubscribe(CheckCollision, self)
        #     self.delete = False
        # self.observer.unsubscribe(DestroyAll, self)
        # self.observer.unsubscribe(Quit, self)
        
    def hit_object(self, collider=None):
        if self.delete:
            return
        
        if collider == "player" or collider == "player_bullet":
            self.observer.notify(CatchPowerUp, type=self.type)
            self.delete = True
        elif "bullet" in str(collider):
            self.delete = True
        elif collider == "powerup":     # Respawn powerups if they collide with each other
            x = random.randint(200, WIDTH*SCALE - 200)
            y = random.randint(200, HEIGHT*SCALE - 200)
            self.position = [x, y]
            self.collision_box.move()
    @classmethod
    def create(cls):
        global powerup_counter

        if powerup_counter >= POWERUP_MAX:
            return None

        powerup_counter += 1
        x = random.randint(200, WIDTH*SCALE - 200)
        y = random.randint(200, HEIGHT*SCALE - 200)

        type = random.choice(["nuke", "life"])
        print(type)
        return PowerUp([x, y], type)

