from typing import Literal, get_args
from pathlib import Path
# from platformdirs import user_data_dir, user_config_dir

# Config related

# CONFIG_PATH = Path(
#     user_config_dir(appname="idle-tui-adventures", appauthor=False, ensure_exists=True)
# )
CONFIG_NAME = "idle_tui_adventures.ini"
CONFIG_PATH = Path(".").cwd()
CONFIG_FULL_PATH = CONFIG_PATH / CONFIG_NAME

# DB related
DB_NAME = "database.db"
DB_PATH = Path(".").cwd()
# DB = Path(
#     user_data_dir(appname="idle-tui-adventures", appauthor=False, ensure_exists=True)
# )
DB_FULL_PATH = DB_PATH / DB_NAME

# Stats related
STATS_LITERAL = Literal["strength", "intelligence", "dexterity", "luck"]
STATS = get_args(STATS_LITERAL)
MIN_START_STAT = 18
MAX_START_STAT = 22
START_STAT_DISTRIBUTION_DICT = {
    "Warrior": [0.4, 0.2, 0.2, 0.2],
    "Mage": [0.2, 0.4, 0.2, 0.2],
    "Ranger": [0.2, 0.2, 0.4, 0.2],
    "Thief": [0.2, 0.2, 0.2, 0.4],
}
PROFESSION_MAINSTAT_DICT = {
    "Warrior": "strength",
    "Mage": "intelligence",
    "Ranger": "dexterity",
    "Thief": "luck",
}

# Item-rarity
RARITIES_LITERAL = Literal["common", "rare", "epic", "legendary", "unique"]
RARITIES = get_args(RARITIES_LITERAL)
ITEM_RARITIES_COLOR_DICT = {
    "common": "green",
    "rare": "blue",
    "epic": "red",
    "orange": "orange",
    "unique": "#aefdfd",
}

# Item-category
ITEM_CATEGORIES_LITERAL = Literal[
    "Consumable",
    "Weapon",
    "Armor",
]
ITEM_CATEGORIES = get_args(ITEM_CATEGORIES_LITERAL)

# Icons-menu
MENU_ICONS_LITERAL = Literal["character", "backpack", "dungeon", "shop", "settings"]
MENU_ICONS = get_args(MENU_ICONS_LITERAL)

# Icons-professions
PROFESSIONS_LITERAL = Literal["Warrior", "Mage", "Ranger", "Thief"]
PROFESSIONS = get_args(PROFESSIONS_LITERAL)
ICONS_LITERAL = MENU_ICONS_LITERAL | PROFESSIONS_LITERAL | ITEM_CATEGORIES_LITERAL
ICON_SCREEN_DICT = {
    "character": "CharacterScreen",
    "backpack": "InventoryEquipScreen",
    "dungeon": "DungeonScreen",
    "shop": "ShopScreen",
    "settings": "SettingsScreen",
}

# Inventory (Row,Cols)
INVENTORY_SIZE = (4, 4)
