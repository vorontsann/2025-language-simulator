from .language import Language


class Topic:
    def __init__(self, topic_id: str, name: str, language: "Language"):
        self.topic_id = topic_id
        self.name = name
        self.language = language
        self.items = []   # список WordItem

    def add_item(self, word_item):
        self.items.append(word_item)
