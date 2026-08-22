"""Grass family: creatures able to heal, and their factory."""

from abc import ABC

from ex0 import CreatureFactory
from ex0.creature import Creature
from ex1.capability import HealCapability


class HealingCreature(Creature, HealCapability, ABC):
    """A creature that also owns the healing capability."""


class Sproutling(HealingCreature):
    """Base-stage creature of the Grass family."""

    def __init__(self) -> None:
        super().__init__("Sproutling", "Grass")

    def attack(self) -> str:
        """Return the message describing this creature's attack."""
        return f"{self.name} uses Vine Whip!"

    def heal(self) -> str:
        """Return the message describing the healing action."""
        return f"{self.name} heals itself for a small amount"


class Bloomelle(HealingCreature):
    """Evolved-stage creature of the Grass family."""

    def __init__(self) -> None:
        super().__init__("Bloomelle", "Grass/Fairy")

    def attack(self) -> str:
        """Return the message describing this creature's attack."""
        return f"{self.name} uses Petal Dance!"

    def heal(self) -> str:
        """Return the message describing the healing action."""
        return f"{self.name} heals itself and others for a large amount"


class HealingCreatureFactory(CreatureFactory):
    """Builds the members of the healing family."""

    def create_base(self) -> HealingCreature:
        """Return a new base-stage creature of this family."""
        return Sproutling()

    def create_evolved(self) -> HealingCreature:
        """Return a new evolved-stage creature of this family."""
        return Bloomelle()
