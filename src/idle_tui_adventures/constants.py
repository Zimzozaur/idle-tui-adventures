from typing import Literal
from pathlib import Path
from rich_pixels import Pixels

BACKPACK_IMG = Path(__file__).parent / "./static/image_backpack.png"
CHARACTER_IMG = Path(__file__).parent / "./static/image_character.png"
DUNGEON_IMG = Path(__file__).parent / "./static/image_dungeon.png"
SHOP_IMG = Path(__file__).parent / "./static/image_shop.png"
SETTINGS_IMG = Path(__file__).parent / "./static/image_settings.png"

ICONS = Literal["character", "backpack", "dungeon", "shop", "settings"]

ICON_SCREEN_DICT = {
    "character": "CharacterScreen",
    "backpack": "InventoryEquipScreen",
    "dungeon": "",
    "shop": "",
    "settings": "",
}


def get_icon(icon: ICONS) -> Path:
    icon_path = Path(__file__).parent / f"./static/image_{icon}.png"
    return Pixels.from_image_path(icon_path, resize=(30, 25))
