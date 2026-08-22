"""Public interface of the ex0 package: factories only."""

from ex0.aqua import AquaFactory
from ex0.factory import CreatureFactory
from ex0.flame import FlameFactory

__all__ = ["CreatureFactory", "FlameFactory", "AquaFactory"]