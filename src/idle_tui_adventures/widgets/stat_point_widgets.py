from __future__ import annotations

from typing_extensions import Iterable, get_args

from textual.widget import Widget
from textual.widgets import Digits, Button
from textual.containers import Horizontal, Vertical

from idle_tui_adventures.constants import STATS_LITERAL, STATS


class StartStatRandomizer(Vertical):
    DEFAULT_CSS = """
    StartStatRandomizer {
        align: center middle;
        layout: grid;
        grid-size: 2 2;
    }
    """

    def compose(self) -> Iterable[Widget]:
        for stat in STATS:
            yield StatDisplayWithoutButton(stat=stat, value=0)
        return super().compose()

    def get_stat_dict(self):
        return {
            stat: self.query_one(f"#stat_{stat}", StatDisplayWithoutButton).int_value
            for stat in STATS
        }

    @property
    def stat_int(self) -> StatDisplayWithoutButton:
        return self.query_one("#stat_intelligence")

    @property
    def stat_str(self) -> StatDisplayWithoutButton:
        return self.query_one("#stat_strenght")

    @property
    def stat_dex(self) -> StatDisplayWithoutButton:
        return self.query_one("#stat_dexterity")

    @property
    def stat_luc(self) -> StatDisplayWithoutButton:
        return self.query_one("#stat_luck")


class StatUpdateDisplay(Vertical):
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


class StatDisplayWithoutButton(Digits):
    DEFAULT_CSS = """ StatDisplayWithoutButton {
        border: solid brown;
        width:1fr;
        height:1fr;
        content-align:center middle;
        text-align:center;

    }
    """

    def __init__(self, stat: STATS_LITERAL, value: int):
        self.stat = stat
        super().__init__(value=f"{value}", id=f"stat_{stat}")

    def compose(self) -> Iterable[Widget]:
        self.border_title = self.stat
        self.styles.border_title_color = "red"

        return super().compose()

    def set_value(self, int_val):
        self.update(value=str(int_val))

    @property
    def int_value(self) -> int:
        return int(self.value)


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
