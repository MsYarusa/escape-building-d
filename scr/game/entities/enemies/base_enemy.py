from typing import Optional

import pygame as pg

from game.groups import all_sprites_group, replica_group, enemies_group
from game.resources import enemy_images, replicas
from game.settings import (
    COCKROACH_RECT_X,
    COCKROACH_RECT_Y,
    COCKROACH_SPEED,
    LOST_SOUL_RECT_X,
    LOST_SOUL_RECT_Y,
    LOST_SOUL_SPEED,
    LOST_GIRL_RECT_X,
    LOST_GIRL_RECT_Y,
    LOST_GIRL_SPEED,
    TILE_WIDTH,
    TILE_HEIGHT,
    SHADOW_COEF,
    MAX_AUDIBLE_DISTANCE,
    SHADOW_WIDTH,
    SHADOW_HEIGHT
)
from game.utils.audio_manager import play_sound, fadeout_sound
from game.utils.images import cut_sheet

# Словарь с данными для каждого типа врага
enemy_data = {
    'lost_soul': (LOST_SOUL_SPEED, LOST_SOUL_RECT_X, LOST_SOUL_RECT_Y),
    'cockroach': (COCKROACH_SPEED, COCKROACH_RECT_X, COCKROACH_RECT_Y),
    'lost_girl': (LOST_GIRL_SPEED, LOST_GIRL_RECT_X, LOST_GIRL_RECT_Y)
}


class BaseEnemy(pg.sprite.Sprite):
    """
    Базовый класс для всех врагов в игре.
    Реализует общую логику, такую как:
    - Инициализация спрайта и анимации
    - Управление звуком в зависимости от видимости и расстояния до игрока
    """

    def __init__(self, enemy_type: str, pos_x: int, pos_y: int):
        super().__init__(all_sprites_group, enemies_group)

        # Настройка анимации
        cols = enemy_images[enemy_type]['cols']
        rows = enemy_images[enemy_type]['rows']
        self.frames = cut_sheet(enemy_images[enemy_type]['img'], cols, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        # Настройка физических параметров
        self.type = enemy_type
        self.speed, width, height = enemy_data[enemy_type]
        self.rect = pg.Rect(pos_x * TILE_WIDTH, pos_y * TILE_HEIGHT, width, height)
        self.inner_rect = pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        # Настройка звука
        self.sound_name = enemy_type
        self.sound_timer = 0
        self.sound_delay = 1000  # Задержка перед повторным запуском звука в мс
        self.sound_channel: Optional[pg.mixer.Channel] = None

    def update(self, player, lighting_system, level, player_it):
        """
        Обновляет состояние врага, включая продвинутую логику звука.
        """
        distance = float('inf')

        # Определяем позицию врага в сетке теней
        enemy_grid_x = self.rect.centerx // SHADOW_WIDTH
        enemy_grid_y = self.rect.centery // SHADOW_HEIGHT

        # Спрашиваем у системы освещения, виден ли враг
        is_visible = lighting_system.is_position_visible((enemy_grid_x, enemy_grid_y))

        if is_visible:
            # Если виден, вычисляем расстояние до игрока
            dx = self.rect.centerx - player.rect.centerx
            dy = self.rect.centery - player.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

        should_be_audible = is_visible and distance <= MAX_AUDIBLE_DISTANCE

        if should_be_audible:
            # Врага должно быть слышно.

            # Вычисляем громкость на основе расстояния (чем ближе, тем громче)
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
                    self.sound_channel = play_sound(self.sound_name, loops=-1)
                    if self.sound_channel:  # Проверяем, что звук успешно запустился
                        self.sound_channel.set_volume(volume)

                    self.sound_timer = current_time  # Сбрасываем таймер
        else:
            # Врага НЕ должно быть слышно.

            # Если звук на нашем канале все еще играет, плавно его выключаем.
            if self.sound_channel and self.sound_channel.get_busy():
                fadeout_sound(self.sound_channel)
                self.sound_channel = None  # "Забываем" канал, чтобы можно было запустить его снова

    def set_replica(self, player, player_pos, pos, level):
        """
        Устанавливает реплику, если игрок видит врага.
        """
        is_visible = True

        # Этот цикл выглядит как упрощенная проверка линии видимости.
        while pos[0] != player_pos[0] or pos[1] != player_pos[1]:
            if pos[0] != player_pos[0]:
                pos[0] += (-1) ** (pos[0] > player_pos[0])
            if pos[1] != player_pos[1]:
                pos[1] += (-1) ** (pos[1] > player_pos[1])

            # Проверка на столкновение с препятствием
            level_y = pos[1] // SHADOW_COEF
            level_x = pos[0] // SHADOW_COEF
            if not (0 <= level_y < len(level) and 0 <= level_x < len(level[0])) or \
                    level[level_y][level_x] == '#':
                is_visible = False
                break

        if is_visible:
            if not player.info_collected[self.type]:
                player.info_collected[self.type] = True
                replica = next(iter(replica_group), None)
                if replica:
                    replica.set_text(replicas[self.type], player.name)
