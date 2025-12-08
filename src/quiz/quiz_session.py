import random
from typing import Optional

from src.data_manager.data_manager import DataManager
from src.data_manager.sqlite_user_manager import SQLiteUserManager
from src.models.language import Language
from src.models.topic import Topic
from src.models.word_item import WordItem


class QuizSession:
    def __init__(
        self,
        user_id: int,
        language: Language,
        topic: Topic,
        data_manager: DataManager,
        user_manager: SQLiteUserManager,
    ):
        self.user_id = user_id
        self.language = language
        self.topic = topic
        self.data_manager = data_manager
        self.user_manager = user_manager

        self.words: list[WordItem] = self.data_manager.load_words(language, topic)
        random.shuffle(self.words)

        self.current_word: Optional[WordItem] = None
        self.correct_answers = 0
        self.total_answers = 0

    def next_item(self) -> Optional[WordItem]:
        if not self.words:
            return None

        self.current_word = self.words.pop()
        return self.current_word

    def check_answer(self, user_answer: str) -> bool:
        if not self.current_word:
            raise RuntimeError("No active word")

        is_correct = (
            user_answer.strip().lower()
            == self.current_word.translation.strip().lower()
        )

        self.total_answers += 1
        if is_correct:
            self.correct_answers += 1

        self.user_manager.update_stats(     # SQLite update
            user_id=self.user_id,
            is_correct=is_correct
        )

        return is_correct

    def show_hint(self) -> str:
        return self.current_word.hint

    def get_correct_answer(self) -> str:
        return self.current_word.translation

    def get_results(self) -> dict:
        accuracy = (
            self.correct_answers / self.total_answers
            if self.total_answers > 0
            else 0
        )

        return {
            "correct": self.correct_answers,
            "wrong": self.total_answers - self.correct_answers,
            "accuracy": accuracy,
        }
