import pygame as pg

all_sprites_group = pg.sprite.Group()
tiles_group = pg.sprite.Group()
walls_group = pg.sprite.Group()
player_group = pg.sprite.Group()
enemies_group = pg.sprite.Group()
shadow_overlay_group = pg.sprite.Group()
stairs_group = pg.sprite.Group()
interactable_objects_group = pg.sprite.Group()
replica_group = pg.sprite.Group()
vents_group = pg.sprite.Group()
keys_group = pg.sprite.Group()
text_boxes_group = pg.sprite.Group()


def clear_all_groups():
    all_sprites_group.empty()
    tiles_group.empty()
    walls_group.empty()
    player_group.empty()
    enemies_group.empty()
    shadow_overlay_group.empty()
    stairs_group.empty()
    interactable_objects_group.empty()
    replica_group.empty()
    vents_group.empty()
    keys_group.empty()
    text_boxes_group.empty()
