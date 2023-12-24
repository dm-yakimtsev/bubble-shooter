import pygame
from constants import *
from bubble import Bubble
from random import choice


def bubble_pos(row, col):
    x = (col * ((W - RADIUS) / GRID_COLS))

    # Сдвиг если строка нечетная

    if not (row % 2) == 0:
        x += RADIUS

    y = RADIUS + (row * RADIUS * 2)

    return x, y


class Grid:
    def __init__(self):
        self.rows = GRID_ROWS
        self.cols = GRID_COLS

        self.grid = [[0 for col in range(self.cols)] for row in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                pos = bubble_pos(row, col)

                # Ложим каждый шарик в сетку
                self.grid[row][col] = Bubble(row, col, pos, None)

    def draw(self, display):
        # Отрисовка каждого шарика в сетке
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].draw(display)
