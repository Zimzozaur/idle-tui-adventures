from __future__ import annotations

from typing_extensions import Self, Iterable, get_args

from textual.binding import Binding
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Static, ProgressBar
from textual.containers import Horizontal

from idle_tui_adventures.constants import get_icon, ICONS


class MenuIconsRow(Horizontal):
    BINDINGS = [
        Binding("b", "open_backpack", priority=True),
        Binding("c", "open_menu", priority=True),
    ]
    DEFAULT_CSS = """MenuIconsRow {
        layout: grid;
        grid-size: 5 1;
        grid-rows: 1fr;
        grid-columns: 1fr;
        grid-gutter: 1;
        column-span: 5;
        height: 30;
    }

"""

    def compose(self) -> Iterable[Widget]:
        self.can_focus = True

        for icon in get_args(ICONS):
            yield MenuIcon(icon=icon)

        return super().compose()

    def action_open_backpack(self):
        self.log.error("Shortcut Test")
        if self.screen.name != "MainScreen":
            self.app.pop_screen()
        else:
            self.app.push_screen("InventoryEquipScreen")

    def action_open_menu(self):
        self.log.error("Shortcut Menu")
        if self.screen.name != "MainScreen":
            self.app.pop_screen()
        else:
            self.app.push_screen("InventoryEquipScreen")


class MenuIcon(Static):
    BINDINGS = [Binding("enter", "press", "Press Icon", show=False)]

    DEFAULT_CSS = """MenuIcon {
        width: 1fr;
        align: center middle;
        &:hover {
            background: yellow;
        }
        &:focus {
            border: round yellow;
        }
    }"""

    class Pressed(Message):
        def __init__(self, icon: MenuIcon) -> None:
            self.icon: MenuIcon = icon
            """The icon that was pressed."""
            super().__init__()

        @property
        def control(self) -> MenuIcon:
            return self.icon

    def __init__(self, icon: ICONS) -> None:
        self.icon = get_icon(icon=icon)

        super().__init__(self.icon, id=f"icon_{icon}")

    def press(self) -> Self:
        # Manage the "active" effect:
        # self._start_active_affect()
        # ...and let other components know that we've just been clicked:
        self.log.error(f"{self.id} was pressed")
        self.post_message(MenuIcon.Pressed(self))
        return self

    def _on_click(self, event):
        self.press()
        return super()._on_click(event=event)


class CharacterProgressbar(ProgressBar):
    DEFAULT_CSS = """
    CharacterProgressbar {
        row-span: 1;
        column-span: 5;
        width: 1fr;
        height: 3;
        border: round yellow;
        align: center middle;

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
        self.timer = self.set_interval(1 / 5, self.make_progress)
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
