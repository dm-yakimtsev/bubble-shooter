from constants import *
import random
import pygame


class Bubble:
    def __init__(self, pos, image=None):
        self.pos = pos
        self.radius = RADIUS
        if image is not None:
            self.image = image
        else:
            self.image = random.choice(BUBLE_IMAGES)

    def draw(self, display):
        if self.image is None:
            return

        x, y = self.pos[0], self.pos[1]
        surface = pygame.image.load(self.image).convert()
        x, y, w, h = surface.get_rect()
        surface = pygame.transform.scale(surface, (int(w * 0.1), int(h * 0.1)))
        display.blit(surface, (x, y))


