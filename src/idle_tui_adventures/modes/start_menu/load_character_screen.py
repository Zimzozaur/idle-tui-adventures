from typing import Iterable
from sqlite3 import Row

from textual.screen import ModalScreen
from textual.widget import Widget
from textual.containers import HorizontalScroll
from textual.widgets import Button

from idle_tui_adventures.database import get_all_characters
from idle_tui_adventures.widgets.icon_widgets import CharacterPreview


class CharacterSelection(ModalScreen):
    name: str = "CharacterSelection"
    BINDINGS = [("escape", "app.pop_screen")]
    DEFAULT_CSS = """
    CharacterSelection {
        align:center middle;

        Button {
            align:center middle;
            height: 10%;
            width:1fr;
        }
        HorizontalScroll {
            width: 1fr;
            height:80%;
            CharacterPreview {
                height:1fr;
                width:33%;
            }
        }
    }
    """

    def compose(self) -> Iterable[Widget]:
        self.characters: list[Row] = get_all_characters()
        with HorizontalScroll():
            for char_data in self.characters:
                yield CharacterPreview(character_data=char_data)
        yield Button("Start Adventure")
        yield Button("Back to Start Screen")
        return super().compose()
