"""services for creature."""

from fake.creature import _creatures
from model.creature import Creature
from typing import Optional


def get_all() -> list[Creature]:
    return _creatures


def get_one(name: str) -> Optional[Creature]:
    return (_explorer for _explorer in _creatures if _explorer.name == name) or None


def create(explorer: Creature) -> Creature:
    """create explorer."""
    return explorer


def delete(name: str) -> None:
    """delete explorer."""
    return None


def modify(name: str, explorer: Creature) -> Creature:
    """modify explorer."""
    return explorer


def replace(name: str, explorer: Creature) -> Creature:
    """replace explorer."""
    return explorer
