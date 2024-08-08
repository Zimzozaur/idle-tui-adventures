from textual.reactive import reactive
from textual.app import App

from idle_tui_adventures.classes.characters import Character
from idle_tui_adventures.database.db_queries import get_character_by_id
from idle_tui_adventures.config import IdleTuiConfig, init_new_config
from idle_tui_adventures.modes.start_menu.start_screen import StartScreen
from idle_tui_adventures.modes.main_menu.main_screen import MainScreen
from idle_tui_adventures.modes.main_menu.inventory_screen import InventoryEquipScreen
from idle_tui_adventures.modes.main_menu.dungeon_screen import DungeonScreen
from idle_tui_adventures.modes.main_menu.shop_screen import ShopScreen
from idle_tui_adventures.modes.main_menu.character_screen import CharacterScreen
from idle_tui_adventures.modes.settings_menu.settings_screen import SettingsScreen


class IdleAdventure(App[None]):
    level: int = reactive(1)
    character: Character | None

    BINDINGS = [
        ("1", "switch_mode('Start')"),
        ("2", "switch_mode('Main')"),
        ("3", "switch_mode('Settings')"),
    ]
    SCREENS = {
        "InventoryEquipScreen": InventoryEquipScreen,
        "DungeonScreen": DungeonScreen,
        "ShopScreen": ShopScreen,
        "CharacterScreen": CharacterScreen,
    }
    MODES = {"Start": StartScreen, "Main": MainScreen, "Settings": SettingsScreen}

    def on_mount(self):
        init_new_config()
        self.cfg = IdleTuiConfig()

        self.set_active_character()

        # If character is present go to main
        if self.character and self.cfg.skip_screen:
            self.switch_mode(mode="Main")
        else:
            self.switch_mode(mode="Start")

    def set_active_character(self):
        db_entry = get_character_by_id(character_id=self.cfg.active_character_id)
        if db_entry:
            info_txt = f'Name:\t\t[blue]{db_entry['name']}[/]\n'
            info_txt += f'Level:\t\t[blue]{db_entry['level']}[/]\n'
            info_txt += f'Profession:\t[blue]{db_entry['profession']}[/]'
            self.notify(title="Character Active", message=info_txt, timeout=2)
            self.character = Character(**db_entry)
        else:
            self.notify(
                title="No Character Found",
                message="Please create a character first",
                severity="warning",
            )
            self.character = None
