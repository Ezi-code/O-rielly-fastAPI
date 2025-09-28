"""user fake data."""

from tabnanny import check
from model.user import User
from data.errors import Missing, Duplicate


fakes = [
    User(username="pope", hash="password"),
    User(username="john", hash="doe"),
]


def find(name: str) -> User:
    """find a fake user by name."""
    for fake in fakes:
        if fake.name == name:
            return fake
    raise Missing("user", name)


def check_missing(name: str) -> None:
    """check if a fake user is missing."""
    if not find(name):
        raise Missing("user", name)


def check_duplicate(name: str) -> None:
    if find(name):
        raise Duplicate("user", name)


def get_all() -> list[User]:
    """get all fake users."""
    return fakes


def get_one(name: str) -> User:
    """get one fake user by name."""
    check_missing(name)
    return find(name)


def create(user: User) -> User:
    """create a fake user."""
    check_duplicate(user.name)
    fakes.append(user)
    return user


def modify(user: User) -> User:
    """partially modify a fake user."""
    check_missing(user.name)
    return user


def delete(name: str) -> None:
    check_missing(name)
    return None
