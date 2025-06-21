from game.groups import player_group

from game.entities.objects.interactable import BaseInteractableObject


class LockedDoorExit(BaseInteractableObject):
    def __init__(self, pos_x, pos_y):
        super().__init__('pair_door', pos_x, pos_y)
        self.pair = None

    def set_pair(self, another):
        self.pair = another

    def interact(self):
        for player in player_group:
            player.rect.x = self.pair.rect.x
            player.rect.y = self.pair.rect.y
            player.set_inner_rect()