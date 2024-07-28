from typing import Iterable

from textual import events
from textual.widget import Widget
from textual.reactive import reactive
from textual.widgets import Placeholder, Label
from textual.screen import Screen, ModalScreen
from textual.events import MouseMove, MouseDown
from textual.geometry import Offset


class PopUpScreen(ModalScreen):
    def __init__(self, clicked_widget: Label, sender: Widget):
        self.clicked_widget = clicked_widget
        self.sender = sender
        super().__init__()

    def compose(self) -> Iterable[Widget]:
        yield self.clicked_widget
        return super().compose()

    def on_mouse_up(self):
        self.log.error(self.sender.parent.get_widget_at(*self.clicked_widget.offset))
        self.dismiss(result=self.clicked_widget)

    def on_mouse_move(self, event: events.MouseMove):
        # if self.sender.pressed:
        self.clicked_widget.text = f"x:{event.screen_x}, y:{event.screen_y}"
        self.clicked_widget.offset = event.screen_offset
        self.clicked_widget.update(f"x:{event.screen_x}, y:{event.screen_y}")

        self.log.error(
            [i for i in self.sender.parent.get_widgets_at(*event.screen_offset)]
        )

        if self.sender.region.contains_point(self.clicked_widget.offset):
            self.clicked_widget.border_title = "[green]In[/]"
            self.clicked_widget.styles.border = ("heavy", "green")
        else:
            self.clicked_widget.border_title = "[red]Out[/]"
            self.clicked_widget.styles.border = ("heavy", "red")


class Position(Placeholder):
    text: reactive = reactive("")

    def __init__(self, id):
        super().__init__(label=f"Tile_No_{id}", id=id)
        self.set_reactive(Position.text, "starter")

    def compose(self) -> Iterable[Widget]:
        self.coord_label = Label(self.text, id="position")
        yield self.coord_label
        return super().compose()

    def watch_text(self, text):
        self.query_one("#position", Label).update(text)

    def on_mouse_down(self, event: MouseDown):
        if event.button == 1:
            return
        # test_widget = Button("Test")
        test_widget = self.coord_label
        test_widget.offset = event.screen_offset
        test_widget.border_title = "[green]In[/]"
        test_widget.styles.border = ("heavy", "green")

        # self.refresh(recompose=True)
        self.app.push_screen(
            screen=PopUpScreen(sender=self, clicked_widget=test_widget),
            callback=self.update_values,
        )
        self.refresh(recompose=True)

    def update_values(self, widget: Label):
        self.coord_label.offset = widget.offset - self.coord_label.region.offset

        self.parent.update_positions(self.coord_label.offset)
        self.parent.pressed = False


class MainScreen2(Screen):
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
        for j in range(4):
            yield Position(id=f"tile_{j}").data_bind(MainScreen2.text)

        return super().compose()

    def on_mouse_move(self, event: MouseMove):
        if self.pressed:
            self.text = f"x:{event.screen_x}, y:{event.screen_y}"
            self.log.error(self.text)

    def update_positions(self, offset: Offset):
        self.text = f"x:{offset.x}, y:{offset.y}"

    def on_mouse_down(self):
        self.pressed = True

    def on_mouse_up(self):
        self.pressed = False
