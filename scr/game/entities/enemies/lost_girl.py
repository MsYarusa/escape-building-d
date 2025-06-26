from game.entities.enemies import BaseSoul


class LostGirl(BaseSoul):
    def __init__(self, pos_x, pos_y):
        super().__init__('lost_girl', pos_x, pos_y)

        self.movement_timer = 0
        self.movement_cooldown = 30
        self.is_moving = True

    def update(self, player, lighting_system, level, player_it):

        self.movement_timer += 1

        # Если таймер достиг кулдауна, переключаем флаг движения и сбрасываем таймер
        if self.movement_timer >= self.movement_cooldown:
            self.is_moving = not self.is_moving  # Переключаем состояние: стоял -> движется, движется -> стоит
            self.movement_timer = 0

        if self.is_moving:
            self.move(player)

        super().update(player, lighting_system, level, player_it)
