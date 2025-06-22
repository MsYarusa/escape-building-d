import pygame as pg
from typing import Optional, Tuple, List
from abc import abstractmethod

from game.entities.base_renderable import BaseRenderable


class BaseCollidable(BaseRenderable):
    """
    Базовый класс для объектов с коллизиями.
    
    Расширяет BaseRenderable функциональностью:
    - Внутренние прямоугольники для точных коллизий
    - Обработка столкновений со стенами
    - Проверка пересечений с другими объектами
    """
    
    def __init__(self, groups: Tuple[pg.sprite.Group, ...], 
                 image: pg.Surface, 
                 pos_x: int, 
                 pos_y: int, 
                 width: int, 
                 height: int,
                 inner_rect_ratio: float = 1.0,
                 offset_x: int = 0,
                 offset_y: int = 0):
        """
        Инициализирует объект с коллизиями.
        
        Args:
            groups: Группы спрайтов для добавления
            image: Изображение объекта
            pos_x: X координата в тайлах
            pos_y: Y координата в тайлах
            width: Ширина объекта в пикселях
            height: Высота объекта в пикселях
            inner_rect_ratio: Коэффициент размера внутреннего прямоугольника (0.0-1.0)
            offset_x: Смещение по X в пикселях
            offset_y: Смещение по Y в пикселях
        """
        super().__init__(groups, image, pos_x, pos_y, width, height, offset_x, offset_y)
        
        # Создаем внутренний прямоугольник для более точных коллизий
        inner_width = int(width * inner_rect_ratio)
        inner_height = int(height * inner_rect_ratio)
        
        self.inner_rect = pg.Rect(
            self.rect.x + (width - inner_width) // 2,
            self.rect.y + (height - inner_height) // 2,
            inner_width,
            inner_height
        )
        
        self._inner_rect_ratio = inner_rect_ratio
        self._collision_groups: List[pg.sprite.Group] = []
    
    def add_collision_group(self, group: pg.sprite.Group) -> None:
        """
        Добавляет группу для проверки коллизий.
        
        Args:
            group: Группа спрайтов для проверки коллизий
        """
        if group not in self._collision_groups:
            self._collision_groups.append(group)
    
    def remove_collision_group(self, group: pg.sprite.Group) -> None:
        """
        Удаляет группу из проверки коллизий.
        
        Args:
            group: Группа спрайтов для удаления
        """
        if group in self._collision_groups:
            self._collision_groups.remove(group)
    
    def update_inner_rect(self) -> None:
        """Обновляет позицию внутреннего прямоугольника"""
        inner_width = int(self._width * self._inner_rect_ratio)
        inner_height = int(self._height * self._inner_rect_ratio)
        
        self.inner_rect.x = self.rect.x + (self._width - inner_width) // 2
        self.inner_rect.y = self.rect.y + (self._height - inner_height) // 2
        self.inner_rect.width = inner_width
        self.inner_rect.height = inner_height
    
    def set_inner_rect_ratio(self, ratio: float) -> None:
        """
        Устанавливает коэффициент размера внутреннего прямоугольника.
        
        Args:
            ratio: Новый коэффициент (0.0-1.0)
        """
        self._inner_rect_ratio = max(0.0, min(1.0, ratio))
        self.update_inner_rect()
    
    def set_inner_rect_custom(self, x: int, y: int, width: int, height: int) -> None:
        """
        Устанавливает кастомные параметры внутреннего прямоугольника.
        
        Args:
            x: Смещение по X относительно основного прямоугольника
            y: Смещение по Y относительно основного прямоугольника
            width: Ширина внутреннего прямоугольника
            height: Высота внутреннего прямоугольника
        """
        self.inner_rect.x = self.rect.x + x
        self.inner_rect.y = self.rect.y + y
        self.inner_rect.width = width
        self.inner_rect.height = height
    
    def check_collision_with_group(self, group: pg.sprite.Group) -> Optional[pg.sprite.Sprite]:
        """
        Проверяет коллизию с объектами из группы.
        
        Args:
            group: Группа спрайтов для проверки
            
        Returns:
            Первый объект, с которым произошла коллизия, или None
        """
        for sprite in group:
            if sprite != self and pg.sprite.collide_rect(self, sprite):
                return sprite
        return None
    
    def check_inner_collision_with_group(self, group: pg.sprite.Group) -> Optional[pg.sprite.Sprite]:
        """
        Проверяет коллизию внутреннего прямоугольника с объектами из группы.
        
        Args:
            group: Группа спрайтов для проверки
            
        Returns:
            Первый объект, с которым произошла коллизия, или None
        """
        for sprite in group:
            if sprite != self and hasattr(sprite, 'inner_rect'):
                if self.inner_rect.colliderect(sprite.inner_rect):
                    return sprite
        return None
    
    def handle_wall_collision(self, x_delta: int, y_delta: int, walls_group: pg.sprite.Group) -> None:
        """
        Обрабатывает коллизии со стенами.
        
        Args:
            x_delta: Изменение позиции по X
            y_delta: Изменение позиции по Y
            walls_group: Группа стен
        """
        for wall in walls_group:
            if pg.sprite.collide_rect(self, wall):
                # Откатываем движение в зависимости от направления
                if x_delta < 0:
                    self.rect.left = wall.rect.right
                elif x_delta > 0:
                    self.rect.right = wall.rect.left
                    
                if y_delta < 0:
                    self.rect.top = wall.rect.bottom
                elif y_delta > 0:
                    self.rect.bottom = wall.rect.top
                
                # Обновляем внутренний прямоугольник
                self.update_inner_rect()
                break
    
    def move_with_collision(self, dx: int, dy: int, walls_group: pg.sprite.Group) -> None:
        """
        Перемещает объект с проверкой коллизий со стенами.
        
        Args:
            dx: Смещение по X
            dy: Смещение по Y
            walls_group: Группа стен
        """
        # Сначала двигаемся по X
        if dx != 0:
            self.rect.x += dx
            self.handle_wall_collision(dx, 0, walls_group)
        
        # Затем двигаемся по Y
        if dy != 0:
            self.rect.y += dy
            self.handle_wall_collision(0, dy, walls_group)
        
        # Обновляем внутренний прямоугольник
        self.update_inner_rect()
    
    def is_colliding_with(self, other: 'BaseCollidable') -> bool:
        """
        Проверяет коллизию с другим объектом.
        
        Args:
            other: Другой объект с коллизиями
            
        Returns:
            True если объекты пересекаются
        """
        return pg.sprite.collide_rect(self, other)
    
    def is_inner_colliding_with(self, other: 'BaseCollidable') -> bool:
        """
        Проверяет коллизию внутренних прямоугольников.
        
        Args:
            other: Другой объект с коллизиями
            
        Returns:
            True если внутренние прямоугольники пересекаются
        """
        return self.inner_rect.colliderect(other.inner_rect)
    
    def get_distance_to(self, other: 'BaseCollidable') -> float:
        """
        Вычисляет расстояние до другого объекта.
        
        Args:
            other: Другой объект
            
        Returns:
            Евклидово расстояние между центрами объектов
        """
        dx = self.center[0] - other.center[0]
        dy = self.center[1] - other.center[1]
        return (dx * dx + dy * dy) ** 0.5
    
    def set_position(self, x: int, y: int) -> None:
        """Переопределяем для обновления внутреннего прямоугольника"""
        super().set_position(x, y)
        self.update_inner_rect()
    
    def move(self, dx: int, dy: int) -> None:
        """Переопределяем для обновления внутреннего прямоугольника"""
        super().move(dx, dy)
        self.update_inner_rect()
    
    def set_size(self, width: int, height: int) -> None:
        """Переопределяем для обновления внутреннего прямоугольника"""
        super().set_size(width, height)
        self.update_inner_rect() 