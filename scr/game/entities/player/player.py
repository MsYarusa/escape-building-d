import pygame as pg
from typing import Optional

from game.resources import player_images
from game.settings import (
    TILE_WIDTH,
    TILE_HEIGHT,
    PLAYER_NAME,
    PLAYER_RECT_X,
    PLAYER_RECT_Y,
    PLAYER_SPEED
)
from game.groups import (
    all_sprites_group,
    player_group,
    interactable_objects_group,
    enemies_group
)
from game.entities.base_movable import BaseMovable


class Player(BaseMovable):
    """
    Класс игрока, отвечающий за управление персонажем и игровую логику.
    
    Наследует от BaseMovable, что предоставляет:
    - Движение персонажа
    - Анимацию
    - Коллизии со стенами
    - Управление состоянием движения
    """
    
    def __init__(self, pos_x: int, pos_y: int):
        """
        Инициализирует игрока.
        
        Args:
            pos_x: X координата в тайлах
            pos_y: Y координата в тайлах
        """
        # Получаем данные спрайта игрока
        sprite_data = player_images['player']
        
        super().__init__(
            groups=(all_sprites_group, player_group),
            sprite_sheet=sprite_data['img'],
            cols=sprite_data['cols'],
            rows=sprite_data['rows'],
            pos_x=pos_x,
            pos_y=pos_y,
            width=PLAYER_RECT_X,
            height=PLAYER_RECT_Y,
            speed=PLAYER_SPEED,
            animation_speed=10,
            inner_rect_ratio=0.5,  # Внутренний прямоугольник в 2 раза меньше
            offset_x=6,  # Смещение для центрирования
            offset_y=0
        )

        self.name = PLAYER_NAME

        # Информация о собранных объектах
        self.info_collected = {
            'lost_soul': False,
            'cockroach': False,
            'stairs': False,
            'vent': False,
            'key': False,
            'locked_door': False,
            'unlocked_door': True
        }

    def set_name(self, name: str) -> None:
        """Устанавливает имя игрока"""
        self.name = name

    def set_inner_rect(self) -> None:
        """
        Обновляет позицию внутреннего прямоугольника для коллизий.
        Метод добавлен для совместимости с другими объектами.
        """
        self.update_inner_rect()

    def check_obj(self) -> Optional[object]:
        """
        Проверяет, есть ли рядом интерактивный объект.
        
        Returns:
            Интерактивный объект или None
        """
        return self.check_collision_with_group(interactable_objects_group)

    def is_attacked(self) -> bool:
        """
        Проверяет, атакован ли игрок врагом.
        
        Returns:
            True если игрок атакован
        """
        return self.check_inner_collision_with_group(enemies_group) is not None

    def update(self, level: list, player_it: int) -> None:
        """
        Обновляет состояние игрока.
        
        Args:
            level: Карта уровня (не используется в новой версии)
            player_it: Счетчик итераций для анимации
        """
        # Обновляем движение и анимацию
        self.update_movement(player_it)

    def get_position(self) -> tuple[int, int]:
        """
        Возвращает текущую позицию игрока.
        
        Returns:
            Кортеж (x, y) с координатами центра игрока
        """
        return self.center
