"""Strategy reserved for creatures able to heal."""

from ex0.creature import Creature
from ex1 import HealCapability
from ex2.strategy import BattleStrategy


class DefensiveStrategy(BattleStrategy):
    """Attacks, then restores health."""

    def __init__(self) -> None:
        super().__init__("defensive")

    def is_valid(self, creature: Creature) -> bool:
        """Return True if the creature suits this strategy."""
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> list[str]:
        """Return the messages produced by the creature's turn."""
        if not isinstance(creature, HealCapability):
            raise self._invalid(creature)
        return [creature.attack(), creature.heal()]