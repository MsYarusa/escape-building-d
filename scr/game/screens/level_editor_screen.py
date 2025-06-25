import pygame as pg
from game.settings import WIN_WIDTH, WIN_HEIGHT, BLACK

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

PANEL_WIDTH = 220
GRID_AREA_WIDTH = WIN_WIDTH - PANEL_WIDTH - 40  # 40px отступ слева
GRID_AREA_HEIGHT = WIN_HEIGHT - 100  # 100px отступ сверху/снизу


def show_level_editor_screen(set_active_screen, screen, clock):
    font = pg.font.SysFont('calibry', 36)
    title = font.render('Редактор уровней', True, (255, 255, 255))
    title_rect = title.get_rect(center=(WIN_WIDTH // 2, 30))

    # Начальные размеры сетки
    grid_rows = 20
    grid_cols = 40
    grid = [['.' for _ in range(grid_cols)] for _ in range(grid_rows)]

    selected_tile = 0
    selected_entity = None
    # Смещение видимой области (скроллинг)
    view_row = 0
    view_col = 0

    # Список сущностей: (тип, row, col)
    entities = []

    # Режим: 0 - карта, 1 - сущности
    mode = 0

    running = True
    while running:
        clock.tick(60)
        screen.fill(BLACK)
        screen.blit(title, title_rect)

        # Панель справа
        panel_x = WIN_WIDTH - PANEL_WIDTH
        pg.draw.rect(screen, (40, 40, 40), (panel_x, 0, PANEL_WIDTH, WIN_HEIGHT))
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

        # Компактные кнопки изменения размера
        btn_font = pg.font.SysFont('calibry', 22)
        size_y = 350
        # Строки
        screen.blit(btn_font.render('Строк:', True, (255,255,255)), (panel_x + 30, size_y))
        minus_row = pg.Rect(panel_x + 100, size_y, 28, 28)
        plus_row = pg.Rect(panel_x + 140, size_y, 28, 28)
        pg.draw.rect(screen, (120,120,120), minus_row, border_radius=6)
        pg.draw.rect(screen, (120,120,120), plus_row, border_radius=6)
        screen.blit(btn_font.render('-', True, (0,0,0)), (minus_row.x+7, minus_row.y+2))
        screen.blit(btn_font.render('+', True, (0,0,0)), (plus_row.x+7, plus_row.y+2))
        screen.blit(btn_font.render(str(grid_rows), True, (255,255,255)), (panel_x + 180, size_y+2))
        # Столбцы
        screen.blit(btn_font.render('Столбцы:', True, (255,255,255)), (panel_x + 30, size_y+40))
        minus_col = pg.Rect(panel_x + 130, size_y+40, 28, 28)
        plus_col = pg.Rect(panel_x + 170, size_y+40, 28, 28)
        pg.draw.rect(screen, (120,120,120), minus_col, border_radius=6)
        pg.draw.rect(screen, (120,120,120), plus_col, border_radius=6)
        screen.blit(btn_font.render('-', True, (0,0,0)), (minus_col.x+7, minus_col.y+2))
        screen.blit(btn_font.render('+', True, (0,0,0)), (plus_col.x+7, plus_col.y+2))
        screen.blit(btn_font.render(str(grid_cols), True, (255,255,255)), (panel_x + 210, size_y+42))

        # Кнопки управления
        btn_font2 = pg.font.SysFont('calibry', 28)
        save_btn = pg.Rect(panel_x + 30, WIN_HEIGHT - 160, 160, 40)
        clear_btn = pg.Rect(panel_x + 30, WIN_HEIGHT - 110, 160, 40)
        back_btn = pg.Rect(panel_x + 30, WIN_HEIGHT - 60, 160, 40)
        pg.draw.rect(screen, (80, 180, 80), save_btn)
        pg.draw.rect(screen, (180, 80, 80), clear_btn)
        pg.draw.rect(screen, (80, 80, 180), back_btn)
        screen.blit(btn_font2.render('Сохранить', True, (0, 0, 0)), (save_btn.x + 20, save_btn.y + 5))
        screen.blit(btn_font2.render('Очистить', True, (0, 0, 0)), (clear_btn.x + 30, clear_btn.y + 5))
        screen.blit(btn_font2.render('Назад', True, (0, 0, 0)), (back_btn.x + 45, back_btn.y + 5))

        # Сетка (только видимая часть)
        max_visible_cols = GRID_AREA_WIDTH // TILE_SIZE
        max_visible_rows = GRID_AREA_HEIGHT // TILE_SIZE
        grid_x0 = 20
        grid_y0 = 70
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
                for idx, (etype, erow, ecol) in enumerate(entities):
                    if erow == grid_row and ecol == grid_col:
                        icon = [e[2] for e in ENTITY_TYPES if e[0] == etype][0]
                        ent_text = font.render(icon, True, (255, 200, 80))
                        screen.blit(ent_text, (x + 6, y + 2))

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return False
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
                                else:
                                    # Добавить сущность, если её нет в этой клетке
                                    if not any(erow == grid_row and ecol == grid_col for _, erow, ecol in entities):
                                        etype = ENTITY_TYPES[selected_entity][0]
                                        entities.append((etype, grid_row, grid_col))
                            elif event.button == 3:
                                # Удалить сущность по правому клику
                                entities = [e for e in entities if not (e[1] == grid_row and e[2] == grid_col)]
                # Кнопки управления размером
                if event.button == 1:
                    if minus_row.collidepoint(mx, my) and grid_rows > MIN_ROWS:
                        grid_rows -= 1
                        grid = [row for i, row in enumerate(grid) if i < grid_rows]
                        entities = [e for e in entities if e[1] < grid_rows]
                    if plus_row.collidepoint(mx, my) and grid_rows < MAX_ROWS:
                        grid_rows += 1
                        grid.append(['.' for _ in range(grid_cols)])
                    if minus_col.collidepoint(mx, my) and grid_cols > MIN_COLS:
                        grid_cols -= 1
                        for row in grid:
                            del row[-1]
                        entities = [e for e in entities if e[2] < grid_cols]
                    if plus_col.collidepoint(mx, my) and grid_cols < MAX_COLS:
                        grid_cols += 1
                        for row in grid:
                            row.append('.')
                # Кнопки управления
                if event.button == 1:
                    if save_btn.collidepoint(mx, my):
                        pass  # TODO: сохранить уровень
                    if clear_btn.collidepoint(mx, my):
                        grid = [['.' for _ in range(grid_cols)] for _ in range(grid_rows)]
                        entities = []
                    if back_btn.collidepoint(mx, my):
                        set_active_screen('level_select')
                        return True 