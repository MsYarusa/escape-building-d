import pygame as pg

from game.groups import all_sprites_group, replica_group, player_group, enemies_group
from game.resources import enemy_images, replicas
from game.settings import (
    COCKROACH_RECT_X,
    COCKROACH_RECT_Y,
    COCKROACH_SPEED,
    LOST_SOUL_RECT_X,
    LOST_SOUL_RECT_Y,
    LOST_SOUL_SPEED,
    TILE_WIDTH,
    TILE_HEIGHT,
    SHADOW_COEF,
    MAX_AUDIBLE_DISTANCE,
    SHADOW_WIDTH,
    SHADOW_HEIGHT
)
from game.utils.audio_manager import play_sound, fadeout_sound
from game.utils.images import cut_sheet

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

        self.sound_name = enemy_type  # Звук будет называться так же, как тип врага ('cockroach', 'lost_soul')
        self.sound_timer = 0
        self.sound_delay = 1000
        self.sound_channel = None

    def update(self, player, lighting_system, level, player_it):
        """
        Обновляет состояние врага, включая продвинутую логику звука.
        """
        # --- Сначала определяем, должен ли враг сейчас издавать звук ---

        is_visible = False
        distance = float('inf')

        # Определяем позицию врага в сетке теней
        enemy_grid_x = self.rect.centerx // SHADOW_WIDTH
        enemy_grid_y = self.rect.centery // SHADOW_HEIGHT

        # Спрашиваем у системы освещения, виден ли враг
        if lighting_system.is_position_visible((enemy_grid_x, enemy_grid_y)):
            is_visible = True
            # Если виден, вычисляем расстояние до игрока
            dx = self.rect.centerx - player.rect.centerx
            dy = self.rect.centery - player.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

        # Врага должно быть слышно, только если он виден И находится в пределах слышимости
        should_be_audible = is_visible and distance <= MAX_AUDIBLE_DISTANCE

        # --- Теперь управляем звуком на основе этого знания ---

        if should_be_audible:
            # Врага должно быть слышно.

            # Вычисляем громкость на основе расстояния
            volume = 1.0 - (distance / MAX_AUDIBLE_DISTANCE)
            volume = max(0.0, min(1.0, volume))

            # Проверяем, играет ли уже звук на нашем персональном канале
            if self.sound_channel and self.sound_channel.get_busy():
                # Звук уже играет. Просто обновляем его громкость.
                self.sound_channel.set_volume(volume)
            else:
                # Звук не играет. Нужно его запустить (с учетом задержки).
                current_time = pg.time.get_ticks()
                if current_time - self.sound_timer > self.sound_delay:
                    # Запускаем звук и СОХРАНЯЕМ его канал в self.sound_channel
                    self.sound_channel = play_sound(self.sound_name, volume=volume)
                    # Сбрасываем таймер, чтобы следующий звук был не сразу
                    self.sound_timer = current_time
        else:
            # Врага НЕ должно быть слышно.

            # Если звук на нашем канале все еще играет, плавно его выключаем.
            if self.sound_channel and self.sound_channel.get_busy():
                fadeout_sound(self.sound_channel)
                # "Забываем" канал, чтобы в следующий раз можно было запустить новый
                self.sound_channel = None

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
