import pygame as pg

from game.resources import replica_images
from game.groups import interactable_objects_group
from game.settings import BLACK, TILE_WIDTH, TILE_HEIGHT

from game.ui.text_box import BaseTextBox


class Replica(BaseTextBox):
    def __init__(self, screen):
        super().__init__(screen)

        text_image = pg.transform.scale(replica_images['replica'], self.size)
        self.image.blit(text_image, (0, 0))

        self.text = []
        self.cur_text = 0
        self.cur_speaker = ''

        self.next = 'Нажмите "Пробел" чтобы продолжить'
        self.font = pg.font.SysFont('cambria', 24)
        self.next_font = pg.font.SysFont('cambria', 18)

    def render_text(self, text, speaker):
        self.image.fill(BLACK)
        text_rendered = self.font.render(text, 0, pg.Color('white'))
        speaker_rendered = self.font.render(speaker + ':', 0, pg.Color('white'))
        next_rendered = self.next_font.render(self.next, 0, pg.Color('white'))
        text_rect = text_rendered.get_rect()
        speaker_rect = speaker_rendered.get_rect()
        next_rect = next_rendered.get_rect()

        text_rect.x = speaker_rect.x = TILE_WIDTH // 4
        speaker_rect.y = TILE_HEIGHT // 4
        text_rect.y = TILE_HEIGHT // 2 + speaker_rect.height
        next_rect.centerx = self.size[0] // 2
        next_rect.bottom = self.size[1] - TILE_HEIGHT // 4

        self.image.blit(text_rendered, text_rect)
        self.image.blit(speaker_rendered, speaker_rect)
        self.image.blit(next_rendered, next_rect)

    def set_text(self, text, speaker):
        self.text = text
        self.cur_speaker = speaker
        self.render_text(self.text[self.cur_text], speaker)
        self.called_change = True

    # Раньше здесь использовалась группа doors, но я не имею понятия что это за группа
    def show(self):
        for object in interactable_objects_group:
            object.set_replica(self)

    def change_text(self):
        self.cur_text += 1
        self.called_change = True

        if self.cur_text >= len(self.text):
            self.cur_text = 0
            self.text = []
        else:
            self.render_text(self.text[self.cur_text], self.cur_speaker)
