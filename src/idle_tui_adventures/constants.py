from typing import Literal
from pathlib import Path
from rich_pixels import Pixels

ICONS = Literal["character", "backpack", "dungeon", "shop", "settings"]

ICON_SCREEN_DICT = {
    "character": "CharacterScreen",
    "backpack": "InventoryEquipScreen",
    "dungeon": "DungeonScreen",
    "shop": "ShopScreen",
    "settings": "SettingsScreen",
}


def get_icon(icon: ICONS) -> Path:
    icon_path = Path(__file__).parent / f"./static/image_{icon}.png"
    return Pixels.from_image_path(icon_path, resize=(30, 25))
