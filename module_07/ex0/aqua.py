"""Water family: concrete creatures and their factory."""

from ex0.creature import Creature
from ex0.factory import CreatureFactory


class Aquabub(Creature):
    """Base-stage creature of the Water family."""

    def __init__(self) -> None:
        super().__init__("Aquabub", "Water")

    def attack(self) -> str:
        """Return the message describing this creature's attack."""
        return f"{self.name} uses Water Gun!"


class Torragon(Creature):
    """Evolved-stage creature of the Water family."""

    def __init__(self) -> None:
        super().__init__("Torragon", "Water")

    def attack(self) -> str:
        """Return the message describing this creature's attack."""
        return f"{self.name} uses Hydro Pump!"


class AquaFactory(CreatureFactory):
    """Builds the members of the Water family."""

    def create_base(self) -> Creature:
        """Return a new base-stage creature of this family."""
        return Aquabub()

    def create_evolved(self) -> Creature:
        """Return a new evolved-stage creature of this family."""
        return Torragon()
