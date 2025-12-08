from enum import Enum


class Topic(str, Enum):
    """The list of used topics."""

    FOOD = 'food'
    ANIMALS = 'animals'
    OBJECTS = 'objects'
    VERBS = 'verbs'
    TRANSPORT = 'transport'
    PLACES = 'places'
