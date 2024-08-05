from pathlib import Path
from rich_pixels import Pixels
import random
from collections import Counter

from idle_tui_adventures.constants import (
    ICONS_LITERAL,
    PROFESSIONS_LITERAL,
    STATS,
    START_STAT_DISTRIBUTION_DICT,
    MIN_START_STAT,
    MAX_START_STAT,
)


def get_icon(icon: ICONS_LITERAL, width: int = 30, heigth: int = 25) -> Pixels:
    icon_path = Path(__file__).parent / f"./assets/static/image_{icon.lower()}.png"
    return Pixels.from_image_path(icon_path, resize=(width, heigth))


def get_random_amount_start_stats(profession: PROFESSIONS_LITERAL):
    amount_stats = random.randint(MIN_START_STAT, MAX_START_STAT)
    return Counter(
        random.choices(
            population=STATS,
            weights=START_STAT_DISTRIBUTION_DICT[profession],
            k=amount_stats,
        )
    )
