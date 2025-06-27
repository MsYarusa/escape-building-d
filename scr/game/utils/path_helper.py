import os
import sys


def resource_path(relative_path):
    """ 
    Возвращает абсолютный путь к ресурсу. Работает как для кода, так и для .exe.
    Этот метод находит путь к папке 'scr' и строит путь к ресурсу от неё.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        current_file_path = os.path.abspath(__file__)
        utils_dir = os.path.dirname(current_file_path)
        base_path = os.path.dirname(os.path.dirname(utils_dir))

    return os.path.join(base_path, relative_path)
