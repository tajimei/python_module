"""Test scenario for the ex0 package: factories and battles."""

from ex0 import AquaFactory, CreatureFactory, FlameFactory


def test_factory(factory: CreatureFactory) -> None:
    """Create both stages of a family and exercise their behaviour."""
    print("Testing factory")
    for creature in (factory.create_base(), factory.create_evolved()):
        print(creature.describe())
        print(creature.attack())
    print()


def test_battle(first: CreatureFactory, second: CreatureFactory) -> None:
    """Make the base creatures of two families fight."""
    print("Testing battle")
    challenger = first.create_base()
    defender = second.create_base()
    print(challenger.describe())
    print(" vs.")
    print(defender.describe())
    print(" fight!")
    print(challenger.attack())
    print(defender.attack())


def main() -> None:
    """Run the full ex0 test scenario."""
    try:
        flame = FlameFactory()
        aqua = AquaFactory()
        test_factory(flame)
        test_factory(aqua)
        test_battle(flame, aqua)
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()