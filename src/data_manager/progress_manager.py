import json
from pathlib import Path
from typing import Dict

from src.models.progress import Progress


class ProgressManager:
    def __init__(self, file_path: str = "data/progress.json"):
        self.file_path = Path(file_path)
        self._data: Dict[str, Progress] = {}

        self.load()

    # File operations

    def load(self) -> None:
        """
        Load all users progress from JSON file.
        """
        if not self.file_path.exists():
            self._data = {}
            return

        with self.file_path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)

        self._data = {
            user_id: Progress.from_dict(progress)
            for user_id, progress in raw_data.items()
        }

    def save(self) -> None:
        """
        Save all users progress to JSON file.
        """
        data_to_save = {
            user_id: progress.to_dict()
            for user_id, progress in self._data.items()
        }

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data_to_save, file, indent=4)

    # User operations

    def get_user_progress(self, user_id: str) -> Progress:
        """
        Return progress for user. Creates new if not exists.
        """
        if user_id not in self._data:
            self._data[user_id] = Progress()
        return self._data[user_id]

    def update_user_progress(self, user_id: str, correct: bool) -> None:
        """
        Update progress for a user after answer.
        """
        progress = self.get_user_progress(user_id)

        if correct:
            progress.record_correct()
        else:
            progress.record_wrong()

        self.save()
