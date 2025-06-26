import pygame as pg


class Slider:
    """UI-элемент для регулировки значения, например, громкости."""

    def __init__(self, pos, size, initial_val, min_val, max_val):
        self.pos = pos
        self.size = size
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val

        self.track_rect = pg.Rect(self.pos, self.size)
        knob_radius = self.size[1] // 2 + 3
        self.knob_rect = pg.Rect(0, 0, knob_radius * 2, knob_radius * 2)
        self.knob_rect.centery = self.track_rect.centery
        self.set_knob_pos_from_value()

        self.dragging = False
        self.font = pg.font.SysFont('calibry', 28)

    def set_knob_pos_from_value(self):
        val_ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        self.knob_rect.centerx = self.track_rect.x + val_ratio * self.track_rect.width

    def set_value_from_knob_pos(self, mouse_x):
        x = max(self.track_rect.left, min(mouse_x, self.track_rect.right))
        val_ratio = (x - self.track_rect.left) / self.track_rect.width
        self.val = self.min_val + val_ratio * (self.max_val - self.min_val)
        self.knob_rect.centerx = x

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.track_rect.collidepoint(event.pos) or self.knob_rect.collidepoint(event.pos):
                self.dragging = True
                self.set_value_from_knob_pos(event.pos[0])
                return True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pg.MOUSEMOTION and self.dragging:
            self.set_value_from_knob_pos(event.pos[0])
            return True
        return False

    def draw(self, screen):
        pg.draw.rect(screen, (50, 50, 50), self.track_rect, border_radius=8)
        filled_width = self.knob_rect.centerx - self.track_rect.x
        if filled_width > 0:
            filled_rect = pg.Rect(self.track_rect.x, self.track_rect.y, filled_width, self.track_rect.height)
            pg.draw.rect(screen, (150, 150, 150), filled_rect, border_radius=8)
        pg.draw.circle(screen, (255, 255, 255), self.knob_rect.center, self.knob_rect.width // 2)
        percent_text = self.font.render(f'{int(self.val * 100)}%', True, (255, 255, 255))
        screen.blit(percent_text, (self.track_rect.right + 20, self.track_rect.centery - 15))
