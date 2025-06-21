import pygame as pg


def load_image(name, color_key=-1):
    image = pg.image.load(name)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image
