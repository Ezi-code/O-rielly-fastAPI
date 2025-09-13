"""test creature."""

from model.creature import Creature
from service import creature as code

sample = Creature(
    name="Yeti",
    country="CN",
    area="*",
    description="Hirsute Himalayan",
    aka="Abominable Snowman",
)


def test_create():
    resp = code.create(sample)
    assert resp == sample


def test_get_exist():
    resp = next(code.get_one("Yeti"))
    assert resp == sample


def test_get_missing():
    resp = next(code.get_one("noting"), None)
    assert resp is None
