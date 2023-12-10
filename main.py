import pygame
from pygame import image
import pygame_menu
from hud import HUD
from input_handler import InputHandler
from observer import Observer
from spawner_manager import SpawnerManager
from service_locator import ServiceLocator
from signals import *
from player import Player
from game_vars import SCALE, WIDTH, HEIGHT

class MainLoop():

    def __init__(self) -> None:
        """ Initializing the main loop """
        self.input_handler = InputHandler()
        self.serv_loc = ServiceLocator.create()
        self.obs = self.serv_loc.get_observer()
        self.sound_manager = self.serv_loc.get_sound_manager()
        self.hud = HUD()
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True

        self.obs.subscribe(Quit, self)


    def quit(self):
        """ when game ends """
        self.running = False

    def run(self):
        """ game logic """
        frame = 0
        player = Player()
        spawner = SpawnerManager()
        self.running = True
        background = image.load(f"./usedAssets/blue.png")
        background = pygame.transform.scale(background,(WIDTH*SCALE,HEIGHT*SCALE))
        self.obs.notify(Start)
        while self.running:
            
            self.display.blit(background, (0,0))
            commands = self.input_handler.handle_input()
            for command in commands:
                self.obs.notify(command, frame=frame)
            
            """ Visual and logic updates to objects.
                Doing checkings for collision
                Spawning more enitities
            """
            self.obs.notify(Move)
            self.obs.notify(CheckCollision)
            self.obs.notify(EnemyShoot)
            self.obs.notify(Update)
            self.obs.notify(Display) # Update all sprites
            self.obs.notify(Spawn, frame=frame)
            """ update window """
            pygame.display.flip()
            self.clock.tick(20)
            frame += 1

        self.obs.notify(UpdateHighScore, score = self.hud.score)
        """ calling end screen """
        self.endScreen()


    def menu(self):
        """ Main menu, presented at the beginning of the game """
        menu = pygame_menu.Menu('Welcome', 1200, 900,
                            theme=pygame_menu.themes.THEME_GREEN)

        if self.running:
            menu.add.button('Start Game', self.run)
        menu.add.button('How To Play', self.options)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(self.display)

    def endScreen(self):
        """ Endscreen, presenting the score of the ended run, highscores and possibility to play again or quit """
        menu = pygame_menu.Menu('Game Over', 1200, 900,
                            theme=pygame_menu.themes.THEME_BLUE)
        menu.add.label(f"Your score was: {self.hud.score}")
        menu.add.label(f"Highscores:\n1 - {self.hud.scores[0]}\n2 - {self.hud.scores[1]}\n3 - {self.hud.scores[2]}")
        menu.add.button('Restart Game', self.run)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        
        menu.mainloop(self.display)
    
    def options(self):
        """ Controls screen. Showing the controls and the objective of the game """
        menu = pygame_menu.Menu('Controls', 1200, 900,
                            theme=pygame_menu.themes.THEME_GREEN)
        menu.add.label(f"W: Accelerate\nS: Brake\nE: Use Nuke\nMouse: Rotate Ship\nSpace: Shoot\nTry to kill as many enemy ships as possible to score points.\nYou have 3 initial lifes and you can pick up more with the power up shield.\nYou can  have 3 nukes maximum at a time.\nAfter being hit you have invulnerability for some seconds, be careful!")
        menu.add.button('Back', self.menu)
        
        menu.mainloop(self.display)




if __name__ == "__main__":
    main = MainLoop()
    main.menu()
    pygame.quit()