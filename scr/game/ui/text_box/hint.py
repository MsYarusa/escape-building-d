import pygame as pg

from game.settings import TILE_HEIGHT

from game.ui.text_box import BaseTextBox


class Hint(BaseTextBox):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pg.font.SysFont('cambria', 18)

    def hide(self):
        self.text = ''
        self.called_change = True

    def set_text(self, text):
        self.text = text
        self.called_change = True
        text_rendered = self.font.render(text, 0, pg.Color('white'))
        text_rect = text_rendered.get_rect()
        text_rect.centerx = self.size[0] // 2
        text_rect.bottom = self.size[1] - TILE_HEIGHT // 4
        self.image.blit(text_rendered, text_rect)
