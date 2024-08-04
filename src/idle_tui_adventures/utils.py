from pathlib import Path
from rich_pixels import Pixels

from idle_tui_adventures.constants import ICONS_LITERAL


def get_icon(icon: ICONS_LITERAL, width: int = 30, heigth: int = 25) -> Pixels:
    icon_path = Path(__file__).parent / f"./static/image_{icon}.png"
    return Pixels.from_image_path(icon_path, resize=(width, heigth))
