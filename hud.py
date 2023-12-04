import pygame
from game_vars import *
import service_locator
from signals import UpdateScore, UpdateHighScore, UpdateLives, Display
class HUD():
    def __init__(self) -> None:
        self.score = 0
        self.lives = 3
        self.high_score = 0
        self.serv_loc = service_locator.ServiceLocator.create()
        self.observer = self.serv_loc.get_observer()
        self.observer.subscribe(UpdateScore, self)
        self.observer.subscribe(UpdateLives, self)
        self.observer.subscribe(UpdateHighScore, self)
        self.observer.subscribe(Display, self)
        self.screen = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))


    def update_score(self, score):
        self.score += score
    
    def update_lives(self, lives):
        self.lives = lives
    
    def update_highScore(self, score):
        if score > self.high_score:
            self.high_score = score

    def display(self):
        font = pygame.font.SysFont("Comic Sans", 36)
        txtsurf = font.render(f'Score: {self.score}', True, "white")
        txtsurf2 = font.render(f'Lives: {self.lives}', True, "white")
        self.screen.blit(txtsurf,(0,0))
        self.screen.blit(txtsurf2,(0,25))

