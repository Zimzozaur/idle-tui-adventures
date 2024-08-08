from __future__ import annotations
from typing import Coroutine, Any


from textual.events import Compose
from textual.widgets import ProgressBar

from idle_tui_adventures.utils import calculate_exp_needed


class CharacterProgressbar(ProgressBar):
    DEFAULT_CSS = """
    CharacterProgressbar {
        column-span: 5;
        row-span: 1;
        width: 1fr;
        height: 3;
        align: center middle;
        layer: above;
        offset: 0 300%;

        & Bar  {
            width: 1fr;
            }

        & Bar > .bar--bar {
            color: blue;
            }

        & PercentageStatus {
        width: 5;
        align: center middle;
        offset: -50vw 0;
        }
    }
"""

    def __init__(
        self,
        show_percentage: bool = True,
        show_eta: bool = False,
    ):
        super().__init__(show_percentage=show_percentage, show_eta=show_eta)

    def _on_compose(self, event: Compose) -> Coroutine[Any, Any, None]:
        self.timer = self.set_interval(1 / 10, self.make_progress, pause=True)
        return super()._on_compose(event)

    def on_mount(self) -> None:
        if self.app.character:
            new_total = calculate_exp_needed(next_lvl=self.app.character.level + 1)
            current_exp = self.app.character.experience

            self.update(progress=0, total=new_total - current_exp)
            self.timer.resume()
        return super().on_mount()

    def make_progress(self):
        self.update(advance=1)
        self.app.character.collect_exp()
        if self.percentage == 1:
            self.advance_level()

    def advance_level(self):
        self.app.character.level_up()
        self.notify(
            title="Level Up",
            message=f"{self.app.character.name} reached level [blue]{self.app.character.level}[/]",
            timeout=1,
        )
        new_total = calculate_exp_needed(next_lvl=self.app.character.level + 1)
        current_exp = self.app.character.experience
        self.update(progress=0, total=new_total - current_exp)
