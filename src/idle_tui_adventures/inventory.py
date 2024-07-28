from typing import Iterable

from textual import events
from textual.widget import Widget
from textual.reactive import reactive
from textual.widgets import Placeholder, Label, Button
from textual.screen import Screen, ModalScreen
from textual.events import MouseMove, MouseDown


class PopUpScreen(ModalScreen):
    def __init__(self, clicked_widget, sender: Widget):
        self.clicked_widget = clicked_widget
        self.sender = sender
        super().__init__()

    def compose(self) -> Iterable[Widget]:
        yield Button()
        yield Button()
        yield self.clicked_widget
        return super().compose()

    def on_mouse_up(self):
        self.sender.pressed = False
        self.dismiss(result=self.clicked_widget)

    def on_mouse_move(self, event: events.MouseMove):
        if self.sender.pressed:
            self.clicked_widget.offset = event.screen_offset - (8, 8)


class Position(Placeholder):
    text: reactive = reactive("")

    def __init__(self, label: str = "Test"):
        super().__init__(label=label)
        self.set_reactive(Position.text, "starter")

    def compose(self) -> Iterable[Widget]:
        yield Label(self.text, id="position")
        return super().compose()

    def watch_text(self, text):
        self.query_one("#position", Label).update(text)

    def on_mouse_down(self, event: MouseDown):
        if event.button == 1:
            return
        test_widget = Button("Test")
        # test_widget = deepcopy(self).recompose()
        test_widget.offset = event.screen_offset - (8, 8)
        self.log.error(f"Offset vorher: {test_widget.offset}")

        self.app.push_screen(
            screen=PopUpScreen(sender=self.parent, clicked_widget=test_widget),
            callback=self.mount_new,
        )
        self.refresh(recompose=True)

    def mount_new(self, widget: Widget):
        self.log.error(widget)
        self.log.error(f"Offset nachher: {widget.offset}")
        self.mount(widget)


class MainScreen2(Screen):
    BINDINGS = [("space", "dismiss()", "Main2")]

    CSS = """MainScreen2 {
        layout: grid;
        grid-size: 2 2;
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
        yield Position().data_bind(MainScreen2.text)
        yield Position().data_bind(MainScreen2.text)
        yield Position().data_bind(MainScreen2.text)
        yield Position().data_bind(MainScreen2.text)

        return super().compose()

    def on_mouse_move(self, event: MouseMove):
        if self.pressed:
            self.text = f"x:{event.screen_x}, y:{event.screen_y}"
            self.log.error(self.text)

    def on_mouse_down(self):
        self.pressed = True

    def on_mouse_up(self):
        self.pressed = False
