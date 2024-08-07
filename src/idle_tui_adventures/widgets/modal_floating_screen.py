from typing import Iterable

from textual import on
from textual.events import MouseUp, MouseMove
from textual.screen import ModalScreen
from textual.widget import Widget

from idle_tui_adventures.widgets.icon_widgets import ItemIcon
from idle_tui_adventures.classes.items import Item
from idle_tui_adventures.widgets.inventory_screen_widgets import Slot


class ItemPopUpScreen(ModalScreen):
    DEFAULT_CSS = """
    ItemPopUpScreen {

        ItemIcon {
        height: 20%;
        width: 20%;
        }
    }
    """

    def __init__(self, clicked_item: Item, slot_list: list[Slot]):
        self.clicked_item = clicked_item
        self.slot_list = slot_list

        super().__init__()

    def compose(self) -> Iterable[Widget]:
        self.floating_icon = ItemIcon(item=self.clicked_item, relocating=True)
        self.floating_icon.offset = self.app.mouse_position
        yield self.floating_icon
        self.notify(f"{self.clicked_item}")
        return super().compose()

    @on(MouseUp)
    def on_mouse_up(self, event: MouseUp):
        self.notify(f"Target Widget: {event.screen_offset}")
        self.log.error(self.slot_list)
        self.dismiss()

    @on(MouseMove)
    def on_mouse_move(self, event: MouseMove):
        self.floating_icon.offset = self.app.mouse_position

        for slot in self.slot_list:
            if slot.region.contains_point(self.app.mouse_position):
                self.log.error(slot)
                self.log.error(slot.region)
                self.log.error(self.app.mouse_position)

        # if self.clicked_widget.parent.region.contains_point(event.screen_offset):
        #     self.clicked_widget.offset = (
        #         event.screen_offset - self.clicked_widget.parent.region.offset
        #     )
        #     self.clicked_widget.border_title = "[green]In[/]"
        #     self.clicked_widget.styles.border = ("heavy", "green")
        # else:
        #     self.clicked_widget.offset = event.screen_offset
        #     self.clicked_widget.border_title = "[red]Out[/]"
        #     self.clicked_widget.styles.border = ("heavy", "red")
