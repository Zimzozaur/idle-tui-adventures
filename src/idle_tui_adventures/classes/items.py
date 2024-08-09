from dataclasses import dataclass

from idle_tui_adventures.constants import RARITIES_LITERAL, ITEM_CATEGORIES_LITERAL


@dataclass
class Item:
    item_id: int
    name: str
    rarity: RARITIES_LITERAL
    category: ITEM_CATEGORIES_LITERAL
    level_needed: int
    damage: int
    attack_speed: float
    strength: int
    intelligence: int
    dexterity: int
    luck: int
    owned_by: int
    equipped: bool

    def __post_init__(self) -> None: ...
