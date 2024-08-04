from __future__ import annotations

from typing_extensions import Self, Iterable

from textual import on
from textual.events import Resize
from textual.binding import Binding
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Horizontal

from idle_tui_adventures.constants import ICONS, ICON_SCREEN_DICT, ICONS_LITERAL
from idle_tui_adventures.utils import get_icon


class MenuIcon(Static):
    BINDINGS = [Binding("enter", "press", "Press Icon", show=False)]

    DEFAULT_CSS = """MenuIcon {
        width: 1fr;
        height: 1fr;
        align: center middle;
        content-align: center middle;
        &:hover {
            background: yellow;
        }
        &:focus {
            border: round yellow;
            }
        &.-active {
            background: $success;
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

    def __init__(self, icon: ICONS_LITERAL) -> None:
        self.icon_name = icon
        self.icon_img = get_icon(icon=self.icon_name)

        super().__init__(self.icon_img, id=f"icon_{self.icon_name}")

    def press(self) -> Self:
        # Manage the "active" effect:
        # self._start_active_affect()
        # ...and let other components know that we've just been clicked:
        self.log.debug(f"{self.id} was pressed")
        self.post_message(MenuIcon.Pressed(self))
        return self

    def _on_click(self, event):
        self.press()
        return super()._on_click(event=event)

    @on(Resize)
    def keep_image_size(self, event: Resize):
        new_width, new_height = event.size
        self.update(
            get_icon(icon=self.icon_name, width=new_width, heigth=int(1.8 * new_height))
        )


class MenuIconsRow(Horizontal):
    BINDINGS = [
        Binding("b", "open_backpack", priority=True),
        Binding("c", "open_character", priority=True),
        Binding("d", "open_dungeon", priority=True),
        Binding("l", "open_shop", priority=True),
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

        for icon in ICONS:
            yield MenuIcon(icon=icon)

        return super().compose()

    @on(MenuIcon.Pressed, "#icon_character")
    def action_open_character(self):
        icon = "character"
        if self.screen.name == ICON_SCREEN_DICT[icon]:
            self.app.pop_screen()
        elif self.screen.name == "MainScreen":
            self.app.push_screen(ICON_SCREEN_DICT[icon])
        else:
            self.app.pop_screen()
            self.app.push_screen(ICON_SCREEN_DICT[icon])

    @on(MenuIcon.Pressed, "#icon_backpack")
    def action_open_backpack(self):
        icon = "backpack"
        if self.screen.name == ICON_SCREEN_DICT[icon]:
            self.app.pop_screen()
        elif self.screen.name == "MainScreen":
            self.app.push_screen(ICON_SCREEN_DICT[icon])
        else:
            self.app.pop_screen()
            self.app.push_screen(ICON_SCREEN_DICT[icon])

    @on(MenuIcon.Pressed, "#icon_dungeon")
    def action_open_dungeon(self):
        icon = "dungeon"
        if self.screen.name == ICON_SCREEN_DICT[icon]:
            self.app.pop_screen()
        elif self.screen.name == "MainScreen":
            self.app.push_screen(ICON_SCREEN_DICT[icon])
        else:
            self.app.pop_screen()
            self.app.push_screen(ICON_SCREEN_DICT[icon])

    @on(MenuIcon.Pressed, "#icon_shop")
    def action_open_shop(self):
        icon = "shop"
        if self.screen.name == ICON_SCREEN_DICT[icon]:
            self.app.pop_screen()
        elif self.screen.name == "MainScreen":
            self.app.push_screen(ICON_SCREEN_DICT[icon])
        else:
            self.app.pop_screen()
            self.app.push_screen(ICON_SCREEN_DICT[icon])

    @on(MenuIcon.Pressed, "#icon_settings")
    def action_open_settings(self):
        self.app.switch_mode("Settings")
