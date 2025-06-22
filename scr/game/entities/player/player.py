import pygame as pg
from typing import Optional

from game.resources import player_images
from game.utils.images import cut_sheet, load_image
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
    enemies_group,
    walls_group
)


class Player(pg.sprite.Sprite):
    """
    Класс игрока, отвечающий за управление персонажем и игровую логику.
    
    Включает в себя:
    - Движение персонажа
    - Анимацию
    - Коллизии со стенами
    - Взаимодействие с объектами
    - Проверку атак от врагов
    """
    
    def __init__(self, pos_x: int, pos_y: int):
        """
        Инициализирует игрока.
        
        Args:
            pos_x: X координата в тайлах
            pos_y: Y координата в тайлах
        """
        super().__init__(all_sprites_group, player_group)

        self.name = PLAYER_NAME

        # Загружаем и нарезаем спрайты анимации
        self.frames = cut_sheet(
            player_images['player']['img'],
            player_images['player']['cols'],
            player_images['player']['rows']
        )

        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        # Основной прямоугольник для коллизий
        self.rect = pg.Rect(
            pos_x * TILE_WIDTH + 6, 
            pos_y * TILE_HEIGHT, 
            PLAYER_RECT_X, 
            PLAYER_RECT_Y
        )
        
        # Внутренний прямоугольник для более точных коллизий
        self.inner_rect = pg.Rect(
            self.rect.x, 
            self.rect.y, 
            PLAYER_RECT_X // 2, 
            PLAYER_RECT_Y // 2
        )
        self.set_inner_rect()

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
        
        # Состояние движения
        self.step = 0
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def set_inner_rect(self) -> None:
        """Обновляет позицию внутреннего прямоугольника для коллизий"""
        self.inner_rect.x = self.rect.x + PLAYER_RECT_X // 4
        self.inner_rect.y = self.rect.y + PLAYER_RECT_Y // 4

    def set_name(self, name: str) -> None:
        """Устанавливает имя игрока"""
        self.name = name

    def check_obj(self) -> Optional[object]:
        """
        Проверяет, есть ли рядом интерактивный объект.
        
        Returns:
            Интерактивный объект или None
        """
        for obj in interactable_objects_group:
            if pg.sprite.collide_rect(self, obj):
                return obj
        return None

    def is_attacked(self) -> bool:
        """
        Проверяет, атакован ли игрок врагом.
        
        Returns:
            True если игрок атакован
        """
        for enemy in enemies_group:
            if self.inner_rect.colliderect(enemy.inner_rect):
                return True
        return False

    def update(self, level: list, player_it: int) -> None:
        """
        Обновляет состояние игрока.
        
        Args:
            level: Карта уровня
            player_it: Счетчик итераций для анимации
        """
        # Обновляем анимацию
        if player_it % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % 8 + self.step * 8
            self.image = self.frames[self.cur_frame]

        # Вычисляем изменение позиции
        x_delta = 0
        y_delta = 0

        if self.left:
            x_delta -= PLAYER_SPEED
            self.step = 3
        if self.right:
            x_delta += PLAYER_SPEED
            self.step = 1
        if self.up:
            y_delta -= PLAYER_SPEED
            self.step = 2
        if self.down:
            y_delta += PLAYER_SPEED
            self.step = 0

        # Сброс анимации при отсутствии движения
        if not (self.up or self.down or self.right or self.left):
            self.cur_frame = -1

        # Применяем движение с проверкой коллизий
        self.rect.x += x_delta
        self.collide(x_delta, 0)

        self.rect.y += y_delta
        self.collide(0, y_delta)

        # Обновляем внутренний прямоугольник
        self.set_inner_rect()

    def collide(self, x_delta: int, y_delta: int) -> None:
        """
        Обрабатывает коллизии со стенами.
        
        Args:
            x_delta: Изменение по X
            y_delta: Изменение по Y
        """
        for wall in walls_group:
            if pg.sprite.collide_rect(self, wall):
                # Откатываем движение в зависимости от направления
                if x_delta < 0:
                    self.rect.left = wall.rect.right
                if x_delta > 0:
                    self.rect.right = wall.rect.left
                if y_delta < 0:
                    self.rect.top = wall.rect.bottom
                if y_delta > 0:
                    self.rect.bottom = wall.rect.top

    def get_position(self) -> tuple[int, int]:
        """
        Возвращает текущую позицию игрока.
        
        Returns:
            Кортеж (x, y) с координатами центра игрока
        """
        return (self.rect.centerx, self.rect.centery)
