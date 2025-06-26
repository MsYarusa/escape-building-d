import pygame as pg

from game.settings import WIN_WIDTH
from game.ui import Button
from game.utils.audio_manager import play_music
from game.utils.images import load_image


def show_start_screen(set_active_screen, screen, clock):
    """
    Отображает главный экран игры с кнопками навигации.

    Args:
        set_active_screen: Функция для смены активного экрана.
        screen: Поверхность для отрисовки (экран Pygame).
        clock: Объект Pygame Clock для контроля FPS.

    Returns:
        bool: False, если игру нужно закрыть, иначе True.
    """
    # --- Инициализация ---

    # Загрузка и отрисовка фона и логотипа
    screen.blit(load_image('..\\assets\\images\\ui\\background.png'), (0, 0))
    logo = load_image('..\\assets\\images\\ui\\logo.png')
    logo_rect = logo.get_rect(center=(WIN_WIDTH // 2, 150))
    screen.blit(logo, logo_rect)

    # Определение размеров и позиций кнопок
    btn_size = (320, 70)
    start_pos = (WIN_WIDTH // 2 - btn_size[0] // 2, 320)
    select_pos = (WIN_WIDTH // 2 - btn_size[0] // 2, 410)
    settings_pos = (WIN_WIDTH // 2 - btn_size[0] // 2, 500)

    # Создание кнопок
    start_btn = Button(start_pos, 'btn')
    start_btn.scale(btn_size)
    start_btn.set_text('Начать игру', font_size=40)

    select_btn = Button(select_pos, 'btn')
    select_btn.scale(btn_size)
    select_btn.set_text('Выбор уровня', font_size=40)

    settings_btn = Button(settings_pos, 'btn')
    settings_btn.scale(btn_size)
    settings_btn.set_text('Настройки', font_size=40)

    # Запуск музыки для меню
    play_music('menu')

    # --- Основной цикл экрана ---
    running = True
    while running:
        # Обработка событий
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False  # Сигнал для полного закрытия игры

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if start_btn.pressed(event.pos):
                    set_active_screen('main')
                    return True  # Переключаем экран и выходим из этой функции

                if select_btn.pressed(event.pos):
                    set_active_screen('level_select')
                    return True  # Переключаем экран и выходим

                if settings_btn.pressed(event.pos):
                    # Переключаем на экран настроек, передавая параметры:
                    # 1. Имя экрана ('settings')
                    # 2. Словарь с параметром, откуда мы пришли ('source_screen': 'start')
                    set_active_screen(('settings', {'source_screen': 'start'}))
                    return True  # Переключаем экран и выходим

        # Отрисовка
        screen.blit(start_btn.image, start_btn.rect)
        screen.blit(select_btn.image, select_btn.rect)
        screen.blit(settings_btn.image, settings_btn.rect)

        # Обновление дисплея
        pg.display.flip()

    # Этот код выполнится, только если цикл завершится иначе (что маловероятно)
    return False
