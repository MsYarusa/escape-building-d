import os
import json

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), 'progress.json')
LEVELS_DIR = os.path.join('..', 'assets', 'levels')

class ProgressManager:
    def __init__(self):
        self.levels = self._get_levels()
        self.progress = self._load_progress()

    def _get_levels(self):
        files = [f for f in os.listdir(LEVELS_DIR) if f.endswith('.txt')]
        files.sort()
        return files

    def _load_progress(self):
        if not os.path.exists(PROGRESS_FILE):
            return {'max_unlocked': 1, 'completed': []}
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_progress(self):
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f)

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