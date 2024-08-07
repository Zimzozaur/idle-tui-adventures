from idle_tui_adventures.app import IdleAdventure
from idle_tui_adventures.database.db_utils import init_new_db


def run():
    init_new_db()
    app = IdleAdventure()
    app.run()
