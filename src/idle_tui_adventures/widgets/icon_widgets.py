from __future__ import annotations
from typing import Coroutine, Any

from typing_extensions import Self, Iterable
from sqlite3 import Row

from textual import on
from textual.reactive import reactive
from textual.events import Click, MouseDown, Resize
from textual.binding import Binding
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Static, Label
from textual.containers import Horizontal, Vertical

from idle_tui_adventures.constants import MENU_ICONS, ICON_SCREEN_DICT, ICONS_LITERAL
from idle_tui_adventures.classes.characters import Character
from idle_tui_adventures.classes.items import Item
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


class ItemSlot(Static):
    amount: reactive = reactive(0)

    DEFAULT_CSS = """ItemSlot {
        width: 1fr;
        height: 1fr;
        align: center middle;
        content-align: center middle;
        background: #ba9f68;
        border:outer #6a4f32;
        border-subtitle-background:#6a4f32;

    }"""

    def __init__(self, id: str | None = None) -> None:
        super().__init__(id=id)

    def compose(self) -> Iterable[Widget]:
        self.styles.border_subtitle_color = "yellow"
        self.border_subtitle = f"{self.amount} x" if self.amount else ""
        yield Static(renderable=get_icon("Mage"))
        return super().compose()

    @on(Click)
    def show_popup(self, event):
        self.query_one(Static).remove()
        return super()._on_click(event=event)

    @property
    def empty(self) -> bool:
        return len(self.children) == 0

    def place_item(self, item) -> None:
        if self.empty:
            self.mount(item)
        else:
            pass

    def _on_mouse_down(self, event: MouseDown) -> Coroutine[Any, Any, None]:
        self.query_one(Static).remove()
        return super()._on_mouse_down(event)

    # weiterer Static drauf
    # bei mouse_down obere static in modal mit offset


class ItemIcon(Static):
    def __init__(self, item: Item) -> None:
        super().__init__()
