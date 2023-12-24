import pygame
from constants import *


class Game:
    def __init__(self):
        self.game_over = False
        self.font = pygame.font.Font(None, 30)


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
