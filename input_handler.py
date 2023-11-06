import pygame
from signals import *

class InputHandler():

    command = {
<<<<<<< HEAD
        pygame.K_UP: Accelerate,
        pygame.K_DOWN: Brake,
=======
        pygame.K_LEFT: Left,
        pygame.K_RIGHT: Right,
        pygame.K_UP: Up,
        pygame.K_DOWN: Down,
>>>>>>> d10fb68e701e7e220295d0bcb2d07aa5d0db7e6e
        pygame.K_q: Quit,
        # pygame.K_ESCAPE: Pause,
        pygame.K_SPACE: Shoot,
    }

    def handle_input(self):
        command = [Nothing]

        for key in self.command:
            if pygame.key.get_pressed()[key]:
                command.append(self.command[key])
                

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                command.append(Quit)
                break

        return command