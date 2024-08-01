from typing import Iterable

from textual import events
from textual.widget import Widget
from textual.reactive import reactive
from textual.widgets import Placeholder, Label, Button
from textual.screen import Screen, ModalScreen


class PopUpScreen(ModalScreen):
    def compose(self) -> Iterable[Widget]:
        yield Button()
        yield Button()
        return super().compose()

    def on_button_pressed(self):
        self.dismiss()


class Position(Placeholder):
    text: reactive = reactive("")

    def __init__(self):
        super().__init__()
        self.set_reactive(Position.text, "starter")

    def compose(self) -> Iterable[Widget]:
        yield Label(self.text, id="position")
        return super().compose()

    def watch_text(self, text):
        self.query_one("#position", Label).update(text)

    def on_click(self):
        self.app.push_screen(PopUpScreen())


class MainScreen(Screen):
    DEFAULT_CSS = """MainScreen {
        layout: grid;
        grid-size: 3 3;
        grid-rows: 1fr;
        grid-columns: 1fr;
        grid-gutter: 1;
    }
    """
    x_pos: reactive = reactive(0)
    y_pos: reactive = reactive(0)
    text: reactive = reactive("Hi")
    pressed: bool = False

    def compose(self) -> Iterable[Widget]:
        for i in range(9):
            yield Placeholder("MainScreen", id=f"tile_{i}")
        # yield Position().data_bind(MainScreen.text)

        return super().compose()

    def on_mouse_move(self, event: events.MouseMove):
        if self.pressed:
            self.text = f"x:{event.screen_x}, y:{event.screen_y}"
            self.log.error(self.text)

    def on_mouse_down(self):
        self.pressed = True

    def on_mouse_up(self):
        self.pressed = False
