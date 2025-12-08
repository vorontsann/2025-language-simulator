class Progress:
    """Stores user progress: number of correct and wrong answers."""

    def __init__(self, correct: int = 0, wrong: int = 0):
        """Initialize progress."""
        if correct < 0 or wrong < 0:
            raise ValueError('Progress values cannot be negative')

        self.correct = correct
        self.wrong = wrong

    def record_correct(self) -> None:
        """Count correct answers."""
        self.correct += 1

    def record_wrong(self) -> None:
        """Count wrong answers."""
        self.wrong += 1

    @property
    def total(self) -> int:
        """Count the number of all answers."""
        return self.correct + self.wrong

    @property
    def accuracy(self) -> float:
        """Count the percent of correct answers."""
        return self.correct / self.total if self.total else 0.0

    def to_dict(self) -> dict:
        """Save the number of correct wrong answers in a dict."""
        return {
            'correct': self.correct,
            'wrong': self.wrong,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Progress':
        """Return the information about correct and wrong answers."""
        return cls(
            correct=int(data.get('correct', 0)),
            wrong=int(data.get('wrong', 0)),
        )
