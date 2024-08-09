from idle_tui_adventures.database.db_transactions import (
    create_new_item,
    create_new_character,
)
from idle_tui_adventures.database.db_utils import init_new_db


def main():
    init_new_db()

    create_new_character(
        name="Test_Char",
        profession="Warrior",
        strength=5,
        intelligence=5,
        dexterity=5,
        luck=5,
    )
    create_new_item(
        name="Axe of Ordinary",
        level_needed=1,
        category="Weapon",
        rarity="unique",
        damage=3,
        attack_speed=1.05,
        strength=0,
        intelligence=0,
        dexterity=0,
        luck=2,
        owned_by=1,
    )


if __name__ == "__main__":
    main()
