from actor import Actor
from observer import Observer

class Enemy(Actor):
    def __init__(self, observer: Observer) -> None:
        self.direction = (0,0)
        self.position = (0,0)
        self.velocity = 0
        self.sprite
        self.fire_interval
        self.observer = observer


    def move(self):
        """ Enemy movement pattern """

    def update(self):
        """ Update sprite """
        pass