from src.model.creature import Creature

_creatures = [
    Creature(name="Yeti",
             aka= "Abominable Snowman",
             country="CN",
             area="Himalayas",
             description="Hirsute Himalayan"),
    Creature(name="Bigfoot",
             aka= "Yeti's Cousin Eddie",
             country="US",
             area="*",
             description="Sasquatch"),           
]

def get_all() -> list[Creature]:
    """Return all creatures"""
    return _creatures

def get_one(name: str) -> Creature | None:
    """Return one creature"""
    for _creature in _creatures:
        if _creature.name == name:
            return _creature
    return None

def create(creature: Creature) -> Creature:
    """Add an creature"""
    return creature

def modify(creature: Creature) -> Creature:
    """"Partitially modify an creature"""
    return creature

def replace(creature: Creature) -> Creature:
    """Completely replace the creature"""
    return creature

def delete(name: str):
    """"Delete an creature; return None if it existed"""
    return None