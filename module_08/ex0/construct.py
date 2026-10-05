import os
import site
import sys


def is_in_venv() -> bool:
    """Return True if running inside a virtual environment."""
    return sys.prefix != sys.base_prefix


def get_site_packages() -> str:
    """Return the main package installation path."""
    try:
        paths: list[str] = site.getsitepackages()
    except AttributeError:
        return "Unknown"
    if not paths:
        return "Unknown"
    return paths[0]


def show_outside() -> None:
    """Display status and instructions when no venv is detected."""
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print(f"Global package path: {get_site_packages()}")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate  # On Windows")
    print()
    print("Then run this program again.")


def show_inside() -> None:
    """Display details about the current virtual environment."""
    env_name: str = os.path.basename(sys.prefix)
    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {env_name}")
    print(f"Environment Path: {sys.prefix}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print()
    print("Package installation path:")
    print(get_site_packages())
    # print()
    # print(f"Global Python (outside the construct): {sys.base_prefix}")


def main() -> None:
    """Entry point."""
    if is_in_venv():
        show_inside()
    else:
        show_outside()


if __name__ == "__main__":
    main()