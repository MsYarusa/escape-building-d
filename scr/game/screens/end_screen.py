import pygame as pg
import time

from game.ui import Button
from game.utils.images import load_image
from game.utils.path_helper import resource_path


def show_end_screen(set_active_screen, screen, clock):
    def render_screen():
        screen.blit(load_image(
            resource_path('assets\\images\\ui\\background.png')), (0, 0))

        label_font = pg.font.SysFont('calibry', 60)
        text_rendered = label_font.render('Пока все!', 0, pg.Color('white'))
        text_rect = text_rendered.get_rect()
        text_rect.centerx = screen.get_width() // 2
        text_rect.centery = 200
        screen.blit(text_rendered, text_rect)

        btn_size = (400, 80)
        menu_pos = (screen.get_width() // 2 - btn_size[0] // 2, screen.get_height() // 2 - btn_size[1] // 2)
        menu_btn = Button(menu_pos, 'btn')
        menu_btn.scale(btn_size)
        menu_btn.set_text('Начальный экран', font_size=40)

        return menu_btn

    menu_btn = render_screen()

    menu = False
    running = True
    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.VIDEORESIZE:
                menu_btn = render_screen()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if menu_btn.pressed(event.pos):
                    running = False
                    menu = True

        screen.blit(menu_btn.image, (menu_btn.rect.x, menu_btn.rect.y))

        pg.display.flip()

    time.sleep(0.2)

    if menu:
        set_active_screen('start')

        return True
