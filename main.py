import pygame
from game_obj import *
from control import Grid
from gun import Gun

pygame.init()


def main():
    # Cчетчик итераций
    iteration = 0
    background = Background()
    game = Game()
    control = Grid()

    display = pygame.display.set_mode((W, H))
    pygame.mixer.music.load(r"data/b703eddf4554b45.mp3")
    pygame.mixer.music.play(-1)
    pygame.display.set_caption(r'Bubble Shooter')
    gun = Gun(pos=(W // 2, H))
    clock = pygame.time.Clock()
    # изначальная позиция для поворота пушки
    pos = (W // 2, H // 2)

    while True:
        iteration += 1
        # Если мы проиграли рисуем меню окончания
        if game.game_over:
            background.draw(display)
            game.game_over_menu(display)
        else:

            # Если игра еще не начиналась рисуем стартовое меню
            if not game.game_running:
                background.draw(display)
                game.start_menu(display)
            else:
                # Если была нажата кнопка start обновляем сетку
                if game.new_game:
                    game.new_game = False
                    control = Grid()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEMOTION:
                        pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gun.shoot()

                background.draw(display)

                # Отображаем рекорд внизу
                game.score_text = game.font.render(f"SCORE - {game.score}", True, (255, 255, 255))
                game.scrore_rect = pygame.Rect(20, H - 20, 150, 30)
                display.blit(game.score_text, game.scrore_rect)

                # Обновляем сетку
                control.update_state(display, gun, game, iteration)
                # Поворачиваем пушку в связи с изменениями позиции
                gun.rotate(display, pos)
                gun.update(display)
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
