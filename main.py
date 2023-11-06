import pygame
import pygame_menu


pygame.font.init()
WIDTH, HEIGHT = 120, 90
SCALE = 10
display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))


def menu():
    menu = pygame_menu.Menu('Welcome', 1200, 900,
                        theme=pygame_menu.themes.THEME_GREEN)

    menu.add.button('Start Game', )
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(display)

pygame.init()



if __name__ == "__main__":
    menu()