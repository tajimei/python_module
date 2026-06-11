#! /usr/bin/env python3

import typing
import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file: '{filename}'")

    file: typing.IO = None

    try:
        file = open(filename, "r")
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return

    content: str = file.read()
    print("---\n")
    print(content)
    print("\n---")
    file.close()
    print(f"File '{filename}' closed")

    lines: list = content.splitlines()
    new_content: str = "\n".join(line + "#" for line in lines)

    print("\nTransform Data:")
    print("---\n")
    print(new_content)
    print("\n---")

    save_filename: str = input("Enter new file name (or empty): ")
    if save_filename == "":
        print("Not saving data.")
        return

    print(f"Saving data to '{save_filename}'")

    save_file: typing.IO = None

    try:
        save_file = open(save_filename, "w")
    except OSError as e:
        print(f"Error opening file '{save_filename}': {e}")
        return

    save_file.write(new_content)
    save_file.close()
    print(f"Data saved in file '{save_filename}'.")


main()
