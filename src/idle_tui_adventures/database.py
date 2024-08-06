import sqlite3
from pathlib import Path
from datetime import datetime

from idle_tui_adventures.constants import DB_FULLNAME


def create_connection(database: Path = DB_FULLNAME) -> sqlite3.Connection:
    return sqlite3.connect(database=database)


def init_new_db():
    if DB_FULLNAME.exists():
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
    damage INTEGER NOT NULL,
    attack_speed REAL NOT NULL
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

    connection = create_connection()
    with connection as con:
        try:
            con.execute(CHAR_DB_CREATION)
            con.execute(ITEM_DB_CREATION)
            con.execute(STORAGE_DB_CREATION)
            con.executescript(INDEXES_CREATION)
            return 1
        except sqlite3.Error as e:
            print(e)
            con.rollback()
            return 1


def create_new_character(
    name: str,
    profession: str,
    strength: int,
    intelligence: int,
    dexterity: int,
    luck: int,
) -> str | int:
    data_character_dict = {
        "name": name,
        "profession": profession,
        "strength": strength,
        "intelligence": intelligence,
        "dexterity": dexterity,
        "luck": luck,
        "creation_time": datetime.now().replace(microsecond=0),
        "level": 1,
        "experience": 0,
        "major_stage": 1,
        "minor_stage": 1,
    }

    transaction = """
    INSERT INTO characters
    VALUES (
        NULL,
        :name,
        :profession,
        :creation_time,
        :level,
        :experience,
        :strength,
        :intelligence,
        :dexterity,
        :luck,
        :major_stage,
        :minor_stage
        );"""

    connection = create_connection()
    with connection as con:
        cu = con.cursor()
        try:
            cu.execute(transaction, data_character_dict)
            con.commit()
            return 0
        except sqlite3.Error as e:
            con.rollback()
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_CHECK:
                return "please provide a character name"
            elif e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                return "character name already taken"
            return e.sqlite_errorname


def get_all_characters() -> list[tuple]:
    characters = []
    with create_connection() as con:
        try:
            for row in con.execute("select * from characters").fetchall():
                characters.append(row)
            return characters
        except sqlite3.Error as e:
            print(e)
            return characters


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
