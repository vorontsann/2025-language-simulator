from src.models.word_item import WordItem
from src.models.language import Language
from src.models.topic import Topic


class MockDataManager:
    def load_words(self, language):
        return [
            WordItem(
                id=1,
                term="apple",
                translation="яблоко",
                example_sentence="I eat an apple",
                hint="A red fruit",
                topic=Topic.FOOD,
                language=Language.EN,
            )
        ] * 10
