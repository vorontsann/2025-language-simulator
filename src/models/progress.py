class Progress:
    """
    Stores user progress: number of correct and wrong answers.
    """

    def __init__(self, correct: int = 0, wrong: int = 0):
        self.correct = correct
        self.wrong = wrong

    def record_correct(self):
        self.correct += 1

    def record_wrong(self):
        self.wrong += 1

    @property
    def total(self) -> int:
        return self.correct + self.wrong

    @property
    def accuracy(self) -> float:
        if self.total == 0:
            return 0.0
        return self.correct / self.total

    def to_dict(self) -> dict:
        return {
            "correct": self.correct,
            "wrong": self.wrong,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Progress":
        return cls(
            correct=data.get("correct", 0),
            wrong=data.get("wrong", 0),
        )
