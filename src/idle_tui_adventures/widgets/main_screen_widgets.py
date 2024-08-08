from __future__ import annotations
from typing import Coroutine, Any, Iterable


from textual.geometry import Offset
from textual.events import Click, Compose
from textual.widget import Widget
from textual.widgets import ProgressBar, Label
from textual.containers import Vertical

from idle_tui_adventures.utils import calculate_exp_needed
from idle_tui_adventures.widgets.icon_widgets import ImageStatic


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
            last_total = calculate_exp_needed(next_lvl=self.app.character.level)
            current_exp = self.app.character.experience - last_total

            self.update(progress=current_exp, total=new_total - last_total)
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
        last_total = calculate_exp_needed(next_lvl=self.app.character.level)
        self.update(progress=0, total=new_total - last_total)


class MonsterPanel(Vertical):
    DEFAULT_CSS = """
    MonsterPanel {
        row-span: 3;
        column-span: 2;
        width: 1fr;
        height: 1fr;

        ProgressBar {
        height: auto;

        & Bar  {
            width: 1fr;
            }

        & Bar > .bar--bar {
            color: red;
            }
        }
        ImageStatic {
        width: 1fr;
        height: 1fr;
        }
    }
    """

    def compose(self) -> Iterable[Widget]:
        self.monster_label = Label("Big Bear")
        yield self.monster_label
        self.pb = ProgressBar(
            total=1000, id="pb_monster_hp", show_eta=False, show_percentage=False
        )
        self.pb.progress = 1000
        yield self.pb
        yield ImageStatic(icon_name="dragon")

        return super().compose()

    def _on_click(self, event: Click) -> Coroutine[Any, Any, None]:
        damage = 125
        self.query_one(ImageStatic).mount(DamageLabel(damage=damage))
        self.pb.progress -= damage
        if self.pb.progress == 0:
            self.monster_label.update("Dead Bear")
        return super()._on_click(event)


class Healthbar(ProgressBar): ...


class DamageLabel(Label):
    DEFAULT_CSS = """
    DamageLabel {
        layer:above;
        color:red;
        text_align:center;
        width:auto;
        background:black 20%;

        & .-crit {
            color: blue;
        }
    }
    """

    def __init__(self, damage: int, crit: bool = False) -> None:
        self.damage = damage
        if crit:
            self.add_class("-crit")
        super().__init__(renderable=f"{damage}")

        self.offset = self.app.mouse_position  # - (self.region.offset[0], 0)
        self.fly_away()

    def fly_away(self):
        self.styles.animate(
            attribute="opacity", value=0, duration=2.0, on_complete=self.remove
        )

        self.animate(
            attribute="offset",
            value=Offset(self.app.mouse_position[0], 0),  # - self.region.offset[0], 0),
            duration=1.5,
            easing="out_expo",
        )
