import json
import os

from game.utils.path_helper import resource_path


class ProgressManager:
    def __init__(self):
        home_dir = os.path.expanduser('~')
        app_data_dir = os.path.join(home_dir, '.D-korpus-save')
        os.makedirs(app_data_dir, exist_ok=True)
        self.progress_file_path = os.path.join(app_data_dir, 'progress.json')

        self.levels = self._get_levels()
        self.progress = self._load_progress()

    def _get_levels(self):
        levels_dir = resource_path('assets/levels')
        try:
            files = [f for f in os.listdir(levels_dir) if f.endswith('.txt')]
            files.sort()
            return files
        except FileNotFoundError:
            print(f"ОШИБКА: Папка с уровнями не найдена по пути {levels_dir}")
            return []

    def _load_progress(self):
        # Используем новый, правильный путь к файлу
        if not os.path.exists(self.progress_file_path):
            return {'max_unlocked': 1, 'completed': []}
        try:
            with open(self.progress_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Если файл поврежден или не найден, создаем новый прогресс
            return {'max_unlocked': 1, 'completed': []}

    def save_progress(self):
        with open(self.progress_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=4)

    def unlock_level(self, level_idx):
        if level_idx > self.progress['max_unlocked']:
            self.progress['max_unlocked'] = level_idx
            self.save_progress()

    def complete_level(self, level_idx):
        if level_idx not in self.progress['completed']:
            self.progress['completed'].append(level_idx)
            self.save_progress()

    def unlock_all(self):
        self.progress['max_unlocked'] = len(self.levels)
        self.save_progress()

    def reset_progress(self):
        self.progress = {'max_unlocked': 1, 'completed': []}
        self.save_progress()

    def is_unlocked(self, level_idx):
        return level_idx <= self.progress['max_unlocked']

    def is_completed(self, level_idx):
        return level_idx in self.progress['completed']


progress_manager = ProgressManager()
