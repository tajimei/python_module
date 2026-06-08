#! /usr/bin/env python3

import random

ALL_ACHIEVEMENTS = [
    'First Steps', 'Speed Runner', 'Boss Slayer', 'Treasure Hunter',
    'Survivor', 'Strategist', 'Unstoppable', 'Untouchable',
    'Master Explorer', 'Sharp Mind', 'Crafting Genius', 'World Savior',
    'Collector Supreme', 'Hidden Path Finder', 'Dragon Slayer',
    'Night Owl', 'Pacifist', 'Completionist'
]


def gen_player_achievements() -> set[str]:
    count = random.randint(3, 10)  # 3から10のランダムな数を生成
    # ALL_ACHIEVEMENTSからcount個のランダムな要素を選択
    picks = random.sample(ALL_ACHIEVEMENTS, count)
    return set(picks)


def main() -> None:
    print("=== Achievement Tracker System ===")

    players = {
        'Alice': gen_player_achievements(),
        'Bob': gen_player_achievements(),
        'Charlie': gen_player_achievements(),
        'Dylan': gen_player_achievements(),
    }

    for name, achievements in players.items():
        print(f"Player {name}: {achievements}")

    # 全実績の和集合
    all_achievements: set[str] = set()
    for achievements in players.values():
        all_achievements = all_achievements.union(achievements)
    print(f"\nAll distinct achievements: {all_achievements}")

    # 全員共通の実績
    common: set[str] = set(ALL_ACHIEVEMENTS)
    for achievements in players.values():
        common = common.intersection(achievements)
    print(f"\nCommon achievements: {common}")

    # 各プレイヤー固有の実績
    print()
    for name, achievements in players.items():
        others: set[str] = set()
        for other_name, other_ach in players.items():
            if other_name != name:
                others = others.union(other_ach)
        unique = achievements.difference(others)
        print(f"Only {name} has: {unique}")

    # 各プレイヤーの不足実績
    full_set = set(ALL_ACHIEVEMENTS)
    print()
    for name, achievements in players.items():
        missing = full_set.difference(achievements)
        print(f"{name} is missing: {missing}")


main()
