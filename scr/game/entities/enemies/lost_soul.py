import pygame as pg

from game.groups import player_group, walls_group
from game.settings import (
    TILE_WIDTH,
    SHADOW_WIDTH,
    SHADOW_HEIGHT
)

from game.entities.enemies import BaseEnemy


class LostSoul(BaseEnemy):
    def __init__(self, pos_x, pos_y):
        super().__init__('lost_soul', pos_x, pos_y)

        self.inner_rect.width = self.rect.width // 2
        self.inner_rect.height = self.rect.height // 4
        self.set_inner_rect()
        self.step = 0

        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def set_inner_rect(self):
        self.inner_rect.x = self.rect.x + self.rect.width // 4
        self.inner_rect.y = self.rect.y + 3 * self.rect.height // 8

    def update(self, level, player_it):

        if player_it % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % 8 + self.step * 8
            self.image = self.frames[self.cur_frame]

        player = None
        for obj in player_group:
            player = obj

        player_x = player.rect.centerx
        player_y = player.rect.centery
        soul_x = self.rect.centerx
        soul_y = self.rect.centery

        dist = ((soul_x - player_x)**2 + (soul_y - player_y)**2)**(1/2)

        if dist <= 3 * TILE_WIDTH and not player.info_collected[self.type]:
            player_pos = [player_x // SHADOW_WIDTH, player_y // SHADOW_HEIGHT]
            pos = [soul_x // SHADOW_WIDTH, soul_y // SHADOW_HEIGHT]
            self.set_replica(player, player_pos, pos, level)

        x_delta = self.speed * (player_x - soul_x) / max(dist, 0.1)
        y_delta = self.speed * (player_y - soul_y) / max(dist, 0.1)

        if y_delta < 0:
            self.step = 2
        if y_delta > 0:
            self.step = 0
        if x_delta < 0 and abs(x_delta) > abs(y_delta):
            self.step = 3
        if x_delta > 0 and abs(x_delta) > abs(y_delta):
            self.step = 1

        self.rect.y += y_delta
        self.collide(0, y_delta)

        self.rect.x += x_delta
        self.collide(x_delta, 0)

        self.set_inner_rect()

    def collide(self, x_delta, y_delta):
        for wall in walls_group:
            if pg.sprite.collide_rect(self, wall):

                self.cur_frame = -1

                if x_delta < 0:
                    self.rect.left = wall.rect.right
                if x_delta > 0:
                    self.rect.right = wall.rect.left
                if y_delta < 0:
                    self.rect.top = wall.rect.bottom
                if y_delta > 0:
                    self.rect.bottom = wall.rect.top
