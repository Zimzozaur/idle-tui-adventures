from dataclasses import dataclass
from datetime import datetime

from idle_tui_adventures.constants import PROFESSIONS_LITERAL
from idle_tui_adventures.database.db_transactions import (
    update_experience_db,
    update_level_db,
)


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

    def __post_init__(self) -> None:
        self.equipped_items = self.get_equipped_items()
        self.inventory_items = self.get_inventory_items()
        # Calculate Stats
        self.attack_speed = 1.00
        self.crit_rate = 0.20

    def level_up(self):
        self.level += 1
        update_level_db(character_id=self.character_id, level=self.level)

    def collect_exp(self, exp_amount: int = 1):
        self.experience += exp_amount
        update_experience_db(character_id=self.character_id, experience=self.experience)

    # von db
    def get_equipped_items(self): ...
    # von db
    def get_inventory_items(self): ...


class Warrior(Character): ...


class Mage(Character): ...


class Ranger(Character): ...


class Thief(Character): ...
