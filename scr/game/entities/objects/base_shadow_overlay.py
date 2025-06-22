import pygame as pg
from typing import Optional

from game.settings import SHADOW_WIDTH, SHADOW_HEIGHT, BLACK
from game.groups import all_sprites_group, shadow_overlay_group


class BaseShadowOverlay(pg.sprite.Sprite):
    """
    Базовый класс для теневых наложений в системе освещения.
    
    Каждый элемент представляет собой черный квадрат с настраиваемой прозрачностью,
    который накладывается поверх игровых объектов для создания эффекта теней.
    """
    
    def __init__(self, pos_x: int, pos_y: int):
        """
        Инициализирует теневой элемент.
        
        Args:
            pos_x: X координата в сетке теней
            pos_y: Y координата в сетке теней
        """
        super().__init__(all_sprites_group, shadow_overlay_group)

        # Создаем прямоугольник для позиционирования
        self.rect = pg.Rect(
            pos_x * SHADOW_WIDTH, 
            pos_y * SHADOW_HEIGHT, 
            SHADOW_WIDTH, 
            SHADOW_HEIGHT
        )
        
        # Создаем поверхность для отрисовки
        self.image = pg.Surface((SHADOW_WIDTH, SHADOW_HEIGHT))
        self.image.fill(BLACK)
        
        # Начальная прозрачность - полностью темный
        self._brightness: int = 250
        self.image.set_alpha(self._brightness)
        
        # Кэш для оптимизации
        self._last_brightness: Optional[int] = None

    @property
    def brightness(self) -> int:
        """Текущая яркость элемента (0-255, где 0 - прозрачный, 255 - непрозрачный)"""
        return self._brightness

    def set_brightness(self, value: int) -> None:
        """
        Устанавливает яркость теневого элемента.
        
        Args:
            value: Значение яркости от 0 (прозрачный) до 255 (непрозрачный)
        """
        # Оптимизация: обновляем только если значение изменилось
        if self._last_brightness != value:
            self._brightness = max(0, min(255, value))  # Ограничиваем диапазон
            self.image.set_alpha(self._brightness)
            self._last_brightness = value

    def reset(self) -> None:
        """Сбрасывает элемент к начальному состоянию (полностью темный)"""
        self.set_brightness(250)
        self._last_brightness = None