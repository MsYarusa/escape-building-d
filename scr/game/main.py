import pygame as pg

from game.screens import show_start_screen, show_end_screen, show_dead_screen, show_main_screen, show_level_select_screen
from game.settings import WIN_SIZE, BLACK


if __name__ == "__main__":
    pg.init()
    pg.mixer.init()

    running = True

    active_screen_name = 'start'

    def set_active_screen(screen_name):
        global active_screen_name
        active_screen_name = screen_name

    pg.display.set_caption('Лабиринт')
    screen = pg.display.set_mode(WIN_SIZE)
    clock = pg.time.Clock()

    while running:

        current_screen_function = None

        if active_screen_name == 'start':
            current_screen_function = show_start_screen
        elif active_screen_name == 'main':
            current_screen_function = show_main_screen
        elif active_screen_name == 'dead':
            current_screen_function = show_dead_screen
        elif active_screen_name == 'end':
            current_screen_function = show_end_screen
        elif active_screen_name == 'level_select':
            current_screen_function = show_level_select_screen

        if current_screen_function:
            screen.fill(BLACK)

            should_continue_game = current_screen_function(set_active_screen, screen, clock)

            if not should_continue_game:
                running = False

