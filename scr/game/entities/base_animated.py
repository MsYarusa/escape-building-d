import pygame as pg
from typing import List, Tuple, Optional
from abc import abstractmethod

from game.entities.base_collidable import BaseCollidable
from game.utils.images import cut_sheet


class BaseAnimated(BaseCollidable):
    """
    Базовый класс для анимированных объектов.
    
    Расширяет BaseCollidable функциональностью:
    - Управление кадрами анимации
    - Автоматическое переключение кадров
    - Направления анимации
    - Скорость анимации
    """
    
    def __init__(self, groups: Tuple[pg.sprite.Group, ...], 
                 sprite_sheet: pg.Surface,
                 cols: int,
                 rows: int,
                 pos_x: int, 
                 pos_y: int, 
                 width: int, 
                 height: int,
                 animation_speed: int = 10,
                 inner_rect_ratio: float = 1.0,
                 offset_x: int = 0,
                 offset_y: int = 0):
        """
        Инициализирует анимированный объект.
        
        Args:
            groups: Группы спрайтов для добавления
            sprite_sheet: Спрайтшит с кадрами анимации
            cols: Количество колонок в спрайтшите
            rows: Количество строк в спрайтшите
            pos_x: X координата в тайлах
            pos_y: Y координата в тайлах
            width: Ширина объекта в пикселях
            height: Высота объекта в пикселях
            animation_speed: Скорость анимации (каждый N-й кадр)
            inner_rect_ratio: Коэффициент размера внутреннего прямоугольника
            offset_x: Смещение по X в пикселях
            offset_y: Смещение по Y в пикселях
        """
        # Нарезаем спрайтшит на кадры
        self.frames = cut_sheet(sprite_sheet, cols, rows)
        
        # Инициализируем базовый объект с первым кадром
        super().__init__(groups, self.frames[0], pos_x, pos_y, width, height, 
                        inner_rect_ratio, offset_x, offset_y)
        
        self._animation_speed = animation_speed
        self._cur_frame = 0
        self._current_direction = 0  # Индекс направления (0-3: вниз, влево, вверх, вправо)
        self._frame_count = 0
        self._is_animating = True
        
        # Кэш для оптимизации
        self._last_animation_update = 0
    
    @property
    def current_frame(self) -> int:
        """Текущий кадр анимации"""
        return self._cur_frame
    
    @property
    def current_direction(self) -> int:
        """Текущее направление анимации"""
        return self._current_direction
    
    @property
    def animation_speed(self) -> int:
        """Скорость анимации"""
        return self._animation_speed
    
    @animation_speed.setter
    def animation_speed(self, value: int) -> None:
        """Устанавливает скорость анимации"""
        self._animation_speed = max(1, value)
    
    @property
    def is_animating(self) -> bool:
        """Активна ли анимация"""
        return self._is_animating
    
    @is_animating.setter
    def is_animating(self, value: bool) -> None:
        """Включает/выключает анимацию"""
        self._is_animating = value
    
    def set_direction(self, direction: int, animate: bool = True) -> None:
        """
        Устанавливает направление анимации.
        
        Args:
            direction: Направление (0-3: вниз, влево, вверх, вправо)
            animate: Включить анимацию при смене направления
        """
        if 0 <= direction <= 3 and direction != self._current_direction:
            self._current_direction = direction
            if animate:
                self._update_frame()
            else:
                # Устанавливаем первый кадр направления без анимации
                base_frame = self._current_direction * 8
                self._cur_frame = base_frame
                self._update_image()
    
    def set_frame(self, frame: int) -> None:
        """
        Устанавливает конкретный кадр анимации.
        
        Args:
            frame: Номер кадра
        """
        if 0 <= frame < len(self.frames):
            self._cur_frame = frame
            self._update_image()
    
    def reset_animation(self) -> None:
        """Сбрасывает анимацию к начальному состоянию"""
        self._cur_frame = 0
        self._frame_count = 0
        self._update_image()
    
    def pause_animation(self) -> None:
        """Приостанавливает анимацию"""
        self._is_animating = False
    
    def resume_animation(self) -> None:
        """Возобновляет анимацию"""
        self._is_animating = True
    
    def update_animation(self, frame_counter: int) -> None:
        """
        Обновляет анимацию.
        
        Args:
            frame_counter: Счетчик кадров игры
        """
        if not self._is_animating:
            return
            
        # Обновляем анимацию только каждый N-й кадр
        if frame_counter % self._animation_speed == 0:
            self._next_frame()
    
    def _next_frame(self) -> None:
        """Переходит к следующему кадру анимации"""
        # Вычисляем базовый индекс для текущего направления
        base_frame = self._current_direction * 8  # 8 кадров на направление
        
        # Вычисляем текущий кадр в рамках направления
        current_direction_frame = self._cur_frame - base_frame
        
        # Переходим к следующему кадру в цикле
        next_direction_frame = (current_direction_frame + 1) % 8
        
        # Устанавливаем новый кадр
        self._cur_frame = base_frame + next_direction_frame
        
        self._update_image()
    
    def _update_frame(self) -> None:
        """Обновляет кадр для текущего направления"""
        base_frame = self._current_direction * 8
        self._cur_frame = base_frame
        self._update_image()
    
    def _update_image(self) -> None:
        """Обновляет изображение объекта"""
        if 0 <= self._cur_frame < len(self.frames):
            self._image = self.frames[self._cur_frame]
    
    def get_frame_count(self) -> int:
        """Возвращает общее количество кадров"""
        return len(self.frames)
    
    def get_frames_per_direction(self) -> int:
        """Возвращает количество кадров на направление"""
        return len(self.frames) // 4 if len(self.frames) >= 4 else len(self.frames)
    
    def set_custom_frames(self, frames: List[pg.Surface]) -> None:
        """
        Устанавливает кастомные кадры анимации.
        
        Args:
            frames: Список кадров анимации
        """
        if frames:
            self.frames = frames
            self._cur_frame = min(self._cur_frame, len(frames) - 1)
            self._update_image()
    
    def get_current_frame_image(self) -> pg.Surface:
        """Возвращает изображение текущего кадра"""
        return self.frames[self._cur_frame] if self.frames else self._image 