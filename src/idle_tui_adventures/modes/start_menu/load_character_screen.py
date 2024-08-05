from typing import Iterable

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
        height:1fr;

        CharacterPreview {
            height:1fr;
            width:33%;
        }

    }


    """

    def compose(self) -> Iterable[Widget]:
        self.characters = get_all_characters()
        with HorizontalScroll():
            for char in self.characters:
                yield CharacterPreview(character_infos=char)
                # with Vertical():
                #     yield MenuIcon(icon=char[2], id=char[1])
                #     yield Placeholder("\n".join([str(i) for i in char]))
        return super().compose()
