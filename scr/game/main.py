import pygame as pg

from game.screens import (
    show_start_screen, show_end_screen, show_dead_screen, show_main_screen,
    show_level_select_screen, show_level_editor_screen, show_settings_screen
)
from game.settings import WIN_SIZE, BLACK

if __name__ == "__main__":
    pg.init()

    # Словарь со всеми экранами для удобства
    screens = {
        'start': show_start_screen,
        'main': show_main_screen,
        'dead': show_dead_screen,
        'end': show_end_screen,
        'level_select': show_level_select_screen,
        'level_editor': show_level_editor_screen,
        'settings': show_settings_screen,
    }

    active_screen_name = 'start'
    active_screen_params = {}  # Словарь для параметров


    def set_active_screen(screen_data):
        # ИЗМЕНЕНИЕ: Используем 'global' для доступа к переменным уровня модуля
        global active_screen_name, active_screen_params

        if isinstance(screen_data, tuple):
            # Если передан кортеж, например ('settings', {'source_screen': 'start'})
            active_screen_name = screen_data[0]
            active_screen_params = screen_data[1]
        else:
            # Если передана просто строка
            active_screen_name = screen_data
            active_screen_params = {}


    pg.display.set_caption('Лабиринт')
    screen = pg.display.set_mode(WIN_SIZE)
    clock = pg.time.Clock()

    running = True
    while running:
        if active_screen_name in screens:
            current_screen_function = screens[active_screen_name]
            screen.fill(BLACK)

            # Вызываем функцию экрана, передавая ей параметры через **
            should_continue_game = current_screen_function(
                set_active_screen, screen, clock, **active_screen_params # Не трогать!
            )

            if not should_continue_game:
                running = False
        else:
            print(f"Ошибка: Экран '{active_screen_name}' не найден!")
            running = False

    pg.quit()