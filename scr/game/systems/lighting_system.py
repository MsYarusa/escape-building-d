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
        self._light_radius_bright = LIGHT_RADIUS_BRIGHT * SHADOW_WIDTH  # Радиус яркого света
        self._light_radius_dim = LIGHT_RADIUS_DIM * SHADOW_WIDTH       # Радиус полутени
        self._last_player_pos: Optional[Tuple[int, int]] = None
        self._cached_visibility: dict = {}
        self._ray_tracer = RayTracer()
        
    def update_lighting(self, player_pos: Tuple[int, int], level: List[str]) -> None:
        """
        Обновляет освещение на основе позиции игрока
        
        Args:
            player_pos: Позиция игрока в пикселях (x, y)
            level: Карта уровня
        """
        # Проверяем, изменилась ли позиция игрока
        if self._last_player_pos == player_pos:
            return
            
        self._last_player_pos = player_pos
        self._cached_visibility.clear()
        
        # Обновляем освещение для всех теневых элементов
        for shadow_element in shadow_overlay_group:
            self._update_shadow_element(shadow_element, player_pos, level)
    
    def _update_shadow_element(self, shadow_element, player_pos: Tuple[int, int], level: List[str]) -> None:
        """
        Обновляет освещение для конкретного теневого элемента
        
        Args:
            shadow_element: Элемент тени для обновления
            player_pos: Позиция игрока в пикселях
            level: Карта уровня
        """
        shadow_center = (shadow_element.rect.centerx, shadow_element.rect.centery)
        distance = self._calculate_distance(player_pos, shadow_center)
        
        # Если элемент слишком далеко, делаем его темным
        if distance > self._light_radius_dim:
            self._set_shadow_brightness(shadow_element, LightLevel.DARK)
            return
            
        # Проверяем видимость через стены
        is_visible = self._check_visibility(shadow_center, player_pos, level)
        
        if not is_visible:
            self._set_shadow_brightness(shadow_element, LightLevel.DARK)
            return
            
        # Устанавливаем уровень освещения в зависимости от расстояния
        if distance <= self._light_radius_bright:
            self._set_shadow_brightness(shadow_element, LightLevel.BRIGHT)
        else:
            self._set_shadow_brightness(shadow_element, LightLevel.DIM)
    
    def _calculate_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Вычисляет евклидово расстояние между двумя точками
        
        Args:
            pos1: Первая точка (x, y)
            pos2: Вторая точка (x, y)
            
        Returns:
            Расстояние между точками
        """
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
    
    def _check_visibility(self, shadow_pos: Tuple[int, int], player_pos: Tuple[int, int], level: List[str]) -> bool:
        """
        Проверяет видимость между двумя точками через стены
        
        Args:
            shadow_pos: Позиция теневого элемента
            player_pos: Позиция игрока
            level: Карта уровня
            
        Returns:
            True если точки видимы друг другу
        """
        # Конвертируем в координаты сетки теней
        shadow_grid_x = shadow_pos[0] // SHADOW_WIDTH
        shadow_grid_y = shadow_pos[1] // SHADOW_HEIGHT
        player_grid_x = player_pos[0] // SHADOW_WIDTH
        player_grid_y = player_pos[1] // SHADOW_HEIGHT
        
        # Создаем ключ для кэширования
        cache_key = (shadow_grid_x, shadow_grid_y, player_grid_x, player_grid_y)
        
        if cache_key in self._cached_visibility:
            return self._cached_visibility[cache_key]
        
        # Используем оптимизированную трассировку лучей
        is_visible = RayTracer.check_line_of_sight(
            (shadow_grid_x, shadow_grid_y), 
            (player_grid_x, player_grid_y), 
            level, 
            SHADOW_COEF
        )
        
        # Кэшируем результат
        self._cached_visibility[cache_key] = is_visible
        return is_visible
    
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
        """Очищает кэш видимости"""
        self._cached_visibility.clear()
        self._last_player_pos = None 