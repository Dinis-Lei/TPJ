import pygame
import pygame_menu
from input_handler import InputHandler
from observer import Observer
from signals import *
from player import Player
from game_vars import SCALE, WIDTH, HEIGHT
from asteroids import Asteroid


class MainLoop():

    def __init__(self) -> None:
        pygame.font.init()
        self.display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))

        self.input_handler = InputHandler()
        self.obs = Observer()
        self.clock = pygame.time.Clock()
        self.running = True

        self.obs.subscribe(Quit, self)

    def quit(self):
        self.running = False

    def run(self):
        print("Starting game")

        player = Player(self.obs)
        asteroid = Asteroid.factory(self.obs)
        

        while self.running:
            self.display.fill("white")
            commands = self.input_handler.handle_input()
            for command in commands:
                self.obs.notify(command)

            self.obs.notify(Move)
            self.obs.notify(Display) # Update all sprites
            # update window
            pygame.display.flip()
            self.clock.tick(15)


    def menu(self):
        menu = pygame_menu.Menu('Welcome', 1200, 900,
                            theme=pygame_menu.themes.THEME_GREEN)

        menu.add.button('Start Game', self.run)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(self.display)

pygame.init()



if __name__ == "__main__":
    main = MainLoop()
    main.menu()
    pygame.quit()