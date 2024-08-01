from typing import Iterable

from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Placeholder


class CharacterSelection(ModalScreen):
    name: str = "CharacterSelection"
    BINDINGS = [("escape", "app.pop_screen")]

    def compose(self) -> Iterable[Widget]:
        yield Placeholder("Load Character Screen")
        return super().compose()
