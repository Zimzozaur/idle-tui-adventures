from sqlite3 import Row
from typing import Iterable

from textual import on
from textual.events import Mount
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.containers import HorizontalScroll
from textual.widgets import Button

from idle_tui_adventures.database.db_queries import get_all_characters
from idle_tui_adventures.widgets.icon_widgets import CharacterPreview


class CharacterSelection(ModalScreen):
    name: str = "CharacterSelection"
    BINDINGS = [("escape", "app.pop_screen")]
    DEFAULT_CSS = """
    CharacterSelection {
        align:center middle;

        CharacterPreview {
            & :hover {
                border: outer yellow;
            }
        }

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
        yield Button("Start Adventure", id="btn_start_adventure")
        yield Button("Back to Start Screen", id="btn_go_back")
        return super().compose()

    def _on_mount(self, event: Mount) -> None:
        try:
            self.query_one(
                f"#character_id_{self.app.cfg.active_character_id}"
            ).add_class("-active")
        except Exception:
            self.notify(
                title="No active character selected",
                message="Please select a character or create one",
                severity="error",
            )
        return super()._on_mount(event)

    @on(Button.Pressed, "#btn_start_adventure")
    def move_to_main_screen(self):
        self.dismiss()
        self.app.switch_mode("Main")

    @on(Button.Pressed, "#btn_go_back")
    def move_to_start_screen(self):
        self.dismiss()

    @on(CharacterPreview.SelectOther)
    def only_highlight_clicked(self, event: CharacterPreview.SelectOther) -> None:
        # remove active class from other Widgets
        self.app.cfg.active_character_id = event.character_preview.id.split("_")[-1]
        self.app.load_active_character()
        self.query(CharacterPreview).exclude(
            f"#{event.character_preview.id}"
        ).remove_class("-active")
