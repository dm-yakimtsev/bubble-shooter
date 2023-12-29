from math import sqrt

import pygame
from constants import *
from bubble import Bubble, GridBubble
from random import choice

def bubble_pos(row, col, offset=0, cols=GRID_COLS):
    x = (col * ((W - RADIUS) / cols))

    # Сдвиг если строка нечетная

    if not (row % 2) == offset:
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
                bubble = GridBubble(row, col, pos, None)
                bubble.alive = True
                # Ложим каждый шарик в сетку
                self.grid[row][col] = bubble

        # Находим соседей для каждого шара
        for row in range(self.rows):
            for col in range(self.cols):
                self.find_neigbours(self.grid[row][col])

        # Находит все стоящие шары
        self.append_buttom_row()
        self.find_exist()
        # Метод нужен для создания нового шара в сетки при попадании пули
        self.collide = False
        self.hit_count = 0

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

    def find_neigbours(self, bubble, offset=0):
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

        if not ((row % 2) == offset):
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

    def find_hanging_balls(self, bubble, bubbles=None, hanging=False):
        if bubbles is None:
            bubbles = []
        # если мы дошли до конца значит шар не левитирует
        if bubble.row == 0:
            return True
        for neighbour in bubble.find_alive():
            if neighbour.alive and neighbour not in bubbles:
                bubbles.append(neighbour)

                hanging = self.find_hanging_balls(neighbour, bubbles)
                # Если мы нашли корень выходим останавливаем поиск.
                if hanging:
                    return True

        return hanging

    def check_colors(self, bubble, bubbles=None):
        # рекурсивно ищет все одноцветные шары стоящие рядом
        if bubbles is None:
            bubbles = []
        for neighbour in bubble.find_alive():
            if neighbour.alive:
                if (neighbour not in bubbles) and (neighbour.image == bubble.image):
                    bubbles.append(neighbour)
                    bubbles = self.check_colors(neighbour, bubbles)
        return bubbles

    def delete_bubbles(self, bubble):
        bubles = self.check_colors(bubble)
        if len(bubles) >= 3:
            self.hit_count += 1
            while len(bubles) > 0:
                bubble = bubles.pop()
                bubble.alive = False
                bubble.image = None
                # проверяем что после удаления все соседи не остались без пары, иначе удаляем соседов тоже
                for neighbour in bubble.find_alive():
                    if neighbour.alive and (neighbour not in bubles):
                        hanging = self.find_hanging_balls(neighbour)
                        if not hanging:
                            bubles.append(neighbour)

    def check_collision(self, bullet):
        bullet_x, bullet_y = bullet.pos
        # делает плавнее превращение пули в шарик
        bullet_x += 0.5 * bullet.dx
        bullet_y += 0.5 * bullet.dy
        size = (RADIUS * 2) - 5
        bullet_rect = pygame.Rect(bullet_x, bullet_y, size, size)
        for bubble in self.points:
            bubble_rect = pygame.Rect(bubble.pos[0], bubble.pos[1], size, size)

            if bubble_rect.colliderect(bullet_rect):
                bullet.ischarged = False
                self.collide = True

        if bullet_y - RADIUS < 0:
            bullet.ischarged = False
            self.collide = True

    def check_game_over(self, game):
        # проверяем есть ли в последнем возможном ряду шары
        if self.rows > 19:
            for col in range(self.cols):

                if self.grid[18][col].alive:
                    game.game_over = True

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

    def append_top_row(self):
        # Сдвигаем все шары на одну строчку

        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].row += 1
        self.rows += 1
        row = []
        for col in range(self.cols):
            bubble = GridBubble(0, col, (0, 0), image=None)
            bubble.alive = True
            row.append(bubble)
        # объединяем
        self.grid.insert(0, row)
        for row in range(self.rows):
            for col in range(self.cols):
                # cчитаем новые позиции и новых соседей для каждого шара
                self.grid[row][col].pos = bubble_pos(row, col)
                self.find_neigbours(self.grid[row][col])

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

    def del_buttom_row(self):
        self.grid.pop()
        self.rows -= 1
        for col in range(self.cols):
            self.find_neigbours(self.grid[self.rows - 1][col])

    def update_rows(self):

        if self.hit_count == UPDATE_ROW_COUNT:
            # Добавляем верхний ряд
            self.hit_count = 0
            self.append_top_row()

        for col in range(self.cols):
            # Добавляем нижний ряд если его еще нет
            if self.grid[self.rows - 1][col].alive:
                self.append_buttom_row()
                return

        # Удоляем нижний ряд если он над ним нет ни одного живого шара
        for col in range(self.cols):
            if self.grid[self.rows - 2][col].alive:
                return

        self.del_buttom_row()

    def update_state(self, display, gun, game):
        if gun.bullet_ball.ischarged:
            self.check_collision(gun.bullet_ball)

        if self.collide:
            new_bubble = self.make_bubble(gun.bullet_ball)
            self.update_rows()
            # После всех обновлений сетки нужно проверять цвета рядом стоящих шаров
            self.delete_bubbles(new_bubble)
            self.find_exist()
            self.collide = False
            self.check_game_over(game)

        self.draw(display)
