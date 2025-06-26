import pygame as pg
from game.settings import BLACK
import os

# Максимальные размеры сетки
MAX_ROWS = 40
MAX_COLS = 80
MIN_ROWS = 5
MIN_COLS = 5
TILE_SIZE = 24

# Символы тайлов
TILE_TYPES = [
    ('#', 'Стена'),
    ('.', 'Пол'),
    ('@', 'Игрок'),
    ('x', 'Выход'),
]

# Сущности (объекты и враги)
ENTITY_TYPES = [
    ('door', 'Дверь', 'D'),
    ('locked_door', 'Закр. дверь', 'L'),
    ('vent', 'Вентиляция', 'V'),
    ('lost_soul', 'LostSoul', 'S'),
    ('cockroach', 'Таракан', 'C'),
]

# Описание параметров для каждого типа сущности
ENTITY_PARAMS = {
    'door': [('x', int), ('y', int)],
    'locked_door': [('x', int), ('y', int), ('x2', int), ('y2', int), ('param1', int), ('param2', int)],
    'vent': [('x', int), ('y', int), ('param1', int), ('param2', int)],
    'lost_soul': [('x', int), ('y', int)],
    'cockroach': [('x', int), ('y', int), ('x2', int), ('y2', int)],
}

PANEL_WIDTH = 220

def show_level_editor_screen(set_active_screen, screen, clock):
    font = pg.font.SysFont('calibry', 36)

    def render_title():
        title = font.render('Редактор уровней', True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 30))

        return title, title_rect

    def update_grid_area():
        grid_area_width = screen.get_width() - PANEL_WIDTH - 40  # 40px отступ слева
        grid_area_height = screen.get_height() - 100  # 100px отступ сверху/снизу

        return grid_area_width, grid_area_height

    grid_area_width, grid_area_height = update_grid_area()

    title, title_rect = render_title()

    # Начальные размеры сетки
    grid_rows = 20
    grid_cols = 20
    grid = [['.' for _ in range(grid_cols)] for _ in range(grid_rows)]

    selected_tile = 0
    selected_entity = None
    # Смещение видимой области (скроллинг)
    view_row = 0
    view_col = 0

    # Список сущностей: dict: type, row, col, params
    entities = []
    selected_entity_on_grid = None  # индекс выбранной сущности на сетке

    # Режим: 0 - карта, 1 - сущности
    mode = 0

    # Вспомогательная переменная для ввода значения параметра
    input_active = False
    input_value = ''
    input_param = None
    input_entity_idx = None
    input_param_type = None

    save_input_active = False
    save_input_value = ''
    save_message = ''

    running = True
    while running:
        clock.tick(60)
        screen.fill(BLACK)
        screen.blit(title, title_rect)

        # Панель справа
        panel_x = screen.get_width() - PANEL_WIDTH
        pg.draw.rect(screen, (40, 40, 40), (panel_x, 0, PANEL_WIDTH, screen.get_height()))
        panel_font = pg.font.SysFont('calibry', 28)

        # Кнопки разделов
        section_btn_font = pg.font.SysFont('calibry', 26, bold=True)
        map_btn = pg.Rect(panel_x + 10, 20, 90, 36)
        ent_btn = pg.Rect(panel_x + 120, 20, 90, 36)
        pg.draw.rect(screen, (200, 200, 80) if mode == 0 else (100, 100, 100), map_btn, border_radius=8)
        pg.draw.rect(screen, (80, 200, 200) if mode == 1 else (100, 100, 100), ent_btn, border_radius=8)
        screen.blit(section_btn_font.render('Карта', True, (0,0,0)), (map_btn.x+13, map_btn.y+4))
        screen.blit(section_btn_font.render('Сущности', True, (0,0,0)), (ent_btn.x+2, ent_btn.y+4))

        y_offset = 70
        # Панель выбора
        if mode == 0:
            for i, (symbol, name) in enumerate(TILE_TYPES):
                y = y_offset + i * 50
                color = (200, 200, 80) if selected_tile == i else (180, 180, 180)
                rect = pg.Rect(panel_x + 30, y, 40, 40)
                pg.draw.rect(screen, color, rect)
                text = panel_font.render(symbol, True, (0, 0, 0))
                screen.blit(text, (rect.x + 10, rect.y + 5))
                name_text = panel_font.render(name, True, (255, 255, 255))
                screen.blit(name_text, (rect.x + 60, rect.y + 5))
        else:
            for i, (etype, name, icon) in enumerate(ENTITY_TYPES):
                y = y_offset + i * 50
                color = (80, 200, 200) if selected_entity == i else (120, 120, 120)
                rect = pg.Rect(panel_x + 30, y, 40, 40)
                pg.draw.rect(screen, color, rect)
                text = panel_font.render(icon, True, (0, 0, 0))
                screen.blit(text, (rect.x + 10, rect.y + 5))
                name_text = panel_font.render(name, True, (255, 255, 255))
                screen.blit(name_text, (rect.x + 60, rect.y + 5))

        # Компактный блок изменения размеров (W/H)
        size_font = pg.font.SysFont('calibry', 26, bold=True)
        btn_font = pg.font.SysFont('calibry', 22)
        size_block_y = 350
        center_x = panel_x + PANEL_WIDTH // 2
        # W (ширина)
        w_label = size_font.render('W:', True, (255,255,255))
        w_label_rect = w_label.get_rect()
        w_label_rect.midleft = (panel_x + 30, size_block_y + 10)
        screen.blit(w_label, w_label_rect)
        minus_w = pg.Rect(center_x - 45, size_block_y, 28, 28)
        plus_w = pg.Rect(center_x + 45, size_block_y, 28, 28)
        pg.draw.rect(screen, (120,120,120), minus_w, border_radius=6)
        pg.draw.rect(screen, (120,120,120), plus_w, border_radius=6)
        screen.blit(btn_font.render('-', True, (0,0,0)), (minus_w.x+7, minus_w.y+2))
        screen.blit(btn_font.render('+', True, (0,0,0)), (plus_w.x+7, plus_w.y+2))
        w_val = size_font.render(str(grid_cols), True, (255,255,255))
        w_val_rect = w_val.get_rect(center=(center_x, size_block_y+14))
        screen.blit(w_val, w_val_rect)
        # H (высота)
        h_label = size_font.render('H:', True, (255,255,255))
        h_label_rect = h_label.get_rect()
        h_label_rect.midleft = (panel_x + 30, size_block_y + 50)
        screen.blit(h_label, h_label_rect)
        minus_h = pg.Rect(center_x - 45, size_block_y+40, 28, 28)
        plus_h = pg.Rect(center_x + 45, size_block_y+40, 28, 28)
        pg.draw.rect(screen, (120,120,120), minus_h, border_radius=6)
        pg.draw.rect(screen, (120,120,120), plus_h, border_radius=6)
        screen.blit(btn_font.render('-', True, (0,0,0)), (minus_h.x+7, minus_h.y+2))
        screen.blit(btn_font.render('+', True, (0,0,0)), (plus_h.x+7, plus_h.y+2))
        h_val = size_font.render(str(grid_rows), True, (255,255,255))
        h_val_rect = h_val.get_rect(center=(center_x, size_block_y+54))
        screen.blit(h_val, h_val_rect)

        # Кнопки управления
        btn_font2 = pg.font.SysFont('calibry', 28)
        save_btn = pg.Rect(panel_x + 30, screen.get_height() - 160, 160, 40)
        clear_btn = pg.Rect(panel_x + 30, screen.get_height() - 110, 160, 40)
        back_btn = pg.Rect(panel_x + 30, screen.get_height() - 60, 160, 40)
        pg.draw.rect(screen, (80, 180, 80), save_btn)
        pg.draw.rect(screen, (180, 80, 80), clear_btn)
        pg.draw.rect(screen, (80, 80, 180), back_btn)
        screen.blit(btn_font2.render('Сохранить', True, (0, 0, 0)), (save_btn.x + 20, save_btn.y + 5))
        screen.blit(btn_font2.render('Очистить', True, (0, 0, 0)), (clear_btn.x + 30, clear_btn.y + 5))
        screen.blit(btn_font2.render('Назад', True, (0, 0, 0)), (back_btn.x + 45, back_btn.y + 5))

        # Окно для ввода имени файла при сохранении
        if save_input_active:
            popup_w, popup_h = 340, 100
            popup_x = screen.get_width() // 2 - popup_w // 2
            popup_y = screen.get_height() // 2 - popup_h // 2
            popup_rect = pg.Rect(popup_x, popup_y, popup_w, popup_h)
            pg.draw.rect(screen, (30,30,30), popup_rect, border_radius=10)
            pg.draw.rect(screen, (80,180,80), popup_rect, 2, border_radius=10)
            font_popup = pg.font.SysFont('calibry', 26)
            screen.blit(font_popup.render('Имя файла:', True, (255,255,255)), (popup_x+20, popup_y+18))
            input_rect = pg.Rect(popup_x+150, popup_y+15, 150, 36)
            pg.draw.rect(screen, (255,255,255), input_rect, border_radius=6)
            input_text = font_popup.render(save_input_value, True, (0,0,0))
            screen.blit(input_text, (input_rect.x+8, input_rect.y+4))
            screen.blit(font_popup.render('.txt', True, (180,180,180)), (input_rect.x+input_rect.width+5, input_rect.y+4))
        # Сообщение об успешном сохранении
        if save_message:
            msg_font = pg.font.SysFont('calibry', 26, bold=True)
            msg_rect = pg.Rect(screen.get_width()//2-120, screen.get_height()//2-30, 240, 60)
            pg.draw.rect(screen, (30,120,30), msg_rect, border_radius=10)
            screen.blit(msg_font.render(save_message, True, (255,255,255)), (msg_rect.x+20, msg_rect.y+15))

        # Сетка (только видимая часть)
        max_visible_cols = grid_area_width // TILE_SIZE
        max_visible_rows = grid_area_height // TILE_SIZE
        grid_x0 = 20
        grid_y0 = 70
        # Нумерация столбцов (W)
        num_font = pg.font.SysFont('calibry', 18, bold=True)
        for col in range(max_visible_cols):
            grid_col = view_col + col
            if grid_col >= grid_cols:
                break
            x = grid_x0 + col * TILE_SIZE
            num_text = num_font.render(str(grid_col), True, (180,180,180))
            screen.blit(num_text, (x + 4, grid_y0 - 22))
        # Нумерация строк (H) — по центру ячейки
        for row in range(max_visible_rows):
            grid_row = view_row + row
            if grid_row >= grid_rows:
                break
            y = grid_y0 + row * TILE_SIZE
            num_text = num_font.render(str(grid_row), True, (180,180,180))
            text_rect = num_text.get_rect()
            text_rect.centery = y + TILE_SIZE // 2
            text_rect.right = grid_x0 - 6
            screen.blit(num_text, text_rect)
        for row in range(max_visible_rows):
            grid_row = view_row + row
            if grid_row >= grid_rows:
                break
            for col in range(max_visible_cols):
                grid_col = view_col + col
                if grid_col >= grid_cols:
                    break
                x = grid_x0 + col * TILE_SIZE
                y = grid_y0 + row * TILE_SIZE
                rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
                pg.draw.rect(screen, (100, 100, 100), rect, 1)
                symbol = grid[grid_row][grid_col]
                if symbol != '.':
                    tile_text = font.render(symbol, True, (255, 255, 255))
                    screen.blit(tile_text, (x + 2, y - 2))
                # Визуализация сущностей
                for idx, ent in enumerate(entities):
                    if ent['row'] == grid_row and ent['col'] == grid_col:
                        icon = [e[2] for e in ENTITY_TYPES if e[0] == ent['type']][0]
                        ent_text = font.render(icon, True, (255, 200, 80))
                        screen.blit(ent_text, (x + 6, y + 2))
                        # Подсветка выбранной сущности
                        if selected_entity_on_grid == idx:
                            pg.draw.rect(screen, (255, 255, 0), rect, 3)
                            # Сохраняем параметры для popup, но не рисуем его здесь
                            popup_params = {
                                'idx': idx,
                                'ent': ent,
                                'x': x,
                                'y': y
                            }

        # После отрисовки сетки и объектов — рисуем popup, если нужно
        if 'popup_params' in locals() and selected_entity_on_grid == popup_params['idx']:
            ent = popup_params['ent']
            x = popup_params['x']
            y = popup_params['y']
            param_font = pg.font.SysFont('calibry', 20)
            param_list = ENTITY_PARAMS[ent['type']]
            param_w = 180
            param_h = 32 * len(param_list) + 36
            popup_x = x + TILE_SIZE + 8
            popup_y = y
            if popup_x + param_w > screen.get_width() - PANEL_WIDTH:
                popup_x = x - param_w - 8
            if popup_y + param_h > screen.get_height():
                popup_y = screen.get_height() - param_h - 8
            popup_rect = pg.Rect(popup_x-2, popup_y-2, param_w+4, param_h+4)
            pg.draw.rect(screen, (30,30,30), popup_rect, border_radius=10)
            pg.draw.rect(screen, (255,255,0), popup_rect, 2, border_radius=10)
            screen.blit(param_font.render('Параметры', True, (255,255,0)), (popup_x+10, popup_y+6))
            for i, (pname, ptype) in enumerate(param_list):
                val = ent['params'].get(pname, '')
                label = param_font.render(f'{pname}:', True, (200,200,200))
                screen.blit(label, (popup_x+10, popup_y+32 + i*28))
                val_rect = pg.Rect(popup_x+70, popup_y+30 + i*28, 90, 24)
                pg.draw.rect(screen, (255,255,255), val_rect)
                val_text = param_font.render(str(val), True, (0,0,0))
                screen.blit(val_text, (val_rect.x+5, val_rect.y+2))
                if input_active and input_entity_idx == popup_params['idx'] and input_param == pname:
                    pg.draw.rect(screen, (255,255,200), val_rect, border_radius=4)
                    input_text = param_font.render(input_value, True, (0,0,0))
                    screen.blit(input_text, (val_rect.x+5, val_rect.y+2))

        pg.display.flip()

        for event in pg.event.get():
            # Если сейчас идёт ввод значения параметра — обрабатываем только ввод
            if input_active:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        # Подтвердить ввод
                        try:
                            entities[input_entity_idx]['params'][input_param] = input_param_type(input_value)
                        except Exception:
                            pass
                        input_active = False
                        input_value = ''
                        input_param = None
                        input_entity_idx = None
                        input_param_type = None
                    elif event.key == pg.K_ESCAPE:
                        # Отмена
                        input_active = False
                        input_value = ''
                        input_param = None
                        input_entity_idx = None
                        input_param_type = None
                    elif event.key == pg.K_BACKSPACE:
                        input_value = input_value[:-1]
                    else:
                        if len(input_value) < 12 and (event.unicode.isprintable() or event.unicode.isdigit()):
                            input_value += event.unicode
                # Игнорируем все остальные события, пока идёт ввод
                continue
            if event.type == pg.QUIT:
                running = False
                return False
            if event.type == pg.VIDEORESIZE:
                title, title_rect = render_title()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    set_active_screen('level_select')
                    return True
                # Перемещение области просмотра
                if event.key == pg.K_LEFT:
                    view_col = max(0, view_col - 1)
                if event.key == pg.K_RIGHT:
                    view_col = min(max(0, grid_cols - max_visible_cols), view_col + 1)
                if event.key == pg.K_UP:
                    view_row = max(0, view_row - 1)
                if event.key == pg.K_DOWN:
                    view_row = min(max(0, grid_rows - max_visible_rows), view_row + 1)
            if event.type == pg.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Сначала проверяем клик по всплывающему окну параметров
                param_click_handled = False
                if selected_entity_on_grid is not None and 0 <= selected_entity_on_grid < len(entities):
                    ent = entities[selected_entity_on_grid]
                    param_list = ENTITY_PARAMS[ent['type']]
                    found = False
                    for row in range(max_visible_rows):
                        grid_row = view_row + row
                        if grid_row >= grid_rows:
                            continue
                        for col in range(max_visible_cols):
                            grid_col = view_col + col
                            if grid_col >= grid_cols:
                                continue
                            x = grid_x0 + col * TILE_SIZE
                            y = grid_y0 + row * TILE_SIZE
                            if ent['row'] == grid_row and ent['col'] == grid_col:
                                param_w = 180
                                param_h = 32 * len(param_list) + 36
                                popup_x = x + TILE_SIZE + 8
                                popup_y = y
                                if popup_x + param_w > screen.get_width() - PANEL_WIDTH:
                                    popup_x = x - param_w - 8
                                if popup_y + param_h > screen.get_height():
                                    popup_y = screen.get_height() - param_h - 8
                                for i, (pname, ptype) in enumerate(param_list):
                                    val_rect = pg.Rect(popup_x+70, popup_y+30 + i*28, 90, 24)
                                    if val_rect.collidepoint(mx, my):
                                        input_active = True
                                        input_value = str(ent['params'].get(pname, ''))
                                        input_param = pname
                                        input_entity_idx = selected_entity_on_grid
                                        input_param_type = ptype
                                        found = True
                                        param_click_handled = True
                                        break
                                break
                        if found:
                            break
                if param_click_handled:
                    # После активации режима ввода прекращаем обработку событий для этого кадра, но не выходим из функции экрана
                    break
                # Кнопки разделов
                if map_btn.collidepoint(mx, my):
                    mode = 0
                    selected_entity = None
                if ent_btn.collidepoint(mx, my):
                    mode = 1
                    selected_tile = 0
                # Панель выбора
                if mode == 0:
                    for i in range(len(TILE_TYPES)):
                        y = y_offset + i * 50
                        rect = pg.Rect(panel_x + 30, y, 40, 40)
                        if rect.collidepoint(mx, my):
                            selected_tile = i
                            selected_entity = None
                else:
                    for i in range(len(ENTITY_TYPES)):
                        y = y_offset + i * 50
                        rect = pg.Rect(panel_x + 30, y, 40, 40)
                        if rect.collidepoint(mx, my):
                            selected_entity = i
                # Клик по сетке (только видимая часть)
                for row in range(max_visible_rows):
                    grid_row = view_row + row
                    if grid_row >= grid_rows:
                        continue
                    for col in range(max_visible_cols):
                        grid_col = view_col + col
                        if grid_col >= grid_cols:
                            continue
                        x = grid_x0 + col * TILE_SIZE
                        y = grid_y0 + row * TILE_SIZE
                        rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
                        if rect.collidepoint(mx, my):
                            if event.button == 1:
                                if mode == 0:
                                    grid[grid_row][grid_col] = TILE_TYPES[selected_tile][0]
                                    selected_entity_on_grid = None
                                else:
                                    # Если клик по уже существующей сущности — выделить её
                                    for idx, ent in enumerate(entities):
                                        if ent['row'] == grid_row and ent['col'] == grid_col:
                                            selected_entity_on_grid = idx
                                            break
                                    else:
                                        # Добавить новую сущность
                                        etype = ENTITY_TYPES[selected_entity][0]
                                        params = {p[0]: 0 for p in ENTITY_PARAMS[etype]}
                                        params['x'] = grid_col
                                        params['y'] = grid_row
                                        new_ent = {'type': etype, 'row': grid_row, 'col': grid_col, 'params': params}
                                        entities.append(new_ent)
                                        selected_entity_on_grid = len(entities)-1
                            elif event.button == 3:
                                # Удалить сущность по правому клику
                                for idx, ent in enumerate(entities):
                                    if ent['row'] == grid_row and ent['col'] == grid_col:
                                        del entities[idx]
                                        if selected_entity_on_grid == idx:
                                            selected_entity_on_grid = None
                                        elif selected_entity_on_grid and selected_entity_on_grid > idx:
                                            selected_entity_on_grid -= 1
                                        break
                # Кнопки управления размером
                if event.button == 1:
                    if minus_h.collidepoint(mx, my) and grid_rows > MIN_ROWS:
                        grid_rows -= 1
                        grid = [row for i, row in enumerate(grid) if i < grid_rows]
                        entities = [e for e in entities if e['row'] < grid_rows]
                    if plus_h.collidepoint(mx, my) and grid_rows < MAX_ROWS:
                        grid_rows += 1
                        grid.append(['.' for _ in range(grid_cols)])
                    if minus_w.collidepoint(mx, my) and grid_cols > MIN_COLS:
                        grid_cols -= 1
                        for row in grid:
                            del row[-1]
                        entities = [e for e in entities if e['col'] < grid_cols]
                    if plus_w.collidepoint(mx, my) and grid_cols < MAX_COLS:
                        grid_cols += 1
                        for row in grid:
                            row.append('.')
                # Кнопки управления
                if event.button == 1:
                    if save_btn.collidepoint(mx, my):
                        save_input_active = True
                        save_input_value = ''
                        save_message = ''
                        break
                    if clear_btn.collidepoint(mx, my):
                        grid = [['.' for _ in range(grid_cols)] for _ in range(grid_rows)]
                        entities = []
                    if back_btn.collidepoint(mx, my):
                        set_active_screen('level_select')
                        return True
            if save_input_active:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        filename = save_input_value.strip()
                        if not filename.endswith('.txt'):
                            filename += '.txt'
                        if filename:
                            # Формируем содержимое файла
                            lines = []
                            for row in grid:
                                lines.append(''.join(row))
                            lines.append('---')
                            for ent in entities:
                                etype = ent['type']
                                params = [str(ent['params'][p[0]]) for p in ENTITY_PARAMS[etype]]
                                lines.append(f"{etype} {' '.join(params)}")
                            save_dir = os.path.join(os.path.dirname(__file__), '../../assets/levels')
                            save_dir = os.path.abspath(save_dir)
                            os.makedirs(save_dir, exist_ok=True)
                            save_path = os.path.join(save_dir, filename)
                            with open(save_path, 'w', encoding='utf-8') as f:
                                f.write('\n'.join(lines))
                            save_message = f'Сохранено: {filename}'
                        save_input_active = False
                        save_input_value = ''
                    elif event.key == pg.K_ESCAPE:
                        save_input_active = False
                        save_input_value = ''
                    elif event.key == pg.K_BACKSPACE:
                        save_input_value = save_input_value[:-1]
                    else:
                        if len(save_input_value) < 32 and event.unicode.isprintable():
                            save_input_value += event.unicode
                continue
    return True 