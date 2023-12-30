import math

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
        self.surface = self.get_image()

    def get_image(self):
        surface = pygame.image.load(self.image)
        surface = pygame.transform.scale(surface, (RADIUS * 2, RADIUS * 2))
        return surface

    def draw(self, display):
        if self.image is None:
            return

        x, y = self.pos[0], self.pos[1]
        display.blit(self.surface, (x, y))


class BubbleBullet(Bubble):
    def __init__(self, pos, angle, image=None):
        super().__init__(pos, image=None)

        self.pos = pos
        if image is not None:
            self.image = image
        else:
            self.image = random.choice(BUBLE_IMAGES)
        self.surface = self.get_image()

        self.surface = self.get_image()
        self.dx = math.cos(angle) * 20
        # Чтобы шарик летел вверх нужно вычитать из y, потому что ось направлена вниз
        self.dy = -math.sin(angle) * 20

        # метод отвечает за то в пушке снаряд или нет
        self.ischarged = True

    def update(self, display):
        if self.ischarged:
            x, y = self.pos

            if (x - RADIUS) <= 0:
                self.dx *= -1
            elif (x + RADIUS) >= W - RADIUS:
                self.dx *= -1

            self.pos = (x + self.dx, y + self.dy)

            self.draw(display)


class GridBubble(Bubble):
    def __init__(self, row, col, pos, image=None):
        super().__init__(pos, image)
        self.row = row
        self.col = col
        self.alive = True
        self.l = None
        self.r = None
        self.ul = None
        self.ur = None
        self.dl = None
        self.dr = None

    def find_alive(self):
        neighbours = [self.l, self.r, self.ul, self.ur, self.dr, self.dl]
        alive = []

        for neighbour in neighbours:
            if neighbour:
                alive.append(neighbour)

        return alive
