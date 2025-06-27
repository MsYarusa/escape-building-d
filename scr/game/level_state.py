# Модуль для хранения текущего выбранного уровня
from game.utils.path_helper import resource_path

current_level_path = resource_path('assets\\levels\\Level_01.txt')


def set_current_level_path(path):
    global current_level_path
    current_level_path = path
