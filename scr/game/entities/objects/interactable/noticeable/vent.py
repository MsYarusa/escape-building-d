from game.groups import vents_group, player_group

from game.entities.objects.interactable.noticeable import BaseNoticeableObject


class Vent(BaseNoticeableObject):
    def __init__(self, pos_x, pos_y):
        super().__init__('vent', pos_x, pos_y)
        self.add(vents_group)
        self.pair = None

    def set_pair(self, another):
        self.pair = another

    def interact(self):
        for player in player_group:
            # Телепортируем игрока к парной вентиляции
            player.rect.x = self.pair.rect.x
            player.rect.y = self.pair.rect.y
            # Обновляем позицию в базовом классе
            player.x = player.rect.x
            player.y = player.rect.y
            # Обновляем внутренний прямоугольник для коллизий
            player.set_inner_rect()
