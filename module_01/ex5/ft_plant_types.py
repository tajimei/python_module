#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self._name: str = name
        self._height: float = height
        self._age: int = age
    def show(self) -> None:
        height = round(self._height, 1)
        print(self._name + ": " + str(height) + "cm, "
              + str(self._age) + " days old")
    def grow(self) -> None:
        self._height += 0.8
    def age(self) -> None:
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

class Flower(Plant):
    def __init__(self, name: str, height: float,
                 age: int, color: str) -> None:
        super().__init__(name, height, age)
        self._color: str = color
        self._blooming: bool = False

    def show(self) -> None:
        super().show()  # Plantのshow()を呼ぶ
        print(" Color: " + self._color)
        if self._blooming:
            print(" " + self._name + " is blooming beautifully!")
        else:
            print(" " + self._name + " has not bloomed yet")

    def bloom(self) -> None:
        self._blooming = True

class Tree(Plant):
    def __init__(self, name: str, height: float,
                 age: int, trunk_diameter: float) -> None:
        super().__init__(name, height, age)
        self._trunk_diameter: float = trunk_diameter

    def show(self) -> None:
        super().show()
        print(" Trunk diameter: " + str(self._trunk_diameter) + "cm")

    def produce_shade(self) -> None:
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

if __name__ == "__main__":
    print("=== Garden Plant Types ===")

    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()

    print()
    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()

    print()
    print("=== Vegetable")
    tomato = Vegetable("Tomato", 5.0, 10, "April")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for _ in range(20):
        tomato.grow()
        tomato.age()
    tomato.show()