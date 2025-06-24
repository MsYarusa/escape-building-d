import pygame as pg
from typing import List, Tuple, Optional
from enum import Enum

from game.settings import (
    SHADOW_WIDTH, SHADOW_HEIGHT, TILE_WIDTH, TILE_HEIGHT, 
    SHADOW_COEF, BLACK,
    LIGHT_RADIUS_BRIGHT, LIGHT_RADIUS_DIM,
    LIGHT_BRIGHTNESS_BRIGHT, LIGHT_BRIGHTNESS_DIM, LIGHT_BRIGHTNESS_DARK
)
from game.groups import shadow_overlay_group
from game.utils.ray_tracer import RayTracer


class LightLevel(Enum):
    """Уровни освещения для теневых элементов"""
    BRIGHT = LIGHT_BRIGHTNESS_BRIGHT  # Полностью освещенная область
    DIM = LIGHT_BRIGHTNESS_DIM        # Полутень
    DARK = LIGHT_BRIGHTNESS_DARK      # Полностью темная область


class LightingSystem:
    """Система освещения и теней для игры"""
    
    def __init__(self):
        self._light_radius_bright = LIGHT_RADIUS_BRIGHT
        self._light_radius_dim = LIGHT_RADIUS_DIM
        self._last_player_pos: Optional[Tuple[int, int]] = None
        self._visible_cells: set = set()
        self._player_grid_pos: Optional[Tuple[int, int]] = None
    
    def update_lighting(self, player_pos: Tuple[int, int], level: List[str]) -> None:
        """
        Обновляет освещение на основе позиции игрока
        
        Args:
            player_pos: Позиция игрока в пикселях (x, y)
            level: Карта уровня
        """
        # Переводим позицию игрока в координаты сетки теней
        player_grid_x = player_pos[0] // SHADOW_WIDTH
        player_grid_y = player_pos[1] // SHADOW_HEIGHT
        player_grid_pos = (player_grid_x, player_grid_y)

        # Проверяем, изменилась ли позиция игрока
        if self._player_grid_pos == player_grid_pos:
            return
        self._player_grid_pos = player_grid_pos

        # Массово вычисляем видимые ячейки в радиусе полутени
        self._visible_cells = RayTracer.get_visible_cells(
            player_grid_pos,
            self._light_radius_dim,
            level,
            SHADOW_COEF
        )

        # Обновляем освещение только для теней в радиусе
        for shadow_element in shadow_overlay_group:
            shadow_grid_x = shadow_element.rect.centerx // SHADOW_WIDTH
            shadow_grid_y = shadow_element.rect.centery // SHADOW_HEIGHT
            shadow_grid_pos = (shadow_grid_x, shadow_grid_y)

            # Если вне радиуса полутени — тьма
            if self._distance(player_grid_pos, shadow_grid_pos) > self._light_radius_dim:
                self._set_shadow_brightness(shadow_element, LightLevel.DARK)
                continue

            # Если не видим — тьма
            if shadow_grid_pos not in self._visible_cells:
                self._set_shadow_brightness(shadow_element, LightLevel.DARK)
                continue

            # Внутри яркого радиуса — ярко, иначе полутень
            if self._distance(player_grid_pos, shadow_grid_pos) <= self._light_radius_bright:
                self._set_shadow_brightness(shadow_element, LightLevel.BRIGHT)
            else:
                self._set_shadow_brightness(shadow_element, LightLevel.DIM)

    def _distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Евклидово расстояние между двумя точками сетки теней"""
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    def _set_shadow_brightness(self, shadow_element, light_level: LightLevel) -> None:
        """
        Устанавливает яркость теневого элемента
        Args:
            shadow_element: Элемент тени
            light_level: Уровень освещения
        """
        if shadow_element.brightness != light_level.value:
            shadow_element.set_brightness(light_level.value)

    def clear_cache(self) -> None:
        """Сброс состояния освещения"""
        self._visible_cells = set()
        self._player_grid_pos = None 