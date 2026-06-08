#!/usr/bin/env python3

import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        raw = input("Enter new coordinates as floats in format 'x,y,z': ")
        parts = raw.split(',')
        if len(parts) != 3:
            print("Invalid syntax")
            continue
        try:
            x = float(parts[0].strip())
            y = float(parts[1].strip())
            z = float(parts[2].strip())
            return (x, y, z)
        except ValueError as e:
            for part in parts:
                try:
                    float(part.strip())
                except ValueError:
                    print(f"Error on parameter '{part.strip()}': {e}")


def calc_distance(
    p1: tuple[float, float, float],
    p2: tuple[float, float, float]
) -> float:
    return round(math.sqrt(
        (p2[0] - p1[0]) ** 2 +
        (p2[1] - p1[1]) ** 2 +
        (p2[2] - p1[2]) ** 2
    ), 4)


def main() -> None:
    print("=== Game Coordinate System ===")

    print("Get a first set of coordinates")
    pos1 = get_player_pos()

    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")

    dist_to_center = calc_distance((0.0, 0.0, 0.0), pos1)
    print(f"Distance to center: {dist_to_center}")

    print("Get a second set of coordinates")
    pos2 = get_player_pos()

    dist = calc_distance(pos1, pos2)
    print(f"Distance between the 2 sets of coordinates: {dist}")


main()
