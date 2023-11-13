import pygame
from game_vars import *
import service_locator
from signals import *
class HUD():
    def __init__(self) -> None:
        self.score = 0
        self.lives = 3
        self.high_score = 0
        self.nukes = 3
        self.serv_loc = service_locator.ServiceLocator.create()
        self.observer = self.serv_loc.get_observer()
        self.observer.subscribe(UpdateScore, self)
        self.observer.subscribe(UpdateLives, self)
        self.observer.subscribe(UpdateHighScore, self)
        self.observer.subscribe(UpdateNukes, self)
        self.observer.subscribe(Display, self)
        self.scores=[]
        self.screen = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))


    def update_score(self, score):
        self.score += score
    
    def update_lives(self, lives):
        self.lives = lives

    def update_nukes(self, nukes):
        self.nukes = nukes
    
    def update_highScore(self, score):
        file = open("./scores.txt","r")
        
        line = file.readline()
        while(line):
            self.scores.append(int(line.split("-")[1].removesuffix("\n")))
            line=file.readline()
        print(self.scores)
        self.scores.append(score)
        self.scores.sort(reverse=True)
        self.scores.pop()
        print(self.scores)
        file.close()
        file = open("./scores.txt","w")
        file.write(f"1-{self.scores[0]}\n2-{self.scores[1]}\n3-{self.scores[2]}")      
        file.close()

    def display(self):
        font = pygame.font.SysFont("Comic Sans", 36)
        txtsurf = font.render(f'Score: {self.score}', True, "white")
        txtsurf2 = font.render(f'Lives: {self.lives}', True, "white")
        txtsurf3 = font.render(f'Nukes: {self.nukes}', True, "white")
        self.screen.blit(txtsurf,(0,0))
        self.screen.blit(txtsurf2,(0,25))
        self.screen.blit(txtsurf3,(0,50))
