from random import randint

from game.entities import (
    BaseTile,
    BaseInteractableObject,
    Stairs,
    LockedDoor,
    LockedDoorExit,
    Key,
    Vent,
    BaseShadowOverlay,
    LostSoul,
    Cockroach,
    Player,
    SimpleDoor
)
from game.settings import SHADOW_COEF


def generate_level(level):
    new_player, x, y, player_x, player_y = None, None, None, None, None

    height = len(level)
    width = len(level[0])

    y = 0
    while y < height:
        for x in range(width):
            if level[y][x] == '.':
                BaseTile('simple_floor', x, y)
            elif level[y][x] == '|':
                BaseTile('floor_near_wall', x, y)
            elif level[y][x] == '0':
                SimpleDoor(x, y)
            elif level[y][x] == '#':
                BaseTile('wall', x, y)
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
            pair_door = LockedDoorExit(pos[2], pos[3])
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
            BaseShadowOverlay(x, y)

    return new_player
