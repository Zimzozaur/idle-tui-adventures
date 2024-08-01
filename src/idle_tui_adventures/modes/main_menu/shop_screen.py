from typing import Iterable

from textual.events import Mount
from textual.widget import Widget
from textual.widgets import Placeholder
from textual.screen import ModalScreen

from idle_tui_adventures.widgets.custom_widgets import MenuIconsRow


class ShopScreen(ModalScreen):
    name: str = "ShopScreen"
    BINDINGS = [("escape", "app.pop_screen"), ("l", "app.pop_screen")]
    DEFAULT_CSS = """ShopScreen {
        layout: grid;
        grid-size: 2 4;
        grid-rows: 1fr;
        grid-columns: 1fr;
        grid-gutter: 1 4;
        align: center middle;
    }
    Placeholder {
        row-span: 3;
    }
    """

    def compose(self) -> Iterable[Widget]:
        yield Placeholder("Inventory")
        yield Placeholder("Shop")
        yield MenuIconsRow()
        return super().compose()

    def _on_mount(self, event: Mount) -> None:
        self.query_one("#icon_shop").add_class("-active")
        self.log.error("set to active")
        return super()._on_mount(event)
