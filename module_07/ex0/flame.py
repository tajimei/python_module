"""Fire family: concrete creatures and their factory."""

from ex0.creature import Creature
from ex0.factory import CreatureFactory


class Flameling(Creature):
    """Base-stage creature of the Fire family."""

    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        """Return the message describing this creature's attack."""
        return f"{self.name} uses Ember!"


class Pyrodon(Creature):
    """Evolved-stage creature of the Fire family."""

    def __init__(self) -> None:
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self) -> str:
        """Return the message describing this creature's attack."""
        return f"{self.name} uses Flamethrower!"


class FlameFactory(CreatureFactory):
    """Builds the members of the Fire family."""

    def create_base(self) -> Creature:
        """Return a new base-stage creature of this family."""
        return Flameling()

    def create_evolved(self) -> Creature:
        """Return a new evolved-stage creature of this family."""
        return Pyrodon()
