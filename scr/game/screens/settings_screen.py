import pygame as pg
from game.settings import BLACK
from game.ui import Button
from game.ui.slider import Slider
from game.settings_manager import settings_manager
from game.utils.audio_manager import update_volumes


def show_settings_screen(set_active_screen, screen, clock, source_screen='start'):
    # Если мы в режиме паузы, рисуем игровой экран на фоне
    if source_screen == 'pause':
        static_background = screen.copy()
    else:
        static_background = None

    overlay = pg.Surface((screen.get_width(), screen.get_height()))
    overlay.fill(BLACK)
    overlay.set_alpha(200)

    def render_screen():
        font_title = pg.font.SysFont('calibry', 56)
        font_label = pg.font.SysFont('calibry', 36)
        title = font_title.render('Настройки', True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 100))

        music_label = font_label.render('Громкость музыки', True, (255, 255, 255))
        sfx_label = font_label.render('Громкость эффектов', True, (255, 255, 255))

        slider_width = 400
        music_slider = Slider((screen.get_width() // 2 - slider_width // 2, 220), (slider_width, 20),
                              settings_manager.music_volume, 0, 1)
        sfx_slider = Slider((screen.get_width() // 2 - slider_width // 2, 320), (slider_width, 20),
                            settings_manager.sfx_volume, 0, 1)

        back_btn = Button((screen.get_width() // 2 - 150, 450), 'btn')
        back_btn.scale((300, 70))
        back_btn.set_text('Назад', font_size=36)

        return title, title_rect, music_label, sfx_label, music_slider, sfx_slider, back_btn

    title, title_rect, music_label, sfx_label, music_slider, sfx_slider, back_btn = render_screen()

    running = True
    while running:
        clock.tick(60)

        # Обновляем громкость в реальном времени
        if music_slider.val != settings_manager.music_volume or sfx_slider.val != settings_manager.sfx_volume:
            settings_manager.music_volume = music_slider.val
            settings_manager.sfx_volume = sfx_slider.val
            update_volumes()

        if static_background:
            screen.blit(static_background, (0, 0))

        screen.blit(overlay, (0, 0))
        screen.blit(title, title_rect)
        screen.blit(music_label, (music_slider.pos[0], music_slider.pos[1] - 45))
        screen.blit(sfx_label, (sfx_slider.pos[0], sfx_slider.pos[1] - 45))
        music_slider.draw(screen)
        sfx_slider.draw(screen)
        screen.blit(back_btn.image, back_btn.rect)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                settings_manager.save_settings()
                return False

            music_slider.handle_event(event)
            sfx_slider.handle_event(event)

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.pressed(event.pos):
                    settings_manager.save_settings()
                    if source_screen == 'pause':
                        return True  # Возвращаемся в меню паузы
                    else:
                        set_active_screen(source_screen)
                        return True  # Возвращаемся в главное меню
            if event.type == pg.VIDEORESIZE:
                title, title_rect, music_label, sfx_label, music_slider, sfx_slider, back_btn = render_screen()
    return True