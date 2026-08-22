"""Normal family: creatures able to transform, and their factory."""

from abc import ABC

from ex0 import CreatureFactory
from ex0.creature import Creature
from ex1.capability import TransformCapability


class TransformingCreature(Creature, TransformCapability, ABC):
    """A creature that also owns the transformation capability.

    Both parents keep their own state, so both initialisers must run.
    """

    def __init__(self, name: str, creature_type: str) -> None:
        Creature.__init__(self, name, creature_type)
        TransformCapability.__init__(self)


class Shiftling(TransformingCreature):
    """Base-stage creature of the transforming family."""

    def __init__(self) -> None:
        super().__init__("Shiftling", "Normal")

    def attack(self) -> str:
        """Return an attack message that depends on the current form."""
        if self.transformed:
            return f"{self.name} performs a boosted strike!"
        return f"{self.name} attacks normally."

    def transform(self) -> str:
        """Enter the alternate form and return the related message."""
        self._transformed = True
        return f"{self.name} shifts into a sharper form!"

    def revert(self) -> str:
        """Leave the alternate form and return the related message."""
        self._transformed = False
        return f"{self.name} returns to normal."


class Morphagon(TransformingCreature):
    """Evolved-stage creature of the transforming family."""

    def __init__(self) -> None:
        super().__init__("Morphagon", "Normal/Dragon")

    def attack(self) -> str:
        """Return an attack message that depends on the current form."""
        if self.transformed:
            return f"{self.name} unleashes a devastating morph strike!"
        return f"{self.name} attacks normally."

    def transform(self) -> str:
        """Enter the alternate form and return the related message."""
        self._transformed = True
        return f"{self.name} morphs into a dragonic battle form!"

    def revert(self) -> str:
        """Leave the alternate form and return the related message."""
        self._transformed = False
        return f"{self.name} stabilizes its form."


class TransformCreatureFactory(CreatureFactory):
    """Builds the members of the transforming family."""

    def create_base(self) -> TransformingCreature:
        """Return a new base-stage creature of this family."""
        return Shiftling()

    def create_evolved(self) -> TransformingCreature:
        """Return a new evolved-stage creature of this family."""
        return Morphagon()