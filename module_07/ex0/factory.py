"""Abstract factory for creature families."""

from abc import ABC, abstractmethod

from ex0.creature import Creature


class CreatureFactory(ABC):
    """Creates the base and evolved creatures of a single family."""

    @abstractmethod
    def create_base(self) -> Creature:
        """Return a new base-stage creature of this family."""

    @abstractmethod
    def create_evolved(self) -> Creature:
        """Return a new evolved-stage creature of this family."""
