import pygame as pg

from game.utils.images import cut_sheet, load_image
from game.settings import (
    SHADOW_WIDTH,
    SHADOW_HEIGHT,
    TILE_WIDTH,
    TILE_HEIGHT,
    PLAYER_RECT_X,
    PLAYER_RECT_Y,
    PLAYER_SPEED,
    SHADOW_COEF
)
from game.groups import (
    all_sprites_group,
    player_group,
    interactable_objects_group,
    enemies_group,
    walls_group,
    shadow_overlay_group
)


class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites_group, player_group)

        self.name = 'Степан'

        self.frames = cut_sheet(load_image(
            'images\\player.png'), 8, 4)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        self.rect = pg.Rect(pos_x * TILE_WIDTH + 6, pos_y * TILE_HEIGHT, PLAYER_RECT_X, PLAYER_RECT_Y)
        self.inner_rect = pg.Rect(self.rect.x, self.rect.y, PLAYER_RECT_X // 2, PLAYER_RECT_Y // 2)
        self.set_inner_rect()

        self.info_collected = {
            'lost_soul': False,
            'cockroach': False,
            'stairs': False,
            'vent': False,
            'key': False,
            'locked_door': False,
            'unlocked_door': True
        }
        self.step = 0
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def set_inner_rect(self):
        self.inner_rect.x = self.rect.x + PLAYER_RECT_X // 4
        self.inner_rect.y = self.rect.y + PLAYER_RECT_Y // 4

    def set_name(self, name):
        self.name = name

    def check_obj(self):
        for obj in interactable_objects_group:
            if pg.sprite.collide_rect(self, obj):
                return obj
        return None

    def is_attacked(self):
        for enemy in enemies_group:
            if self.inner_rect.colliderect(enemy.inner_rect):
                return True
        return False

    def update(self, level, player_it):

        if player_it % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % 8 + self.step * 8
            self.image = self.frames[self.cur_frame]

        x_delta = 0
        y_delta = 0

        if self.left:
            x_delta -= PLAYER_SPEED
            self.step = 3
        if self.right:
            x_delta += PLAYER_SPEED
            self.step = 1
        if self.up:
            y_delta -= PLAYER_SPEED
            self.step = 2
        if self.down:
            y_delta += PLAYER_SPEED
            self.step = 0

        if not (self.up or self.down or self.right or self.left):
            self.cur_frame = -1

        self.rect.x += x_delta
        self.collide(x_delta, 0)

        self.rect.y += y_delta
        self.collide(0, y_delta)

        self.set_inner_rect()
        self.set_light(level)

    def collide(self, x_delta, y_delta):
        for wall in walls_group:
            if pg.sprite.collide_rect(self, wall):

                if x_delta < 0:
                    self.rect.left = wall.rect.right
                if x_delta > 0:
                    self.rect.right = wall.rect.left
                if y_delta < 0:
                    self.rect.top = wall.rect.bottom
                if y_delta > 0:
                    self.rect.bottom = wall.rect.top

    def set_light(self, level):
        player_x = self.rect.centerx
        player_y = self.rect.centery
        player_pos = (player_x // SHADOW_WIDTH, player_y // SHADOW_HEIGHT)

        for elem in shadow_overlay_group:
            elem_x = elem.rect.centerx
            elem_y = elem.rect.centery
            is_visible = True

            dist = ((elem_x - player_x)**2 + (elem_y - player_y)**2)**(1/2)

            if dist <= 6 * SHADOW_WIDTH:
                pos_x = elem_x // SHADOW_WIDTH
                pos_y = elem_y // SHADOW_HEIGHT

                while pos_x != player_pos[0] or pos_y != player_pos[1]:
                    if pos_x != player_pos[0]:
                        pos_x += (-1) ** (pos_x > player_pos[0])
                    if pos_y != player_pos[1]:
                        pos_y += (-1) ** (pos_y > player_pos[1])
                    if level[pos_y // SHADOW_COEF][pos_x // SHADOW_COEF] == '#':
                        is_visible = False

            if dist <= 5 * SHADOW_WIDTH and is_visible:
                elem.set_brightness(0)
            elif dist <= 6 * SHADOW_WIDTH and is_visible:
                elem.set_brightness(121)
            elif elem.brightness != 250:
                elem.set_brightness(250)
