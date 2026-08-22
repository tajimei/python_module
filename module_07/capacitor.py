"""Test scenario for the ex1 package: creatures with capabilities."""

from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex1.heal import HealingCreature
from ex1.transform import TransformingCreature


def test_healing(creature: HealingCreature) -> None:
    """Describe the creature, then make it attack and heal."""
    print(creature.describe())
    print(creature.attack())
    print(creature.heal())


def test_transforming(creature: TransformingCreature) -> None:
    """Describe the creature, then attack around a transformation."""
    print(creature.describe())
    print(creature.attack())
    print(creature.transform())
    print(creature.attack())
    print(creature.revert())


def main() -> None:
    """Run the full ex1 test scenario."""
    try:
        healers = HealingCreatureFactory()
        print("Testing Creature with healing capability")
        print(" base:")
        test_healing(healers.create_base())
        print(" evolved:")
        test_healing(healers.create_evolved())
        print()

        shifters = TransformCreatureFactory()
        print("Testing Creature with transform capability")
        print(" base:")
        test_transforming(shifters.create_base())
        print(" evolved:")
        test_transforming(shifters.create_evolved())
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()