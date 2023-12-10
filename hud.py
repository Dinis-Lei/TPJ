import pygame
from game_vars import *
import service_locator
from signals import *
class HUD():
    def __init__(self) -> None:
        """ intitiate hud class, that gives visual representation during game """
        self.score = 0
        self.lives = 3
        self.high_score = 0
        self.nukes = 0
        self.serv_loc = service_locator.ServiceLocator.create()
        self.observer = self.serv_loc.get_observer()
        self.observer.subscribe(UpdateScore, self)
        self.observer.subscribe(UpdateLives, self)
        self.observer.subscribe(UpdateHighScore, self)
        self.observer.subscribe(UpdateNukes, self)
        self.observer.subscribe(Display, self)
        self.observer.subscribe(Start, self)
        self.scores=[]
        self.screen = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))

    def start(self):
        """ start game variables """
        self.score = 0
        self.lives = 3
        self.nukes = 0
        self.scores = []

    def update_score(self, score):
        """ update score """
        self.score += score
    
    def update_lives(self, lives):
        """ Update player's lives """
        self.lives = lives

    def update_nukes(self, nukes):
        """ Update nuke count """
        self.nukes = nukes
    
    def update_highScore(self, score):
        """ Update highscore. Reads Highscores from a file and updates them if needed, with the current score.
            If the current score is bigger than any of the scores in the previous top3, the highscores file is
            updated 
        """
        file = open("./scores.txt","r")
        
        line = file.readline()
        while(line):
            self.scores.append(int(line.split("-")[1].removesuffix("\n")))
            line=file.readline()
        self.scores.append(score)
        self.scores.sort(reverse=True)
        self.scores.pop()
        file.close()
        file = open("./scores.txt","w")
        file.write(f"1-{self.scores[0]}\n2-{self.scores[1]}\n3-{self.scores[2]}")      
        file.close()

    def display(self):
        """ dsplays visual information to player about score, lives and nukes """
        font = pygame.font.SysFont("Comic Sans", 36)
        txtsurf = font.render(f'Score: {self.score}', True, "white")
        txtsurf2 = font.render(f'Lives: {self.lives}', True, "white")
        txtsurf3 = font.render(f'Nukes: {self.nukes}', True, "white")
        self.screen.blit(txtsurf,(0,0))
        self.screen.blit(txtsurf2,(0,25))
        self.screen.blit(txtsurf3,(0,50))
