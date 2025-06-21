import pygame as pg
import time

from game.utils.images import load_image
from game.settings import WIN_WIDTH, WIN_SIZE

from game.ui import Button

from game import main


def start_screen():
    screen = pg.display.set_mode(WIN_SIZE)
    pg.display.set_caption('Лабиринт')

    screen.blit(load_image(
        'images\\background.png'), (0, 0))

    logo = load_image(
        'images\\logo.png')
    logo_rect = logo.get_rect()
    logo_rect.x = WIN_WIDTH // 2 - logo_rect.width // 2
    logo_rect.y = 50

    screen.blit(logo, logo_rect)

    btn_size = (280, 80)
    start_pos = (WIN_WIDTH // 2 - btn_size[0] // 2, 400)
    start_btn = Button(start_pos, 'btn')
    start_btn.scale(btn_size)
    start_btn.set_text('Начать игру', font_size=40)

    start = False
    running = True
    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if start_btn.pressed(event.pos):
                    running = False
                    start = True

        screen.blit(start_btn.image, (start_btn.rect.x, start_btn.rect.y))

        pg.display.flip()
    time.sleep(0.2)
    if start:
        main()
