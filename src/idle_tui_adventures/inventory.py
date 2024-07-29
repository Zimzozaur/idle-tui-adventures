from typing import Iterable
from copy import copy


from textual import events
from textual.widget import Widget
from textual.reactive import reactive
from textual.widgets import Placeholder, Label
from textual.screen import Screen, ModalScreen
from textual.events import MouseMove, MouseDown
from textual.geometry import Offset
from textual.message import Message


class PopUpScreen(ModalScreen):
    def __init__(self, clicked_widget: Label, sender: Widget):
        self.clicked_widget = clicked_widget
        self.sender = sender
        super().__init__()

    def compose(self) -> Iterable[Widget]:
        yield self.clicked_widget
        return super().compose()

    def on_mouse_up(self, event: events.MouseUp):
        # parent_widget = self.sender.parent.get_widget_at(*self.clicked_widget.offset)[0]
        parent_widget = self.sender.parent.get_widget_at(*event.screen_offset)[0]
        self.clicked_widget.border_title = ""
        self.clicked_widget.styles.border = None
        self.dismiss(result=(self.clicked_widget, parent_widget))

    def on_mouse_move(self, event: events.MouseMove):
        # if self.sender.pressed:
        self.clicked_widget.text = f"x:{event.screen_x}, y:{event.screen_y}"
        self.clicked_widget.offset = event.screen_offset  # - self.sender.region.offset
        self.clicked_widget.update(f"x:{event.screen_x}, y:{event.screen_y}")

        self.log.error(f"parent region: {self.sender.region}")
        self.log.error(f"current offset: {self.clicked_widget.offset}")
        if self.sender.region.contains_point(self.clicked_widget.offset):
            self.clicked_widget.border_title = "[green]In[/]"
            self.clicked_widget.styles.border = ("heavy", "green")
        else:
            self.log.error("Should be red")
            self.clicked_widget.border_title = "[red]Out[/]"
            self.clicked_widget.styles.border = ("heavy", "red")


class Position(Placeholder):
    text: reactive = reactive("")

    class Moved(Message):
        def __init__(self, widget: Widget, target: Widget) -> None:
            self.widget = widget
            self.target = target
            super().__init__()

    def __init__(self, id):
        super().__init__(label=f"Tile_No_{id}", id=id)
        self.set_reactive(Position.text, "starter")

    def compose(self) -> Iterable[Widget]:
        self.coord_label = Label(self.text, id=f"position_{self.id}")
        self.coord_label.styles.border = ("solid", "black")
        yield self.coord_label
        return super().compose()

    def watch_text(self, text):
        self.query_one(f"#position_{self.id}", Label).update(text)

    def on_mouse_down(self, event: MouseDown):
        if event.button == 1:
            return
        # test_widget = self.query_one(Label)
        # test_widget = self.coord_label
        try:
            test_widget = self.parent.get_widget_at(*event.screen_offset)[0]
            if not isinstance(test_widget, Label):
                raise Exception
        except Exception as e:
            self.log.error(e)
            return
        test_widget.offset = event.screen_offset - test_widget.parent.offset
        test_widget.border_title = "[green]In[/]"
        test_widget.styles.border = ("heavy", "green")

        # self.refresh(recompose=True)
        self.app.push_screen(
            screen=PopUpScreen(sender=self, clicked_widget=test_widget),
            callback=self.calc_new_position,
        )
        self.refresh(recompose=True)

    def calc_new_position(self, return_tuple):
        widget: Label = return_tuple[0]
        parent_widget: Placeholder = return_tuple[1]
        self.log.error(f"widget:{widget.region}")
        self.log.error(f"parent_widget:{parent_widget.region}")
        self.log.error(f"mouse:{self.app.cursor_position}")
        if self.region.contains_point(widget.offset):
            self.coord_label.offset = widget.offset
        else:
            widget.offset = widget.offset - parent_widget.region.offset
            self.post_message(self.Moved(widget=widget, target=parent_widget))
            # self.coord_label.mount()

        # self.coord_label.offset = widget.offset - parent_widget.region.offset

        self.parent.update_texts(self.coord_label.offset)
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

    def update_texts(self, offset: Offset):
        self.text = f"x:{offset.x}, y:{offset.y}"

    def on_mouse_down(self):
        self.pressed = True

    def on_mouse_up(self):
        self.pressed = False

    def on_position_moved(self, message: Message):
        self.log.error(
            f"try mounting {message.widget}, {message.widget.region} on {message.target}, {message.target.region}"
        )
        new_widget = copy(message.widget)
        new_widget.offset -= message.target.offset
        message.target.mount(new_widget)
        message.widget.parent.refresh(recompose=True)
        message.widget.remove()
