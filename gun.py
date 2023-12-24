import pygame
from constants import *


class Gun:
    def __init__(self, pos):
        self.pos = pos
        self.gun = pygame.image.load('data/пушка.png').convert_alpha()
        self.gun_rect = self.gun.get_rect()

        self.gun_w = self.gun_rect[2]
        self.gun_h = self.gun_rect[3]

        self.gun = pygame.transform.scale(self.gun, (100, 150))

    def draw(self, display):
        display.blit(self.gun, self.pos)
