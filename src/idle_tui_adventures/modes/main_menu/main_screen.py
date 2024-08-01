from typing import Iterable

from textual import events, on
from textual.widget import Widget
from textual.reactive import reactive
from textual.widgets import Placeholder, Label, Button
from textual.screen import Screen, ModalScreen

from idle_tui_adventures.widgets.custom_widgets import (
    MenuIconsRow,
    CharacterProgressbar,
)
from idle_tui_adventures.modes.main_menu.inventory_screen import (
    InventoryEquipScreen,
)


class PopUpScreen(ModalScreen):
    def compose(self) -> Iterable[Widget]:
        yield Button()
        yield Button()
        return super().compose()

    def on_button_pressed(self):
        self.dismiss()


class Position(Placeholder):
    text: reactive = reactive("")

    def __init__(self):
        super().__init__()
        self.set_reactive(Position.text, "starter")

    def compose(self) -> Iterable[Widget]:
        yield Label(self.text, id="position")
        return super().compose()

    def watch_text(self, text):
        self.query_one("#position", Label).update(text)

    def on_click(self):
        self.app.push_screen(PopUpScreen())


class MainScreen(Screen):
    name: str = "MainScreen"
    DEFAULT_CSS = """MainScreen {
        layout: grid;
        grid-size: 3 4;
        grid-rows: 1fr;
        grid-columns: 1fr;
        grid-gutter: 1;
        align: center middle;
    }
    """

    def compose(self) -> Iterable[Widget]:
        for i in range(9):
            yield Placeholder("MainScreen", id=f"tile_{i}")
        yield CharacterProgressbar()
        yield MenuIconsRow()

        return super().compose()

    @on(
        events.MouseDown,
    )
    def open_backpack(self, event: events.MouseDown):
        position = event.screen_offset
        if self.get_widget_at(*position)[0].id == "backpack":
            self.app.push_screen(InventoryEquipScreen())
