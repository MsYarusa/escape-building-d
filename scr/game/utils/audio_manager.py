import pygame

from game.resources import music_paths


def play_music(track_name, loops=-1, fade_ms=1000):
    pygame.mixer.music.fadeout(fade_ms)

    pygame.mixer.music.load(music_paths[track_name])

    pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)


def stop_music(fade_ms=1000):
    pygame.mixer.music.fadeout(fade_ms)


def set_volume(volume):
    pygame.mixer.music.set_volume(volume)
