from textual.app import App

from idle_tui_adventures.main_screen import MainScreen
from idle_tui_adventures.inventory import MainScreen2
from idle_tui_adventures.test_positioning import TestScreen


class IdleAdventure(App[None]):
    BINDINGS = [
        ("1", "push_screen('Main')", "move2Main"),
        ("2", "push_screen('Main2')", "move2Main2"),
        ("space", "push_screen('Test')", "move2Test"),
    ]
    SCREENS = {"Main": MainScreen, "Main2": MainScreen2, "Test": TestScreen}

    def on_mount(self):
        self.push_screen(screen="Test")

    # def compose(self) -> ComposeResult:
    #     yield MainScreen()
    #     return super().compose()


def main():
    # MainScreen().run()

    IdleAdventure().run()


if __name__ == "__main__":
    main()
