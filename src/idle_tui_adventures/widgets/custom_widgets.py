from typing import Iterable

from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Horizontal

from rich_pixels import Pixels
from idle_tui_adventures.constants import (
    BACKPACK_IMG,
    CHARACTER_IMG,
    DUNGEON_IMG,
    SETTINGS_IMG,
    SHOP_IMG,
)


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

    Static {
        width: 1fr;
        align: center middle;
        &:hover {
            background: yellow;
        }
        &:focus {
            border: round yellow;
        }
    }
"""

    def compose(self) -> Iterable[Widget]:
        self.can_focus = True
        img_backpack = Pixels.from_image_path(BACKPACK_IMG, resize=(30, 25))
        img_char = Pixels.from_image_path(CHARACTER_IMG, resize=(30, 25))
        img_shop = Pixels.from_image_path(SHOP_IMG, resize=(30, 25))
        img_dungeon = Pixels.from_image_path(DUNGEON_IMG, resize=(30, 25))
        img_settings = Pixels.from_image_path(SETTINGS_IMG, resize=(30, 25))

        character_icon = Static(img_char, id="character")
        yield character_icon

        backpack_icon = Static(img_backpack, id="backpack")
        yield backpack_icon

        dungeon_icon = Static(img_dungeon, id="dungeon")
        yield dungeon_icon

        shop_icon = Static(img_shop, id="shop")
        yield shop_icon

        settings_icon = Static(img_settings, id="settings")
        yield settings_icon

        return super().compose()

    def action_open_backpack(self):
        self.log.error("Shortcut Test")
        if self.screen.name != "MainScreen":
            self.app.pop_screen()
        else:
            self.app.push_screen("InventoryCharacterScreen")

    def action_open_menu(self):
        self.log.error("Shortcut Menu")
        if self.screen.name != "MainScreen":
            self.app.pop_screen()
        else:
            self.app.push_screen("InventoryCharacterScreen")
