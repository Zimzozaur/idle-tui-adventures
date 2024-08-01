from typing import Iterable

from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Placeholder


class CharacterCreation(ModalScreen):
    BINDINGS = [("escape", "app.pop_screen")]

    def compose(self) -> Iterable[Widget]:
        yield Placeholder("New Character Screen")
        return super().compose()
