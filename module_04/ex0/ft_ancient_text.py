#! /usr/bin/env python3

import sys
import typing


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file: {filename}")

    try:
        file: typing.IO = open(filename, "r")
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return

    content: str = file.read()
    print("---\n")
    print(content)
    print("\n---")
    file.close()
    print(f"File '{filename}' closed")


main()
