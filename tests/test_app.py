import pytest

from idle_tui_adventures.app import IdleAdventure


@pytest.mark.asyncio
async def test_mode_switches():
    app = IdleAdventure()

    async with app.run_test() as pilot:
        await pilot.press("2")
        assert app.screen.name == "MainScreen"

        await pilot.press("1")
        assert app.screen.name == "StartScreen"

        await pilot.press("3")
        assert app.screen.name == "SettingsScreen"


@pytest.mark.asyncio
async def test_buttons():
    app = IdleAdventure()

    async with app.run_test() as pilot:
        await pilot.click("#btn_new_character")
        assert app.screen.name == "CharacterCreation"

        await pilot.press("escape")
        assert app.screen.name == "StartScreen"

        await pilot.click("#btn_load_character")
        assert app.screen.name == "CharacterSelection"

        await pilot.press("escape")
        assert app.screen.name == "StartScreen"
