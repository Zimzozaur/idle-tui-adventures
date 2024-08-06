from dataclasses import dataclass


@dataclass
class Character:
    character_data: tuple

    def __post_init__(self) -> None:
        self.char_id = self.character_data[0]
        self.name = self.character_data[1]
        self.profession = self.character_data[2]
        self.created_at = self.character_data[3]
        self.level = self.character_data[4]
        self.experience = self.character_data[5]
        self.base_str = self.character_data[6]
        self.base_int = self.character_data[7]
        self.base_dex = self.character_data[8]
        self.base_luc = self.character_data[9]
        self.major_stage = self.character_data[10]
        self.minor_stage = self.character_data[11]

        self.equipped_items = self.get_equipped_items()
        self.inventory_items = self.get_inventory_items()

    ...

    # von db
    def get_equipped_items(self): ...
    # von db
    def get_inventory_items(self): ...
