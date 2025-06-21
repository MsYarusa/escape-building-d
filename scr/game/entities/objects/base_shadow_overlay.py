import pygame as pg

from game.settings import SHADOW_WIDTH, SHADOW_HEIGHT, BLACK
from game.groups import all_sprites_group, shadow_overlay_group


class BaseShadowOverlay(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites_group, shadow_overlay_group)

        self.rect = pg.Rect(pos_x * SHADOW_WIDTH, pos_y * SHADOW_HEIGHT, SHADOW_WIDTH, SHADOW_HEIGHT)
        self.image = pg.Surface((SHADOW_WIDTH, SHADOW_HEIGHT))
        self.image.fill(BLACK)
        self.image.set_alpha(250)
        self.brightness = 250

    def set_brightness(self, value):
        self.image.set_alpha(value)
        self.brightness = value