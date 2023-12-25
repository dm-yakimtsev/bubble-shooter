from constants import *
import random
import pygame


class Bubble:
    def __init__(self, row, col, pos, image=None):
        self.pos = pos
        self.radius = RADIUS
        self.row = row
        self.col = col
        if image is not None:
            self.image = image
        else:
            self.image = random.choice(BUBLE_IMAGES)
        self.surface = self.get_image()

    def get_image(self):
        surface = pygame.image.load(self.image)
        surface = pygame.transform.scale(surface, (RADIUS * 2, RADIUS * 2))
        return surface

    def draw(self, display):
        if self.image is None:
            return

        x, y = int(self.pos[0]), int(self.pos[1])
        display.blit(self.surface, (x, y))
