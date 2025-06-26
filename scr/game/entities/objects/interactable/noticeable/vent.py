from game.entities.objects.interactable.noticeable import BaseNoticeableObject
from game.groups import vents_group, player_group
from game.utils.audio_manager import play_sound


class Vent(BaseNoticeableObject):
    def __init__(self, pos_x, pos_y):
        super().__init__('vent', pos_x, pos_y)
        self.add(vents_group)
        self.pair = None

    def set_pair(self, another):
        self.pair = another

    def interact(self):
        play_sound('vent')

        for player in player_group:
            player.rect.x = self.pair.rect.x
            player.rect.y = self.pair.rect.y
            player.set_inner_rect()
