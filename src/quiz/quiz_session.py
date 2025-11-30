import random
from typing import List, Optional

from src.models.word_item import WordItem
from src.models.topic import Topic
from src.models.language import Language
from src.data_manager.progress_manager import ProgressManager
from src.data_manager.data_manager import DataManager


class QuizSession:
    SESSION_SIZE = 10

    def __init__(
        self,
        user_id: str,
        language: Language,
        topic: Topic,
        data_manager: DataManager,
        progress_manager: ProgressManager,
    ):
        self.session_id = id(self)
        self.user_id = user_id
        self.language = language
        self.topic = topic
        self.data_manager = data_manager
        self.progress_manager = progress_manager

        self.items: List[WordItem] = []
        self.current_item: Optional[WordItem] = None

        self.correct_answers = 0
        self.wrong_answers = 0

        self._prepare_session()

    def _prepare_session(self) -> None:
        """
        Load words by language and topic and prepare session queue.
        """
        all_words = self.data_manager.load_words(self.language)
        topic_words = [w for w in all_words if w.topic == self.topic]

        if len(topic_words) < self.SESSION_SIZE:
            raise ValueError("Not enough words for selected topic")

        self.items = random.sample(topic_words, self.SESSION_SIZE)

    def next_item(self) -> Optional[WordItem]:
        if not self.items:
            self.current_item = None
            return None

        self.current_item = self.items.pop()
        return self.current_item

    def check_answer(self, answer: str) -> bool:
        if not self.current_item:
            raise RuntimeError("No active word")

        is_correct = (
                answer.strip().lower()
                == self.current_item.translation.strip().lower()
        )

        if is_correct:
            self.correct_answers += 1
        else:
            self.wrong_answers += 1

        self.progress_manager.update_user_progress(
            self.user_id, correct=is_correct
        )

        return is_correct

    def get_correct_answer(self) -> str:
        if not self.current_item:
            raise RuntimeError("No active word")
        return self.current_item.translation

    def show_hint(self) -> Optional[str]:
        return self.current_item.hint if self.current_item else None

    def is_finished(self) -> bool:
        return self.current_item is None and not self.items

    def get_results(self) -> dict:
        return {
            "correct": self.correct_answers,
            "wrong": self.wrong_answers,
            "total": self.correct_answers + self.wrong_answers,
            "accuracy": (
                self.correct_answers /
                (self.correct_answers + self.wrong_answers)
                if self.correct_answers + self.wrong_answers > 0 else 0.0
            )
        }

