from typing import Iterable

from textual.widget import Widget
from textual.widgets import Placeholder
from textual.screen import Screen

from idle_tui_adventures.widgets.main_screen_widgets import (
    MenuIconsRow,
    CharacterProgressbar,
)


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
