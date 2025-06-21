from game.resources import replicas
from game.groups import replica_group, player_group
from game.settings import TILE_WIDTH, TILE_HEIGHT

from game.entities.objects.interactable import BaseInteractableObject


class  BaseNoticeableObject(BaseInteractableObject):
    def __init__(self, obj_type, pos_x, pos_y):
        super().__init__(obj_type, pos_x, pos_y)

    def update(self, level):
        player = None
        for obj in player_group:
            player = obj

        replica = None
        for obj in replica_group:
            replica = obj

        player_x = player.rect.centerx
        player_y = player.rect.centery
        obj_x = self.rect.centerx
        obj_y = self.rect.centery

        dist = ((obj_x - player_x) ** 2 + (obj_y - player_y) ** 2) ** (1 / 2)

        if dist <= 3 * TILE_WIDTH and not player.info_collected[self.type]:
            is_visible = True
            player_pos = (player_x // TILE_WIDTH, player_y // TILE_HEIGHT)
            pos_x = obj_x // TILE_WIDTH
            pos_y = obj_y // TILE_HEIGHT

            while pos_x != player_pos[0] or pos_y != player_pos[1]:
                if pos_x != player_pos[0]:
                    pos_x += (-1) ** (pos_x > player_pos[0])
                if pos_y != player_pos[1]:
                    pos_y += (-1) ** (pos_y > player_pos[1])
                if level[pos_y][pos_x] == '#':
                    is_visible = False

            if is_visible:
                player.info_collected[self.type] = True
                replica.set_text(replicas[self.type], player.name)
