from pydantic import BaseModel

from .language import Language
from .topic import Topic


class WordItem(BaseModel):
    """Signs for each trained word."""

    id: int
    term: str
    translation: str
    example_sentence: str
    hint: str
    topic: Topic
    language: Language
