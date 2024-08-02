from typing import Iterable

from textual import on
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Placeholder, Button, Input
from textual.containers import Vertical, Horizontal

from idle_tui_adventures.database import create_new_character, get_all_characters


class CharacterCreation(ModalScreen):
    CSS = """
    CharacterCreation {
        align:center middle;
    }

    Horizontal {
        align:center middle;
    }
    Vertical {
        align:center middle;
    }

    Button {
        width: auto;
    }
    Input {
        width: auto;
    }
    """
    name: str = "CharacterCreation"
    BINDINGS = [("escape", "app.pop_screen")]

    def compose(self) -> Iterable[Widget]:
        with Horizontal():
            yield Placeholder("New Character Screen")
            yield Placeholder("Stat Roller")
        with Vertical():
            yield Input(placeholder="Enter Character Name")
            yield Button("Create", id="btn_create_character")
            yield Button("Check", id="btn_check")
        return super().compose()

    @on(Button.Pressed, "#btn_create_character")
    def create_new_char(self):
        val = self.query_one(Input).value
        create_new_character(
            name=val,
            profession="tester",
            strength=1,
            intelligence=2,
            dexterity=2,
            luck=4,
        )

    @on(Button.Pressed, "#btn_check")
    def check_chars(self):
        get_all_characters()
