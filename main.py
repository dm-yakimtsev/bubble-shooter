import pygame
from game_obj import *

pygame.init()


def main():
    background = Background()
    game = Game()
    display = pygame.display.set_mode((W, H))

    pygame.display.set_caption('Bubble Shooter')
    clock = pygame.time.Clock()

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        background.draw(display)
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
