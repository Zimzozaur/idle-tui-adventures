import pytest

from idle_tui_adventures.app import IdleAdventure


@pytest.mark.asyncio
async def test_mode_switches():
    app = IdleAdventure()

    async with app.run_test() as pilot:
        await pilot.press("1")
        assert app.screen.name == "StartScreen"

        await pilot.press("2")
        assert app.screen.name == "MainScreen"

        await pilot.press("3")
        assert app.screen.name == "SettingsScreen"


@pytest.mark.asyncio
async def test_start_screen_buttons():
    app = IdleAdventure()

    async with app.run_test() as pilot:
        await pilot.press("1")
        await pilot.click("#btn_move_to_character_creation")
        assert app.screen.name == "CharacterCreation"

        await pilot.press("escape")
        assert app.screen.name == "StartScreen"

        await pilot.click("#btn_move_to_load_character")
        assert app.screen.name == "CharacterSelection"

        await pilot.press("escape")
        assert app.screen.name == "StartScreen"


@pytest.mark.asyncio
async def test_main_screen_buttons():
    app = IdleAdventure()

    async with app.run_test() as pilot:
        await pilot.press("2")

        await pilot.press("c")
        assert app.screen.name == "CharacterScreen"
        await pilot.click("#icon_character")
        assert app.screen.name == "MainScreen"
        await pilot.press("c")
        assert app.screen.name == "CharacterScreen"

        await pilot.click("#icon_backpack")
        assert app.screen.name == "InventoryEquipScreen"
        await pilot.press("b")
        assert app.screen.name == "MainScreen"

        await pilot.press("d")
        assert app.screen.name == "DungeonScreen"
        await pilot.click("#icon_shop")
        assert app.screen.name == "ShopScreen"

        await pilot.click("#icon_settings")
        assert app.screen.name == "SettingsScreen"

        await pilot.press("escape")
        assert app.screen.name == "ShopScreen"
        await pilot.press("l")
        assert app.screen.name == "MainScreen"

        await pilot.press("b")
        assert app.screen.name == "InventoryEquipScreen"
        await pilot.click("#icon_character")
        assert app.screen.name == "CharacterScreen"

        await pilot.press("d")
        assert app.screen.name == "DungeonScreen"
        await pilot.click("#icon_dungeon")
        assert app.screen.name == "MainScreen"

        await pilot.press("l")
        assert app.screen.name == "ShopScreen"
