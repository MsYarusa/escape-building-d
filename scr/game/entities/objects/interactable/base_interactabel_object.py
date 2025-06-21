import pygame as pg
from copy import deepcopy

from game.resources import replicas
from game.groups import replica_group, player_group, interactable_objects_group

from game.entities.objects import BaseTile


class BaseInteractableObject(BaseTile):
    def __init__(self, obj_type, pos_x, pos_y):
        super().__init__(obj_type, pos_x, pos_y)
        self.type = obj_type
        self.add(interactable_objects_group)
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