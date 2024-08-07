import sqlite3
from pathlib import Path

from idle_tui_adventures.constants import (
    DB_FULLNAME,
)


def create_connection(database: Path = DB_FULLNAME) -> sqlite3.Connection:
    return sqlite3.connect(database=database, autocommit=False)


def init_new_db(database: Path = DB_FULLNAME):
    if database.exists():
        return

    CHAR_DB_CREATION = """
    CREATE TABLE IF NOT EXISTS characters (
    character_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    profession TEXT NOT NULL,
    created_at TIMESTAMP,
    level INTEGER NOT NULL,
    experience INTEGER NOT NULL,
    strength INTEGER NOT NULL,
    intelligence INTEGER NOT NULL,
    dexterity INTEGER NOT NULL,
    luck INTEGER NOT NULL,
    major_stage INTEGER NOT NULL,
    minor_stage INTEGER NOT NULL,
    Check (name <> ""),
    Check (profession in ('Mage', 'Warrior', 'Ranger', 'Thief'))
    );
    """

    ITEM_DB_CREATION = """
    CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    rarity TEXT NOT NULL,
    category TEXT NOT NULL,
    level_needed INTEGER NOT NULL,
    damage INTEGER NOT NULL,
    attack_speed REAL NOT NULL,
    strength INTEGER NOT NULL,
    intelligence INTEGER NOT NULL,
    dexterity INTEGER NOT NULL,
    luck INTEGER NOT NULL
    );
    """

    STORAGE_DB_CREATION = """
    CREATE TABLE IF NOT EXISTS storages (
    storage_id INTEGER PRIMARY KEY,
    character_id INTEGER,
    item_id INTEGER,
    FOREIGN KEY (character_id) REFERENCES character(character_id),
    FOREIGN KEY (item_id) REFERENCES item(item_id)
    );
    """

    INDEXES_CREATION = """
    CREATE INDEX IF NOT EXISTS idx_characters_name ON characters(name);
    CREATE INDEX IF NOT EXISTS idx_items_name ON items(name);
    CREATE INDEX IF NOT EXISTS idx_storages_character_id ON storages(character_id);
    CREATE INDEX IF NOT EXISTS idx_storages_item_id ON storages(item_id);
    """

    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(CHAR_DB_CREATION)
            con.execute(ITEM_DB_CREATION)
            con.execute(STORAGE_DB_CREATION)
            con.executescript(INDEXES_CREATION)

            return 0
        except sqlite3.Error as e:
            print(e)
            con.rollback()
            return 1


def store_item(character_name, item):
    with create_connection() as con:
        try:
            character_id = con.execute(
                "SELECT character_id FROM characters WHERE name = ?",
                (character_name,),
            ).fetchone()[0]

            item_id = con.execute(
                "SELECT item_id FROM items WHERE name = ?", (item,)
            ).fetchone()[0]

            # Insert into storages
            storage_data = {"character_id": character_id, "item_id": item_id}
            con.execute(
                "INSERT INTO storages (character_id, item_id) VALUES (:character_id, :item_id)",
                storage_data,
            )
            return 0
        except sqlite3.Error as e:
            print(e)
            return 1


def get_items_for_character(character_name: str):
    query = """
    SELECT items.*
    FROM characters
    JOIN storages ON characters.character_id = storages.character_id
    JOIN items ON storages.item_id = items.item_id
    WHERE characters.name = ?
    """

    with create_connection() as con:
        items = con.execute(query, (character_name,)).fetchall()

        for item in items:
            print(item)


# Update
# UPDATE Customers
# SET ContactName = 'Alfred Schmidt', City = 'Frankfurt'
# WHERE CustomerID = 1;

# Delete
# DELETE FROM Customers WHERE CustomerName='Alfreds Futterkiste';
