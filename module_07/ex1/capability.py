"""Capabilities, deliberately independent from any Creature class.

Nothing here inherits from Creature: a capability describes what an
entity can do, not what it is. Any future entity type may gain them.
"""

from abc import ABC, abstractmethod


class HealCapability(ABC):
    """Grants the ability to restore health."""

    @abstractmethod
    def heal(self) -> str:
        """Return the message describing the healing action."""


class TransformCapability(ABC):
    """Grants a reversible alternate form that alters the attack."""

    def __init__(self) -> None:
        self._transformed = False

    @property
    def transformed(self) -> bool:
        """Return True while the alternate form is active."""
        return self._transformed

    @abstractmethod
    def transform(self) -> str:
        """Enter the alternate form and return the related message."""

    @abstractmethod
    def revert(self) -> str:
        """Leave the alternate form and return the related message."""
