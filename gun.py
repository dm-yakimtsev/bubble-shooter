import pygame
from constants import *
from math import atan2, degrees


class Gun:
    def __init__(self, pos):
        self.pos = pos
        self.gun = pygame.image.load('data/пушка.png').convert_alpha()
        self.gun = pygame.transform.scale(self.gun, (100, 150))
        self.gun_rect = self.gun.get_rect()

        self.gun_w = self.gun_rect[2]
        self.gun_h = self.gun_rect[3]

        # Создаем поверхность в которую мы будем поворачивать
        self.roteted_field = pygame.Surface((self.gun_w, self.gun_h * 2), pygame.SRCALPHA, 32)
        self.roteted_field.fill((0, 0, 0, 0))
        # Отображаем на ней пушку
        self.roteted_field.blit(self.gun, (0, 0))

        # Поворачиваем область вправо, потому что изначально она лежит перпендикулярно полу
        self.roteted_field = pygame.transform.rotate(self.roteted_field, -90)

    def rotate(self, display, pos):
        angle = self.calc_angle(pos)
        # Поворачиваем область поотому что если поворачивать изображение оно не будет стоять в одной точке
        image = pygame.transform.rotate(self.roteted_field, angle)
        cords = image.get_rect(center=self.pos)
        display.blit(image, cords)

    def calc_angle(self, pos):
        # Cчитаем катеты
        cat_1 = pos[0] - self.pos[0]
        cat_2 = self.pos[1] - pos[1]

        # Считаем угл через арктангенс
        angle = atan2(cat_2, cat_1)
        # Переводим из радиан в градусы
        degre = degrees(angle)

        # делаем угл от 15 до 170
        degre = max(degre, 15)
        degre = min(degre, 170)

        return degre
