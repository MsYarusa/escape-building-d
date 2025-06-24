import pygame as pg
import os
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

    back_btn = Button((30, 30), 'btn')
    back_btn.scale((180, 60))
    back_btn.set_text('Назад', font_size=28, color='black')

    font = pg.font.SysFont('calibry', 48)
    title = font.render('Выберите уровень', True, (255, 255, 255))
    title_rect = title.get_rect(center=(WIN_WIDTH // 2, 100))

    running = True
    while running:
        clock.tick(60)
        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        screen.blit(title, title_rect)

        # Формируем список отображаемых кнопок
        visible_btns = []
        for i in range(num_visible):
            idx = start_index + i
            pos = (WIN_WIDTH // 2 - btn_size[0] // 2, start_y + i * (btn_size[1] + gap))
            btn = Button(pos, 'btn')
            btn.scale(btn_size)
            # Первая кнопка — стрелка вверх, если можно листать вверх
            if i == 0 and start_index > 0:
                # Очищаем кнопку и рисуем стрелку
                btn.set_text('', font_size=1, color='black')
                draw_arrow(btn.image, direction='up', color=(0, 0, 0))
                visible_btns.append(('up', btn))
            # Последняя кнопка — стрелка вниз, если можно листать вниз
            elif i == num_visible - 1 and (start_index + num_visible) < len(level_files):
                btn.set_text('', font_size=1, color='black')
                draw_arrow(btn.image, direction='down', color=(0, 0, 0))
                visible_btns.append(('down', btn))
            # Обычные кнопки уровней
            elif idx < len(level_files):
                btn.set_text(f'Уровень {idx+1}', font_size=32, color='black')
                visible_btns.append(('level', btn, level_files[idx]))
        # Кнопка назад
        screen.blit(back_btn.image, (back_btn.rect.x, back_btn.rect.y))
        # Рисуем кнопки
        for item in visible_btns:
            btn = item[1]
            screen.blit(btn.image, (btn.rect.x, btn.rect.y))
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # Кнопка назад
                if back_btn.rect.collidepoint(event.pos):
                    set_active_screen('start')
                    return True
                # Кнопки меню
                for item in visible_btns:
                    btn = item[1]
                    if btn.rect.collidepoint(event.pos):
                        if item[0] == 'up':
                            start_index = max(0, start_index - 1)
                        elif item[0] == 'down':
                            start_index = min(len(level_files) - num_visible, start_index + 1)
                        elif item[0] == 'level':
                            set_current_level_path(os.path.join('..', 'assets', 'levels', item[2]))
                            set_active_screen('main')
                            return True
    return False 