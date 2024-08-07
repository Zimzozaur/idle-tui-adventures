from typing import Iterable
from math import prod

from textual.widget import Widget
from textual.containers import Grid

from idle_tui_adventures.widgets.icon_widgets import ItemSlot
from idle_tui_adventures.constants import INVENTORY_SIZE


class Inventory(Grid):
    inventory_dict: dict

    DEFAULT_CSS = (
        """
    Inventory {
        grid-size: %d %d;

        ItemSlot {
            width:1fr;
            height:1fr;
        }
    }
    """
        % INVENTORY_SIZE
    )

    # On Mount?
    # query items
    # place items
    def compose(self) -> Iterable[Widget]:
        for i in range(prod(INVENTORY_SIZE)):
            yield ItemSlot(id=f"slot_{i}")

        return super().compose()
