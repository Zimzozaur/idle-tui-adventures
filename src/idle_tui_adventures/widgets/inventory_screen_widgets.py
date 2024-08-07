from typing import Iterable
from math import prod

from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Grid

from idle_tui_adventures.constants import INVENTORY_SIZE, ITEM_CATEGORIES_LITERAL


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


class Equipment(Grid):
    equipment_dict: dict

    DEFAULT_CSS = (
        """
    Equipment {
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
            yield EquipSlot(id=f"slot_{i}")

        return super().compose()


class Slot(Static):
    amount: reactive = reactive(0)

    def __init__(self, id: str | None = None) -> None:
        super().__init__(id=id)

    def compose(self) -> Iterable[Widget]:
        self.styles.border_subtitle_color = "yellow"
        self.border_subtitle = f"{self.amount} x" if self.amount else ""
        # yield Static(renderable=get_icon("Mage"))
        return super().compose()

    @property
    def empty(self) -> bool:
        return len(self.children) == 0

    def place_item(self, item) -> None:
        if self.empty:
            self.mount(item)
            self.amount = 1
        else:
            pass

    def watch_amount(self, value):
        self.border_subtitle = f"{self.amount} x" if self.amount else ""

    # def _on_mouse_down(self, event: MouseDown) -> Coroutine[Any, Any, None]:
    #     if event.button == 1:
    #         try:
    #             self.query_one(Static).remove()
    #             self.amount -= 1
    #         except Exception as e:
    #             self.notify(str(e))
    #     return super()._on_mouse_down(event)

    # weiterer Static drauf
    # bei mouse_down obere static in modal mit offset


class ItemSlot(Slot):
    DEFAULT_CSS = """ItemSlot {
        width: 1fr;
        height: 1fr;
        align: center middle;
        content-align: center middle;
        background: #ba9f68;
        border:outer #6a4f32;
        border-subtitle-background:#6a4f32;

    }"""

    def __init__(self, id: str | None = None) -> None:
        super().__init__(id)


class EquipSlot(Slot):
    category: ITEM_CATEGORIES_LITERAL
    in_use: bool = False

    DEFAULT_CSS = """EquipSlot {
        width: 1fr;
        height: 1fr;
        align: center middle;
        content-align: center middle;
        background:  #6b6c6f;
        border:outer #474748;
        border-subtitle-background:#474748;

    }"""

    def __init__(self, id: str | None = None) -> None:
        super().__init__(id)
