import pygame as pg

from game.settings import WIN_WIDTH, WIN_HEIGHT
from game.groups import text_boxes_group


class Camera:
    def __init__(self, total_width, total_height):
        self.rect = pg.Rect(0, 0, total_width, total_height)

    def apply(self, target):
        return target.rect.move(self.rect.topleft)

    def update(self, target):
        x, y = target.rect.centerx, target.rect.centery
        w, h = self.rect.width, self.rect.height
        x, y = WIN_WIDTH // 2 - x, WIN_HEIGHT // 2 - y

        x = min(0, x)  # Не движемся дальше левой границы
        x = max(-(w - WIN_WIDTH), x)  # Не движемся дальше правой границы
        y = max(-(h - WIN_HEIGHT), y)  # Не движемся дальше нижней границы
        y = min(0, y)  # Не движемся дальше верхней границы

        for elem in text_boxes_group:
            elem.rect.x = elem.pos[0] - x
            elem.rect.y = elem.pos[1] - y

        self.rect = pg.Rect(x, y, w, h)