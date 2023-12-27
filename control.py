from math import sqrt

import pygame
from constants import *
from bubble import Bubble, GridBubble
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
        self.points = []
        for row in range(self.rows):
            for col in range(self.cols):
                pos = bubble_pos(row, col)

                # Ложим каждый шарик в сетку
                self.grid[row][col] = GridBubble(row, col, pos, None)

        # Находим соседей для каждого шара
        for row in range(self.rows):
            for col in range(self.cols):
                self.find_neigbours(self.grid[row][col])

        # Находит все стоящие шары
        self.append_buttom_row()
        self.find_exist()
        # Метод нужен для создания нового шара в сетки при попадании пули
        self.collide = False

    def find_exist(self):
        self.points = []

        # Ищем все существующие шары для проверки на столкновение
        for row in range(self.rows):
            for col in range(self.cols):
                bubble = self.grid[row][col]

                if not bubble.alive:
                    for neighbour in bubble.find_alive():
                        if (neighbour not in self.points) and neighbour.alive:
                            self.points.append(neighbour)


    def find_neigbours(self, bubble):
        bubble.l = None
        bubble.r = None
        bubble.ul = None
        bubble.ur = None
        bubble.dr = None
        bubble.dl = None

        row = bubble.row
        col = bubble.col

        if col > 0:
            bubble.l = self.grid[row][col - 1]
        if col < (self.cols - 1):
            bubble.r = self.grid[row][col + 1]

        if not ((row % 2) == 0):
            if row > 0:
                bubble.ul = self.grid[row - 1][col]

                if col < (self.cols - 1):
                    bubble.ur = self.grid[row - 1][col + 1]

            if row < (self.rows - 1):
                bubble.dl = self.grid[row + 1][col]

                if col < (self.cols - 1):
                    bubble.dr = self.grid[row + 1][col + 1]

        else:
            if row > 0:
                bubble.ur = self.grid[row - 1][col]

                if col > 0:
                    bubble.ul = self.grid[row - 1][col - 1]

            if row < (self.rows - 1):
                bubble.dr = self.grid[row + 1][col]

                if col > 0:
                    bubble.dl = self.grid[row + 1][col - 1]

    def check_collision(self, bullet):
        bullet_x, bullet_y = bullet.pos
        # делает плавнее превращение пули в шарик
        bullet_x += 0.5 * bullet.dx
        bullet_y += 0.5 * bullet.dy

        for bubble in self.points:
            bubble_rect = pygame.Rect(bubble.pos[0], bubble.pos[1], RADIUS, RADIUS)

            if bubble_rect.collidepoint(bullet_x, bullet_y):
                bullet.ischarged = False
                self.collide = True

        if bullet_y - RADIUS < 0:
            bullet.ischarged = False
            self.collide = True

    def make_bubble(self, bullet):
        collide_point = bullet.pos
        empty = []
        dists = []

        # Помещаем все пустые шары на которые может встать пуля
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.grid[row][col].alive:
                    empty.append(self.grid[row][col])

        # считаем ближайшую дистанцию от пули до пустого места
        for bubble in empty:
            x, y = collide_point
            bubble_x, bubble_y = bubble.pos

            dist = sqrt((((x - bubble_x) ** 2) + (y - bubble_y) ** 2))
            dists.append(dist)

        # Даем пустому шарику картинку пули
        idx = dists.index(min(dists))
        replacement = empty[idx]

        replacement.image = bullet.image
        replacement.surface = bullet.surface
        # Делаем из пустого места шарик
        replacement.alive = True

        return replacement

    def draw(self, display):
        # Отрисовка каждого шарика в сетке
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].draw(display)

    def append_buttom_row(self):
        """Добавляем пустые шары на места которых будут становиться пули"""
        row = []
        for col in range(self.cols):
            pos = bubble_pos(self.rows, col)
            bubble = GridBubble(self.rows, col, pos, image=None)
            bubble.alive = False
            bubble.image = None
            row.append(bubble)

        self.grid.append(row)
        self.rows += 1
        # ищем соседей для новых двух строчек
        for row in range(self.rows - 2, self.rows):
            for col in range(self.cols):
                self.find_neigbours(self.grid[row][col])

    def update_state(self, display, gun):
        if gun.bullet_ball.ischarged:
            self.check_collision(gun.bullet_ball)

        if self.collide:
            self.make_bubble(gun.bullet_ball)
            self.append_buttom_row()
            self.find_exist()
            self.collide = False
        self.draw(display)
