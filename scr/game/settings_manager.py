import json
import os


class SettingsManager:
    """
    Управляет настройками игры, сохраняет и загружает их из файла.
    """

    def __init__(self, settings_file='settings.json'):
        self.settings_file = settings_file
        # Настройки по умолчанию
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        self.load_settings()

    def load_settings(self):
        """Загружает настройки из файла. Если файла нет, создает его."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.music_volume = float(settings.get('music_volume', 0.5))
                    self.sfx_volume = float(settings.get('sfx_volume', 0.5))
            except (json.JSONDecodeError, IOError, TypeError):
                self.save_settings()
        else:
            self.save_settings()

    def save_settings(self):
        """Сохраняет текущие настройки в файл."""
        settings = {
            'music_volume': self.music_volume,
            'sfx_volume': self.sfx_volume
        }
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=4)


# Создаем глобальный экземпляр, чтобы он был доступен везде
settings_manager = SettingsManager()
