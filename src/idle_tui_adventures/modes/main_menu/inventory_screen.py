from typing import Iterable, Any, Coroutine

from textual.events import Mount, Key
from textual.widget import Widget
from textual.widgets import Static, Placeholder
from textual.screen import ModalScreen

from idle_tui_adventures.widgets.icon_widgets import MenuIconsRow
from idle_tui_adventures.widgets.inventory_screen_widgets import Inventory
from idle_tui_adventures.utils import get_icon


class InventoryEquipScreen(ModalScreen):
    name: str = "InventoryEquipScreen"
    BINDINGS = [("escape", "app.pop_screen"), ("b", "app.pop_screen")]
    DEFAULT_CSS = """InventoryEquipScreen {
        layout: grid;
        grid-size: 2 2;
        grid-rows: 75% 24%;
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
        yield Inventory()
        yield Placeholder()

        yield MenuIconsRow()
        return super().compose()

    def _on_mount(self, event: Mount) -> None:
        self.query_one("#backpack").add_class("-active")
        return super()._on_mount(event)

    def _on_key(self, event: Key) -> Coroutine[Any, Any, None]:
        key_pressed = event.key
        try:
            self.query_one(Inventory).query_one(f"#slot_{key_pressed}").place_item(
                Static(get_icon("Mage"))
            )
            self.notify(f"That key was pressed {key_pressed}")
        except Exception as e:
            self.log.error(e)
        return super()._on_key(event)
