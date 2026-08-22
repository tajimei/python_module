"""Test scenario for the ex2 package: strategy driven tournaments."""

from ex0 import AquaFactory, CreatureFactory, FlameFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    AggressiveStrategy,
    BattleStrategy,
    DefensiveStrategy,
    InvalidCombinationError,
    NormalStrategy,
)

Opponent = tuple[CreatureFactory, BattleStrategy]


def battle(opponents: list[Opponent]) -> None:
    """Run a round robin tournament between the given opponents.

    Each opponent is a factory paired with the strategy driving its
    creature. The tournament stops as soon as one pairing is invalid.
    """
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    print()

    fighters = [(factory.create_base(), s) for factory, s in opponents]
    for index, (first, first_strategy) in enumerate(fighters):
        for second, second_strategy in fighters[index + 1:]:
            print("* Battle *")
            print(first.describe())
            print(" vs.")
            print(second.describe())
            print(" now fight!")
            try:
                for message in first_strategy.act(first):
                    print(message)
                for message in second_strategy.act(second):
                    print(message)
            except InvalidCombinationError as error:
                print(f"Battle error, aborting tournament: {error}")
                print()
                return
            print()


def main() -> None:
    """Run three tournaments: basic, invalid, and multiple opponents."""
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    print("Tournament 0 (basic)")
    print(" [ (Flameling+Normal), (Healing+Defensive) ]")
    battle([
        (FlameFactory(), normal),
        (HealingCreatureFactory(), defensive),
    ])

    print("Tournament 1 (error)")
    print(" [ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([
        (FlameFactory(), aggressive),
        (HealingCreatureFactory(), defensive),
    ])

    print("Tournament 2 (multiple)")
    print(" [ (Aquabub+Normal), (Healing+Defensive),"
          " (Transform+Aggressive) ]")
    battle([
        (AquaFactory(), normal),
        (HealingCreatureFactory(), defensive),
        (TransformCreatureFactory(), aggressive),
    ])


if __name__ == "__main__":
    main()
