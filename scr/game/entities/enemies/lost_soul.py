from game.entities.enemies import BaseSoul


class LostSoul(BaseSoul):
    def __init__(self, pos_x, pos_y):
        super().__init__('lost_soul', pos_x, pos_y)

    def update(self, player, lighting_system, level, player_it):

        self.move(player)

        super().update(player, lighting_system, level, player_it)
