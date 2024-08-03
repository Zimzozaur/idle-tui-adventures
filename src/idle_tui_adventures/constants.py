from typing import Literal, get_args
from pathlib import Path

DB_NAME = "test.db"
DB_PATH = Path(".").cwd()
DB_FULLNAME = DB_PATH / DB_NAME

ICONS_LITERAL = Literal["character", "backpack", "dungeon", "shop", "settings"]
STATS_LITERAL = Literal["strength", "intelligence", "dexterity", "luck"]
PROFESSIONS_LITERAL = Literal["Warrior", "Mage", "Ranger", "Thief"]

ICONS = get_args(ICONS_LITERAL)
STATS = get_args(STATS_LITERAL)
PROFESSIONS = get_args(PROFESSIONS_LITERAL)

ICON_SCREEN_DICT = {
    "character": "CharacterScreen",
    "backpack": "InventoryEquipScreen",
    "dungeon": "DungeonScreen",
    "shop": "ShopScreen",
    "settings": "SettingsScreen",
}
