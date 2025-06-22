import pygame as pg
from typing import Tuple

from game.settings import TILE_WIDTH, TILE_HEIGHT
from game.resources import tile_images
from game.groups import all_sprites_group, tiles_group, walls_group
from game.entities.base_renderable import BaseRenderable


class BaseTile(BaseRenderable):
    """
    Базовый класс для тайлов уровня.
    
    Наследует от BaseRenderable, что предоставляет:
    - Управление изображениями
    - Позиционирование
    - Размеры
    - Группы спрайтов
    """
    
    def __init__(self, tile_type: str, pos_x: int, pos_y: int):
        """
        Инициализирует тайл.
        
        Args:
            tile_type: Тип тайла (ключ в tile_images)
            pos_x: X координата в тайлах
            pos_y: Y координата в тайлах
        """
        # Получаем изображение тайла
        image = tile_images.get(tile_type)
        if not image:
            raise ValueError(f"Неизвестный тип тайла: {tile_type}")
        
        # Определяем группы для тайла
        groups: Tuple[pg.sprite.Group, ...] = (all_sprites_group, tiles_group)
        
        # Стены добавляются в дополнительную группу
        if tile_type == 'wall':
            groups = groups + (walls_group,)
        
        super().__init__(
            groups=groups,
            image=image,
            pos_x=pos_x,
            pos_y=pos_y,
            width=TILE_WIDTH,
            height=TILE_HEIGHT
        )
        
        self.tile_type = tile_type

    def update(self, *args, **kwargs) -> None:
        """
        Обновление тайла (не требуется для статических объектов).
        Реализован для совместимости с абстрактным методом.
        """
        pass