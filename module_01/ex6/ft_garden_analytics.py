#!/usr/bin/env python3


class Plant:
    class _Stats:
        def __init__(self) -> None:
            self._grow_count: int = 0
            self._age_count: int = 0
            self._show_count: int = 0

        def display(self) -> None:
            print("Stats: " + str(self._grow_count) + " grow, "
                  + str(self._age_count) + " age, "
                  + str(self._show_count) + " show")

    def __init__(self, name: str, height: float, age: int) -> None:
        self._name: str = name
        self._height: float = height
        self._age: int = age
        self._stats: Plant._Stats = Plant._Stats()

    def show(self) -> None:
        self._stats._show_count += 1
        height = round(self._height, 1)
        print(self._name + ": " + str(height) + "cm, "
              + str(self._age) + " days old")

    def grow(self) -> None:
        self._stats._grow_count += 1
        self._height += 0.8

    def age(self) -> None:
        self._stats._age_count += 1
        self._age += 1

    def set_height(self, height: float) -> None:
        if height < 0:
            print(self._name + ": Error, height can't be negative")
        else:
            self._height = height
            print("Height updated: " + str(height) + "cm")

    def get_height(self) -> float:
        return self._height

    def set_age(self, age: int) -> None:
        if age < 0:
            print(self._name + ": Error, age can't be negative")
        else:
            self._age = age
            print("Age updated: " + str(age) + " days")

    def get_age(self) -> int:
        return self._age

    @staticmethod
    def is_older_than_a_year(age: int) -> bool:
        return age > 365

    @classmethod
    def create_anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0)


class Flower(Plant):
    def __init__(self, name: str, height: float,
                 age: int, color: str) -> None:
        super().__init__(name, height, age)
        self._color: str = color
        self._blooming: bool = False

    def show(self) -> None:
        super().show()
        print(" Color: " + self._color)
        if self._blooming:
            print(" " + self._name + " is blooming beautifully!")
        else:
            print(" " + self._name + " has not bloomed yet")

    def bloom(self) -> None:
        self._blooming = True


class Seed(Flower):
    def __init__(self, name: str, height: float,
                 age: int, color: str) -> None:
        super().__init__(name, height, age, color)
        self._seeds: int = 0

    def show(self) -> None:
        super().show()
        print(" Seeds: " + str(self._seeds))

    def bloom(self) -> None:
        super().bloom()
        self._seeds = 42


class Tree(Plant):
    class _TreeStats:
        def __init__(self) -> None:
            self._shade_count: int = 0

        def display(self) -> None:
            print(" " + str(self._shade_count) + " shade")

    def __init__(self, name: str, height: float,
                 age: int, trunk_diameter: float) -> None:
        super().__init__(name, height, age)
        self._trunk_diameter: float = trunk_diameter
        self._tree_stats: Tree._TreeStats = Tree._TreeStats()

    def show(self) -> None:
        super().show()
        print(" Trunk diameter: " + str(self._trunk_diameter) + "cm")

    def produce_shade(self) -> None:
        self._tree_stats._shade_count += 1
        print("Tree " + self._name + " now produces a shade of "
              + str(round(self._height, 1)) + "cm long and "
              + str(self._trunk_diameter) + "cm wide.")


class Vegetable(Plant):
    def __init__(self, name: str, height: float,
                 age: int, harvest_season: str) -> None:
        super().__init__(name, height, age)
        self._harvest_season: str = harvest_season
        self._nutritional_value: int = 0

    def show(self) -> None:
        super().show()
        print(" Harvest season: " + self._harvest_season)
        print(" Nutritional value: " + str(self._nutritional_value))

    def grow(self) -> None:
        self._height += 2.1
        self._nutritional_value += 1

    def age(self) -> None:
        super().age()


def display_stats(plant: Plant) -> None:
    plant._stats.display()
    if isinstance(plant, Tree):
        plant._tree_stats.display()


if __name__ == "__main__":
    print("=== Garden statistics ===")

    print("=== Check year-old")
    print("Is 30 days more than a year? -> "
          + str(Plant.is_older_than_a_year(30)))
    print("Is 400 days more than a year? -> "
          + str(Plant.is_older_than_a_year(400)))

    print()
    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    print("[statistics for Rose]")
    display_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    print("[statistics for Rose]")
    display_stats(rose)

    print()
    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print("[statistics for Oak]")
    display_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print("[statistics for Oak]")
    display_stats(oak)

    print()
    print("=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow")
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age()
    sunflower.bloom()
    sunflower.show()
    print("[statistics for Sunflower]")
    display_stats(sunflower)

    print()
    print("=== Anonymous")
    unknown = Plant.create_anonymous()
    unknown.show()
    print("[statistics for Unknown plant]")
    display_stats(unknown)