import pygame as pg
from typing import Optional, Tuple
from abc import ABC, abstractmethod


class BaseRenderable(pg.sprite.Sprite, ABC):
    """
    Базовый класс для всех рендерируемых объектов в игре.
    
    Предоставляет общую функциональность для:
    - Управления изображениями
    - Позиционирования
    - Размеров
    - Групп спрайтов
    """
    
    def __init__(self, groups: Tuple[pg.sprite.Group, ...], 
                 image: pg.Surface, 
                 pos_x: int, 
                 pos_y: int, 
                 width: int, 
                 height: int,
                 offset_x: int = 0,
                 offset_y: int = 0):
        """
        Инициализирует рендерируемый объект.
        
        Args:
            groups: Группы спрайтов для добавления
            image: Изображение объекта
            pos_x: X координата в тайлах
            pos_y: Y координата в тайлах
            width: Ширина объекта в пикселях
            height: Высота объекта в пикселях
            offset_x: Смещение по X в пикселях
            offset_y: Смещение по Y в пикселях
        """
        super().__init__(*groups)
        
        self._image = image
        self._width = width
        self._height = height
        self._offset_x = offset_x
        self._offset_y = offset_y
        
        # Создаем прямоугольник для позиционирования и коллизий
        self.rect = pg.Rect(
            pos_x * width + offset_x,
            pos_y * height + offset_y,
            width,
            height
        )
        
        # Кэш для оптимизации
        self._last_pos: Optional[Tuple[int, int]] = None
    
    @property
    def image(self) -> pg.Surface:
        """Текущее изображение объекта"""
        return self._image
    
    @image.setter
    def image(self, value: pg.Surface) -> None:
        """Устанавливает изображение объекта"""
        self._image = value
    
    @property
    def width(self) -> int:
        """Ширина объекта"""
        return self._width
    
    @property
    def height(self) -> int:
        """Высота объекта"""
        return self._height
    
    @property
    def center(self) -> Tuple[int, int]:
        """Центр объекта"""
        return self.rect.center
    
    @property
    def position(self) -> Tuple[int, int]:
        """Позиция объекта (x, y)"""
        return (self.rect.x, self.rect.y)
    
    def set_position(self, x: int, y: int) -> None:
        """
        Устанавливает позицию объекта.
        
        Args:
            x: X координата в пикселях
            y: Y координата в пикселях
        """
        self.rect.x = x
        self.rect.y = y
        self._last_pos = (x, y)
    
    def move(self, dx: int, dy: int) -> None:
        """
        Перемещает объект на указанное расстояние.
        
        Args:
            dx: Смещение по X
            dy: Смещение по Y
        """
        self.rect.x += dx
        self.rect.y += dy
        self._last_pos = (self.rect.x, self.rect.y)
    
    def set_size(self, width: int, height: int) -> None:
        """
        Устанавливает размер объекта.
        
        Args:
            width: Новая ширина
            height: Новая высота
        """
        self._width = width
        self._height = height
        self.rect.width = width
        self.rect.height = height
    
    def scale_image(self, scale_factor: float) -> None:
        """
        Масштабирует изображение объекта.
        
        Args:
            scale_factor: Коэффициент масштабирования
        """
        new_width = int(self._width * scale_factor)
        new_height = int(self._height * scale_factor)
        self._image = pg.transform.scale(self._image, (new_width, new_height))
        self.set_size(new_width, new_height)
    
    def has_moved(self) -> bool:
        """
        Проверяет, изменилась ли позиция объекта.
        
        Returns:
            True если позиция изменилась
        """
        current_pos = (self.rect.x, self.rect.y)
        if self._last_pos != current_pos:
            self._last_pos = current_pos
            return True
        return False
    
    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """
        Абстрактный метод обновления объекта.
        Должен быть реализован в дочерних классах.
        """
        pass 