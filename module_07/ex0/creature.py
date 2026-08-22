"""Base abstraction for every DataDeck creature card."""

from abc import ABC, abstractmethod


class Creature(ABC):
    """A creature card, defined by a name and an elemental type."""

    def __init__(self, name: str, creature_type: str) -> None:
        self._name = name
        self._creature_type = creature_type

    @property
    def name(self) -> str:
        return self._name

    @property
    def creature_type(self) -> str:
        return self._creature_type

    def describe(self) -> str:
        """Return the standard presentation message."""
        return f"{self._name} is a {self._creature_type} type Creature"

    @abstractmethod
    def attack(self) -> str:
        """Return the message describing this creature's attack."""