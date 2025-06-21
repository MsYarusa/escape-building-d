from game.groups import player_group
from game.settings import (
    TILE_WIDTH,
    TILE_HEIGHT,
    SHADOW_WIDTH,
    SHADOW_HEIGHT
)

from game.entities.enemies import BaseEnemy


class Cockroach(BaseEnemy):
    def __init__(self, start_x, start_y, end_x, end_y):
        super().__init__('cockroach', start_x, start_y)

        self.rect.y -= TILE_WIDTH // 2
        self.inner_rect.width = 3 * self.rect.width // 4
        self.inner_rect.height = 3 * self.rect.height // 4
        self.set_inner_rect()
        self.start_x = start_x * TILE_WIDTH
        self.start_y = start_y * TILE_HEIGHT
        self.end_x = end_x * TILE_WIDTH
        self.end_y = end_y * TILE_HEIGHT
        self.inverse = False

    def set_inner_rect(self):
        self.inner_rect.x = self.rect.x + self.rect.width // 8
        self.inner_rect.y = self.rect.y + self.rect.height // 4

    def update(self, level, player_it):

        player = None
        for obj in player_group:
            player = obj

        player_x = player.rect.centerx
        player_y = player.rect.centery
        soul_x = self.rect.centerx
        soul_y = self.rect.centery

        dist = ((soul_x - player_x) ** 2 + (soul_y - player_y) ** 2) ** (1 / 2)

        if dist <= 3 * TILE_WIDTH and not player.info_collected[self.type]:
            player_pos = [player_x // SHADOW_WIDTH, player_y // SHADOW_HEIGHT]
            pos = [soul_x // SHADOW_WIDTH, soul_y // SHADOW_HEIGHT]
            self.set_replica(player, player_pos, pos, level)

        inv_x = self.start_x > self.end_x
        inv_y = self.start_y > self.end_y

        if not self.inverse:

            if self.start_x < self.end_x:
                self.cur_frame = 2
            if self.start_x > self.end_x:
                self.cur_frame = 0
            if self.start_y < self.end_y:
                self.cur_frame = 3
            if self.start_y > self.end_y:
                self.cur_frame = 1

            con1 = self.rect.x * (-1) ** inv_x < self.end_x * (-1) ** inv_x
            con2 = self.rect.y * (-1) ** inv_y < self.end_y * (-1) ** inv_y

            if con1:
                self.rect.x += self.speed * (-1) ** inv_x

            if con2:
                self.rect.y += self.speed * (-1) ** inv_y

            if not con1 and not con2:
                self.inverse = True
        else:

            if self.start_x < self.end_x:
                self.cur_frame = 0
            if self.start_x > self.end_x:
                self.cur_frame = 2
            if self.start_y < self.end_y:
                self.cur_frame = 1
            if self.start_y > self.end_y:
                self.cur_frame = 3

            con1 = self.rect.x * (-1) ** inv_x > self.start_x * (-1) ** inv_x
            con2 = self.rect.y * (-1) ** inv_y > self.start_y * (-1) ** inv_y

            if con1:
                self.rect.x -= self.speed * (-1) ** inv_x

            if con2:
                self.rect.y -= self.speed * (-1) ** inv_y

            if not con1 and not con2:
                self.inverse = False


        self.image = self.frames[self.cur_frame]
        self.set_inner_rect()