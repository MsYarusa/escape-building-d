import os
import sys


def resource_path(relative_path):
    """ Возвращает абсолютный путь к ресурсу, работает как для кода, так и для .exe """
    try:
        # PyInstaller создает временную папку и сохраняет путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Если запускается из кода, то _MEIPASS не будет, используем обычный путь
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
