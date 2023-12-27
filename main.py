import pygame
from game_obj import *
from control import Grid
from gun import Gun

pygame.init()


def main():
    background = Background()
    game = Game()
    control = Grid()

    display = pygame.display.set_mode((W, H))

    pygame.display.set_caption('Bubble Shooter')
    gun = Gun(pos=(W // 2, H))
    clock = pygame.time.Clock()
    # изначальная позиция для поворота пушки
    pos = (W // 2, H // 2)

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                gun.shoot()

        background.draw(display)
        control.draw(display)
        # Поворачиваем пушку в связи с изменениями позиции
        gun.rotate(display, pos)
        gun.update(display)
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
