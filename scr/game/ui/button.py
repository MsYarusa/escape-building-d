import pygame as pg

from game.resources import button_images


class Button(pg.sprite.Sprite):
    def __init__(self, pos, button_type):
        super().__init__()
        self.pos = pos
        self.image = button_images[button_type][False]
        self.buff_image = button_images[button_type][True]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.type = button_type
        self.text = None
        self.size = (self.rect.width, self.rect.height)

    def set_text(self, text, font_size=18, color='black', font='calibry'):
        # Пересоздаём image из исходного шаблона, чтобы не было наложения текста
        self.image = pg.transform.scale(button_images[self.type][False], self.size)
        text_font = pg.font.SysFont(font, font_size)
        text_rendered = text_font.render(text, 0, pg.Color(color))
        text_rect = text_rendered.get_rect()
        text_rect.centerx = self.rect.width // 2
        text_rect.centery = self.rect.height // 2
        self.text = (text_rendered, text_rect)
        self.image.blit(*self.text)

    def scale(self, size):
        self.size = size
        self.image = pg.transform.scale(button_images[self.type][False], size)
        self.buff_image = pg.transform.scale(button_images[self.type][True], size)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def change_state(self):
        self.image, self.buff_image = self.buff_image, self.image
        if self.text:
            self.image.blit(*self.text)

    def pressed(self, event_pos):
        x_in = self.rect.left < event_pos[0] < self.rect.right
        y_in = self.rect.top < event_pos[1] < self.rect.bottom

        if x_in and y_in:
            self.change_state()
            return True
        else:
            return False
