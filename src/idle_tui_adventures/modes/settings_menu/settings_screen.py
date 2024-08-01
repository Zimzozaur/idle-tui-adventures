from typing import Iterable

from textual.widget import Widget
from textual.screen import Screen
from textual.widgets import Placeholder


class SettingsScreen(Screen):
    name: str = "SettingsScreen"
    DEFAULT_CSS = """SettingsScreen {
        layout: grid;
        grid-size: 2 1;
        grid-rows: 1fr;
        grid-columns: 1fr;
        grid-gutter: 1;
    }
    """

    def compose(self) -> Iterable[Widget]:
        for i in range(2):
            yield Placeholder("SettingsScreen", id=f"tile_{i}")

        return super().compose()
