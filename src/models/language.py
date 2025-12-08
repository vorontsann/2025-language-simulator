from enum import Enum


class Language(str, Enum):
    """The list of used languages."""

    EN = 'english'
    FR = 'french'
    JP = 'japanese'
