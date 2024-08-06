from typing import Iterable

from textual.events import Mount
from textual.widget import Widget
from textual.widgets import Placeholder
from textual.screen import ModalScreen

from idle_tui_adventures.widgets.icon_widgets import MenuIconsRow, DragableSlot


class InventoryEquipScreen(ModalScreen):
    name: str = "InventoryEquipScreen"
    BINDINGS = [("escape", "app.pop_screen"), ("b", "app.pop_screen")]
    DEFAULT_CSS = """InventoryEquipScreen {
        layout: grid;
        grid-size: 2 4;
        grid-rows: 1fr;
        grid-columns: 1fr;
        grid-gutter: 1 4;
        align: center middle;
    }
    Placeholder {
        row-span: 1;
    }
    DragableSlot {
        row-span: 1;
        width:1fr;
        height:1fr;
    }
    """

    def compose(self) -> Iterable[Widget]:
        yield DragableSlot("Thief", id="slot1")
        yield DragableSlot("Mage", id="slot2")
        yield Placeholder("Inventory")
        yield Placeholder("Equipment")
        yield Placeholder("Inventory")
        yield Placeholder("Equipment")
        yield MenuIconsRow()
        return super().compose()

    def _on_mount(self, event: Mount) -> None:
        self.query_one("#backpack").add_class("-active")
        return super()._on_mount(event)

    def _on_screen_suspend(self) -> None:
        return super()._on_screen_suspend()
