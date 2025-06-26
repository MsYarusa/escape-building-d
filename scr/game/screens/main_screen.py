import os
import pygame as pg

import game.level_state as level_state
from game.camera import Camera
from game.groups import (
    replica_group,
    text_boxes_group,
    player_group,
    enemies_group,
    stairs_group,
    vents_group,
    keys_group,
    all_sprites_group,
    clear_all_groups
)
from game.levels import load_level, generate_level
from game.progress_manager import progress_manager
from game.screens.end_level_screen import show_end_level_screen
from game.settings import (
    WIN_WIDTH,
    TILE_WIDTH,
    TILE_HEIGHT,
    BLACK,
    FPS
)
from game.systems import LightingSystem
from game.ui import Hint, Replica, Button
from game.utils.audio_manager import play_music, stop_music, play_sound


def show_main_screen(set_active_screen, screen, clock):
    """
    Основной игровой экран.
    
    Отвечает за:
    - Игровой цикл
    - Обработку событий
    - Обновление игровых объектов
    - Рендеринг
    - Систему освещения
    """

    def pause():
        """Переключает состояние паузы"""
        if paused:
            shadow.set_alpha(120)
        else:
            shadow.set_alpha(0)

    # Очищаем все группы спрайтов
    clear_all_groups()

    # Загружаем уровень и создаем игрока
    level = load_level(level_state.current_level_path)
    player = generate_level(level)

    # Запускаем игровую музыку
    play_music('game')

    # Вычисляем размеры уровня
    total_level_width = len(level[0]) * TILE_WIDTH
    total_level_height = len(level) * TILE_HEIGHT

    # Создаем поверхность для паузы
    shadow = pg.Surface((total_level_width, total_level_height))
    shadow.fill(BLACK)
    shadow.set_alpha(0)

    # Инициализируем системы
    camera = Camera(total_level_width, total_level_height)
    lighting_system = LightingSystem()

    # Создаем UI элементы
    hint = Hint()
    replica = Replica()
    replica.add(replica_group)
    pause_btn = Button((WIN_WIDTH - TILE_WIDTH, 0), 'pause')
    pause_btn.add(text_boxes_group)

    # Игровые переменные
    player_it = 0
    running = True
    paused = False
    dead = False
    end = False

    # Получаем индекс текущего уровня
    current_level_name = level_state.current_level_path.split('Level_')[-1].split('.txt')[0]
    try:
        current_level_idx = int(current_level_name)
    except Exception:
        current_level_idx = 1

    while running:
        clock.tick(FPS)

        # Обработка событий
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                event_pos = (event.pos[0] - camera.rect.x, event.pos[1] - camera.rect.y)
                if pause_btn.pressed(event_pos):
                    paused = not paused
                    pause()

            if event.type == pg.KEYDOWN:
                # Управление движением
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    player.left = True
                if event.key == pg.K_w or event.key == pg.K_UP:
                    player.up = True
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    player.down = True
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    player.right = True

                # Взаимодействие
                if event.key == pg.K_e:
                    hint.hide()
                    if player.check_obj():
                        player.check_obj().interact()

                # Управление репликами
                if event.key == pg.K_SPACE:
                    replica.change_text()

                # Пауза
                if event.key == pg.K_ESCAPE:
                    pause_btn.change_state()
                    paused = not paused
                    pause()

            if event.type == pg.KEYUP:
                # Остановка движения
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    player.left = False
                if event.key == pg.K_w or event.key == pg.K_UP:
                    player.up = False
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    player.down = False
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    player.right = False

        # Обновление игровой логики (только если не на паузе)
        if not paused:
            if player_it % 2 == 0:
                # Обновляем игрока как обычно
                player_group.update(level, player_it)

                # Обновляем врагов с помощью цикла, передавая все нужные аргументы
                for enemy in enemies_group:
                    enemy.update(player, lighting_system, level, player_it)

                # Обновляем остальные группы как обычно
                stairs_group.update(level)
                vents_group.update(level)
                keys_group.update(level)
            player_it += 1

        # Проверка условий завершения игры
        if player.is_attacked():
            dead = True
            running = False

        for stairs in stairs_group:
            if stairs.opened:
                end = True
                running = False

        # Обновление подсказок
        if player.check_obj():
            player.check_obj().make_hint(hint)
        else:
            hint.hide()

        # Обновление системы освещения
        lighting_system.update_lighting(player.get_position(), level)

        # Рендеринг
        screen.fill(BLACK)
        camera.update(player)

        # Отрисовка всех спрайтов
        for obj in all_sprites_group:
            screen.blit(obj.image, camera.apply(obj))

        # Обновление UI
        hint.update()
        replica.update()

        # Наложение паузы
        screen.blit(shadow, (0, 0))

        # Отрисовка текстовых элементов
        for obj in text_boxes_group:
            screen.blit(obj.image, camera.apply(obj))

        pg.display.flip()

    # Останавливаем музыку
    stop_music()

    # Очистка ресурсов
    for obj in all_sprites_group:
        obj.kill()
    for obj in text_boxes_group:
        obj.kill()

    # Очистка кэша системы освещения
    lighting_system.clear_cache()

    # Переход к соответствующему экрану
    if dead:
        set_active_screen('dead')
        return True

    if end:
        # Отмечаем уровень как завершённый и открываем следующий
        progress_manager.complete_level(current_level_idx)
        progress_manager.unlock_level(current_level_idx + 1)
        # Переходим на экран завершения уровня
        next_level = show_end_level_screen(set_active_screen, screen, clock, current_level_idx)
        if next_level is not None:
            # Если выбран следующий уровень, меняем путь и запускаем main_screen снова
            if next_level <= len(progress_manager.levels):
                from game.level_state import set_current_level_path
                set_current_level_path(os.path.join('..', 'assets', 'levels', progress_manager.levels[next_level - 1]))
                show_main_screen(set_active_screen, screen, clock)
        return True
