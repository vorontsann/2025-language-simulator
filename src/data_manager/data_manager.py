from abc import ABC, abstractmethod
from typing import List

from src.models.language import Language
from src.models.topic import Topic
from src.models.word_item import WordItem


class DataManager(ABC):
    """Abstract interface for word data access."""

    @abstractmethod
    def load_words(
        self, language: Language, topic: Topic
    ) -> List[WordItem]:
        """Load words for given language and topic."""
        pass

    @abstractmethod
    def get_topics(self, language: Language) -> List[Topic]:
        """Get available topics for a language."""
        pass
