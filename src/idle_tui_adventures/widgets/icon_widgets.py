from __future__ import annotations
from typing import Coroutine, Any

from typing_extensions import Self, Iterable
from sqlite3 import Row

from textual import on
from textual.reactive import reactive
from textual.events import Click, Resize
from textual.binding import Binding
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Static, Label
from textual.containers import Horizontal, Vertical

from idle_tui_adventures.constants import MENU_ICONS, ICON_SCREEN_DICT, ICONS_LITERAL
from idle_tui_adventures.classes.character import Character
from idle_tui_adventures.utils import get_icon


class MenuIcon(Static):
    BINDINGS = [Binding("enter", "press", "Press Icon", show=False)]

    DEFAULT_CSS = """MenuIcon {
        width: 1fr;
        height: 1fr;
        align: center middle;
        content-align: center middle;

    }"""

    class Pressed(Message):
        def __init__(self, icon: MenuIcon) -> None:
            self.icon: MenuIcon = icon
            """The icon that was pressed."""
            super().__init__()

        @property
        def control(self) -> MenuIcon:
            return self.icon

    def __init__(self, icon: ICONS_LITERAL, id: str) -> None:
        self.icon_name = icon
        self.icon_img = get_icon(icon=self.icon_name)

        super().__init__(self.icon_img, id=id)

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
    def keep_image_size(self, event: Resize) -> None:
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

        & MenuIcon {
            &:hover {
                background: yellow;
            }
            &.-active {
                background: $success;
            }
        }

    }

"""

    def compose(self) -> Iterable[Widget]:
        self.can_focus = True

        for icon in MENU_ICONS:
            yield MenuIcon(icon=icon, id=icon)

        return super().compose()

    @on(MenuIcon.Pressed, "#character")
    def action_open_character(self):
        icon = "character"
        if self.screen.name == ICON_SCREEN_DICT[icon]:
            self.app.pop_screen()
        elif self.screen.name == "MainScreen":
            self.app.push_screen(ICON_SCREEN_DICT[icon])
        else:
            self.app.pop_screen()
            self.app.push_screen(ICON_SCREEN_DICT[icon])

    @on(MenuIcon.Pressed, "#backpack")
    def action_open_backpack(self):
        icon = "backpack"
        if self.screen.name == ICON_SCREEN_DICT[icon]:
            self.app.pop_screen()
        elif self.screen.name == "MainScreen":
            self.app.push_screen(ICON_SCREEN_DICT[icon])
        else:
            self.app.pop_screen()
            self.app.push_screen(ICON_SCREEN_DICT[icon])

    @on(MenuIcon.Pressed, "#dungeon")
    def action_open_dungeon(self):
        icon = "dungeon"
        if self.screen.name == ICON_SCREEN_DICT[icon]:
            self.app.pop_screen()
        elif self.screen.name == "MainScreen":
            self.app.push_screen(ICON_SCREEN_DICT[icon])
        else:
            self.app.pop_screen()
            self.app.push_screen(ICON_SCREEN_DICT[icon])

    @on(MenuIcon.Pressed, "#shop")
    def action_open_shop(self):
        icon = "shop"
        if self.screen.name == ICON_SCREEN_DICT[icon]:
            self.app.pop_screen()
        elif self.screen.name == "MainScreen":
            self.app.push_screen(ICON_SCREEN_DICT[icon])
        else:
            self.app.pop_screen()
            self.app.push_screen(ICON_SCREEN_DICT[icon])

    @on(MenuIcon.Pressed, "#settings")
    def action_open_settings(self):
        self.app.switch_mode("Settings")


class CharacterPreview(Vertical):
    DEFAULT_CSS = """
    CharacterPreview {
        width:1fr;
        height:1fr;


        Label {
            height:10%;
            width:1fr;
            content-align:center middle;
            text-align: center;
            border:solid brown;
        }
        MenuIcon {
            height:50%;
            width:1fr;
        }
    }
    """

    def __init__(self, character_data: Row):
        self.character: Character = Character(**dict(character_data))

        super().__init__()

    def compose(self) -> Iterable[Widget]:
        yield MenuIcon(
            icon=self.character.profession,
            id=f"character_{self.character.character_id}",
        )
        yield Label(self.character.name)
        yield Label(self.character.created_at)
        yield Label(f"Level: {self.character.level}")
        yield Label(f"Experience: {self.character.experience}")
        yield Label(f"Stage: {self.character.major_stage}-{self.character.minor_stage}")
        return super().compose()


class DragableSlot(MenuIcon):
    amount: reactive = reactive(0)
    DEFAULT_CSS = """
    DragableSlot {
        border: solid brown;
    }
    """

    def compose(self) -> Iterable[Widget]:
        # yield MenuIcon('Warrior', id='upper_stat')
        self.tooltip = f"{self.amount} stacked"
        self.border_subtitle = f"{self.amount} stacked"
        return super().compose()

    def _on_click(self, event: Click) -> Coroutine[Any, Any, None]:
        if event.button == 1:  # left click
            self.remove_item()
        elif event.button == 3:  # right click
            self.add_item()
        return super()._on_click(event)

    def remove_item(self):
        if self.amount > 1:
            self.amount -= 1
            self.tooltip = f"{self.amount} stacked"
            self.border_subtitle = f"{self.amount} stacked"
        elif self.amount == 1:
            self.amount -= 1
            self.tooltip = f"{self.amount} stacked"
            self.border_subtitle = f"{self.amount} stacked"
            self.query_one("#stacked").remove()

    def add_item(self):
        if self.amount >= 1:
            self.amount += 1
            self.tooltip = f"{self.amount} stacked"
            self.border_subtitle = f"{self.amount} stacked"
        else:
            self.amount += 1
            self.border_subtitle = f"{self.amount} stacked"
            self.tooltip = f"{self.amount} stacked"
            new_icon = MenuIcon("Warrior", id="stacked")
            self.mount(new_icon)
