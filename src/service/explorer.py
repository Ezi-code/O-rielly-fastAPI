"""services for explorer."""

from fake.explorer import _explorers
from model.explorer import Explorer


def get_all() -> list[Explorer]:
    return _explorers


def get_one(name: str) -> Explorer:
    return (_explorer for _explorer in _explorers if _explorer.name == name) or None


def create(explorer: Explorer) -> Explorer:
    """create explorer."""
    return explorer


def delete(name: str) -> None:
    """delete explorer."""
    return None


def modify(name: str, explorer: Explorer) -> Explorer:
    """modify explorer."""
    return explorer


def replace(name: str, explorer: Explorer) -> Explorer:
    """replace explorer."""
    return explorer
