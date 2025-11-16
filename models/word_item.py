class WordItem:
    def __init__(self, item_id, term, translation, example=None, hint=None, difficulty=1):
        self.item_id = item_id
        self.term = term
        self.translation = translation
        self.example = example
        self.hint = hint
        self.difficulty = difficulty
