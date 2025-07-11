import pygame as pg

from game.settings_manager import settings_manager
from game.utils.path_helper import resource_path

pg.mixer.init()

music_paths = {
    'menu': resource_path('assets/audio/music/menu_music.mp3'),
    'game': resource_path('assets/audio/music/game_music.mp3')
}

sound_effects = {
    'footsteps': pg.mixer.Sound(resource_path('assets/audio/effects/footsteps_sound.wav')),
    'door_open': pg.mixer.Sound(resource_path('assets/audio/effects/door_opened_sound.wav')),
    'door_closed': pg.mixer.Sound(resource_path('assets/audio/effects/door_closed_sound.wav')),
    'raise_item': pg.mixer.Sound(resource_path('assets/audio/effects/raise_item_sound.wav')),
    'lost_soul': pg.mixer.Sound(resource_path('assets/audio/effects/ghost_whisper_sound.wav')),
    'lost_girl': pg.mixer.Sound(resource_path('assets/audio/effects/ghost_whisper_sound.wav')),
    'cockroach': pg.mixer.Sound(resource_path('assets/audio/effects/cockroach_sound.wav')),
    'lose': pg.mixer.Sound(resource_path('assets/audio/effects/lose_sound.wav')),
    'win': pg.mixer.Sound(resource_path('assets/audio/effects/win_sound.wav')),
    'vent': pg.mixer.Sound(resource_path('assets/audio/effects/vent_sound.wav'))
}


def update_volumes():
    """Обновляет громкость всей музыки и эффектов согласно настройкам."""
    pg.mixer.music.set_volume(settings_manager.music_volume)
    for sound in sound_effects.values():
        sound.set_volume(settings_manager.sfx_volume)


def play_music(track_name, loops=-1, fade_ms=1000):
    """Воспроизводит музыку с текущей громкостью."""
    pg.mixer.music.set_volume(settings_manager.music_volume)
    pg.mixer.music.fadeout(fade_ms)
    pg.mixer.music.load(music_paths[track_name])
    pg.mixer.music.play(loops=loops, fade_ms=fade_ms)


def stop_music(fade_ms=1000):
    pg.mixer.music.fadeout(fade_ms)


def play_sound(name, loops=0):
    """
    Воспроизводит звуковой эффект с текущей громкостью.
    loops: количество повторений, -1 для бесконечного цикла.
    """
    if name in sound_effects:
        sound = sound_effects[name]
        sound.set_volume(settings_manager.sfx_volume)
        return sound.play(loops=loops)
    else:
        print(f"Внимание: Звуковой эффект '{name}' не найден!")
        return None


def fadeout_sound(channel, fade_time_ms: int = 500):
    if channel and channel.get_busy():
        channel.fadeout(fade_time_ms)


def stop_all_sfx(fade_time_ms: int = 200):
    """
    Плавно останавливает ВСЕ активные звуковые эффекты на всех каналах.
    Музыка при этом не затрагивается.
    """
    for i in range(pg.mixer.get_num_channels()):
        channel = pg.mixer.Channel(i)
        if channel.get_busy():
            channel.fadeout(fade_time_ms)


# Применяем громкость при первом импорте модуля, чтобы все звуки
# сразу имели правильную громкость при старте игры.
update_volumes()
