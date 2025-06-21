from game.groups import stairs_group

from game.entities.objects.interactable.noticeable import BaseNoticeableObject


class Stairs(BaseNoticeableObject):
    def __init__(self, pos_x, pos_y):
        super().__init__('stairs', pos_x, pos_y)
        self.add(stairs_group)
        self.opened = False

    def interact(self):
        self.opened = True
