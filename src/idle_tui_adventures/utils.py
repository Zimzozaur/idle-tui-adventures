from pathlib import Path
from rich_pixels import Pixels

from idle_tui_adventures.constants import ICONS_LITERAL


def get_icon(icon: ICONS_LITERAL) -> Path:
    icon_path = Path(__file__).parent / f"./static/image_{icon}.png"
    return Pixels.from_image_path(icon_path, resize=(30, 25))
