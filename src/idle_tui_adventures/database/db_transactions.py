import sqlite3
from datetime import datetime
from pathlib import Path

from idle_tui_adventures.database.db_utils import create_connection
from idle_tui_adventures.constants import (
    PROFESSIONS_LITERAL,
    DB_FULL_PATH,
    RARITIES_LITERAL,
    ITEM_CATEGORIES_LITERAL,
)


def create_new_character(
    name: str,
    profession: PROFESSIONS_LITERAL,
    strength: int,
    intelligence: int,
    dexterity: int,
    luck: int,
    database: Path = DB_FULL_PATH,
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

    transaction_str = """
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

    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(transaction_str, data_character_dict)
            con.commit()
            return 0
        except sqlite3.Error as e:
            con.rollback()
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_CHECK:
                return "please provide a character name"
            elif e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                return "character name already taken"
            return e.sqlite_errorname


def create_new_item(
    name: str,
    level_needed: int,
    rarity: RARITIES_LITERAL,
    category: ITEM_CATEGORIES_LITERAL,
    damage: int,
    attack_speed: float,
    strength: int,
    intelligence: int,
    dexterity: int,
    luck: int,
    database: Path = DB_FULL_PATH,
) -> str | int:
    data_item_dict = {
        "name": name,
        "rarity": rarity,
        "category": category,
        "level_needed": level_needed,
        "damage": damage,
        "attack_speed": attack_speed,
        "strength": strength,
        "intelligence": intelligence,
        "dexterity": dexterity,
        "luck": luck,
    }

    transaction_str = """
    INSERT INTO items
    VALUES (
        NULL,
        :name,
        :rarity,
        :category,
        :level_needed,
        :damage,
        :attack_speed,
        :strength,
        :intelligence,
        :dexterity,
        :luck
        );"""

    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(transaction_str, data_item_dict)
            con.commit()
            return 0
        except sqlite3.Error as e:
            con.rollback()
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_CHECK:
                return "Item Insertion Error"
            elif e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                return "Iterm Insertion Error"
            return e.sqlite_errorname


def update_experience_db(
    character_id: int, experience: int, database: Path = DB_FULL_PATH
) -> int | str:
    exp_dict = {"character_id": character_id, "experience": experience}
    query_str = """
    UPDATE characters
    SET experience = :experience
    WHERE character_id = :character_id
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(query_str, exp_dict)
            return 0
        except sqlite3.Error as e:
            print(e.sqlite_errorname)
            return e.sqlite_errorname


def update_level_db(
    character_id: int, level: int, database: Path = DB_FULL_PATH
) -> int | str:
    lvl_dict = {"character_id": character_id, "level": level}
    query_str = """
    UPDATE characters
    SET level = :level
    WHERE character_id = :character_id
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(query_str, lvl_dict)
            return 0
        except sqlite3.Error as e:
            print(e.sqlite_errorname)
            return e.sqlite_errorname
