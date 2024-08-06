from typing import Iterable

from textual import on
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Button, Input, Select
from textual.containers import Vertical, Horizontal, Center

from idle_tui_adventures.database import create_new_character
from idle_tui_adventures.widgets.stat_point_widgets import (
    StartStatRandomizer,
)  # , StatDisplay
from idle_tui_adventures.constants import PROFESSIONS
from idle_tui_adventures.widgets.icon_widgets import MenuIcon


class CharacterCreation(ModalScreen):
    name: str = "CharacterCreation"
    BINDINGS = [("escape", "app.pop_screen")]

    CSS = """
    CharacterCreation {
        content-align:center middle;
        align:center middle;

        & > Horizontal {
            layout: grid;
            grid-size: 2 1;
            grid-columns: 1fr;
            align:center middle;
            }
        & > Vertical {
            align:center middle;
            text-align: center;
            width: 1fr;

            Center {
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
    }

    """

    def compose(self) -> Iterable[Widget]:
        with Horizontal():
            # profession image mounted here
            yield StartStatRandomizer(id="stat_randomizer")
        with Vertical():
            with Center():
                yield Input(placeholder="Enter Character Name")
                yield Select(
                    options=[(prof, prof) for prof in PROFESSIONS],
                    prompt="Select Profession",
                    allow_blank=False,
                    id="select_profession_choice",
                )
                yield Button("Create", id="btn_create_character")
                yield Button("Go Back to Start Screen", id="btn_return")

        return super().compose()

    def on_mount(self):
        start_class = self.query_one(Select).value
        self.mount(
            MenuIcon(icon=start_class, id=start_class), before="#stat_randomizer"
        )

    @on(Button.Pressed, "#btn_create_character")
    def create_new_char(self):
        name = self.query_one(Input).value
        profession = self.query_one(Select).value
        stats = self.query_one(StartStatRandomizer).get_stat_dict()
        char_dict = {
            "name": name,
            "profession": profession,
            **stats,
        }
        if (msg := create_new_character(**char_dict)) == 0:
            self.notify(
                title="Character Creation Successful",
                message=f"[blue]{name}[/], the [blue]{profession}[/] is ready for Adventures",
                timeout=1.0,
            )
            # Create Character and go back to Start Screen
            self.dismiss()
        else:
            self.notify(
                title="Character Creation Failed",
                message=f"Error [red]{msg}[/]",
                severity="error",
                timeout=3.0,
            )

    @on(Button.Pressed, "#btn_return")
    def go_to_start_screen(self):
        self.app.pop_screen()

    @on(Select.Changed, "#select_profession_choice")
    async def select_a_profession(self, event: Select.Changed):
        selected_class_name = event.value
        self.query_one(StartStatRandomizer).query_one(Button).press()
        await self.query_one(MenuIcon).remove()
        self.mount(
            MenuIcon(icon=selected_class_name, id=selected_class_name),
            before="#stat_randomizer",
        )
