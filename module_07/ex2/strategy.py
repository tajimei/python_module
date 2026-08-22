"""Abstract battle strategy and the error raised on misuse."""

from abc import ABC, abstractmethod

from ex0.creature import Creature


class InvalidCombinationError(Exception):
    """Raised when a strategy is applied to an unsuitable creature."""


class BattleStrategy(ABC):
    """Defines how a creature behaves during its turn of a battle."""

    def __init__(self, label: str) -> None:
        self._label = label

    @property
    def label(self) -> str:
        """Return the human readable name of the strategy."""
        return self._label

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        """Return True if the creature suits this strategy."""

    @abstractmethod
    def act(self, creature: Creature) -> list[str]:
        """Return the messages produced by the creature's turn."""

    def _invalid(self, creature: Creature) -> InvalidCombinationError:
        """Build the error describing an unsuitable creature."""
        return InvalidCombinationError(
            f"Invalid Creature '{creature.name}' "
            f"for this {self._label} strategy"
        )
