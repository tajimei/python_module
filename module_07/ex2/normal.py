"""Strategy usable by any creature: plain attack."""

from ex0.creature import Creature
from ex2.strategy import BattleStrategy


class NormalStrategy(BattleStrategy):
    """Simply attacks. Every creature suits this strategy."""

    def __init__(self) -> None:
        super().__init__("normal")

    def is_valid(self, creature: Creature) -> bool:
        """Return True if the creature suits this strategy."""
        return isinstance(creature, Creature)

    def act(self, creature: Creature) -> list[str]:
        """Return the messages produced by the creature's turn."""
        if not self.is_valid(creature):
            raise self._invalid(creature)
        return [creature.attack()]
