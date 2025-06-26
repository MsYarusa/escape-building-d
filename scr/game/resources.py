import pygame as pg

from utils.images import load_image
from .settings import TILE_WIDTH, TILE_HEIGHT

tile_images = {
    'simple_floor': pg.transform.scale(load_image(
        '..\\assets\\images\\entities\\objects\\floor.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'floor_near_wall': pg.transform.scale(load_image(
        '..\\assets\\images\\entities\\objects\\floor_near_wall.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'wall': pg.transform.scale(load_image(
        '..\\assets\\images\\entities\\objects\\wall.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'door': pg.transform.scale(load_image(
        '..\\assets\\images\\entities\\objects\\interactable_objects\\door.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'stairs': pg.transform.scale(load_image(
        '..\\assets\\images\\entities\\objects\\interactable_objects\\noticeable_objects\\stairs.png'),
        (TILE_WIDTH, TILE_HEIGHT)),
    'vent': pg.transform.scale(load_image(
        '..\\assets\\images\\entities\\objects\\interactable_objects\\noticeable_objects\\vent.png'),
        (TILE_WIDTH, TILE_HEIGHT)),
    'key': load_image(
        '..\\assets\\images\\entities\\objects\\interactable_objects\\noticeable_objects\\key.png'),
    'locked_door': pg.transform.scale(load_image(
        '..\\assets\\images\\entities\\objects\\interactable_objects\\locked_door.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'unlocked_door': pg.transform.scale(load_image(
        '..\\assets\\images\\entities\\objects\\interactable_objects\\unlocked_door.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'pair_door': pg.transform.scale(load_image(
        '..\\assets\\images\\entities\\objects\\interactable_objects\\locked_door_exit.png'), (TILE_WIDTH, TILE_HEIGHT))

}

enemy_images = {
    'lost_soul': {
        'img': load_image(
            '..\\assets\\images\\entities\\enemies\\lost_soul.png'),
        'cols': 8,
        'rows': 4
    },
    'lost_girl': {
        'img': load_image(
            '..\\assets\\images\\entities\\enemies\\lost_girl.png'),
        'cols': 8,
        'rows': 4
    },
    'cockroach': {
        'img': load_image(
            '..\\assets\\images\\entities\\enemies\\cockroach.png'),
        'cols': 4,
        'rows': 1
    }
}

player_images = {
    'player': {
        'img': load_image(
            '..\\assets\\images\\entities\\player\\player.png'),
        'cols': 8,
        'rows': 4
    }
}

button_images = {
    'pause': {
        False: load_image('..\\assets\\images\\ui\\buttons\\pause_dis.png'),
        True: load_image('..\\assets\\images\\ui\\buttons\\pause_act.png')
    },
    'btn': {
        False: load_image('..\\assets\\images\\ui\\buttons\\btn_dis.png', (0, 0, 0)),
        True: load_image('..\\assets\\images\\ui\\buttons\\btn_act.png', (0, 0, 0))
    }
}

replica_images = {
    'replica': load_image(
        '..\\assets\\images\\ui\\text_box\\replica.png'),
}

replicas = {
    'vent': ['О, это же вентиляция', 'Что будет если я туда залезу?'],
    'key': ['Это же ключ!', 'Интересно от какой он двери'],
    'key_collected': [],
    'locked_door': ['Замочная скважина! Стоит поискать ключ'],
    'unlocked_door': ['Дверь открыта!'],
    'lost_soul': ['Что это за странная тень?', 'Она преследует меня?!', 'Думаю стоит держаться от нее подальше'],
    'lost_girl': ['Откуда ОНА возникла?', 'Может ей нужная помощь?', 'СТОП, её ноги не касаются земли!!! Я думаю стоит уходить'],
    'door': ['Дверь закрыта, нет даже замочной скважины'],
    'stairs': ['О боже, это лестница!', 'Я на один шаг ближе к выходу!'],
    'cockroach': ['ОГРОМНЫЙ таракан!!!', 'Хмм.. Кажется он не заинтересован во мне',
                  'Но все равно думаю лучше его не касаться']
}
