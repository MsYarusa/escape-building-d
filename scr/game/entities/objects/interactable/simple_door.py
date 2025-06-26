from . import BaseInteractableObject
from game.utils.audio_manager import play_sound


class SimpleDoor(BaseInteractableObject):
    """
    Класс для простой, всегда запертой двери.
    Ее единственное действие - издать звук и показать реплику.
    """

    def __init__(self, pos_x, pos_y):
        super().__init__('door', pos_x, pos_y)

    def interact(self):
        # Проигрываем звук закрытой двери
        play_sound('door_closed')

        # Вызываем родительский метод, чтобы показать реплику
        super().interact()