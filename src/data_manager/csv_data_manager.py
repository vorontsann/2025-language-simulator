import csv
from pathlib import Path
from typing import List, Dict

from src.data_manager.data_manager import DataManager
from src.models.language import Language
from src.models.topic import Topic
from src.models.word_item import WordItem


class CSVDataManager(DataManager):
    """CSV-based implementation of DataManager."""

    DATA_DIR = Path("data")

    FILES = {
        Language.EN: "english.csv",
        Language.FR: "french.csv",
        Language.JP: "japanese.csv",
    }

    def load_words(
        self, language: Language, topic: Topic
    ) -> List[WordItem]:

        file_path = self._get_file_path(language)
        words: list[WordItem] = []

        with file_path.open(encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                row: Dict[str, str]

                if row["topic"] != topic.value:
                    continue

                word = WordItem(
                    id=int(row["id"]),
                    term=row["term"].strip(),
                    translation=row["translation"].strip(),
                    example_sentence=row["example_sentence"].strip(),
                    hint=row["hint"].strip(),
                    topic=Topic(row["topic"]),
                    language=language,
                )
                words.append(word)

        return words

    def get_topics(self, language: Language) -> List[Topic]:
        file_path = self._get_file_path(language)
        topics: set[Topic] = set()

        with file_path.open(encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                row: Dict[str, str]
                topics.add(Topic(row["topic"]))

        return sorted(topics, key=lambda t: t.value)

    def _get_file_path(self, language: Language) -> Path:
        file_name = self.FILES.get(language)
        if not file_name:
            raise ValueError(f"No CSV file for language {language}")

        file_path = self.DATA_DIR / file_name
        if not file_path.exists():
            raise FileNotFoundError(file_path)

        return file_path
