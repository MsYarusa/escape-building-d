
from scr.load import *
from copy import deepcopy


all_sprites = pg.sprite.Group()
all_tiles = pg.sprite.Group()
walls = pg.sprite.Group()
player_group = pg.sprite.Group()
enemies = pg.sprite.Group()
shadows = pg.sprite.Group()
stairs_group = pg.sprite.Group()
InteractableObjects = pg.sprite.Group()
replica_group = pg.sprite.Group()
vents_group = pg.sprite.Group()
keys = pg.sprite.Group()


tile_images = {
   'simple_floor': pg.transform.scale(load_image(
       'Images\\floor.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'floor_near_wall': pg.transform.scale(load_image(
        'Images\\floor_near_wall.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'wall': pg.transform.scale(load_image(
        'Images\\wall.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'door': pg.transform.scale(load_image(
        'Images\\door.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'stairs': pg.transform.scale(load_image(
        'Images\\stairs.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'vent': pg.transform.scale(load_image(
        'Images\\vent.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'key': load_image(
        'Images\\key.png'),
    'locked_door': pg.transform.scale(load_image(
        'Images\\locked_door.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'unlocked_door': pg.transform.scale(load_image(
        'Images\\unlocked_door.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'pair_door': pg.transform.scale(load_image(
        'Images\\pair_door.png'), (TILE_WIDTH, TILE_HEIGHT))

}

enemy_images = {
    'lost_soul': load_image(
        'Images\\lost_soul_.png'),
    'cockroach': load_image(
        'Images\\cockroach.png')
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


class Shadow(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, shadows)

        self.rect = pg.Rect(pos_x * SHADOW_WIDTH, pos_y * SHADOW_HEIGHT, SHADOW_WIDTH, SHADOW_HEIGHT)
        self.image = pg.Surface((SHADOW_WIDTH, SHADOW_HEIGHT))
        self.image.fill(BLACK)
        self.image.set_alpha(250)
        self.brightness = 250

    def set_brightness(self, value):
        self.image.set_alpha(value)
        self.brightness = value


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, all_tiles)

        self.rect = pg.Rect(pos_x * TILE_WIDTH, pos_y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
        self.image = tile_images[tile_type]

        if tile_type == 'wall':
            self.add(walls)


class InteractableObject(Tile):
    def __init__(self, obj_type, pos_x, pos_y):
        super().__init__(obj_type, pos_x, pos_y)
        self.type = obj_type
        self.add(InteractableObjects)
        self.called_replica = False
        self.info = ''

    def set_replica(self):

        replica = None
        for obj in replica_group:
            replica = obj

        player = None
        for obj in player_group:
            player = obj

        if pg.sprite.collide_rect(self, player):
            rep = deepcopy(replicas[self.type])

            if self.info:
                rep.append(self.info)

            replica.set_text(rep, player.name)

    def make_hint(self, hint):

        player = None
        for obj in player_group:
            player = obj

        if pg.sprite.collide_rect(self, player):
            hint.set_text('Нажмите "E" для взаимодействия')

    def interact(self):
        self.set_replica()


class PairDoor(InteractableObject):
    def __init__(self, pos_x, pos_y):
        super().__init__('pair_door', pos_x, pos_y)
        self.pair = None

    def set_pair(self, another):
        self.pair = another

    def interact(self):
        for player in player_group:
            player.rect.x = self.pair.rect.x
            player.rect.y = self.pair.rect.y
            player.set_inner_rect()


class LockedDoor(InteractableObject):
    def __init__(self, pos_x, pos_y):
        super().__init__('locked_door', pos_x, pos_y)
        self.locked = True
        self.number = '???'
        self.pair = None

    def set_pair(self, another):
        self.pair = another

    def interact(self):
        if self.locked:
            self.set_replica()
        else:
            for player in player_group:

                if not player.info_collected[self.type]:
                    self.type = 'unlocked_door'
                    self.info = ''
                    self.image = tile_images[self.type]
                    self.set_replica()

            for player in player_group:
                player.rect.x = self.pair.rect.x
                player.rect.y = self.pair.rect.y
                player.set_inner_rect()


class NoticableObject(InteractableObject):
    def __init__(self, obj_type, pos_x, pos_y):
        super().__init__(obj_type, pos_x, pos_y)

    def update(self, level):
        player = None
        for obj in player_group:
            player = obj

        replica = None
        for obj in replica_group:
            replica = obj

        player_x = player.rect.centerx
        player_y = player.rect.centery
        obj_x = self.rect.centerx
        obj_y = self.rect.centery

        dist = ((obj_x - player_x) ** 2 + (obj_y - player_y) ** 2) ** (1 / 2)

        if dist <= 3 * TILE_WIDTH and not player.info_collected[self.type]:
            is_visible = True
            player_pos = (player_x // TILE_WIDTH, player_y // TILE_HEIGHT)
            pos_x = obj_x // TILE_WIDTH
            pos_y = obj_y // TILE_HEIGHT

            while pos_x != player_pos[0] or pos_y != player_pos[1]:
                if pos_x != player_pos[0]:
                    pos_x += (-1) ** (pos_x > player_pos[0])
                if pos_y != player_pos[1]:
                    pos_y += (-1) ** (pos_y > player_pos[1])
                if level[pos_y][pos_x] == '#':
                    is_visible = False

            if is_visible:
                player.info_collected[self.type] = True
                replica.set_text(replicas[self.type], player.name)


class Key(NoticableObject):
    def __init__(self, pos_x, pos_y):
        super().__init__('key', pos_x, pos_y)
        self.add(keys)
        self.door = None
        self.number = None

    def set_door(self, door):
        self.door = door

    def set_number(self, number):
        self.door.number = number
        self.number = number
        self.info = 'Номер D' + str(number)
        self.door.info = 'Аудитория D' + str(number)

    def interact(self):
        self.type = 'key_collected'
        self.set_replica()
        self.door.locked = False
        self.kill()


class Stairs(NoticableObject):
    def __init__(self, pos_x, pos_y):
        super().__init__('stairs', pos_x, pos_y)
        self.add(stairs_group)
        self.opened = False

    def interact(self):
        self.opened = True


class Vent(NoticableObject):
    def __init__(self, pos_x, pos_y):
        super().__init__('vent', pos_x, pos_y)
        self.add(vents_group)
        self.pair = None

    def set_pair(self, another):
        self.pair = another

    def interact(self):
        for player in player_group:
            player.rect.x = self.pair.rect.x
            player.rect.y = self.pair.rect.y
            player.set_inner_rect()


class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, player_group)

        self.name = 'Степан'

        self.frames = cut_sheet(load_image(
            'Images\\player.png'), 8, 4)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        self.rect = pg.Rect(pos_x * TILE_WIDTH + 6, pos_y * TILE_HEIGHT, PLAYER_RECT_X, PLAYER_RECT_Y)
        self.inner_rect = pg.Rect(self.rect.x, self.rect.y, PLAYER_RECT_X // 2, PLAYER_RECT_Y // 2)
        self.set_inner_rect()

        self.info_collected = {
            'lost_soul': False,
            'cockroach': False,
            'stairs': False,
            'vent': False,
            'key': False,
            'locked_door': False,
            'unlocked_door': True
        }
        self.step = 0
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def set_inner_rect(self):
        self.inner_rect.x = self.rect.x + PLAYER_RECT_X // 4
        self.inner_rect.y = self.rect.y + PLAYER_RECT_Y // 4

    def set_name(self, name):
        self.name = name

    def check_obj(self):
        for obj in InteractableObjects:
            if pg.sprite.collide_rect(self, obj):
                return obj
        return None

    def is_attacked(self):
        for enemy in enemies:
            if self.inner_rect.colliderect(enemy.inner_rect):
                return True
        return False

    def update(self, level, player_it):

        if player_it % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % 8 + self.step * 8
            self.image = self.frames[self.cur_frame]

        x_delta = 0
        y_delta = 0

        if self.left:
            x_delta -= PLAYER_SPEED
            self.step = 3
        if self.right:
            x_delta += PLAYER_SPEED
            self.step = 1
        if self.up:
            y_delta -= PLAYER_SPEED
            self.step = 2
        if self.down:
            y_delta += PLAYER_SPEED
            self.step = 0

        if not (self.up or self.down or self.right or self.left):
            self.cur_frame = -1

        self.rect.x += x_delta
        self.collide(x_delta, 0)

        self.rect.y += y_delta
        self.collide(0, y_delta)

        self.set_inner_rect()
        self.set_light(level)

    def collide(self, x_delta, y_delta):
        for wall in walls:
            if pg.sprite.collide_rect(self, wall):

                if x_delta < 0:
                    self.rect.left = wall.rect.right
                if x_delta > 0:
                    self.rect.right = wall.rect.left
                if y_delta < 0:
                    self.rect.top = wall.rect.bottom
                if y_delta > 0:
                    self.rect.bottom = wall.rect.top

    def set_light(self, level):
        player_x = self.rect.centerx
        player_y = self.rect.centery
        player_pos = (player_x // SHADOW_WIDTH, player_y // SHADOW_HEIGHT)

        for elem in shadows:
            elem_x = elem.rect.centerx
            elem_y = elem.rect.centery
            is_visible = True

            dist = ((elem_x - player_x)**2 + (elem_y - player_y)**2)**(1/2)

            if dist <= 6 * SHADOW_WIDTH:
                pos_x = elem_x // SHADOW_WIDTH
                pos_y = elem_y // SHADOW_HEIGHT

                while pos_x != player_pos[0] or pos_y != player_pos[1]:
                    if pos_x != player_pos[0]:
                        pos_x += (-1) ** (pos_x > player_pos[0])
                    if pos_y != player_pos[1]:
                        pos_y += (-1) ** (pos_y > player_pos[1])
                    if level[pos_y // SHADOW_COEF][pos_x // SHADOW_COEF] == '#':
                        is_visible = False

            if dist <= 5 * SHADOW_WIDTH and is_visible:
                elem.set_brightness(0)
            elif dist <= 6 * SHADOW_WIDTH and is_visible:
                elem.set_brightness(121)
            elif elem.brightness != 250:
                elem.set_brightness(250)


enemy_data = {
    'lost_soul': (1.6, 38, 64, 8, 4), # скорость, ширина прямоугольника, высота прямоугольника, количество кадров
    'cockroach': (4, 64, 64, 4, 1)
}


class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, pos_x, pos_y):
        super().__init__(all_sprites, enemies)

        cols = enemy_data[enemy_type][3]
        rows = enemy_data[enemy_type][4]
        self.frames = cut_sheet(enemy_images[enemy_type], cols, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        self.type = enemy_type
        self.speed = enemy_data[enemy_type][0]
        width = enemy_data[enemy_type][1]
        height = enemy_data[enemy_type][2]
        self.rect = pg.Rect(pos_x * TILE_WIDTH, pos_y * TILE_HEIGHT, width, height)
        self.inner_rect = pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def set_replica(self, player, player_pos, pos, level):

        is_visible = True

        while pos[0] != player_pos[0] or pos[1] != player_pos[1]:
            if pos[0] != player_pos[0]:
                pos[0] += (-1) ** (pos[0] > player_pos[0])
            if pos[1] != player_pos[1]:
                pos[1] += (-1) ** (pos[1] > player_pos[1])
            if level[pos[1] // SHADOW_COEF][pos[0] // SHADOW_COEF] == '#':
                is_visible = False

        if is_visible:
            player.info_collected[self.type] = True
            replica = None
            for obj in replica_group:
                replica = obj

            for player in player_group:
                replica.set_text(replicas[self.type], player.name)


class Cockroach(Enemy):
    def __init__(self, start_x, start_y, end_x, end_y):
        super().__init__('cockroach', start_x, start_y)

        self.rect.y -= TILE_WIDTH // 2
        self.inner_rect.width = 3 * self.rect.width // 4
        self.inner_rect.height = 3 * self.rect.height // 4
        self.set_inner_rect()
        self.start_x = start_x * TILE_WIDTH
        self.start_y = start_y * TILE_HEIGHT
        self.end_x = end_x * TILE_WIDTH
        self.end_y = end_y * TILE_HEIGHT
        self.inverse = False

    def set_inner_rect(self):
        self.inner_rect.x = self.rect.x + self.rect.width // 8
        self.inner_rect.y = self.rect.y + self.rect.height // 4

    def update(self, level, player_it):

        player = None
        for obj in player_group:
            player = obj

        player_x = player.rect.centerx
        player_y = player.rect.centery
        soul_x = self.rect.centerx
        soul_y = self.rect.centery

        dist = ((soul_x - player_x) ** 2 + (soul_y - player_y) ** 2) ** (1 / 2)

        if dist <= 3 * TILE_WIDTH and not player.info_collected[self.type]:
            player_pos = [player_x // SHADOW_WIDTH, player_y // SHADOW_HEIGHT]
            pos = [soul_x // SHADOW_WIDTH, soul_y // SHADOW_HEIGHT]
            self.set_replica(player, player_pos, pos, level)

        inv_x = self.start_x > self.end_x
        inv_y = self.start_y > self.end_y

        if not self.inverse:

            if self.start_x < self.end_x:
                self.cur_frame = 2
            if self.start_x > self.end_x:
                self.cur_frame = 0
            if self.start_y < self.end_y:
                self.cur_frame = 3
            if self.start_y > self.end_y:
                self.cur_frame = 1

            con1 = self.rect.x * (-1) ** inv_x < self.end_x * (-1) ** inv_x
            con2 = self.rect.y * (-1) ** inv_y < self.end_y * (-1) ** inv_y

            if con1:
                self.rect.x += self.speed * (-1) ** inv_x

            if con2:
                self.rect.y += self.speed * (-1) ** inv_y

            if not con1 and not con2:
                self.inverse = True
        else:

            if self.start_x < self.end_x:
                self.cur_frame = 0
            if self.start_x > self.end_x:
                self.cur_frame = 2
            if self.start_y < self.end_y:
                self.cur_frame = 1
            if self.start_y > self.end_y:
                self.cur_frame = 3

            con1 = self.rect.x * (-1) ** inv_x > self.start_x * (-1) ** inv_x
            con2 = self.rect.y * (-1) ** inv_y > self.start_y * (-1) ** inv_y

            if con1:
                self.rect.x -= self.speed * (-1) ** inv_x

            if con2:
                self.rect.y -= self.speed * (-1) ** inv_y

            if not con1 and not con2:
                self.inverse = False


        self.image = self.frames[self.cur_frame]
        self.set_inner_rect()


class LostSoul(Enemy):
    def __init__(self, pos_x, pos_y):
        super().__init__('lost_soul', pos_x, pos_y)

        self.inner_rect.width = self.rect.width // 2
        self.inner_rect.height = self.rect.height // 4
        self.set_inner_rect()
        self.step = 0

        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def set_inner_rect(self):
        self.inner_rect.x = self.rect.x + self.rect.width // 4
        self.inner_rect.y = self.rect.y + 3 * self.rect.height // 8

    def update(self, level, player_it):

        if player_it % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % 8 + self.step * 8
            self.image = self.frames[self.cur_frame]

        player = None
        for obj in player_group:
            player = obj

        player_x = player.rect.centerx
        player_y = player.rect.centery
        soul_x = self.rect.centerx
        soul_y = self.rect.centery

        dist = ((soul_x - player_x)**2 + (soul_y - player_y)**2)**(1/2)

        if dist <= 3 * TILE_WIDTH and not player.info_collected[self.type]:
            player_pos = [player_x // SHADOW_WIDTH, player_y // SHADOW_HEIGHT]
            pos = [soul_x // SHADOW_WIDTH, soul_y // SHADOW_HEIGHT]
            self.set_replica(player, player_pos, pos, level)

        x_delta = self.speed * (player_x - soul_x) / max(dist, 0.1)
        y_delta = self.speed * (player_y - soul_y) / max(dist, 0.1)

        if y_delta < 0:
            self.step = 2
        if y_delta > 0:
            self.step = 0
        if x_delta < 0 and abs(x_delta) > abs(y_delta):
            self.step = 3
        if x_delta > 0 and abs(x_delta) > abs(y_delta):
            self.step = 1

        self.rect.y += y_delta
        self.collide(0, y_delta)

        self.rect.x += x_delta
        self.collide(x_delta, 0)

        self.set_inner_rect()

    def collide(self, x_delta, y_delta):
        for wall in walls:
            if pg.sprite.collide_rect(self, wall):

                self.cur_frame = -1

                if x_delta < 0:
                    self.rect.left = wall.rect.right
                if x_delta > 0:
                    self.rect.right = wall.rect.left
                if y_delta < 0:
                    self.rect.top = wall.rect.bottom
                if y_delta > 0:
                    self.rect.bottom = wall.rect.top