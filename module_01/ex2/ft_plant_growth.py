#!/usr/bin/env python3

class Plant:
    def __init__(self) -> None:
        self.name: str = ""
        self.height: float = 0.0
        self.first_age: int = 0
    def show(self) -> None:
        height = round(self.height, 1)
        print(self.name + ": " + str(height) + "cm, "
              + str(self.first_age) + " days old")
    def grow(self) -> None:
        self.height += 0.8
    def age(self) -> None:
        self.first_age += 1


if __name__ == "__main__":
    print("=== Garden Plant Growth ===")

    rose = Plant()
    rose.name = "Rose"
    rose.height = 25
    rose.first_age = 30
    rose.show()

    start_height = rose.height

    for day in range(7):
        rose.grow()
        rose.age()
        print("=== Day " + str(day + 1) + " ===")
        rose.show()

    growth = round(rose.height - start_height, 1)
    print("Growth this week: " + str(growth) + "cm")