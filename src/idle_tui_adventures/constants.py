from typing import Literal, get_args
from pathlib import Path

DB_NAME = "database.db"
DB_PATH = Path(".").cwd()
DB_FULLNAME = DB_PATH / DB_NAME

MENU_ICONS_LITERAL = Literal["character", "backpack", "dungeon", "shop", "settings"]
STATS_LITERAL = Literal["strength", "intelligence", "dexterity", "luck"]
PROFESSIONS_LITERAL = Literal["Warrior", "Mage", "Ranger", "Thief"]
ICONS_LITERAL = MENU_ICONS_LITERAL | PROFESSIONS_LITERAL

MENU_ICONS = get_args(MENU_ICONS_LITERAL)
STATS = get_args(STATS_LITERAL)
PROFESSIONS = get_args(PROFESSIONS_LITERAL)

ICON_SCREEN_DICT = {
    "character": "CharacterScreen",
    "backpack": "InventoryEquipScreen",
    "dungeon": "DungeonScreen",
    "shop": "ShopScreen",
    "settings": "SettingsScreen",
}

MIN_START_STAT = 18
MAX_START_STAT = 22
START_STAT_DISTRIBUTION_DICT = {
    "Warrior": [0.4, 0.2, 0.2, 0.2],
    "Mage": [0.2, 0.4, 0.2, 0.2],
    "Ranger": [0.2, 0.2, 0.4, 0.2],
    "Thief": [0.2, 0.2, 0.2, 0.4],
}
