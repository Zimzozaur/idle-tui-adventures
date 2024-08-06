from typing import Iterable
from sqlite3 import Row

from textual.screen import ModalScreen
from textual.widget import Widget
from textual.containers import HorizontalScroll

from idle_tui_adventures.database import get_all_characters
from idle_tui_adventures.widgets.icon_widgets import CharacterPreview


class CharacterSelection(ModalScreen):
    name: str = "CharacterSelection"
    BINDINGS = [("escape", "app.pop_screen")]
    DEFAULT_CSS = """
    CharacterSelection {
    }
    HorizontalScroll {
        width: 1fr;
        height:auto;

        CharacterPreview {
            height:1fr;
            width:33%;
        }

    }


    """

    def compose(self) -> Iterable[Widget]:
        self.characters: list[Row] = get_all_characters()
        with HorizontalScroll():
            for char_data in self.characters:
                yield CharacterPreview(character_data=char_data)
        return super().compose()
