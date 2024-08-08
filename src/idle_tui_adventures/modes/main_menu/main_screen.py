from typing import Iterable

from textual import on
from textual.events import ScreenResume, ScreenSuspend
from textual.widget import Widget
from textual.widgets import Placeholder
from textual.screen import Screen

from idle_tui_adventures.widgets.main_screen_widgets import (
    CharacterProgressbar,
    MonsterPanel,
)
from idle_tui_adventures.widgets.icon_widgets import MenuIconsRow
from idle_tui_adventures.utils import calculate_exp_needed


class MainScreen(Screen):
    name: str = "MainScreen"
    DEFAULT_CSS = """MainScreen {
        layout: grid;
        grid-size: 3 4;
        grid-rows: 1fr;
        grid-columns: 1fr;
        grid-gutter: 1;
        align: center middle;
    }

    """

    def compose(self) -> Iterable[Widget]:
        yield Placeholder("MainScreen", id="tile_0")
        yield MonsterPanel()
        yield Placeholder("MainScreen", id="tile_1")
        yield Placeholder("MainScreen", id="tile_2")

        yield CharacterProgressbar()
        yield MenuIconsRow()

        return super().compose()

    @on(ScreenSuspend)
    def pause_progress(self):
        p_bar = self.query_one(CharacterProgressbar)
        p_bar.timer.pause()

    @on(ScreenResume)
    def recalibrate_progressbar(self):
        if self.app.character:
            new_total = calculate_exp_needed(next_lvl=self.app.character.level + 1)
            last_total = calculate_exp_needed(next_lvl=self.app.character.level)
            current_exp = self.app.character.experience - last_total

            p_bar = self.query_one(CharacterProgressbar)
            p_bar.update(progress=current_exp, total=new_total - last_total)
            p_bar.timer.resume()
