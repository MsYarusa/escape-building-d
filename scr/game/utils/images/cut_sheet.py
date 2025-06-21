import pygame as pg


def cut_sheet(sheet, columns, rows):
    rect = pg.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
    frames = []
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pg.Rect(
                frame_location, rect.size)))
    return frames
