#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self._name: str = name
        self._height: float = height
        self._age: int = age

    def show(self) -> None:
        height = round(self._height, 1)
        print(f"{self._name}: {height}cm, {self._age} days old")

    def grow(self) -> None:
        self._height += 0.8

    def age(self) -> None:
        self._age += 1

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
        else:
            self._height = height
            print(f"Height updated: {height}cm")

    def get_height(self) -> float:
        return self._height

    def set_age(self, age: int) -> None:
        if age < 0:
            print(f"{self._name}: Error, age can't be negative")
        else:
            self._age = age
            print(f"Age updated: {age} days")

    def get_age(self) -> int:
        return self._age


if __name__ == "__main__":
    print("=== Garden Security System ===")

    rose = Plant("Rose", 15.0, 10)
    print("Plant created: ", end="")
    rose.show()
    print()

    rose.set_height(25.0)
    rose.set_age(30)
    print()

    rose.set_height(-5.0)
    print("Height update rejected")
    rose.set_age(-10)
    print("Age update rejected")
    print()

    print("Current state: ", end="")
    rose.show()
