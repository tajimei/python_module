#!/usr/bin/env python3

import sys


def parse_inventory(args: list[str]) -> dict[str, int]:
    inventory: dict[str, int] = {}

    for arg in args:
        # コロンで分割して2つに分かれるか確認
        parts = arg.split(':')
        if len(parts) != 2:
            print(f"Error - invalid parameter '{arg}'")
            continue

        name = parts[0]
        quantity_str = parts[1]

        # 重複チェック
        if name in inventory:
            print(f"Redundant item '{name}' - discarding")
            continue

        # 数量をintに変換
        try:
            quantity = int(quantity_str)
        except ValueError as e:
            print(f"Quantity error for '{name}': {e}")
            continue

        inventory[name] = quantity

    return inventory


def print_stats(inventory: dict[str, int]) -> None:
    # アイテムリスト
    item_list = list(inventory.keys())
    print(f"Item list: {item_list}")

    # 合計数量
    total = sum(inventory.values())
    print(f"Total quantity of the {len(inventory)} items: {total}")

    # 各アイテムの割合
    for name, qty in inventory.items():
        percentage = round(qty / total * 100, 1)
        print(f"Item {name} represents {percentage}%")

    # 最多・最少アイテム
    most = max(inventory.keys(), key=lambda k: inventory[k])
    least = min(inventory.keys(), key=lambda k: inventory[k])
    print(f"Item most abundant: {most} with quantity {inventory[most]}")
    print(f"Item least abundant: {least} with quantity {inventory[least]}")


def main() -> None:
    print("=== Inventory System Analysis ===")

    if len(sys.argv) == 1:
        print("No items provided.")
        return

    inventory = parse_inventory(sys.argv[1:])

    if len(inventory) == 0:
        print("No valid items provided.")
        return

    print(f"Got inventory: {inventory}")

    print_stats(inventory)

    # 新アイテムを追加
    inventory.update({'magic_item': 1})
    print(f"Updated inventory: {inventory}")


main()
