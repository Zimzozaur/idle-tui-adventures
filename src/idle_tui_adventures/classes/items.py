from dataclasses import dataclass

from idle_tui_adventures.constants import RARITIES_LITERAL, ITEM_CATEGORIES_LITERAL


@dataclass
class Item:
    item_id: int
    name: str
    level_needed: int
    rarity: RARITIES_LITERAL
    category: ITEM_CATEGORIES_LITERAL
    damage: int
    attack_speed: float
    strength: int
    intelligence: int
    dexterity: int
    luck: int

    def __post_init__(self) -> None: ...
