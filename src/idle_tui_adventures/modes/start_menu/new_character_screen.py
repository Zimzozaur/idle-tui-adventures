from typing import Iterable

from textual import on
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Placeholder, Button, Input, Select
from textual.containers import Vertical, Horizontal, Center

from idle_tui_adventures.database import create_new_character, get_all_characters
from idle_tui_adventures.widgets.stat_point_widgets import (
    StartStatRandomizer,
)  # , StatDisplay
from idle_tui_adventures.constants import PROFESSIONS


class CharacterCreation(ModalScreen):
    selected_class: str

    CSS = """
    CharacterCreation {
        content-align:center middle;
        align:center middle;
    }

    Horizontal {
        layout: grid;
        grid-size: 3 1;
        grid-columns: 1fr;
        align:center middle;
    }
    CharacterCreation > Vertical {
        align:center middle;
        text-align: center;
        width: 1fr;

        Center{
            align:center middle;
            width: 33%;
        Button {
            width: 1fr;
            text-align: center;

        }
        Input {
            width: 1fr;
            text-align: center;
        }
        Select {
            width: 1fr;
        }
            }
    }

    """
    name: str = "CharacterCreation"
    BINDINGS = [("escape", "app.pop_screen")]

    def compose(self) -> Iterable[Widget]:
        with Horizontal():
            yield Placeholder("Test")
            yield StartStatRandomizer()
        with Vertical():
            with Center():
                yield Input(placeholder="Enter Character Name")
                yield Select(
                    options=[(prof, prof) for prof in PROFESSIONS],
                    prompt="Select Profession",
                    allow_blank=False,
                )
                yield Button("Create", id="btn_create_character")
                yield Button("Check", id="btn_check")
        return super().compose()

    @on(Button.Pressed, "#btn_create_character")
    def create_new_char(self):
        name = self.query_one(Input).value
        profession = self.query_one(Select).value
        if (
            msg := create_new_character(
                name=name,
                profession=profession,
                strength=1,
                intelligence=2,
                dexterity=2,
                luck=4,
            )
        ) == 0:
            self.notify(
                title="Character Creation Successful",
                message=f"[blue]{name}[/], the [blue]{profession}[/] is ready for Adventures",
            )
        else:
            self.notify(
                title="Charcter Creation Failed",
                message=f"Error [red]{msg}[/]",
                severity="error",
            )

    @on(Button.Pressed, "#btn_check")
    def check_chars(self):
        get_all_characters()
