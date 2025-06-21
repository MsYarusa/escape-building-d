import pygame as pg

from game.utils.images import cut_sheet
from game.resources import enemy_images, replicas
from game.groups import all_sprites_group, replica_group, player_group, enemies_group
from game.settings import (
    COCKROACH_RECT_X,
    COCKROACH_RECT_Y,
    COCKROACH_SPEED,
    LOST_SOUL_RECT_X,
    LOST_SOUL_RECT_Y,
    LOST_SOUL_SPEED,
    TILE_WIDTH,
    TILE_HEIGHT,
    SHADOW_COEF
)

# скорость, ширина прямоугольника, высота прямоугольника
enemy_data = {
    'lost_soul': (LOST_SOUL_SPEED, LOST_SOUL_RECT_X, LOST_SOUL_RECT_Y),
    'cockroach': (COCKROACH_SPEED, COCKROACH_RECT_X, COCKROACH_RECT_Y)
}


class BaseEnemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, pos_x, pos_y):
        super().__init__(all_sprites_group, enemies_group)

        cols = enemy_images[enemy_type]['cols']
        rows = enemy_images[enemy_type]['rows']
        self.frames = cut_sheet(enemy_images[enemy_type]['img'], cols, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        self.type = enemy_type
        self.speed = enemy_data[enemy_type][0]
        width = enemy_data[enemy_type][1]
        height = enemy_data[enemy_type][2]
        self.rect = pg.Rect(pos_x * TILE_WIDTH, pos_y * TILE_HEIGHT, width, height)
        self.inner_rect = pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def set_replica(self, player, player_pos, pos, level):

        is_visible = True

        while pos[0] != player_pos[0] or pos[1] != player_pos[1]:
            if pos[0] != player_pos[0]:
                pos[0] += (-1) ** (pos[0] > player_pos[0])
            if pos[1] != player_pos[1]:
                pos[1] += (-1) ** (pos[1] > player_pos[1])
            if level[pos[1] // SHADOW_COEF][pos[0] // SHADOW_COEF] == '#':
                is_visible = False

        if is_visible:
            player.info_collected[self.type] = True
            replica = None
            for obj in replica_group:
                replica = obj

            for player in player_group:
                replica.set_text(replicas[self.type], player.name)
