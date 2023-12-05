import pygame
from signals import *

class InputHandler():

    command = {
        pygame.K_UP: Accelerate,
        pygame.K_w: Accelerate,
        pygame.K_DOWN: Brake,
        pygame.K_s: Brake,
        pygame.K_q: Quit,
        # pygame.K_ESCAPE: Pause,
        pygame.K_SPACE: Shoot,
        pygame.K_e: Nuke,
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