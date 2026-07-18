print("=== Kaboom 1 ===")
print("Access to alchemy/grimoire/dark_spellbook.py directly")
print(
    "Test import now"
    " - THIS WILL RAISE AN UNCAUGHT EXCEPTION"
)
from alchemy.grimoire.dark_spellbook import (  # noqa: E402
    dark_spell_record,
)

result: str = dark_spell_record('Curse', 'bats and frogs')
print(f"Testing record dark spell: {result}")
