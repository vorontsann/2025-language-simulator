from pydantic import BaseModel
from .topic import Topic
from .language import Language


class WordItem(BaseModel):
    id: int
    term: str
    translation: str
    example_sentence: str
    hint: str
    topic: Topic
    language: Language
