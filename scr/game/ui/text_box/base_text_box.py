import pygame as pg

from game.groups import text_boxes_group
from game.settings import WIN_WIDTH, TILE_WIDTH, TILE_HEIGHT, WIN_HEIGHT


class BaseTextBox(pg.sprite.Sprite):
    def __init__(self):
        super().__init__(text_boxes_group)
        self.text = ''
        self.size = (WIN_WIDTH - 4 * TILE_WIDTH, TILE_HEIGHT * 3)
        self.pos = (TILE_WIDTH * 2, WIN_HEIGHT - TILE_HEIGHT * 3)
        self.rect = pg.Rect(*self.pos, *self.size)
        self.image = pg.Surface(self.size)

        self.image.set_alpha(0)
        self.called_change = False

    def update(self):
        if self.text and self.called_change:
            self.image.set_alpha(200)
        elif self.called_change:
            self.image.set_alpha(0)
        self.called_change = False
