
from load import *


moving = pg.sprite.Group()

button_images = {
    'pause': {
        False: load_image('images\\Buttons\\pause_dis.png'),
        True: load_image('images\\Buttons\\pause_act.png')
    },
    'btn': {
        False: load_image('images\\Buttons\\btn_dis.png', (0, 0, 0)),
        True: load_image('images\\Buttons\\btn_act.png', (0, 0, 0))
    }
}


class Button(pg.sprite.Sprite):
    def __init__(self, pos, button_type):
        super().__init__()
        self.pos = pos
        self.image = button_images[button_type][False]
        self.buff_image = button_images[button_type][True]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.type = button_type
        self.text = None
        self.size = (self.rect.width, self.rect.height)

    def set_text(self, text, font_size=18, color='black', font='calibry'):
        text_font = pg.font.SysFont(font, font_size)
        text_rendered = text_font.render(text, 0, pg.Color(color))
        text_rect = text_rendered.get_rect()
        text_rect.centerx = self.rect.width // 2
        text_rect.centery = self.rect.height // 2
        self.text = (text_rendered, text_rect)
        self.image.blit(*self.text)

    def scale(self, size):
        self.size = size
        self.image = pg.transform.scale(self.image, size)
        self.buff_image = pg.transform.scale(self.buff_image, size)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def change_state(self):
        self.image, self.buff_image = self.buff_image, self.image
        if self.text:
            self.image.blit(*self.text)

    def pressed(self, event_pos):
        x_in = self.rect.left < event_pos[0] < self.rect.right
        y_in = self.rect.top < event_pos[1] < self.rect.bottom

        if x_in and y_in:
            self.change_state()
            return True
        else:
            return False


class Text(pg.sprite.Sprite):
    def __init__(self):
        super().__init__(moving)
        self.text = ''
        self.size = (WIN_WIDTH - 4 * TILE_WIDTH, TILE_HEIGHT * 3)
        self.pos = (TILE_WIDTH * 2, WIN_HEIGHT - TILE_HEIGHT * 3)
        self.rect = pg.Rect(*self.pos, *self.size)
        self.image = pg.Surface(self.size)

        self.image.set_alpha(0)
        self.called_change = False

    def update(self):
        if self.text and self.called_change:
            self.image.set_alpha(200)
        elif self.called_change:
            self.image.set_alpha(0)
        self.called_change = False


class Replica(Text):
    def __init__(self):
        super().__init__()

        text_image = pg.transform.scale(load_image(
            'images\\replica.png'), self.size)
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

    def show(self):
        for door in doors:
            door.set_replica(self)

    def change_text(self):
        self.cur_text += 1
        self.called_change = True

        if self.cur_text >= len(self.text):
            self.cur_text = 0
            self.text = []
        else:
            self.render_text(self.text[self.cur_text], self.cur_speaker)


class Hint(Text):
    def __init__(self):
        super().__init__()
        self.font = pg.font.SysFont('cambria', 18)

    def hide(self):
        self.text = ''
        self.called_change = True

    def set_text(self, text):
        self.text = text
        self.called_change = True
        text_rendered = self.font.render(text, 0, pg.Color('white'))
        text_rect = text_rendered.get_rect()
        text_rect.centerx = self.size[0] // 2
        text_rect.bottom = self.size[1] - TILE_HEIGHT // 4
        self.image.blit(text_rendered, text_rect)
