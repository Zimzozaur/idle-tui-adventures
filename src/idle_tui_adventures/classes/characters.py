from dataclasses import dataclass
from datetime import datetime

from idle_tui_adventures.constants import PROFESSIONS_LITERAL


@dataclass
class Character:
    character_id: int
    name: str
    profession: PROFESSIONS_LITERAL
    created_at: datetime
    level: int
    experience: int
    strength: int
    intelligence: int
    dexterity: int
    luck: int
    major_stage: int
    minor_stage: int

    def __post_init__(self) -> None:
        self.equipped_items = self.get_equipped_items()
        self.inventory_items = self.get_inventory_items()

    ...

    # von db
    def get_equipped_items(self): ...
    # von db
    def get_inventory_items(self): ...


class Warrior(Character): ...


class Mage(Character): ...


class Ranger(Character): ...


class Thief(Character): ...
