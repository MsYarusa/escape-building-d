
from buttons import *
from objects import *
import time
from random import choice, randint

levels = ['Levels\\level_03.txt']


def generate_level(level):
    new_player, x, y, player_x, player_y = None, None, None, None, None

    height = len(level)
    width = len(level[0])

    y = 0
    while y < height:
        for x in range(width):
            if level[y][x] == '.':
                Tile('simple_floor', x, y)
            elif level[y][x] == '|':
                Tile('floor_near_wall', x, y)
            elif level[y][x] == '0':
                InteractableObject('door', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'x':
                Stairs(x, y)
            if level[y][x] == '@':
                height = y
                break
        y += 1

    entities = {}

    while y < len(level):
        entity, *pos = level[y].split()
        if entity not in entities.keys():
            entities[entity] = []
        entities[entity].append(tuple(map(lambda x: int(x), pos)))
        y += 1

    if 'locked_door' in entities.keys():
        numbers = []
        for pos in entities['locked_door']:
            locked_door = LockedDoor(pos[0], pos[1])
            pair_door = PairDoor(pos[2], pos[3])
            key = Key(pos[4], pos[5])
            key.set_door(locked_door)
            number = randint(0, 99)
            while number in numbers:
                number = randint(0, 99)
            key.set_number(900 + number)
            numbers.append(number)
            locked_door.set_pair(pair_door)
            pair_door.set_pair(locked_door)

    if 'vent' in entities.keys():
        for pos in entities['vent']:
            vent1 = Vent(pos[0], pos[1])
            vent2 = Vent(pos[2], pos[3])
            vent1.set_pair(vent2)
            vent2.set_pair(vent1)

    for pos in entities['player']:
        new_player = Player(*pos)

    if 'lost_soul' in entities.keys():
        for pos in entities['lost_soul']:
            LostSoul(*pos)

    if 'cockroach' in entities.keys():
        for pos in entities['cockroach']:
            Cockroach(*pos)

    for y in range(height * SHADOW_COEF):
        for x in range(width * SHADOW_COEF):
            Shadow(x, y)

    return new_player


class Camera:
    def __init__(self, total_width, total_height):
        self.rect = pg.Rect(0, 0, total_width, total_height)

    def apply(self, target):
        return target.rect.move(self.rect.topleft)

    def update(self, target):
        x, y = target.rect.centerx, target.rect.centery
        w, h = self.rect.width, self.rect.height
        x, y = WIN_WIDTH // 2 - x, WIN_HEIGHT // 2 - y

        x = min(0, x)  # Не движемся дальше левой границы
        x = max(-(w - WIN_WIDTH), x)  # Не движемся дальше правой границы
        y = max(-(h - WIN_HEIGHT), y)  # Не движемся дальше нижней границы
        y = min(0, y)  # Не движемся дальше верхней границы

        for elem in moving:
            elem.rect.x = elem.pos[0] - x
            elem.rect.y = elem.pos[1] - y

        self.rect = pg.Rect(x, y, w, h)


def start_screen():
    screen = pg.display.set_mode(WIN_SIZE)
    pg.display.set_caption('Лабиринт')

    screen.blit(load_image(
        'Images\\background.png'), (0, 0))

    logo = load_image(
        'Images\\logo.png')
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


def end_screen():
    screen = pg.display.set_mode(WIN_SIZE)
    pg.display.set_caption('Лабиринт')

    screen.blit(load_image(
        'Images\\background.png'), (0, 0))

    label_font = pg.font.SysFont('calibry', 60)
    text_rendered = label_font.render('Пока все!', 0, pg.Color('white'))
    text_rect = text_rendered.get_rect()
    text_rect.centerx = WIN_WIDTH // 2
    text_rect.centery = 200
    screen.blit(text_rendered, text_rect)

    btn_size = (400, 80)
    menu_pos = (WIN_WIDTH // 2 - btn_size[0] // 2, WIN_HEIGHT // 2 - btn_size[1] // 2)
    menu_btn = Button(menu_pos, 'btn')
    menu_btn.scale(btn_size)
    menu_btn.set_text('Начальный экран', font_size=40)

    menu = False
    running = True
    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if menu_btn.pressed(event.pos):
                    running = False
                    menu = True

        screen.blit(menu_btn.image, (menu_btn.rect.x, menu_btn.rect.y))

        pg.display.flip()

    time.sleep(0.2)
    if menu:
        start_screen()


def dead_screen():
    screen = pg.display.set_mode(WIN_SIZE)
    pg.display.set_caption('Лабиринт')

    screen.blit(load_image(
        'Images\\background.png'), (0, 0))

    label_font = pg.font.SysFont('calibry', 60)
    text_rendered = label_font.render('D корпус поглотил Вас!', 0, pg.Color('white'))
    text_rect = text_rendered.get_rect()
    text_rect.centerx = WIN_WIDTH // 2
    text_rect.centery = 200
    screen.blit(text_rendered, text_rect)

    btn_size = (400, 80)
    menu_pos = (WIN_WIDTH // 2 - btn_size[0] // 2, WIN_HEIGHT // 2 - btn_size[1] // 2)
    menu_btn = Button(menu_pos, 'btn')
    menu_btn.scale(btn_size)
    menu_btn.set_text('Начальный экран', font_size=40)

    restart_pos = (menu_pos[0], menu_pos[1] + btn_size[1] + 20)
    restart_btn = Button(restart_pos, 'btn')
    restart_btn.scale(btn_size)
    restart_btn.set_text('Бросить вызов еще раз', font_size=40)

    restart = False
    menu = False
    running = True
    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if menu_btn.pressed(event.pos):
                    running = False
                    menu = True
                if restart_btn.pressed(event.pos):
                    running = False
                    restart = True

        screen.blit(menu_btn.image, (menu_btn.rect.x, menu_btn.rect.y))
        screen.blit(restart_btn.image, (restart_btn.rect.x, restart_btn.rect.y))

        pg.display.flip()
    time.sleep(0.2)
    if menu:
        start_screen()
    if restart:
        main()


def main():

    def pause():
        if paused:
            shadow.set_alpha(120)
        else:
            shadow.set_alpha(0)

    screen = pg.display.set_mode(WIN_SIZE)
    pg.display.set_caption('Лабиринт')

    level = load_level(choice(levels))
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
    pause_btn.add(moving)

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
                enemies.update(level, player_it)
                stairs_group.update(level)
                vents_group.update(level)
                keys.update(level)
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

        for obj in all_sprites:
            screen.blit(obj.image, camera.apply(obj))

        hint.update()
        replica.update()

        screen.blit(shadow, (0, 0))

        for obj in moving:
            screen.blit(obj.image, camera.apply(obj))

        pg.display.flip()

    for obj in all_sprites:
        obj.kill()
    for obj in moving:
        obj.kill()

    if dead:
        dead_screen()
    if end:
        end_screen()


if __name__ == "__main__":
    pg.init()
    start_screen()