from textual.reactive import reactive
from textual.app import App

from idle_tui_adventures.modes.start_menu.start_screen import StartScreen
from idle_tui_adventures.modes.main_menu.main_screen import MainScreen
from idle_tui_adventures.modes.main_menu.inventory_screen import (
    InventoryEquipScreen,
)
from idle_tui_adventures.modes.settings_menu.settings_screen import SettingsScreen


class IdleAdventure(App[None]):
    level: int = reactive(1)
    BINDINGS = [
        ("1", "switch_mode('Start')"),
        ("2", "switch_mode('Main')"),
        ("3", "switch_mode('Settings')"),
    ]
    SCREENS = {"InventoryEquipScreen": InventoryEquipScreen}
    MODES = {"Start": StartScreen, "Main": MainScreen, "Settings": SettingsScreen}

    def on_mount(self):
        # self.switch_mode(mode="Start")
        self.switch_mode(mode="Main")
