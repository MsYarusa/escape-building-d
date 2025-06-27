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
from game.screens.settings_screen import show_settings_screen
from game.settings import (
    TILE_WIDTH,
    TILE_HEIGHT,
    BLACK,
    FPS
)
from game.systems import LightingSystem
from game.ui import Hint, Replica, Button
from game.utils.audio_manager import play_music, stop_music, stop_all_sfx


def show_main_screen(set_active_screen, screen, clock):
    """
    Основной игровой экран.
    """

    def show_pause_menu():
        """
        Отрисовывает и обрабатывает меню паузы с корректной логикой кнопок.
        """
        game_background = screen.copy()
        overlay = pg.Surface((screen.get_width(), screen.get_height()))
        overlay.fill(BLACK)
        overlay.set_alpha(180)

        def render_pause_menu():
            font_title = pg.font.SysFont('calibry', 60, bold=True)
            title = font_title.render('Пауза', True, (255, 255, 255))
            title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
            btn_size = (320, 70)
            continue_btn = Button((screen.get_width() // 2 - btn_size[0] // 2, 250), 'btn')
            continue_btn.scale(btn_size)
            continue_btn.set_text('Продолжить', font_size=36)
            settings_btn = Button((screen.get_width() // 2 - btn_size[0] // 2, 340), 'btn')
            settings_btn.scale(btn_size)
            settings_btn.set_text('Настройки', font_size=36)
            exit_btn = Button((screen.get_width() // 2 - btn_size[0] // 2, 430), 'btn')
            exit_btn.scale(btn_size)
            exit_btn.set_text('Выйти в меню', font_size=36)
            buttons = [continue_btn, settings_btn, exit_btn]

            return title, title_rect, buttons, continue_btn, settings_btn, exit_btn

        title, title_rect, buttons, continue_btn, settings_btn, exit_btn = render_pause_menu()

        pressed_button = None
        paused_loop = True

        while paused_loop:
            screen.blit(game_background, (0, 0))
            screen.blit(overlay, (0, 0))
            screen.blit(title, title_rect)
            for btn in buttons:
                screen.blit(btn.image, btn.rect)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'quit_game'
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return 'continue'
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in buttons:
                        if btn.rect.collidepoint(event.pos):
                            btn.change_state()
                            pressed_button = btn
                            break
                if event.type == pg.VIDEORESIZE:
                    title, title_rect, buttons, continue_btn, settings_btn, exit_btn = render_pause_menu()
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    if pressed_button:
                        if pressed_button.rect.collidepoint(event.pos):
                            if pressed_button is continue_btn: return 'continue'
                            if pressed_button is exit_btn: return 'exit_to_menu'
                            if pressed_button is settings_btn:
                                pressed_button.change_state()
                                pg.display.flip()
                                if not show_settings_screen(set_active_screen, screen, clock, source_screen='pause'):
                                    return 'quit_game'
                                pressed_button = None
                                break
                        pressed_button.change_state()
                        pressed_button = None
        return 'continue'

    clear_all_groups()
    level = load_level(level_state.current_level_path)
    player = generate_level(level)
    play_music('game')
    camera = Camera(len(level[0]) * TILE_WIDTH, len(level) * TILE_HEIGHT)
    lighting_system = LightingSystem()

    def render_text_boxes():
        text_boxes_group.empty()
        replica_group.empty()

        hint = Hint(screen)
        replica = Replica(screen)
        replica.add(replica_group)

        return hint, replica

    hint, replica = render_text_boxes()

    player_it = 0
    running = True
    paused = False
    dead = False
    end = False
    try:
        level_name = level_state.current_level_path.split('Level_')[-1].split('.txt')[0]
        current_level_idx = int(level_name)
    except (ValueError, IndexError):
        current_level_idx = 1

    while running:
        if paused:
            action = show_pause_menu()
            if action == 'continue':
                paused = False

                keys = pg.key.get_pressed()
                player.left = keys[pg.K_a] or keys[pg.K_LEFT]
                player.right = keys[pg.K_d] or keys[pg.K_RIGHT]
                player.up = keys[pg.K_w] or keys[pg.K_UP]
                player.down = keys[pg.K_s] or keys[pg.K_DOWN]

            elif action == 'exit_to_menu':
                set_active_screen('start')
                return True
            elif action == 'quit_game':
                return False
            continue

        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.VIDEORESIZE:
                hint, replica = render_text_boxes()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    paused = True
                    continue
                if event.key in (pg.K_a, pg.K_LEFT): player.left = True
                if event.key in (pg.K_d, pg.K_RIGHT): player.right = True
                if event.key in (pg.K_w, pg.K_UP): player.up = True
                if event.key in (pg.K_s, pg.K_DOWN): player.down = True
                if event.key == pg.K_e:
                    hint.hide()
                    obj = player.check_obj()
                    if obj: obj.interact()
                if event.key == pg.K_SPACE:
                    replica.change_text()
            if event.type == pg.KEYUP:
                if event.key in (pg.K_a, pg.K_LEFT): player.left = False
                if event.key in (pg.K_d, pg.K_RIGHT): player.right = False
                if event.key in (pg.K_w, pg.K_UP): player.up = False
                if event.key in (pg.K_s, pg.K_DOWN): player.down = False

        if player_it % 2 == 0:
            player_group.update(level, player_it)
            for enemy in enemies_group:
                enemy.update(player, lighting_system, level, player_it)
            stairs_group.update(level)
            vents_group.update(level)
            keys_group.update(level)
        player_it += 1

        # Здесь определяется смерть, после чего цикл завершается
        if player.is_attacked():
            dead, running = True, False

        for stairs in stairs_group:
            if stairs.opened:
                end, running = True, False
        obj = player.check_obj()
        if obj:
            obj.make_hint(hint)
        else:
            hint.hide()
        lighting_system.update_lighting(player.get_position(), level)
        camera.update(player, screen)
        hint.update()
        replica.update()
        screen.fill(BLACK)
        for obj in all_sprites_group:
            screen.blit(obj.image, camera.apply(obj))
        for obj in text_boxes_group:
            screen.blit(obj.image, camera.apply(obj))
        pg.display.flip()

    stop_music()

    if dead:
        stop_all_sfx()
        set_active_screen('dead')
        clear_all_groups()
        lighting_system.clear_cache()
        return True

    if end:
        progress_manager.complete_level(current_level_idx)
        progress_manager.unlock_level(current_level_idx + 1)
        clear_all_groups()
        lighting_system.clear_cache()
        next_level = show_end_level_screen(set_active_screen, screen, clock, current_level_idx)
        if next_level is not None and next_level <= len(progress_manager.levels):
            level_path = os.path.join('..', 'assets', 'levels', progress_manager.levels[next_level - 1])
            level_state.set_current_level_path(level_path)
            return show_main_screen(set_active_screen, screen, clock)
        return True

    clear_all_groups()
    lighting_system.clear_cache()
    return False
