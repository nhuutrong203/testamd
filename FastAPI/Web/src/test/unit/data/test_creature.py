import os
import pytest
from src.model.creature import Creature
from error import Missing, Duplicate

# Set this before data import below
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from src.data import creature

@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="yeti",
        description="Hirsute Himalayan",
        aka="Abominable Snowman",
        country="CN",
        area="Himalayas"
    )

def test_create(sample: Creature):
    resp = creature.create(sample)
    assert resp == sample

def test_create_duplicate(sample: Creature):
    with pytest.raises(Duplicate):
        _ = creature.create(sample)

def test_get_exists(sample: Creature):
    resp = creature.get_one(sample.name)
    assert resp == sample

def test_get_missing():
    with pytest.raises(Missing):
        _ = creature.get_one("boxturtle")

def test_modify(sample: Creature):
    creature.country = "GL"  # Greenland!
    resp = creature.modify(sample)
    assert resp == sample

def test_modify_missing():
    bob: Creature = Creature(name="bob", description="some guy", country="ZZ", area="aa", aka="bb")
    with pytest.raises(Missing):
        _ = creature.modify(bob)

def test_delete(sample):
    resp = creature.delete(sample.name)
    assert resp is None

def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = creature.delete(sample.name)
