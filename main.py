import pygame
from pygame import image
import pygame_menu
from hud import HUD
from input_handler import InputHandler
from observer import Observer
from spriteloader import SpriteLoader
from service_locator import ServiceLocator
from signals import *
from player import Player
from game_vars import SCALE, WIDTH, HEIGHT
from asteroids import Asteroid
from enemy import Enemy
from soundManager import SoundManager


class MainLoop():

    def __init__(self) -> None:
        self.input_handler = InputHandler()
        self.serv_loc = ServiceLocator.create()
        self.obs = self.serv_loc.get_observer()
        self.sound_manager = self.serv_loc.get_sound_manager()
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True

        self.obs.subscribe(Quit, self)

    def quit(self):
        self.running = False

    def run(self):
        HUD()
        print("Starting game")
        frame = 0
        player = Player()
        self.running = True
        background = image.load(f"./usedAssets/blue.png")
        background = pygame.transform.scale(background,(WIDTH*SCALE,HEIGHT*SCALE))

        while self.running:
            self.display.blit(background, (0,0))
            commands = self.input_handler.handle_input()
            for command in commands:
                self.obs.notify(command, frame=frame)
            #print(f"Frame: {frame}")
            self.obs.notify(Move)
            self.obs.notify(CheckCollision)
            self.obs.notify(Update)
            self.obs.notify(Display) # Update all sprites
            # update window
            pygame.display.flip()
            self.clock.tick(15)

            if (frame % 30) == 0:
                Asteroid.factory()
                Enemy.factory(player)

            frame += 1


    def menu(self):
        menu = pygame_menu.Menu('Welcome', 1200, 900,
                            theme=pygame_menu.themes.THEME_GREEN)

        menu.add.button('Start Game', self.run)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(self.display)




if __name__ == "__main__":
    main = MainLoop()
    main.menu()
    pygame.quit()