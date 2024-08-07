from configparser import ConfigParser
from pathlib import Path
from dataclasses import dataclass

from idle_tui_adventures.constants import CONFIG_FULL_PATH, DB_FULL_PATH


@dataclass
class IdleTuiConfig:
    config_path: Path = CONFIG_FULL_PATH

    def __post_init__(self):
        self.config = ConfigParser(default_section=None, allow_no_value=True)
        self.config.optionxform = str
        self.config.read(self.config_path)

    @property
    def active_character_id(self) -> int:
        return self.config.getint(section="character.active", option="character_id")

    @active_character_id.setter
    def active_character_id(self, active_id: int):
        self.config.set(
            section="character.active", option="character_id", value=f"{active_id}"
        )
        self.save()

    def save(self):
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)


def create_init_config(conf_path=CONFIG_FULL_PATH):
    config = ConfigParser(default_section=None, allow_no_value=True)
    config.optionxform = str
    config["database"] = {"database_path": DB_FULL_PATH}
    config["character.active"] = {"character_id": 0}

    with open(conf_path, "w") as conf_file:
        config.write(conf_file)
