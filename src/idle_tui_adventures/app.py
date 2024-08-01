from textual.app import App

from idle_tui_adventures.modes.start_menu.start_screen import StartScreen
from idle_tui_adventures.modes.main_menu.main_screen import MainScreen
from idle_tui_adventures.modes.settings_menu.settings_screen import SettingsScreen


class IdleAdventure(App[None]):
    #     CSS = """
    # StartScreen {
    #         layout: grid;
    #         grid-size: 2 2;
    #         grid-rows: 1fr;
    #         grid-columns: 1fr;
    #         grid-gutter: 1;
    #     }
    # MainScreen {
    #         layout: grid;
    #         grid-size: 3 3;
    #         grid-rows: 1fr;
    #         grid-columns: 1fr;
    #         grid-gutter: 1;
    #     }
    # SettingsScreen {
    #         layout: grid;
    #         grid-size: 2 1;
    #         grid-rows: 1fr;
    #         grid-columns: 1fr;
    #         grid-gutter: 1;
    #     }

    # """
    BINDINGS = [
        ("1", "switch_mode('Start')"),
        ("2", "switch_mode('Main')"),
        ("3", "switch_mode('Settings')"),
    ]
    MODES = {"Start": StartScreen, "Main": MainScreen, "Settings": SettingsScreen}

    def on_mount(self):
        self.switch_mode(mode="Start")
