from typing import Iterable

from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Placeholder
from textual.containers import HorizontalScroll, Vertical

from idle_tui_adventures.database import get_all_characters
from idle_tui_adventures.widgets.icon_widgets import MenuIcon


class CharacterSelection(ModalScreen):
    name: str = "CharacterSelection"
    BINDINGS = [("escape", "app.pop_screen")]
    DEFAULT_CSS = """
    CharacterSelection {
    }
    HorizontalScroll {
        width: 1fr;
        height:1fr;

        Vertical{
            height:auto;
            width:33%;
        }
    }

    Placeholder {
        height:60%;
        width:1fr;
    }
    MenuIcon {
        height:40%;
        width:1fr;
        &:hover{
            border: panel green;
        }
    }

    """

    def compose(self) -> Iterable[Widget]:
        self.characters = get_all_characters()
        with HorizontalScroll():
            for char in self.characters:
                with Vertical():
                    yield MenuIcon(icon=char[2], id=char[1])
                    yield Placeholder("\n".join([str(i) for i in char]))
        return super().compose()
