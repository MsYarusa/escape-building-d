import pygame

from game.resources import music_paths, sound_effects


def play_music(track_name, loops=-1, fade_ms=1000):
    pygame.mixer.music.fadeout(fade_ms)

    pygame.mixer.music.load(music_paths[track_name])

    pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)


def stop_music(fade_ms=1000):
    pygame.mixer.music.fadeout(fade_ms)


def set_volume(volume):
    pygame.mixer.music.set_volume(volume)


def play_sound(name, volume: float = -1.0):
    """
    Воспроизводит звуковой эффект по его имени.
    :param name: Ключ из словаря sound_effects.
    :param volume: Громкость от 0.0 до 1.0. Если -1, используется громкость по умолчанию.
    """
    if name in sound_effects:
        sound_to_play = sound_effects[name]

        if 0.0 <= volume <= 1.0:
            sound_to_play.set_volume(volume)

        return sound_to_play.play()
    else:
        print(f"Внимание: Звуковой эффект '{name}' не найден!")
        return None


def fadeout_sound(channel, fade_time_ms: int = 500):
    """
    Плавно останавливает звук на указанном канале.

    Args:
        channel: Объект pygame.mixer.Channel, на котором играет звук.
        fade_time_ms: Время затухания в миллисекундах.
    """
    # Проверяем, что канал существует и на нем что-то играет
    if channel and channel.get_busy():
        channel.fadeout(fade_time_ms)
