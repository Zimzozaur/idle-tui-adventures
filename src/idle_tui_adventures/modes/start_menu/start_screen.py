from typing import Iterable

from textual import on
from textual.widget import Widget
from textual.screen import Screen
from textual.widgets import Button, Checkbox

from idle_tui_adventures.modes.start_menu.new_character_screen import CharacterCreation
from idle_tui_adventures.modes.start_menu.load_character_screen import (
    CharacterSelection,
)


class StartScreen(Screen):
    name: str = "StartScreen"
    DEFAULT_CSS = """StartScreen {
        align: center middle;
    }

    """

    def compose(self) -> Iterable[Widget]:
        yield Button("New Character", id="btn_move_to_character_creation")
        yield Button("Load Character", id="btn_move_to_load_character")
        yield Checkbox(label="Skip this Screen and Start with latest Character")

        return super().compose()

    @on(Button.Pressed, "#btn_move_to_character_creation")
    def open_character_creation_screen(self, _message: Button.Pressed) -> None:
        # message needs a control attribute
        self.log.debug('Pressed "New Character" Button')
        self.app.push_screen(CharacterCreation())

    @on(Button.Pressed, "#btn_move_to_load_character")
    def open_load_character_screen(self, _message: Button.Pressed) -> None:
        # message needs a control attribute
        self.log.debug('Pressed "Load Character" Button')
        self.app.push_screen(CharacterSelection())
