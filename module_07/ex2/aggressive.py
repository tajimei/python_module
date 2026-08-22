"""Strategy reserved for creatures able to transform."""

from ex0.creature import Creature
from ex1 import TransformCapability
from ex2.strategy import BattleStrategy


class AggressiveStrategy(BattleStrategy):
    """Transforms, attacks in the alternate form, then reverts."""

    def __init__(self) -> None:
        super().__init__("aggressive")

    def is_valid(self, creature: Creature) -> bool:
        """Return True if the creature suits this strategy."""
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        """Return the messages produced by the creature's turn."""
        if not isinstance(creature, TransformCapability):
            raise self._invalid(creature)
        return [
            creature.transform(),
            creature.attack(),
            creature.revert(),
        ]