from random import randint, choice

from game.settings import SHADOW_COEF
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
    Player
)


def generate_level(level):
    # Разделяем карту и секцию сущностей
    entity_start = None
    for y, line in enumerate(level):
        if line.strip() == '---':
            entity_start = y
            break

    if entity_start is not None:
        map_lines = level[:entity_start]
        entity_lines = level[entity_start+1:]
    else:
        map_lines = level
        entity_lines = []

    height = len(map_lines)
    width = len(map_lines[0])
    player_spawns = []
    exit_positions = []
    door_candidates = []
    map_matrix = [list(row) for row in map_lines]

    # Проход по карте
    for y in range(height):
        for x in range(width):
            char = map_matrix[y][x]
            match char:
                case '@':
                    player_spawns.append((x, y))
                    tile_type = 'floor_near_wall' if y > 0 and map_matrix[y-1][x] == '#' else 'simple_floor'
                    BaseTile(tile_type, x, y)
                case 'x':
                    exit_positions.append((x, y))
                    tile_type = 'floor_near_wall' if y > 0 and map_matrix[y-1][x] == '#' else 'simple_floor'
                    BaseTile(tile_type, x, y)
                case '?':
                    door_candidates.append((x, y))
                    tile_type = 'floor_near_wall' if y > 0 and map_matrix[y-1][x] == '#' else 'simple_floor'
                    BaseTile(tile_type, x, y)
                case '#':
                    BaseTile('wall', x, y)
                case '.':
                    tile_type = 'floor_near_wall' if y > 0 and map_matrix[y-1][x] == '#' else 'simple_floor'
                    BaseTile(tile_type, x, y)
                case _:
                    pass

    # Размещаем выходы
    for pos in exit_positions:
        Stairs(*pos)

    if door_candidates:
        door_pos = choice(door_candidates)
        Stairs(*door_pos)

    # Парсим секцию сущностей
    entities = {}
    for line in entity_lines:
        if not line.strip():
            continue
        entity, *pos = line.split()
        if entity not in entities:
            entities[entity] = []
        entities[entity].append(tuple(map(int, pos)))

    if 'door' in entities:
        for pos in entities['door']:
            BaseInteractableObject('door', *pos)
    
    
    if 'locked_door' in entities:
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

    if 'vent' in entities:
        for pos in entities['vent']:
            vent1 = Vent(pos[0], pos[1])
            vent2 = Vent(pos[2], pos[3])
            vent1.set_pair(vent2)
            vent2.set_pair(vent1)

    if 'lost_soul' in entities:
        for pos in entities['lost_soul']:
            LostSoul(*pos)

    if 'cockroach' in entities:
        for pos in entities['cockroach']:
            Cockroach(*pos)

    for y in range(height * SHADOW_COEF):
        for x in range(width * SHADOW_COEF):
            BaseShadowOverlay(x, y)

    new_player = None
    if player_spawns:
        spawn = choice(player_spawns)
        new_player = Player(*spawn)

    return new_player
