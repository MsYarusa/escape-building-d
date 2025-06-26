from enum import Enum
from typing import List, Tuple, Optional

from game.groups import shadow_overlay_group
from game.settings import (
    SHADOW_WIDTH, SHADOW_HEIGHT, SHADOW_COEF,
    LIGHT_RADIUS_BRIGHT, LIGHT_RADIUS_DIM,
    LIGHT_BRIGHTNESS_BRIGHT, LIGHT_BRIGHTNESS_DIM, LIGHT_BRIGHTNESS_DARK
)
from game.utils.ray_tracer import RayTracer


class LightLevel(Enum):
    """Уровни освещения для теневых элементов"""
    BRIGHT = LIGHT_BRIGHTNESS_BRIGHT
    DIM = LIGHT_BRIGHTNESS_DIM
    DARK = LIGHT_BRIGHTNESS_DARK


class LightingSystem:
    """Система освещения и теней для игры"""

    def __init__(self):
        self._light_radius_bright_sq = LIGHT_RADIUS_BRIGHT ** 2
        self._light_radius_dim_sq = LIGHT_RADIUS_DIM ** 2
        self._visible_cells: set = set()
        self._player_grid_pos: Optional[Tuple[int, int]] = None

    def update_lighting(self, player_pos: Tuple[int, int], level: List[str]) -> None:
        """Обновляет освещение на основе позиции игрока."""
        player_grid_x = player_pos[0] // SHADOW_WIDTH
        player_grid_y = player_pos[1] // SHADOW_HEIGHT
        player_grid_pos = (player_grid_x, player_grid_y)

        if self._player_grid_pos == player_grid_pos:
            return  # Не пересчитываем, если игрок не сдвинулся на новую клетку

        self._player_grid_pos = player_grid_pos

        self._visible_cells = RayTracer.get_visible_cells(
            player_grid_pos, LIGHT_RADIUS_DIM, level, SHADOW_COEF
        )

        for shadow_element in shadow_overlay_group:
            shadow_grid_pos = (
                shadow_element.rect.centerx // SHADOW_WIDTH,
                shadow_element.rect.centery // SHADOW_HEIGHT
            )
            dist_sq = self._distance_sq(player_grid_pos, shadow_grid_pos)

            # Упрощение: если клетка невидима ИЛИ слишком далеко, делаем ее темной
            if shadow_grid_pos not in self._visible_cells or dist_sq > self._light_radius_dim_sq:
                self._set_shadow_brightness(shadow_element, LightLevel.DARK)
                continue

            # Определяем уровень света для видимых клеток
            if dist_sq <= self._light_radius_bright_sq:
                self._set_shadow_brightness(shadow_element, LightLevel.BRIGHT)
            else:
                self._set_shadow_brightness(shadow_element, LightLevel.DIM)

    def is_position_visible(self, grid_pos: Tuple[int, int]) -> bool:
        """Проверяет, находится ли ячейка сетки в видимой области."""
        return grid_pos in self._visible_cells

    def _distance_sq(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Вычисляет квадрат евклидова расстояния для быстрой проверки."""
        return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2

    def _set_shadow_brightness(self, shadow_element, light_level: LightLevel) -> None:
        """Устанавливает яркость, только если она изменилась."""
        if shadow_element.brightness != light_level.value:
            shadow_element.set_brightness(light_level.value)

    def clear_cache(self) -> None:
        """Сбрас состояния освещения для перезагрузки уровня."""
        self._visible_cells = set()
        self._player_grid_pos = None
