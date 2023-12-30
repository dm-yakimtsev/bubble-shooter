import pygame
from constants import *


class Game:
    def __init__(self):
        self.game_over = False
        self.game_running = False
        self.font = pygame.font.Font(None, 30)
        self.start_text = self.font.render("START!", True, (255, 255, 255))
        self.start_rect = pygame.Rect(W // 2 - 25, H // 2 - 50, 80, 30)

    def start_menu(self, display):
        if not self.game_running:
            display.blit(self.start_text, self.start_rect)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_rect.collidepoint(event.pos):
                        self.game_running = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    if self.start_rect.collidepoint(event.pos):
                        self.start_text = self.font.render("START!", True, (255, 255, 255), (100, 100, 100))
                    else:
                        self.start_text = self.font.render("START!", True, (255, 255, 255))


class Background:
    def __init__(self):
        self.image = self.get_image()

    def get_image(self):
        bg = pygame.image.load('data/bg.jpg')
        x, y, w, h = bg.get_rect()
        bg = pygame.transform.scale(bg, (int(w * 0.18), int(h * 0.18)))
        return bg

    def draw(self, display):
        display.blit(self.image, (0, 0))
