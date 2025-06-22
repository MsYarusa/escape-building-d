import pygame as pg
from typing import Tuple, Optional
from abc import abstractmethod

from game.entities.base_animated import BaseAnimated
from game.groups import walls_group


class BaseMovable(BaseAnimated):
    """
    Базовый класс для движущихся объектов.
    
    Расширяет BaseAnimated функциональностью:
    - Управление движением
    - Скорость и направление
    - Обработка коллизий при движении
    - Автоматическое обновление анимации
    """
    
    def __init__(self, groups: Tuple[pg.sprite.Group, ...], 
                 sprite_sheet: pg.Surface,
                 cols: int,
                 rows: int,
                 pos_x: int, 
                 pos_y: int, 
                 width: int, 
                 height: int,
                 speed: float = 1.0,
                 animation_speed: int = 10,
                 inner_rect_ratio: float = 1.0,
                 offset_x: int = 0,
                 offset_y: int = 0):
        """
        Инициализирует движущийся объект.
        
        Args:
            groups: Группы спрайтов для добавления
            sprite_sheet: Спрайтшит с кадрами анимации
            cols: Количество колонок в спрайтшите
            rows: Количество строк в спрайтшите
            pos_x: X координата в тайлах
            pos_y: Y координата в тайлах
            width: Ширина объекта в пикселях
            height: Высота объекта в пикселях
            speed: Скорость движения
            animation_speed: Скорость анимации
            inner_rect_ratio: Коэффициент размера внутреннего прямоугольника
            offset_x: Смещение по X в пикселях
            offset_y: Смещение по Y в пикселях
        """
        super().__init__(groups, sprite_sheet, cols, rows, pos_x, pos_y, width, height,
                        animation_speed, inner_rect_ratio, offset_x, offset_y)
        
        self._speed = speed
        self._dx = 0.0  # Текущее смещение по X
        self._dy = 0.0  # Текущее смещение по Y
        self._target_x = 0.0  # Целевая позиция X
        self._target_y = 0.0  # Целевая позиция Y
        self._is_moving = False
        self._last_direction = 0  # Последнее направление движения (0: вниз, 1: вправо, 2: вверх, 3: влево)
        
        # Состояние движения
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        
        # Устанавливаем начальное направление (вниз) и синхронизируем
        self.set_direction(0)
        self._last_direction = self._current_direction
    
    @property
    def speed(self) -> float:
        """Скорость движения"""
        return self._speed
    
    @speed.setter
    def speed(self, value: float) -> None:
        """Устанавливает скорость движения"""
        self._speed = max(0.0, value)
    
    @property
    def is_moving(self) -> bool:
        """Двигается ли объект"""
        return self._is_moving
    
    @property
    def direction(self) -> Tuple[float, float]:
        """Текущее направление движения (dx, dy)"""
        return (self._dx, self._dy)
    
    def set_movement_direction(self, up: bool = False, down: bool = False, 
                              left: bool = False, right: bool = False) -> None:
        """
        Устанавливает направление движения.
        
        Args:
            up: Движение вверх
            down: Движение вниз
            left: Движение влево
            right: Движение вправо
        """
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        
        # Вычисляем смещение
        self._dx = 0.0
        self._dy = 0.0
        
        if self.left:
            self._dx -= self._speed
        if self.right:
            self._dx += self._speed
        if self.up:
            self._dy -= self._speed
        if self.down:
            self._dy += self._speed
        
        # Нормализуем диагональное движение
        if self._dx != 0 and self._dy != 0:
            self._dx *= 0.707  # 1/sqrt(2)
            self._dy *= 0.707
        
        # Обновляем анимацию
        self._update_movement_animation()
        
        # Проверяем, движется ли объект
        self._is_moving = self._dx != 0 or self._dy != 0
    
    def move_towards(self, target_x: float, target_y: float) -> None:
        """
        Двигает объект к целевой точке.
        
        Args:
            target_x: Целевая X координата
            target_y: Целевая Y координата
        """
        self._target_x = target_x
        self._target_y = target_y
        
        # Вычисляем направление к цели
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        
        # Нормализуем и применяем скорость
        distance = (dx * dx + dy * dy) ** 0.5
        if distance > 0:
            self._dx = (dx / distance) * self._speed
            self._dy = (dy / distance) * self._speed
        else:
            self._dx = 0
            self._dy = 0
        
        self._is_moving = distance > self._speed
        self._update_movement_animation()
    
    def stop_movement(self) -> None:
        """Останавливает движение"""
        self._dx = 0.0
        self._dy = 0.0
        self._is_moving = False
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        
        # Обновляем анимацию для сохранения направления
        self._update_movement_animation()
    
    def update_movement(self, frame_counter: int) -> None:
        """
        Обновляет движение объекта.
        
        Args:
            frame_counter: Счетчик кадров игры
        """
        # Обновляем анимацию
        self.update_animation(frame_counter)
        
        # Применяем движение только если объект действительно движется
        if self._is_moving and (self._dx != 0 or self._dy != 0):
            # Используем округление для более точного движения
            dx = round(self._dx)
            dy = round(self._dy)
            self.move_with_collision(dx, dy, walls_group)
    
    def update(self, *args) -> None:
        """
        Стандартный метод обновления для совместимости с Pygame.
        Может принимать любые аргументы, но игнорирует их.
        """
        # Используем простой счетчик кадров для анимации
        # В реальной игре это должно передаваться извне
        import pygame as pg
        frame_counter = pg.time.get_ticks() // 50  # Примерный счетчик кадров
        self.update_movement(frame_counter)
    
    def _update_movement_animation(self) -> None:
        """Обновляет анимацию в зависимости от направления движения"""
        if not self._is_moving:
            # Останавливаем анимацию при отсутствии движения, но сохраняем направление
            self.pause_animation()
            # Синхронизируем _last_direction с текущим направлением анимации
            self._last_direction = self._current_direction
            return
        
        # Возобновляем анимацию
        self.resume_animation()
        
        # Определяем направление анимации
        # 0: вниз, 1: вправо, 2: вверх, 3: влево
        new_direction = None
        
        # Проверяем вертикальное движение
        if self._dy < 0:
            new_direction = 2  # Вверх
        if self._dy > 0:
            new_direction = 0  # Вниз
        # Проверяем горизонтальное движение
        if self._dx < 0:
            new_direction = 3  # Влево
        if self._dx > 0:
            new_direction = 1  # Вправо
        
        # Обновляем направление только если оно изменилось
        if new_direction is not None and new_direction != self._current_direction:
            self._last_direction = new_direction
            self.set_direction(self._last_direction)
    
    def get_distance_to_target(self) -> float:
        """
        Вычисляет расстояние до целевой точки.
        
        Returns:
            Расстояние до цели
        """
        dx = self._target_x - self.rect.centerx
        dy = self._target_y - self.rect.centery
        return (dx * dx + dy * dy) ** 0.5
    
    def has_reached_target(self, tolerance: float = 5.0) -> bool:
        """
        Проверяет, достиг ли объект целевой точки.
        
        Args:
            tolerance: Допустимое расстояние до цели
            
        Returns:
            True если объект достиг цели
        """
        return self.get_distance_to_target() <= tolerance
    
    def set_speed_multiplier(self, multiplier: float) -> None:
        """
        Устанавливает множитель скорости.
        
        Args:
            multiplier: Множитель скорости
        """
        self._speed *= multiplier
    
    def get_movement_vector(self) -> Tuple[float, float]:
        """
        Возвращает вектор движения.
        
        Returns:
            Кортеж (dx, dy) с компонентами движения
        """
        return (self._dx, self._dy) 