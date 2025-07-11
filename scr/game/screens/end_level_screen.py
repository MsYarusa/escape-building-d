import pygame as pg

from game.progress_manager import progress_manager
from game.utils.images import load_image
from game.ui import Button
from game.utils.audio_manager import play_sound
from game.settings import BLACK
from game.utils.path_helper import resource_path


def show_end_level_screen(set_active_screen, screen, clock, current_level_idx):
    def render_screen():
        screen.fill(BLACK)
        screen.blit(load_image(
            resource_path('assets\\images\\ui\\background.png')), (0, 0))
        font = pg.font.SysFont('calibry', 56)
        title = font.render('Уровень пройден!', True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 120))

        btn_size = (340, 80)
        next_pos = (screen.get_width() // 2 - btn_size[0] // 2, 260)
        select_pos = (screen.get_width() // 2 - btn_size[0] // 2, 370)
        exit_pos = (screen.get_width() // 2 - btn_size[0] // 2, 480)
        next_btn = Button(next_pos, 'btn')
        next_btn.scale(btn_size)
        next_btn.set_text('Следующий уровень', font_size=36)
        select_btn = Button(select_pos, 'btn')
        select_btn.scale(btn_size)
        select_btn.set_text('Выбор уровня', font_size=36)
        exit_btn = Button(exit_pos, 'btn')
        exit_btn.scale(btn_size)
        exit_btn.set_text('Выйти в меню', font_size=36)

        return title, title_rect, next_btn, select_btn, exit_btn

    title, title_rect, next_btn, select_btn, exit_btn = render_screen()

    play_sound('win')

    running = True
    while running:
        clock.tick(60)
        screen.blit(title, title_rect)
        screen.blit(next_btn.image, (next_btn.rect.x, next_btn.rect.y))
        screen.blit(select_btn.image, (select_btn.rect.x, select_btn.rect.y))
        screen.blit(exit_btn.image, (exit_btn.rect.x, exit_btn.rect.y))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.VIDEORESIZE:
                title, title_rect, next_btn, select_btn, exit_btn = render_screen()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if next_btn.pressed(event.pos):
                    if current_level_idx < len(progress_manager.levels):
                        set_active_screen('main')
                        return current_level_idx + 1

                    set_active_screen('start')
                    return None
                if select_btn.pressed(event.pos):
                    set_active_screen('level_select')
                    return None
                if exit_btn.pressed(event.pos):
                    set_active_screen('start')
                    return None
    return None
