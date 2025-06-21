import pygame as pg

from utils.images import load_image
from .settings import TILE_WIDTH, TILE_HEIGHT


tile_images = {
    'simple_floor': pg.transform.scale(load_image(
       'images\\floor.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'floor_near_wall': pg.transform.scale(load_image(
        'images\\floor_near_wall.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'wall': pg.transform.scale(load_image(
        'images\\wall.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'door': pg.transform.scale(load_image(
        'images\\door.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'stairs': pg.transform.scale(load_image(
        'images\\stairs.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'vent': pg.transform.scale(load_image(
        'images\\vent.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'key': load_image(
        'images\\key.png'),
    'locked_door': pg.transform.scale(load_image(
        'images\\locked_door.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'unlocked_door': pg.transform.scale(load_image(
        'images\\unlocked_door.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'pair_door': pg.transform.scale(load_image(
        'images\\pair_door.png'), (TILE_WIDTH, TILE_HEIGHT))

}

enemy_images = {
    'lost_soul': load_image(
        'images\\lost_soul_.png'),
    'cockroach': load_image(
        'images\\cockroach.png')
}

button_images = {
    'pause': {
        False: load_image('images\\Buttons\\pause_dis.png'),
        True: load_image('images\\Buttons\\pause_act.png')
    },
    'btn': {
        False: load_image('images\\Buttons\\btn_dis.png', (0, 0, 0)),
        True: load_image('images\\Buttons\\btn_act.png', (0, 0, 0))
    }
}

replicas = {
    'vent': ['О, это же вентиляция', 'Что будет если я туда залезу?'],
    'key': ['Это же ключ!', 'Интересно от какой он двери'],
    'key_collected': [],
    'locked_door': ['Замочная скважина! Стоит поискать ключ'],
    'unlocked_door': ['Дверь открыта!'],
    'lost_soul': ['Что это за странная тень?', 'Она преследует меня?!', 'Думаю стоит держаться от нее подальше'],
    'door': ['Дверь закрыта, нет даже замочной скважины'],
    'stairs': ['О боже, это лестница!', 'Я на один шаг ближе к выходу!'],
    'cockroach': ['ОГРОМНЫЙ таракан!!!', 'Хмм.. Кажется он не заинтересован во мне',
                  'Но все равно думаю лучше его не касаться']
}
