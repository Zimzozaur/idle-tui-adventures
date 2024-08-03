from __future__ import annotations

from typing_extensions import Iterable, get_args

from textual.widget import Widget
from textual.widgets import Label, Digits, Button
from textual.containers import Horizontal, Vertical

from idle_tui_adventures.constants import STATS_LITERAL, STATS


class StartStatRandomizer(Vertical):
    DEFAULT_CSS = """
    StartStatRandomizer {
        align: center middle;
    }
    """

    def compose(self) -> Iterable[Widget]:
        for stat in STATS:
            yield StatDisplayWithoutButton(stat=stat, value=0)
        return super().compose()


class StatDisplay(Vertical):
    DEFAULT_CSS = """
    StatDisplay {
        align: center middle;
        layout:grid;
        grid-size: 3 4;
        width: 1fr;
    }
    """

    def compose(self) -> Iterable[Widget]:
        for stat in get_args(STATS):
            yield StatDisplayWithButton(stat=stat, value=0)
        return super().compose()


class StatDisplayWithoutButton(Vertical):
    DEFAULT_CSS = """ StatDisplayWithoutButton {
        layout: grid;
        grid-size: 1 2;
        grid-rows: 1fr;
        column-span: 1;

        & Label {
            align: center middle;
            width: auto;
        }
        & Digits {
            align: center middle;
            width: auto;
        }
    }
    """

    def __init__(self, stat: STATS_LITERAL, value: int):
        self.stat = stat
        self.value = value
        super().__init__()

    def compose(self) -> Iterable[Widget]:
        yield Label(renderable=self.stat)
        yield Digits(value=f"{self.value}")
        return super().compose()


class StatDisplayWithButton(Horizontal):
    DEFAULT_CSS = """ StatDisplayWithButton {
        layout: grid;
        grid-size: 3 2;
        grid-rows: 1fr;
        grid-columns: 1fr;
        column-span: 3;

        & Button {
            column-span:1;
            row-span: 2;
            width:1fr;
        }

        & StatDisplayWithoutButton {
            column-span:1;
            width:1fr;
        }
    }
    """

    def __init__(self, stat: STATS_LITERAL, value: int):
        self.stat = stat
        self.value = value
        super().__init__()

    def compose(self) -> Iterable[Widget]:
        yield Button("-", variant="error")
        yield StatDisplayWithoutButton(stat=self.stat, value=self.value)
        yield Button("+", variant="error")
        return super().compose()
