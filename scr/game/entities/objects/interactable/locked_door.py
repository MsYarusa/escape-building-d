from game.entities.objects.interactable import BaseInteractableObject
from game.groups import player_group
from game.resources import tile_images
from game.utils.audio_manager import play_sound


class LockedDoor(BaseInteractableObject):
    def __init__(self, pos_x, pos_y):
        super().__init__('locked_door', pos_x, pos_y)
        self.locked = True
        self.number = '???'
        self.pair = None

    def set_pair(self, another):
        self.pair = another

    def interact(self):
        if self.locked:
            play_sound('door_closed')
            self.set_replica()
        else:
            play_sound('door_open')

            for player in player_group:

                if not player.info_collected[self.type]:
                    self.type = 'unlocked_door'
                    self.info = ''
                    self.image = tile_images[self.type]
                    self.set_replica()

            for player in player_group:
                player.rect.x = self.pair.rect.x
                player.rect.y = self.pair.rect.y
                player.set_inner_rect()
