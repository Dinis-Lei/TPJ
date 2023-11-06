from actor import Actor
from observer import Observer
from signal import Up, Down, Left, Right, Shoot, Update
from spriteloader import PlayerSprite

class Player(Actor):
    def __init__(self, observer: Observer) -> None:
        self.direction = (0,0)
        self.position = (40,20)
        self.velocity = 1
        self.lives = 3
        self.sprite = PlayerSprite(name="player1.png")
        self.observer = observer

        # Subscribe to events
        self.observer.subscribe(Up, self)
        self.observer.subscribe(Down, self)
        self.observer.subscribe(Left, self)
        self.observer.subscribe(Right, self)
        self.observer.subscribe(Shoot, self)
        self.observer.subscribe(Update, self)

    def up(self):
        self.direction[1] = -1

    def down(self):
        self.direction[1] = 1
    
    def left(self):
        self.direction[0] = -1

    def right(self):
        self.direction[0] = 1

    def move(self):
        self.position[0] = self.direction[0] * self.velocity
        self.position[1] = self.direction[1] * self.velocity

    def update_sprite(self):
        """ Update sprite """
        if self.lives == 2:
            self.sprite = self.sprite.update_sprite("player2.png")
        elif self.lives == 1:
            self.sprite = self.sprite.update_sprite("player1.png")
        else:
            self.sprite = self.sprite.update_sprite("player3.png")
    
    # def updatedir(self, dir):
    #     super().updatedir(dir)