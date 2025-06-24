import pygame as pg
import os
import time
from game.settings import WIN_WIDTH, WIN_HEIGHT, BLACK
from game.ui import Button
from game.level_state import set_current_level_path
from game.utils.images import load_image

def draw_arrow(surface, direction='up', color=(0, 0, 0)):
    w, h = surface.get_size()
    if direction == 'up':
        points = [(w // 2, h // 3), (16 * w // 40, 2 * h // 3), (24 * w // 40, 2 * h // 3)]
    else:  # 'down'
        points = [(w // 2, 2 * h // 3), (16 * w // 40, h // 3), (24 * w // 40, h // 3)]
    pg.draw.polygon(surface, color, points)

def show_level_select_screen(set_active_screen, screen, clock):
    background = load_image('..\\assets\\images\\ui\\background.png')

    levels_dir = os.path.join('..', 'assets', 'levels')
    level_files = [f for f in os.listdir(levels_dir) if f.endswith('.txt')]
    level_files.sort()
    num_visible = 4
    start_index = 0

    btn_size = (400, 70)
    gap = 20
    start_y = 180

    # Кнопка назад
    back_btn = Button((30, 30), 'btn')
    back_btn.scale((180, 60))
    back_btn.set_text('Назад', font_size=28, color='black')

    font = pg.font.SysFont('calibry', 48)
    title = font.render('Выберите уровень', True, (255, 255, 255))
    title_rect = title.get_rect(center=(WIN_WIDTH // 2, 100))

    # Создаём кнопки уровней и стрелок один раз
    level_btns = []
    for i in range(num_visible):
        pos = (WIN_WIDTH // 2 - btn_size[0] // 2, start_y + i * (btn_size[1] + gap))
        btn = Button(pos, 'btn')
        btn.scale(btn_size)
        level_btns.append(btn)
    up_btn = Button(level_btns[0].pos, 'btn')
    up_btn.scale(btn_size)
    up_btn.set_text('', font_size=1, color='black')
    draw_arrow(up_btn.image, direction='up', color=(0, 0, 0))
    down_btn = Button(level_btns[-1].pos, 'btn')
    down_btn.scale(btn_size)
    down_btn.set_text('', font_size=1, color='black')
    draw_arrow(down_btn.image, direction='down', color=(0, 0, 0))

    running = True
    back_pressed = False
    pressed_btn = None  # (item, btn)
    while running:
        clock.tick(60)
        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        screen.blit(title, title_rect)
        screen.blit(back_btn.image, (back_btn.rect.x, back_btn.rect.y))

        # Определяем, какие кнопки показывать
        visible = []
        for i in range(num_visible):
            idx = start_index + i
            btn = level_btns[i]
            btn.rect.y = start_y + i * (btn_size[1] + gap)
            is_pressed = pressed_btn and pressed_btn[1] is btn
            if i == 0 and start_index > 0:
                up_btn.rect.y = btn.rect.y
                screen.blit(up_btn.image, (up_btn.rect.x, up_btn.rect.y))
                visible.append(('up', up_btn))
            elif i == num_visible - 1 and (start_index + num_visible) < len(level_files):
                down_btn.rect.y = btn.rect.y
                screen.blit(down_btn.image, (down_btn.rect.x, down_btn.rect.y))
                visible.append(('down', down_btn))
            elif idx < len(level_files):
                if not is_pressed:
                    btn.set_text(f'Уровень {idx+1}', font_size=32, color='black')
                screen.blit(btn.image, (btn.rect.x, btn.rect.y))
                visible.append(('level', btn, level_files[idx]))
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.rect.collidepoint(event.pos):
                    back_btn.change_state()
                    back_pressed = True
                for item in visible:
                    btn = item[1]
                    if btn.rect.collidepoint(event.pos):
                        btn.change_state()
                        # Если это стрелка — перерисовать стрелку на новом image
                        if item[0] == 'up':
                            draw_arrow(btn.image, direction='up', color=(0, 0, 0))
                        elif item[0] == 'down':
                            draw_arrow(btn.image, direction='down', color=(0, 0, 0))
                        pressed_btn = (item, btn)
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if back_pressed:
                    if back_btn.rect.collidepoint(event.pos):
                        back_btn.change_state()
                        set_active_screen('start')
                        return True
                    else:
                        back_btn.change_state()
                    back_pressed = False
                if pressed_btn:
                    item, btn = pressed_btn
                    if btn.rect.collidepoint(event.pos):
                        btn.change_state()
                        # Если это стрелка — перерисовать стрелку на новом image
                        if item[0] == 'up':
                            draw_arrow(btn.image, direction='up', color=(0, 0, 0))
                        elif item[0] == 'down':
                            draw_arrow(btn.image, direction='down', color=(0, 0, 0))
                        pg.display.flip()
                        time.sleep(0.12)
                        if item[0] == 'up':
                            start_index = max(0, start_index - 1)
                        elif item[0] == 'down':
                            start_index = min(len(level_files) - num_visible, start_index + 1)
                        elif item[0] == 'level':
                            set_current_level_path(os.path.join('..', 'assets', 'levels', item[2]))
                            set_active_screen('main')
                            return True
                    else:
                        btn.change_state()
                        if item[0] == 'up':
                            draw_arrow(btn.image, direction='up', color=(0, 0, 0))
                        elif item[0] == 'down':
                            draw_arrow(btn.image, direction='down', color=(0, 0, 0))
                    pressed_btn = None
    return False 