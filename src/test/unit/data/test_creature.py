"""test creature."""

import os
from time import CLOCK_MONOTONIC_RAW
from unicodedata import category

import pytest
from model.creature import Creature
from data.errors import Missing, Duplicate

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import creature


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="yeti",
        country="CN",
        area="himalayas",
        description="harmless himalayan",
        aka="abominable snowman",
    )


def test_creature(sample):
    resp = creature.create(sample)
    assert resp == sample


def test_creature_duplicate(sample):
    """test creature duplicate."""
    with pytest.raises(Duplicate):
        _ = creature.create(sample)


def test_get_one(sample):
    """test get one creature object."""
    resp = creature.get_one(sample.name)
    assert resp == sample


def test_get_one_missing():
    """test get one missing."""

    with pytest.raises(Missing):
        _ = creature.get("boxturtle")


def test_modify(smaple):
    """test modify creature object."""

    creature.area = "Sesame street"
    resp = creature.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing():
    """test modify missing."""
    thing: Creature = Creature(
        name="snurfle", country="EU", area="", description="some thing", aka=""
    )
    with pytest.raises(Missing):
        _ = creature.modify(thing.name, thing)
