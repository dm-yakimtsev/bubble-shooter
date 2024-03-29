import pygame
from constants import *
import sys

class Game:
    def __init__(self):
        self.game_over = False
        self.game_running = False
        self.score = 0
        self.new_game = False
        self.font = pygame.font.Font(None, 30)  # Для кнопок
        self.font2 = pygame.font.Font(None, 52)  # Для надписей
        self.start_text = self.font.render("START!", True, (255, 255, 255))
        self.exit_text = self.font.render("EXIT", True, (255, 255, 255))
        self.game_over_text = self.font2.render("GAME OVER!", True, (255, 255, 255))
        self.score_text = self.font2.render(f"{self.score}", True, (255, 255, 255))
        self.scrore_rect = pygame.Rect(W // 2 - 120, H // 2 - 120, 200, 30)
        self.start_rect = pygame.Rect(W // 2 - 35, H // 2 - 20, 80, 30)
        self.exit_rect = pygame.Rect(W // 2 - 25, H // 2 + 20, 80, 30)
        self.game_over_rect = pygame.Rect(W // 2 - 110, H // 2 - 190, 150, 30)

    def start_menu(self, display):

        if not self.game_running:
            display.blit(self.start_text, self.start_rect)
            display.blit(self.exit_text, self.exit_rect)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_rect.collidepoint(event.pos):
                        self.game_running = True
                    if self.exit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Рисует задний фон в тексте при наведении мыши
                if event.type == pygame.MOUSEMOTION:
                    if self.start_rect.collidepoint(event.pos):
                        self.start_text = self.font.render("START!", True, (255, 255, 255),
                                                           (100, 100, 100))
                    else:
                        self.start_text = self.font.render("START!", True, (255, 255, 255))
                    if self.exit_rect.collidepoint(event.pos):
                        self.exit_text = self.font.render("EXIT", True, (255, 255, 255),
                                                          (100, 100, 100))
                    else:
                        self.exit_text = self.font.render("EXIT", True, (255, 255, 255))

    def game_over_menu(self, display):
        if self.game_over:
            self.game_running = False
            # Делаем счетчик очков больше и размещаем в центре
            self.score_text = self.font2.render(f"SCORE - {self.score}", True, (255, 255, 255))
            self.scrore_rect = pygame.Rect(W // 2 - 100, H // 2 - 120, 150, 30)
            display.blit(self.score_text, self.scrore_rect)
            display.blit(self.game_over_text, self.game_over_rect)
            display.blit(self.start_text, self.start_rect)
            display.blit(self.exit_text, self.exit_rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_rect.collidepoint(event.pos):
                        self.game_running = True
                        self.game_over = False
                        self.new_game = True
                    if self.exit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    if self.start_rect.collidepoint(event.pos):
                        self.start_text = self.font.render("START!", True, (255, 255, 255),
                                                           (100, 100, 100))
                    else:
                        self.start_text = self.font.render("START!", True, (255, 255, 255))
                    if self.exit_rect.collidepoint(event.pos):
                        self.exit_text = self.font.render("EXIT", True, (255, 255, 255),
                                                          (100, 100, 100))
                    else:
                        self.exit_text = self.font.render("EXIT", True, (255, 255, 255))


class Background:
    def __init__(self):
        self.image = self.get_image()

    def get_image(self):
        bg = pygame.image.load(r'data/bg.jpg')
        x, y, w, h = bg.get_rect()
        bg = pygame.transform.scale(bg, (int(W), int(H)))
        return bg

    def draw(self, display):
        display.blit(self.image, (0, 0))
