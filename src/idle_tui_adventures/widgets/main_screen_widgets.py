from __future__ import annotations


from textual.widgets import ProgressBar


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
            padding:0 0 0 0;
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
        total: float | None = 5,
        show_percentage: bool = True,
        show_eta: bool = False,
    ):
        super().__init__(total, show_percentage=show_percentage, show_eta=show_eta)

    def on_mount(self) -> None:
        self.timer = self.set_interval(1 / 5, self.make_progress, pause=True)
        return super().on_mount()

    def make_progress(self):
        self.update(advance=1)
        if self.percentage == 1:
            self.app.level += 1
            self.notify(
                title="Level Up",
                message=f"reached level [blue]{self.app.level}[/]",
                timeout=1,
            )
            self.update(progress=0, total=self.app.level * 5)
