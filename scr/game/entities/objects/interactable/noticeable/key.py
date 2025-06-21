from game.groups import keys_group

from game.entities.objects.interactable.noticeable import BaseNoticeableObject


class Key(BaseNoticeableObject):
    def __init__(self, pos_x, pos_y):
        super().__init__('key', pos_x, pos_y)
        self.add(keys_group)
        self.door = None
        self.number = None

    def set_door(self, door):
        self.door = door

    def set_number(self, number):
        self.door.number = number
        self.number = number
        self.info = 'Номер D' + str(number)
        self.door.info = 'Аудитория D' + str(number)

    def interact(self):
        self.type = 'key_collected'
        self.set_replica()
        self.door.locked = False
        self.kill()
