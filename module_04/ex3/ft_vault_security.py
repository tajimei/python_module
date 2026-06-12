#! /usr/bin/env python3

def secure_archive(
    filename: str,
    mode: str = "r",
    content: str = ""
) -> tuple:

    try:
        if mode == "r":
            with open(filename, "r") as file:
                return (True, file.read())

        elif mode == "w":
            with open(filename, "w") as file:
                file.write(content)
                return (True, "Content successfully written to file")

    except OSError as e:
        return (False, str(e))

    return (False, "Invalid mode")


def main() -> None:
    print("=== Cyber Archives Security ===")

    # 存在しないファイルの読み込み
    print("\nUsing 'secure_archive' to read from a nonexistent file:")
    result = secure_archive("/not/existing/file", "r")
    print(result)

    # アクセス権限のないファイルの読み込み
    print("\nUsing 'secure_archive' to read from an inaccessible file:")
    result = secure_archive("/etc/master.passwd", "r")
    print(result)

    # 通常ファイルの読み込み
    print("\nUsing 'secure_archive' to read from a regular file:")
    result = secure_archive("ancient_fragment.txt", "r")
    print(result)

    # 新しいファイルへの書き込み
    print("\nUsing 'secure_archive' to write previous content to a new file:")
    result = secure_archive("new_vault.txt", "w", result[1])
    print(result)


main()
