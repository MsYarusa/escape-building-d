import pygame as pg

from game.settings import TILE_WIDTH, TILE_HEIGHT
from game.resources import tile_images
from game.groups import all_sprites_group, tiles_group, walls_group


class BaseTile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites_group, tiles_group)

        self.rect = pg.Rect(pos_x * TILE_WIDTH, pos_y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
        self.image = tile_images[tile_type]

        if tile_type == 'wall':
            self.add(walls_group)