import pygame as pg

from game.settings import (
    LEVEL_PATH,
    WIN_SIZE,
    WIN_WIDTH,
    TILE_WIDTH,
    TILE_HEIGHT,
    BLACK
)
from game.levels import load_level, generate_level
from game.camera import Camera

from game.groups import (
    replica_group,
    text_boxes_group,
    player_group,
    enemies_group,
    stairs_group,
    vents_group,
    keys_group,
    all_sprites_group
)
from game.ui import Hint, Replica, Button
from game.screens import dead_screen, start_screen, end_screen

def main():

    def pause():
        if paused:
            shadow.set_alpha(120)
        else:
            shadow.set_alpha(0)

    screen = pg.display.set_mode(WIN_SIZE)
    pg.display.set_caption('Лабиринт')

    level = load_level(LEVEL_PATH)
    player = generate_level(level)

    total_level_width = len(level[0]) * TILE_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * TILE_HEIGHT  # высоту

    shadow = pg.Surface((total_level_width, total_level_height))
    shadow.fill(BLACK)
    shadow.set_alpha(0)

    camera = Camera(total_level_width, total_level_height)
    hint = Hint()
    replica = Replica()
    replica.add(replica_group)
    pause_btn = Button((WIN_WIDTH - TILE_WIDTH, 0), 'pause')
    pause_btn.add(text_boxes_group)

    clock = pg.time.Clock()
    FPS = 90
    player_it = 0


    running = True
    paused = False
    dead = False
    end = False
    while running:

        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                event_pos = (event.pos[0] - camera.rect.x, event.pos[1] - camera.rect.y)
                if pause_btn.pressed(event_pos):
                    paused = not paused
                    pause()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    player.left = True
                if event.key == pg.K_w or event.key == pg.K_UP:
                    player.up = True
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    player.down = True
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    player.right = True
                if event.key == pg.K_e:
                    hint.hide()
                    if player.check_obj():
                        player.check_obj().interact()
                if event.key == pg.K_SPACE:
                    replica.change_text()
                if event.key == pg.K_ESCAPE:
                    pause_btn.change_state()
                    paused = not paused
                    pause()
            if event.type == pg.KEYUP:
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    player.left = False
                if event.key == pg.K_w or event.key == pg.K_UP:
                    player.up = False
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    player.down = False
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    player.right = False

        if not paused:
            if player_it % 2 == 0:
                player_group.update(level, player_it)
                enemies_group.update(level, player_it)
                stairs_group.update(level)
                vents_group.update(level)
                keys_group.update(level)
            player_it += 1

        if player.is_attacked():
            dead = True
            running = False

        for stairs in stairs_group:
            if stairs.opened:
                end = True
                running = False

        if player.check_obj():
            player.check_obj().make_hint(hint)
        else:
            hint.hide()

        screen.fill(BLACK)
        camera.update(player)

        for obj in all_sprites_group:
            screen.blit(obj.image, camera.apply(obj))

        hint.update()
        replica.update()

        screen.blit(shadow, (0, 0))

        for obj in text_boxes_group:
            screen.blit(obj.image, camera.apply(obj))

        pg.display.flip()

    for obj in all_sprites_group:
        obj.kill()
    for obj in text_boxes_group:
        obj.kill()

    if dead:
        dead_screen()
    if end:
        end_screen()


if __name__ == "__main__":
    pg.init()
    start_screen()
